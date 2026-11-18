"""Distancias sobre el mapa, en metros."""
from math import asin, cos, radians, sin, sqrt

RADIO_DE_LA_TIERRA_M = 6_371_000


def distancia_en_metros(punto_a, punto_b):
    """Distancia entre dos puntos `(latitud, longitud)` (fórmula del haversine)."""
    lat_a, lng_a = map(radians, punto_a)
    lat_b, lng_b = map(radians, punto_b)
    d_lat = lat_b - lat_a
    d_lng = lng_b - lng_a
    h = sin(d_lat / 2) ** 2 + cos(lat_a) * cos(lat_b) * sin(d_lng / 2) ** 2
    return 2 * RADIO_DE_LA_TIERRA_M * asin(sqrt(h))


def coordenadas_validas(latitud, longitud):
    return -90 <= latitud <= 90 and -180 <= longitud <= 180
