"""HU-01 · Registrarme con el padrón (BUS-RF-01)."""
import pytest
from django.contrib.auth import authenticate

from cuentas.models import Usuario
from cuentas.padron import leer_padron

pytestmark = pytest.mark.django_db

CONTRASENA = "clave-segura-123"


def registrar(cliente, codigo, correo, contrasena=CONTRASENA, confirmacion=CONTRASENA):
    return cliente.post(
        "/api/registro",
        {"codigo": codigo, "correo": correo, "contrasena": contrasena, "confirmacion": confirmacion},
        format="json",
    )


def test_HU01_CA1_registra_cuenta_con_codigo_y_correo_del_padron(cliente):
    padron_antes = leer_padron()

    respuesta = registrar(cliente, "70004", "ismael@upb.example")

    assert respuesta.status_code == 201
    cuenta = Usuario.objects.get(codigo="70004")
    assert cuenta.rol == "estudiante"
    assert authenticate(username="70004", password=CONTRASENA) == cuenta
    assert leer_padron() == padron_antes


def test_HU01_CA2_rechaza_registro_de_persona_inactiva(cliente):
    respuesta = registrar(cliente, "70005", "lucia.pena@upb.example")

    assert respuesta.status_code == 400
    assert respuesta.json()["causa"] == "persona no activa en el padrón"
    assert Usuario.objects.count() == 0


def test_HU01_CA3_rechaza_si_las_contrasenas_no_coinciden(cliente):
    respuesta = registrar(cliente, "70004", "ismael@upb.example", confirmacion="otra-clave-456")

    assert respuesta.status_code == 400
    assert respuesta.json()["causa"] == "las contraseñas no coinciden"
    assert Usuario.objects.count() == 0


def test_HU01_CA4_la_cuenta_toma_el_rol_de_administrador_del_padron(cliente):
    respuesta = registrar(cliente, "70001", "hugo.zuniga@upb.example")

    assert respuesta.status_code == 201
    cuenta = Usuario.objects.get(codigo="70001")
    assert cuenta.rol == "administrador"
    assert cuenta.puede_actuar_como_estudiante
