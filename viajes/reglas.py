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
