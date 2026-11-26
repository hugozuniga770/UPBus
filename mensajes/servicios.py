"""Servicios de los chats: consultan, validan, guardan y publican eventos."""
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction

from comun.rechazos import NoExiste, Rechazo
from comun.tiempo import ahora as ahora_local
from cuentas.models import Usuario
from rutas.models import Ruta
from viajes.consumers import grupo_del_chofer
from viajes.models import AvisoDeSubida, Viaje

from . import reglas
from .consumers import grupo_del_chat_directo, grupo_del_chat_de_ruta
from .models import Mensaje, MiembroDeRuta


def buscar_viaje(viaje_id):
    viaje = Viaje.objects.select_related("chofer", "ruta").filter(pk=viaje_id).first()
    if viaje is None:
        raise NoExiste("el viaje no existe")
    return viaje


def buscar_ruta(ruta_id):
    ruta = Ruta.objects.filter(pk=ruta_id).first()
    if ruta is None:
        raise NoExiste("la ruta no existe")
    return ruta


def buscar_estudiante(estudiante_id):
    estudiante = Usuario.objects.filter(pk=estudiante_id).first()
    if estudiante is None:
        raise NoExiste("el estudiante no existe")
    return estudiante


def _aviso_confirmado(viaje, estudiante):
    return AvisoDeSubida.objects.filter(
        viaje=viaje,
        estudiante=estudiante,
        estado=AvisoDeSubida.Estado.CONFIRMADO,
    ).first()


def _estudiante_del_chat(
    usuario,
    viaje,
    estudiante_id=None,
    respuesta_rapida=None,
    exigir_respuesta_rapida=False,
):
    if usuario.es_chofer:
        reglas.verificar_chofer_del_viaje(viaje, usuario)
        estudiante = buscar_estudiante(estudiante_id)
        if exigir_respuesta_rapida:
            reglas.verificar_respuesta_rapida(respuesta_rapida)
    else:
        estudiante = usuario
    reglas.verificar_confirmado(_aviso_confirmado(viaje, estudiante))
    return estudiante


def _publicar(grupo, tipo, mensaje):
    from .serializadores import mensaje_a_dict

    datos = {"tipo": tipo, "mensaje": mensaje_a_dict(mensaje)}
    capa = get_channel_layer()
    async_to_sync(capa.group_send)(
        grupo,
        {"type": "mensaje.del.chat", "datos": datos},
    )


def _publicar_mensaje_directo(viaje_id, estudiante_id, mensaje):
    """Entrega la conversación y avisa al chofer aunque no tenga abierto ese chat."""
    from .serializadores import mensaje_a_dict

    datos = {"tipo": "mensaje_directo", "mensaje": mensaje_a_dict(mensaje)}
    capa = get_channel_layer()
    async_to_sync(capa.group_send)(
        grupo_del_chat_directo(viaje_id, estudiante_id),
        {"type": "mensaje.del.chat", "datos": datos},
    )
    if mensaje.autor_id == estudiante_id:
        async_to_sync(capa.group_send)(
            grupo_del_chofer(viaje_id),
            {
                "type": "evento.del.viaje",
                "datos": {
                    "tipo": "mensaje_directo_nuevo",
                    "estudiante": estudiante_id,
                },
            },
        )


@transaction.atomic
def enviar_mensaje_directo(
    usuario,
    viaje_id,
    id_cliente,
    texto="",
    estudiante_id=None,
    respuesta_rapida=None,
):
    viaje = buscar_viaje(viaje_id)
    repetido = Mensaje.objects.filter(id_cliente=id_cliente).first()
    if repetido is not None:
        estudiante = usuario if not usuario.es_chofer else buscar_estudiante(estudiante_id)
        reglas.verificar_mismo_reenvio(repetido, usuario, viaje, estudiante)
        return repetido, False

    estudiante = _estudiante_del_chat(
        usuario,
        viaje,
        estudiante_id,
        respuesta_rapida,
        exigir_respuesta_rapida=usuario.es_chofer,
    )

    contenido = respuesta_rapida if usuario.es_chofer else texto
    reglas.verificar_texto(contenido)
    mensaje = Mensaje.objects.create(
        id_cliente=id_cliente,
        autor=usuario,
        viaje=viaje,
        estudiante=estudiante,
        texto=contenido.strip(),
        enviado_en=ahora_local(),
    )
    transaction.on_commit(
        lambda: _publicar_mensaje_directo(viaje.pk, estudiante.pk, mensaje)
    )
    return mensaje, True


