"""HU-02 · Entrar y salir con código o correo (BUS-RF-02)."""
import pytest

pytestmark = pytest.mark.django_db

CONTRASENA = "clave-segura-123"
MENSAJE = "Código, correo o contraseña incorrectos"


def entrar(cliente, identificador, contrasena=CONTRASENA):
    return cliente.post(
        "/api/sesion", {"identificador": identificador, "contrasena": contrasena}, format="json"
    )


def test_HU02_CA1_entra_con_su_codigo(cliente, ismael):
    respuesta = entrar(cliente, "70004")

    assert respuesta.status_code == 200
    assert respuesta.json()["usuario"]["rol"] == "estudiante"
    assert cliente.get("/api/sesion").json()["usuario"]["codigo"] == "70004"


def test_HU02_CA2_entra_con_su_correo(cliente, ismael):
    respuesta = entrar(cliente, "ISMAEL@upb.example")

    assert respuesta.status_code == 200
    assert respuesta.json()["usuario"]["nombre"] == "Ismael"


def test_HU02_CA3_un_solo_mensaje_si_algo_no_coincide(cliente, ismael):
    con_contrasena_incorrecta = entrar(cliente, "70004", "no-es-la-clave")
    con_codigo_inexistente = entrar(cliente, "79999")

    assert con_contrasena_incorrecta.status_code == 400
    assert con_contrasena_incorrecta.json()["causa"] == MENSAJE
    assert con_codigo_inexistente.json()["causa"] == MENSAJE


def test_HU02_CA4_al_cerrar_sesion_vuelve_a_pedir_inicio(cliente, ismael, ruta_norte):
    entrar(cliente, "70004")

    assert cliente.delete("/api/sesion").status_code == 204

    respuesta = cliente.get("/api/rutas")
    assert respuesta.status_code == 403
    assert respuesta.json()["causa"] == "debes iniciar sesión"
    assert cliente.get("/api/sesion").json()["usuario"] is None
