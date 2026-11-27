"""Servicios de viajes: orquestan reglas, transacciones y WebSockets."""
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction
from django.db.models import Q

from comun.rechazos import NoExiste
from comun.tiempo import a_hora_local, ahora as ahora_local
from rutas import reglas as reglas_de_rutas
from rutas.models import Parada
from rutas.servicios import minutos_aprendidos, registrar_paso

from . import reglas
from .consumers import grupo_del_chofer, grupo_del_viaje
from .models import AvisoDeSubida, Viaje


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
        # En curso, o programados desde hoy: para avisar «Voy a subir» antes de que salga (HU-07).
        hoy = a_hora_local(ahora_local()).date()
        viajes = viajes.filter(
            Q(estado=Viaje.Estado.EN_CURSO) | Q(estado=Viaje.Estado.PROGRAMADO, fecha__gte=hoy)
        )
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
    cerrar_avisos_del_viaje(viaje)
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
        if not viaje.simulado:  # C-28: solo los viajes reales enseñan horas
            salida = reglas_de_rutas.salida_programada(viaje.horario.salida, tomada_en)
            registrar_paso(
                parada,
                viaje.horario,
                reglas_de_rutas.minutos_entre(salida, tomada_en),
                tomada_en,
            )
        viaje.paradas_registradas.add(parada)
        cerrar_no_presentados(viaje, parada)

    if es_la_mas_reciente:
        _procesar_cercania_y_sugerencias(viaje, latitud, longitud, tomada_en)
        _procesar_abordaje_automatico(viaje, latitud, longitud, tomada_en)
        datos = _datos_de_posicion(viaje, latitud, longitud, tomada_en)
        transaction.on_commit(lambda: _enviar_posicion(viaje.pk, datos))
    return viaje, True


# «Voy a subir» y ubicación del estudiante (HU-07, BUS-RF-08 y BUS-RF-09)

def _publicar_al_chofer(viaje_id, datos):
    capa = get_channel_layer()
    async_to_sync(capa.group_send)(
        grupo_del_chofer(viaje_id), {"type": "evento.del.viaje", "datos": datos}
    )


def buscar_aviso(aviso_id):
    aviso = (
        AvisoDeSubida.objects.select_related("viaje", "parada", "estudiante")
        .filter(pk=aviso_id)
        .first()
    )
    if aviso is None:
        raise NoExiste("el aviso no existe")
    return aviso


@transaction.atomic
def avisar_que_va_a_subir(usuario, viaje_id, parada_id):
    viaje = buscar_viaje(viaje_id)
    reglas.verificar_puede_avisar(usuario)
    reglas.verificar_viaje_abierto(viaje)
    parada = Parada.objects.filter(pk=parada_id).first()
    reglas.verificar_parada_de_la_ruta(parada, viaje)
    reglas.verificar_bus_no_paso(viaje.paradas_registradas.filter(pk=parada.pk).exists())
    reglas.verificar_sin_aviso_activo(
        viaje.avisos.filter(estudiante=usuario, estado__in=AvisoDeSubida.ACTIVOS).exists()
    )
    aviso = AvisoDeSubida.objects.create(viaje=viaje, estudiante=usuario, parada=parada)
    datos = {
        "tipo": "aviso",
        "aviso": aviso.pk,
        "estudiante": usuario.nombre,
        "parada": parada.nombre,
        "mensaje": f"{usuario.nombre} va a subir en {parada.nombre}",
    }
    transaction.on_commit(lambda: _publicar_al_chofer(viaje.pk, datos))
    return aviso


def dejar_de_compartir(aviso):
    """Borra la ubicación del estudiante. Lo usan cancelar, cerrar y «subió» (BUS-RF-08)."""
    aviso.ubicacion_latitud = aviso.ubicacion_longitud = aviso.ubicacion_en = None
    aviso.ubicacion_anterior_cerca_del_bus = False


def _cerrar(aviso, estado, momento=None):
    aviso.estado = estado
    aviso.cerrado_en = momento or ahora_local()
    dejar_de_compartir(aviso)
    aviso.save(update_fields=[
        "estado",
        "cerrado_en",
        "ubicacion_latitud",
        "ubicacion_longitud",
        "ubicacion_en",
        "ubicacion_anterior_cerca_del_bus",
    ])
    datos = {"tipo": "aviso_cerrado", "aviso": aviso.pk, "estado": estado}
    transaction.on_commit(lambda: _publicar_al_chofer(aviso.viaje_id, datos))


@transaction.atomic
def marcar_a_bordo(usuario, aviso_id, momento=None):
    """HU-10 CA1-CA3 y HU07-CA6: registra que el estudiante subió y deja de compartir ubicación."""
    aviso = buscar_aviso(aviso_id)
    reglas.verificar_puede_marcar_abordaje(aviso, aviso.viaje, usuario)
    _completar_abordaje(aviso, momento)
    return aviso


