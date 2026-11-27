"""Reglas puras de viajes y posiciones. No tocan la base de datos."""
from comun.geo import coordenadas_validas
from comun.rechazos import Rechazo, SinPermiso
from comun.geo import coordenadas_validas, distancia_en_metros

DISTANCIA_BUS_CERCA_M = 500
DISTANCIA_BUS_ALEJADO_M = 100
DISTANCIA_A_BORDO_M = 50

def verificar_es_su_viaje(viaje, usuario):
    if viaje.chofer_id != usuario.pk:
        raise SinPermiso("este viaje no es tuyo")


def verificar_programado(viaje):
    if viaje.estado != "programado":
        raise Rechazo("el viaje no está programado")


def verificar_sin_viaje_en_curso(hay_otro_en_curso):
    if hay_otro_en_curso:
        raise Rechazo("ya tienes un viaje en curso")


def verificar_en_curso(viaje):
    if viaje.estado != "en_curso":
        raise Rechazo("el viaje no está en curso")


def verificar_coordenadas(latitud, longitud):
    if not coordenadas_validas(latitud, longitud):
        raise Rechazo("coordenadas no válidas")


# «Voy a subir» y ubicación del estudiante (HU-07, BUS-RF-08 y BUS-RF-09)

def verificar_puede_avisar(usuario):
    if not usuario.puede_actuar_como_estudiante:
        raise SinPermiso("solo un estudiante puede avisar que va a subir")


def verificar_viaje_abierto(viaje):
    if viaje.estado not in ("programado", "en_curso"):
        raise Rechazo("el viaje ya terminó")


def verificar_parada_de_la_ruta(parada, viaje):
    if parada is None or parada.ruta_id != viaje.ruta_id or parada.estado != "aprobada":
        raise Rechazo("esa parada no es de esta ruta")


def verificar_bus_no_paso(ya_paso):
    if ya_paso:
        raise Rechazo("el bus ya pasó por esa parada")


def verificar_sin_aviso_activo(hay_aviso_activo):
    if hay_aviso_activo:
        raise Rechazo("ya avisaste que vas a subir en este viaje")


def verificar_es_su_aviso(aviso, usuario):
    if aviso.estudiante_id != usuario.pk:
        raise SinPermiso("este aviso no es tuyo")


def verificar_aviso_confirmado(aviso):
    if aviso.estado != "confirmado":
        raise Rechazo("el aviso ya no está confirmado")


def verificar_puede_ver_avisos(viaje, usuario):
    if viaje.chofer_id != usuario.pk and not usuario.es_administrador:
        raise SinPermiso("solo el chofer de este viaje puede ver quién va a subir")


# Simulador de escenarios (T23)

def verificar_escenario(escenario, escenarios):
    if escenario not in escenarios:
        raise Rechazo("ese escenario no existe")


def verificar_velocidad(velocidad):
    if not 1 <= velocidad <= 60:
        raise Rechazo("la velocidad debe estar entre 1 y 60")


def verificar_recorrido(recorrido):
    if len(recorrido or []) < 2:
        raise Rechazo("la ruta no tiene recorrido: grábala con el modo registro")


def verificar_hay_paradas(paradas):
    if not paradas:
        raise Rechazo("la ruta no tiene paradas aprobadas")


def verificar_sin_simulacion_en_curso(hay_otra):
    if hay_otra:
        raise Rechazo("ya hay una simulación en curso: detenla primero")

def esta_cerca_de_parada(posicion_bus, punto_parada):
    return distancia_en_metros(posicion_bus, punto_parada) <= DISTANCIA_BUS_CERCA_M


def debe_sugerir_saltar_parada(posicion_bus, punto_parada, nadie_espera, va_atrasado):
    return (
        nadie_espera
        and va_atrasado
        and esta_cerca_de_parada(posicion_bus, punto_parada)
    )


def verificar_puede_marcar_abordaje(aviso, viaje, usuario):
    verificar_viaje_abierto(viaje)
    es_estudiante_del_aviso = aviso.estudiante_id == usuario.pk
    es_chofer_o_admin = viaje.chofer_id == usuario.pk or getattr(usuario, "es_administrador", False)
    if not (es_estudiante_del_aviso or es_chofer_o_admin):
        raise SinPermiso("no tienes permiso para registrar este abordaje")
    verificar_aviso_confirmado(aviso)


def verificar_puede_marcar_no_se_presento(aviso, viaje, usuario):
    verificar_viaje_abierto(viaje)
    verificar_puede_ver_avisos(viaje, usuario)
    verificar_aviso_confirmado(aviso)


def cumple_abordaje_automatico(posicion_bus, punto_parada, ubicacion_actual, anterior_cerca_del_bus):
    """C-30, P-33: bus > 100 m lejos de la parada y 2 ubicaciones seguidas < 50 m del bus."""
    if posicion_bus is None or ubicacion_actual is None or not anterior_cerca_del_bus:
        return False
    if distancia_en_metros(posicion_bus, punto_parada) <= DISTANCIA_BUS_ALEJADO_M:
        return False
    return distancia_en_metros(ubicacion_actual, posicion_bus) < DISTANCIA_A_BORDO_M