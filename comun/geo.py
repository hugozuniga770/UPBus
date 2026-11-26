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


def _distancia_a_segmento_m(punto, inicio, fin):
    """Distancia en metros desde `punto` hasta el segmento `[inicio, fin]`."""
    lat_0 = radians(punto[0])
    cos_lat = cos(lat_0)
    m_por_rad = RADIO_DE_LA_TIERRA_M

    def a_xy(p):
        return (radians(p[1]) * cos_lat * m_por_rad, radians(p[0]) * m_por_rad)

    px, py = a_xy(punto)
    ax, ay = a_xy(inicio)
    bx, by = a_xy(fin)
    dx, dy = bx - ax, by - ay
    largo_cuadrado = dx * dx + dy * dy
    if largo_cuadrado == 0:
        return sqrt((px - ax) ** 2 + (py - ay) ** 2)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / largo_cuadrado))
    proy_x = ax + t * dx
    proy_y = ay + t * dy
    return sqrt((px - proy_x) ** 2 + (py - proy_y) ** 2)


def distancia_a_recorrido(punto, recorrido):
    """Distancia mínima en metros desde `punto` hasta la polilínea `recorrido`."""
    if not recorrido:
        return float("inf")
    if len(recorrido) == 1:
        return distancia_en_metros(punto, recorrido[0])
    return min(
        _distancia_a_segmento_m(punto, recorrido[i], recorrido[i + 1])
        for i in range(len(recorrido) - 1)
    )


def coordenadas_validas(latitud, longitud):
    return -90 <= latitud <= 90 and -180 <= longitud <= 180