@transaction.atomic
def marcar_no_se_presento(usuario, aviso_id, momento=None):
    """HU-10 CA4: el chofer marca que el estudiante no se presentó en la parada."""
    aviso = buscar_aviso(aviso_id)
    reglas.verificar_puede_marcar_no_se_presento(aviso, aviso.viaje, usuario)
    _cerrar(aviso, AvisoDeSubida.Estado.NO_SE_PRESENTO, momento)
    return aviso


@transaction.atomic
def cancelar_aviso(usuario, aviso_id):
    aviso = buscar_aviso(aviso_id)
    reglas.verificar_es_su_aviso(aviso, usuario)
    reglas.verificar_aviso_confirmado(aviso)
    reglas.verificar_bus_no_paso(
        aviso.viaje.paradas_registradas.filter(pk=aviso.parada_id).exists()
    )
    _cerrar(aviso, AvisoDeSubida.Estado.CANCELADO)
    return aviso


@transaction.atomic
def compartir_ubicacion(usuario, aviso_id, latitud, longitud, tomada_en):
    aviso = buscar_aviso(aviso_id)
    reglas.verificar_es_su_aviso(aviso, usuario)
    reglas.verificar_aviso_confirmado(aviso)
    reglas.verificar_coordenadas(latitud, longitud)
    aviso.ubicacion_latitud, aviso.ubicacion_longitud, aviso.ubicacion_en = latitud, longitud, tomada_en
    aviso.save(
        update_fields=[
            "ubicacion_latitud",
            "ubicacion_longitud",
            "ubicacion_en",
        ]
    )
    viaje = aviso.viaje
    posicion_bus = (
        (viaje.ultima_latitud, viaje.ultima_longitud)
        if viaje.ultima_posicion_en is not None
        else None
    )
    if _evaluar_abordaje_automatico_aviso(aviso, posicion_bus, tomada_en):
        return aviso

    datos = {
        "tipo": "ubicacion",
        "aviso": aviso.pk,
        "estudiante": aviso.estudiante.nombre,
        "latitud": latitud,
        "longitud": longitud,
        "tomada_en": a_hora_local(tomada_en).isoformat(),
    }
    transaction.on_commit(lambda: _publicar_al_chofer(aviso.viaje_id, datos))
    return aviso


def avisos_del_viaje(usuario, viaje_id):
    """Los que van a subir o ya subieron, con su ubicación: solo para el chofer y el administrador."""
    viaje = buscar_viaje(viaje_id)
    reglas.verificar_puede_ver_avisos(viaje, usuario)
    return viaje.avisos.select_related("estudiante", "parada").filter(
        estado__in=AvisoDeSubida.ACTIVOS
    )


def aviso_activo_de(usuario, viaje_id):
    viaje = buscar_viaje(viaje_id)
    return viaje.avisos.select_related("estudiante", "parada").filter(
        estudiante=usuario, estado__in=AvisoDeSubida.ACTIVOS
    ).first()


def cerrar_no_presentados(viaje, parada_actual):
    """El bus llegó a otra parada: quien esperaba en una que ya pasó queda «no se presentó» (RF-09)."""
    pendientes = viaje.avisos.filter(
        estado=AvisoDeSubida.Estado.CONFIRMADO,
        parada__in=viaje.paradas_registradas.exclude(pk=parada_actual.pk),
    )
    for aviso in pendientes:
        _cerrar(aviso, AvisoDeSubida.Estado.NO_SE_PRESENTO)


def cerrar_avisos_del_viaje(viaje):
    """Al terminar el viaje nadie sigue esperando ni compartiendo su ubicación (RF-08, HU05-CA3)."""
    for aviso in viaje.avisos.filter(estado=AvisoDeSubida.Estado.CONFIRMADO):
        _cerrar(aviso, AvisoDeSubida.Estado.NO_SE_PRESENTO, viaje.terminado_en)
    viaje.avisos.filter(estado=AvisoDeSubida.Estado.A_BORDO).exclude(ubicacion_en=None).update(
        ubicacion_latitud=None, ubicacion_longitud=None, ubicacion_en=None
    )


