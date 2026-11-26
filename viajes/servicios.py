"""Servicios de viajes: orquestan reglas, transacciones y WebSockets."""
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction

from comun.rechazos import NoExiste
from comun.tiempo import a_hora_local, ahora as ahora_local
from rutas import reglas as reglas_de_rutas
from rutas.models import Parada
from rutas.servicios import registrar_paso

from . import reglas
from .consumers import grupo_del_viaje
from .models import Viaje


def buscar_viaje(viaje_id):
    viaje = (
        Viaje.objects.select_related("ruta", "horario", "chofer")
        .filter(pk=viaje_id)
        .first()
    )
    if viaje is None:
        raise NoExiste("el viaje no existe")
    return viaje


def listar_viajes(usuario, ruta_id=None, estado=None):
    viajes = Viaje.objects.select_related("ruta", "horario", "chofer")
    if getattr(usuario, "rol", None) == "chofer":
        viajes = viajes.filter(chofer=usuario)
    elif getattr(usuario, "rol", None) == "estudiante":
        viajes = viajes.filter(estado=Viaje.Estado.EN_CURSO)
    if ruta_id:
        viajes = viajes.filter(ruta_id=ruta_id)
    if estado:
        viajes = viajes.filter(estado=estado)
    return viajes


@transaction.atomic
def iniciar_viaje(usuario, viaje_id, ahora=None):
    viaje = buscar_viaje(viaje_id)
    reglas.verificar_es_su_viaje(viaje, usuario)
    reglas.verificar_programado(viaje)
    hay_otro = Viaje.objects.filter(
        chofer=usuario, estado=Viaje.Estado.EN_CURSO
    ).exclude(pk=viaje.pk).exists()
    reglas.verificar_sin_viaje_en_curso(hay_otro)
    viaje.estado = Viaje.Estado.EN_CURSO
    viaje.iniciado_en = ahora or ahora_local()
    viaje.save(update_fields=["estado", "iniciado_en"])
    return viaje


@transaction.atomic
def terminar_viaje(usuario, viaje_id, ahora=None):
    viaje = buscar_viaje(viaje_id)
    reglas.verificar_es_su_viaje(viaje, usuario)
    reglas.verificar_en_curso(viaje)
    viaje.estado = Viaje.Estado.TERMINADO
    viaje.terminado_en = ahora or ahora_local()
    viaje.save(update_fields=["estado", "terminado_en"])
    return viaje


def _datos_de_posicion(viaje, latitud, longitud, tomada_en):
    return {
        "tipo": "posicion",
        "viaje": viaje.pk,
        "ruta": viaje.ruta_id,
        "latitud": latitud,
        "longitud": longitud,
        "tomada_en": a_hora_local(tomada_en).isoformat(),
    }


def _enviar_posicion(viaje_id, datos):
    capa = get_channel_layer()
    async_to_sync(capa.group_send)(
        grupo_del_viaje(viaje_id), {"type": "evento.del.viaje", "datos": datos}
    )


@transaction.atomic
def registrar_posicion(usuario, viaje_id, id_cliente, latitud, longitud, tomada_en):
    viaje = buscar_viaje(viaje_id)
    reglas.verificar_es_su_viaje(viaje, usuario)
    repetida = viaje.posiciones.filter(id_cliente=id_cliente).first()
    if repetida is not None:
        return viaje, False
    reglas.verificar_en_curso(viaje)
    reglas.verificar_coordenadas(latitud, longitud)
    viaje.posiciones.create(
        id_cliente=id_cliente,
        latitud=latitud,
        longitud=longitud,
        tomada_en=tomada_en,
    )

    es_la_mas_reciente = (
        viaje.ultima_posicion_en is None or tomada_en >= viaje.ultima_posicion_en
    )
    if es_la_mas_reciente:
        viaje.ultima_latitud = latitud
        viaje.ultima_longitud = longitud
        viaje.ultima_posicion_en = tomada_en
        viaje.save(
            update_fields=["ultima_latitud", "ultima_longitud", "ultima_posicion_en"]
        )

    paradas = list(
        viaje.ruta.paradas.exclude(estado=Parada.Estado.RECHAZADA).exclude(
            pk__in=viaje.paradas_registradas.values("pk")
        )
    )
    parada = reglas_de_rutas.parada_mas_cercana((latitud, longitud), paradas)
    if parada is not None:
        salida = reglas_de_rutas.salida_programada(viaje.horario.salida, tomada_en)
        registrar_paso(
            parada,
            viaje.horario,
            reglas_de_rutas.minutos_entre(salida, tomada_en),
            tomada_en,
        )
        viaje.paradas_registradas.add(parada)

    if es_la_mas_reciente:
        datos = _datos_de_posicion(viaje, latitud, longitud, tomada_en)
        transaction.on_commit(lambda: _enviar_posicion(viaje.pk, datos))
    return viaje, True
