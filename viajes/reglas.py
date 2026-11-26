"""Reglas puras de viajes y posiciones. No tocan la base de datos."""
from comun.geo import coordenadas_validas
from comun.rechazos import Rechazo, SinPermiso


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
