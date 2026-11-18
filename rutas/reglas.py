"""Reglas de rutas, paradas y modo registro. No tocan la base de datos."""
from datetime import date, datetime, timedelta
from math import floor

from comun.geo import coordenadas_validas, distancia_en_metros
from comun.rechazos import Rechazo, SinPermiso

RADIO_DE_LLEGADA_M = 50  # RF-11: el bus «llega» a menos de 50 m
PASOS_PARA_EL_PROMEDIO = 5  # P-11 [PROVISIONAL]
MINUTOS_HASTA_LA_U = 60  # P-06 [PROVISIONAL] cuando un horario no tiene llegada


# ---- HU-18: modo registro (BUS-RF-23) ----

def verificar_puede_registrar(usuario):
    if getattr(usuario, "rol", None) not in ("chofer", "administrador"):
        raise SinPermiso("solo un chofer o un administrador puede usar el modo registro")


def verificar_horario_de_la_ruta(horario, ruta):
    if horario is not None and horario.ruta_id != ruta.id:
        raise Rechazo("ese horario no es de esta ruta")


def verificar_sin_registro_en_curso(hay_registro_en_curso):
    if hay_registro_en_curso:
        raise Rechazo("ya tienes un registro en curso")


def verificar_es_su_registro(registro, usuario):
    if registro.usuario_id != usuario.pk:
        raise SinPermiso("este registro no es tuyo")


def verificar_registro_en_curso(registro):
    if registro.estado != "en_curso":
        raise Rechazo("el registro no está en curso")


def verificar_coordenadas(latitud, longitud):
    if not coordenadas_validas(latitud, longitud):
        raise Rechazo("coordenadas no válidas")


def verificar_lejos_de_las_otras_marcas(punto, marcas_anteriores):
    for marca in marcas_anteriores:
        if distancia_en_metros(punto, marca.punto) < RADIO_DE_LLEGADA_M:
            raise Rechazo("ya marcaste una parada a menos de 50 m")


def verificar_hay_marcas(cantidad):
    if cantidad == 0:
        raise Rechazo("no marcaste ninguna parada")


def estado_de_una_parada_nueva(usuario):
    """La de un administrador queda aprobada; la de un chofer, propuesta (C-17, P-25)."""
    return "aprobada" if getattr(usuario, "es_administrador", False) else "propuesta"


# ---- Paradas y horas aproximadas (BUS-RF-11) ----

def llego_a_la_parada(distancia_m):
    return distancia_m < RADIO_DE_LLEGADA_M


def parada_mas_cercana(punto, paradas):
    """La parada a menos de 50 m más cercana, o `None`."""
    mejor, mejor_distancia = None, None
    for parada in paradas:
        distancia = distancia_en_metros(punto, parada.punto)
        if llego_a_la_parada(distancia) and (mejor is None or distancia < mejor_distancia):
            mejor, mejor_distancia = parada, distancia
    return mejor


def minutos_entre(inicio, fin):
    return (fin - inicio).total_seconds() / 60


def promedio_de_los_ultimos(minutos_del_mas_nuevo_al_mas_viejo, cantidad=PASOS_PARA_EL_PROMEDIO):
    ultimos = list(minutos_del_mas_nuevo_al_mas_viejo)[:cantidad]
    if not ultimos:
        return None
    return sum(ultimos) / len(ultimos)


def hora_aproximada(salida, minutos):
    """Hora de salida del horario + minutos aprendidos, redondeada al minuto."""
    if minutos is None:
        return None
    momento = datetime.combine(date(2000, 1, 1), salida) + timedelta(minutes=floor(minutos + 0.5))
    return momento.time()


def llegada_limite(horario):
    if horario.llegada_limite:
        return horario.llegada_limite
    momento = datetime.combine(date(2000, 1, 1), horario.salida) + timedelta(minutes=MINUTOS_HASTA_LA_U)
    return momento.time()