def mensajes_directos(usuario, viaje_id, estudiante_id=None):
    viaje = buscar_viaje(viaje_id)
    estudiante = _estudiante_del_chat(usuario, viaje, estudiante_id)
    return Mensaje.objects.filter(viaje=viaje, estudiante=estudiante).select_related("autor")


def _es_chofer_de_la_ruta(usuario, ruta):
    return usuario.es_chofer and Viaje.objects.filter(ruta=ruta, chofer=usuario).exists()


def _verificar_chat_de_ruta(usuario, ruta):
    es_miembro = MiembroDeRuta.objects.filter(usuario=usuario, ruta=ruta).exists()
    reglas.verificar_es_miembro_de_la_ruta(
        es_miembro, _es_chofer_de_la_ruta(usuario, ruta), usuario
    )


@transaction.atomic
def elegir_ruta(usuario, ruta_id):
    ruta = buscar_ruta(ruta_id)
    reglas.verificar_puede_elegir_ruta(usuario)
    miembro, creado = MiembroDeRuta.objects.get_or_create(usuario=usuario, ruta=ruta)
    return miembro, creado


def membresia_de_ruta(usuario, ruta_id):
    ruta = buscar_ruta(ruta_id)
    es_miembro = MiembroDeRuta.objects.filter(usuario=usuario, ruta=ruta).exists()
    puede_entrar = es_miembro or _es_chofer_de_la_ruta(usuario, ruta) or usuario.es_administrador
    return ruta, es_miembro, puede_entrar


@transaction.atomic
def enviar_mensaje_de_ruta(usuario, ruta_id, id_cliente, texto):
    ruta = buscar_ruta(ruta_id)
    repetido = Mensaje.objects.filter(id_cliente=id_cliente).first()
    if repetido is not None:
        reglas.verificar_mismo_reenvio(repetido, usuario, ruta=ruta)
        return repetido, False

    _verificar_chat_de_ruta(usuario, ruta)
    reglas.verificar_texto(texto)
    mensaje = Mensaje.objects.create(
        id_cliente=id_cliente,
        autor=usuario,
        ruta=ruta,
        texto=texto.strip(),
        enviado_en=ahora_local(),
    )
    transaction.on_commit(
        lambda: _publicar(grupo_del_chat_de_ruta(ruta.pk), "mensaje_de_ruta", mensaje)
    )
    return mensaje, True


def mensajes_de_ruta(usuario, ruta_id):
    ruta = buscar_ruta(ruta_id)
    _verificar_chat_de_ruta(usuario, ruta)
    return Mensaje.objects.filter(ruta=ruta).select_related("autor")


def puede_entrar_al_chat_directo(usuario, viaje_id, estudiante_id):
    try:
        viaje = buscar_viaje(viaje_id)
        estudiante = buscar_estudiante(estudiante_id)
        if usuario.pk == estudiante.pk:
            reglas.verificar_confirmado(_aviso_confirmado(viaje, estudiante))
        else:
            reglas.verificar_chofer_del_viaje(viaje, usuario)
        return _aviso_confirmado(viaje, estudiante) is not None
    except Rechazo:
        return False


def puede_entrar_al_chat_de_ruta(usuario, ruta_id):
    try:
        ruta = buscar_ruta(ruta_id)
        _verificar_chat_de_ruta(usuario, ruta)
        return True
    except Rechazo:
        return False
