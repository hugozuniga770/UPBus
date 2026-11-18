"""Datos comunes de las pruebas: los de la sección 0 de la sesión 6.

Las coordenadas son ficticias: solo importan las distancias entre puntos.
"""
from datetime import datetime, time
from io import StringIO
from math import cos, radians
from pathlib import Path

import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from comun.tiempo import ZONA_HORARIA
from cuentas.models import Usuario
from rutas.models import Ruta

CONTRASENA = "clave-segura-123"
PADRON_DE_PRUEBA = Path(__file__).parent / "datos" / "padron_de_prueba.json"
LA_FONTANA = (-17.7200, -63.1650)


def punto_a(desde, metros_al_norte=0, metros_al_este=0):
    """Un punto a cierta distancia de otro, para armar distancias exactas."""
    latitud = desde[0] + metros_al_norte / 111_320
    longitud = desde[1] + metros_al_este / (111_320 * cos(radians(desde[0])))
    return (latitud, longitud)


SEVILLA = punto_a(LA_FONTANA, metros_al_norte=-3_000)
PETROL = punto_a(LA_FONTANA, metros_al_norte=-5_000, metros_al_este=1_500)
CAMPOS = punto_a(LA_FONTANA, metros_al_norte=-7_000, metros_al_este=2_500)
CAMPUS_UPB = punto_a(LA_FONTANA, metros_al_norte=-12_000, metros_al_este=4_000)


@pytest.fixture(autouse=True)
def padron_de_prueba(settings):
    settings.UPBUS_PADRON = str(PADRON_DE_PRUEBA)


@pytest.fixture
def hora():
    def armar(dia, horas, minutos=0):
        return datetime(2026, 11, dia, horas, minutos, tzinfo=ZONA_HORARIA)

    return armar


def crear_cuenta(nombre, correo, rol, codigo=None):
    return Usuario.objects.create_user(
        correo=correo, password=CONTRASENA, nombre=nombre, rol=rol, codigo=codigo
    )


@pytest.fixture
def hugo(db):
    return crear_cuenta("Hugo Zuñiga", "hugo.zuniga@upb.example", "administrador", "70001")


@pytest.fixture
def sebastian(db):
    return crear_cuenta("Sebastian Cruz", "sebastian.cruz@upb.example", "administrador", "70002")


@pytest.fixture
def ismael(db):
    return crear_cuenta("Ismael", "ismael@upb.example", "estudiante", "70004")


@pytest.fixture
def marco(db):
    return crear_cuenta("Marco", "marco.chofer@upbus.example", "chofer")


@pytest.fixture
def cliente():
    return APIClient()


@pytest.fixture
def cliente_de():
    def armar(usuario):
        cliente = APIClient()
        cliente.force_login(usuario)
        return cliente

    return armar


@pytest.fixture
def ruta_norte(db):
    call_command("cargar_rutas", stdout=StringIO())
    return Ruta.objects.get(clave="norte")


@pytest.fixture
def horario_0640(ruta_norte):
    return ruta_norte.horarios.get(sentido="ingreso", salida=time(6, 40))
