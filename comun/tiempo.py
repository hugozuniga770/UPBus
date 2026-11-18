"""La hora del proyecto (BUS-RT-07).

Los servicios reciben `ahora` como parámetro, con este valor por defecto, para
que las pruebas no dependan del reloj (igual que en el proyecto de salas).
"""
from zoneinfo import ZoneInfo

from django.utils import timezone

ZONA_HORARIA = ZoneInfo("America/La_Paz")


def ahora():
    return timezone.now().astimezone(ZONA_HORARIA)


def a_hora_local(momento):
    return momento.astimezone(ZONA_HORARIA)