def _procesar_cercania_y_sugerencias(viaje, latitud, longitud, tomada_en):
    posicion_bus = (latitud, longitud)

    # HU-09 CA1-CA3: «Tu bus está cerca» a 500 m o menos, una sola vez por viaje (RF-13).
    pendientes = viaje.avisos.select_related("parada").filter(
        estado=AvisoDeSubida.Estado.CONFIRMADO,
        aviso_cercania_enviado=False,
    )
    for aviso in pendientes:
        if reglas.esta_cerca_de_parada(posicion_bus, aviso.parada.punto):
            aviso.aviso_cercania_enviado = True
            aviso.save(update_fields=["aviso_cercania_enviado"])
            # Va por el canal público del viaje, sin datos de la persona: cada estudiante
            # reconoce su aviso por su id (la ubicación de los estudiantes es sensible, ENT-07).
            datos = {
                "tipo": "bus_cerca",
                "aviso": aviso.pk,
                "parada": aviso.parada_id,
                "mensaje": f"Tu bus está cerca de {aviso.parada.nombre}",
            }
            transaction.on_commit(lambda d=datos: _enviar_posicion(viaje.pk, d))

    # HU-09 CA4-CA5: si nadie espera y el bus va atrasado, se sugiere seguir; el chofer decide (RF-12).
    paradas_con_espera = viaje.avisos.filter(estado=AvisoDeSubida.Estado.CONFIRMADO).values("parada_id")
    sin_nadie = (
        viaje.ruta.paradas.filter(estado=Parada.Estado.APROBADA)
        .exclude(pk__in=paradas_con_espera)
        .exclude(pk__in=viaje.paradas_registradas.values("pk"))
        .exclude(pk__in=viaje.paradas_sugeridas_saltar.values("pk"))
    )
    salida = reglas_de_rutas.salida_programada(viaje.horario.salida, tomada_en)
    for parada in sin_nadie:
        if not reglas.esta_cerca_de_parada(posicion_bus, parada.punto):
            continue
        minutos = minutos_aprendidos(parada, viaje.horario)
        if not reglas.va_atrasado(salida, minutos, viaje.iniciado_en, tomada_en):
            continue
        viaje.paradas_sugeridas_saltar.add(parada)
        datos = {
            "tipo": "sugerencia_saltar",
            "viaje": viaje.pk,
            "parada": parada.pk,
            "parada_nombre": parada.nombre,
            "mensaje": f"Nadie espera en {parada.nombre}: puedes seguir",
        }
        transaction.on_commit(lambda d=datos: _publicar_al_chofer(viaje.pk, d))


def _evaluar_abordaje_automatico_aviso(aviso, posicion_bus, momento=None, desde_bus=False):
    if posicion_bus is None or aviso.ubicacion_en is None:
        return False
    ubicacion_actual = (aviso.ubicacion_latitud, aviso.ubicacion_longitud)
    # Sube solo con una ubicación nueva del estudiante: la anterior ya estuvo junto al bus y
    # esta también. Una posición nueva del bus no cuenta como otra ubicación suya (P-33).
    if not desde_bus and reglas.cumple_abordaje_automatico(
        posicion_bus, aviso.parada.punto, ubicacion_actual, aviso.ubicacion_anterior_cerca_del_bus
    ):
        _completar_abordaje(aviso, momento)
        return True
    cerca_ahora = reglas.distancia_en_metros(ubicacion_actual, posicion_bus) < reglas.DISTANCIA_A_BORDO_M
    if cerca_ahora and not aviso.ubicacion_anterior_cerca_del_bus:
        aviso.ubicacion_anterior_cerca_del_bus = True
        aviso.save(update_fields=["ubicacion_anterior_cerca_del_bus"])
    elif not desde_bus and not cerca_ahora and aviso.ubicacion_anterior_cerca_del_bus:
        # Solo reinicia si el bus ya reportó una posición posterior a esta ubicación del estudiante
        if aviso.viaje.ultima_posicion_en and aviso.viaje.ultima_posicion_en >= aviso.ubicacion_en:
            aviso.ubicacion_anterior_cerca_del_bus = False
            aviso.save(update_fields=["ubicacion_anterior_cerca_del_bus"])
    return False


def _procesar_abordaje_automatico(viaje, latitud, longitud, tomada_en):
    posicion_bus = (latitud, longitud)
    candidatos = viaje.avisos.select_related("parada", "estudiante").filter(
        estado=AvisoDeSubida.Estado.CONFIRMADO,
        ubicacion_en__isnull=False,
    )
    for aviso in candidatos:
        _evaluar_abordaje_automatico_aviso(aviso, posicion_bus, tomada_en, desde_bus=True)


def _completar_abordaje(aviso, momento=None):
    aviso.estado = AvisoDeSubida.Estado.A_BORDO
    aviso.cerrado_en = momento or ahora_local()
    dejar_de_compartir(aviso)
    aviso.save(
        update_fields=[
            "estado",
            "cerrado_en",
            "ubicacion_latitud",
            "ubicacion_longitud",
            "ubicacion_en",
            "ubicacion_anterior_cerca_del_bus",
        ]
    )
    nombre = aviso.estudiante.nombre
    al_chofer = {
        "tipo": "aviso_actualizado",
        "aviso": aviso.pk,
        "estado": aviso.estado,
        "estudiante": nombre,
        "mensaje": f"{nombre}: ha subido",
    }
    # Al canal público va sin el nombre: solo el estudiante de ese aviso lo reconoce.
    al_viaje = {"tipo": "aviso_actualizado", "aviso": aviso.pk, "estado": aviso.estado}
    transaction.on_commit(lambda: _publicar_al_chofer(aviso.viaje_id, al_chofer))
    transaction.on_commit(lambda: _enviar_posicion(aviso.viaje_id, al_viaje))
