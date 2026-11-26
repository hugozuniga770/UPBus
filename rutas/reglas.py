"""Reglas de rutas, paradas y modo registro. No tocan la base de datos."""
from datetime import date, datetime, timedelta
from math import floor

from django.conf import settings

from comun.geo import coordenadas_validas, distancia_en_metros
from comun.rechazos import Rechazo, SinPermiso
from comun.tiempo import ZONA_HORARIA, a_hora_local

from comun.geo import coordenadas_validas, distancia_a_recorrido, distancia_en_metros

RADIO_DE_LLEGADA_M = 50  # RF-11: por defecto, el bus «llega» a menos de 50 m (C-34)
PASOS_PARA_EL_PROMEDIO = 5  # P-11 [PROVISIONAL]
MINUTOS_HASTA_LA_U = 60  # P-06 [PROVISIONAL] cuando un horario no tiene llegada
DISTANCIA_MAXIMA_PROPUESTA_M = 200  # P-07: propuesta de parada a menos de 200 m del recorrido


def radio_de_llegada():
    """Metros a los que el bus «llega» a una parada (RF-11).

    Empieza en 50 m y se calibra con `UPBUS_RADIO_DE_LLEGADA_M`, sin cambiar el
    código, después de los viajes de prueba (C-34). La usan también el modo
    registro (RF-23) y el simulador.
    """
    return getattr(settings, "UPBUS_RADIO_DE_LLEGADA_M", RADIO_DE_LLEGADA_M)


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
    radio = radio_de_llegada()
    for marca in marcas_anteriores:
        if distancia_en_metros(punto, marca.punto) < radio:
            raise Rechazo(f"ya marcaste una parada a menos de {radio:g} m")


def verificar_hay_marcas(cantidad):
    if cantidad == 0:
        raise Rechazo("no marcaste ninguna parada")


def estado_de_una_parada_nueva(usuario):
    """La de un administrador queda aprobada; la de un chofer, propuesta (C-17, P-25)."""
    return "aprobada" if getattr(usuario, "es_administrador", False) else "propuesta"


# ---- Paradas y horas aproximadas (BUS-RF-11) ----

def llego_a_la_parada(distancia_m):
    return distancia_m < radio_de_llegada()


def parada_mas_cercana(punto, paradas):
    """La parada más cercana entre las que están a menos del radio de llegada, o `None`."""
    mejor, mejor_distancia = None, None
    for parada in paradas:
        distancia = distancia_en_metros(punto, parada.punto)
        if llego_a_la_parada(distancia) and (mejor is None or distancia < mejor_distancia):
            mejor, mejor_distancia = parada, distancia
    return mejor


def minutos_entre(inicio, fin):
    return (fin - inicio).total_seconds() / 60


def salida_programada(salida, momento):
    """La hora de salida del horario en el día de `momento`, en la hora de La Paz.

    Los minutos de cada paso se cuentan desde aquí y no desde la primera marca:
    si el bus sale tarde, ese atraso también se aprende (C-23).
    """
    return datetime.combine(a_hora_local(momento).date(), salida, tzinfo=ZONA_HORARIA)


def promedio_de_los_ultimos(minutos_del_mas_nuevo_al_mas_viejo, cantidad=PASOS_PARA_EL_PROMEDIO):
    ultimos = list(minutos_del_mas_nuevo_al_mas_viejo)[:cantidad]
    if not ultimos:
        return None
    return sum(ultimos) / len(ultimos)


def hora_aproximada(salida, minutos):
    """Hora de salida del horario + minutos aprendidos, redondeada hacia abajo.

    Hacia abajo para que nadie llegue tarde: si el bus pasó a las 07:00:54,
    la parada muestra 07:00 (C-23).
    """
    if minutos is None:
        return None
    momento = datetime.combine(date(2000, 1, 1), salida) + timedelta(minutes=floor(minutos))
    return momento.time()


def llegada_limite(horario):
    if horario.llegada_limite:
        return horario.llegada_limite
    momento = datetime.combine(date(2000, 1, 1), horario.salida) + timedelta(minutes=MINUTOS_HASTA_LA_U)
    return momento.time()

# ---- HU-08: paradas propuestas y su aprobación (BUS-RF-10, P-07, P-28) ----

def verificar_ruta_con_recorrido(recorrido):
    if len(recorrido or []) < 2:
        raise Rechazo("esta ruta aún no tiene un recorrido grabado")


def verificar_cerca_del_recorrido(punto, recorrido):
    verificar_ruta_con_recorrido(recorrido)
    if distancia_a_recorrido(punto, recorrido) > DISTANCIA_MAXIMA_PROPUESTA_M:
        raise Rechazo(f"la parada debe estar a menos de {DISTANCIA_MAXIMA_PROPUESTA_M} m del recorrido")


def verificar_lejos_de_paradas_existentes(punto, paradas):
    radio = radio_de_llegada()
    for parada in paradas:
        if distancia_en_metros(punto, parada.punto) < radio:
            raise Rechazo(f"ya existe una parada a menos de {radio:g} m")


def verificar_puede_aprobar_parada(usuario):
    if not getattr(usuario, "es_administrador", False):
        raise SinPermiso("solo un administrador puede aprobar o rechazar paradas")


def verificar_parada_propuesta(parada):
    if parada.estado != "propuesta":
        raise Rechazo("esa parada no está pendiente de aprobación")