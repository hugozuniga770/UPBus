"""HU-03 · Gestionar usuarios (BUS-RF-03, BUS-RF-04)."""
import pytest

from cuentas.models import Usuario

pytestmark = pytest.mark.django_db

CONTRASENA_DE_MARCO = "volante-norte-2026"


def crear_chofer(cliente, correo="marco.chofer@upbus.example"):
    return cliente.post(
        "/api/usuarios",
        {"nombre": "Marco", "correo": correo, "rol": "chofer", "contrasena": CONTRASENA_DE_MARCO},
        format="json",
    )


def entrar(cliente, identificador, contrasena):
    return cliente.post(
        "/api/sesion", {"identificador": identificador, "contrasena": contrasena}, format="json"
    )


def test_HU03_CA1_el_administrador_crea_la_cuenta_de_un_chofer(cliente_de, hugo, cliente):
    respuesta = crear_chofer(cliente_de(hugo))

    assert respuesta.status_code == 201
    sesion = entrar(cliente, "marco.chofer@upbus.example", CONTRASENA_DE_MARCO)
    assert sesion.status_code == 200
    assert sesion.json()["usuario"]["rol"] == "chofer"
    assert sesion.json()["usuario"]["puede_actuar_como_estudiante"] is False


def test_HU03_CA2_rechaza_un_correo_que_ya_tiene_cuenta(cliente_de, hugo, ismael):
    respuesta = crear_chofer(cliente_de(hugo), correo="ismael@upb.example")

    assert respuesta.status_code == 400
    assert respuesta.json()["causa"] == "ya existe una cuenta con ese correo"


def test_HU03_CA3_un_estudiante_no_puede_crear_cuentas(cliente_de, ismael):
    cuentas_antes = Usuario.objects.count()

    respuesta = crear_chofer(cliente_de(ismael))

    assert respuesta.status_code == 403
    assert respuesta.json()["causa"] == "solo el administrador puede hacer esto"
    assert Usuario.objects.count() == cuentas_antes


def test_HU03_CA4_eliminar_desactiva_la_cuenta(cliente_de, hugo, marco, cliente):
    respuesta = cliente_de(hugo).delete(f"/api/usuarios/{marco.pk}")

    assert respuesta.status_code == 204
    marco.refresh_from_db()
    assert marco.is_active is False
    sesion = entrar(cliente, "marco.chofer@upbus.example", "clave-segura-123")
    assert sesion.json()["causa"] == "Código, correo o contraseña incorrectos"
