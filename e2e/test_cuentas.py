"""Registro e inicio de sesión de punta a punta (HU-01, HU-02).

Son los ocho pasos de la verificación de la sesión 12, sección 7, que ahora
corren solos en cada Pull Request.
"""
import re

from playwright.sync_api import expect

from e2e import datos


def registrar(pagina, codigo, correo):
    pagina.goto("/registrarse")
    pagina.get_by_label("Código de estudiante").fill(codigo)
    pagina.get_by_label("Correo institucional").fill(correo)
    pagina.get_by_label("Nueva contraseña para UPBus").fill(datos.CONTRASENA)
    pagina.get_by_label("Repite la contraseña").fill(datos.CONTRASENA)
    pagina.get_by_role("button", name="Crear cuenta").click()


def entrar_con(pagina, identificador, contrasena=datos.CONTRASENA):
    pagina.get_by_label("Código o correo").fill(identificador)
    pagina.get_by_label("Contraseña de UPBus").fill(contrasena)
    pagina.get_by_role("button", name="Acceder").click()


def salir(pagina):
    pagina.get_by_role("button", name="Salir").click()
    expect(pagina).to_have_url(re.compile(r"/ingresar$"))


def test_una_persona_del_padron_se_registra_y_entra(abrir_como):
    pagina = abrir_como(None)
    hola = pagina.get_by_role("heading", name="Hola, Ismael")

    # 1. Sin sesión, /rutas lleva al inicio de sesión, con el enlace para crear la cuenta (RF-01).
    pagina.goto("/rutas")
    expect(pagina).to_have_url(re.compile(r"/ingresar$"))
    expect(pagina.get_by_role("link", name="Crea tu cuenta")).to_be_visible()

    # 2. Ismael se registra con el padrón de ejemplo y queda con la sesión abierta (HU01-CA1).
    registrar(pagina, datos.ISMAEL, "ismael@upb.example")
    expect(hola).to_be_visible()

    # 3. Cierra sesión (HU02-CA4).
    salir(pagina)

    # 4. Entra con su código (HU02-CA1) y 5. con su correo (HU02-CA2).
    for identificador in (datos.ISMAEL, "ismael@upb.example"):
        entrar_con(pagina, identificador)
        expect(hola).to_be_visible()
        salir(pagina)

    # 6. Con una contraseña incorrecta no entra (HU02-CA3).
    entrar_con(pagina, datos.ISMAEL, "no-es-su-clave")
    expect(pagina.get_by_role("alert")).to_have_text("Código, correo o contraseña incorrectos")

    # 7. Lucía, inactiva en el padrón, no puede crear su cuenta (HU01-CA3).
    registrar(pagina, datos.LUCIA, "lucia.pena@upb.example")
    expect(pagina.get_by_role("alert")).to_have_text("persona no activa en el padrón")

    # 8. Ismael no puede registrarse otra vez (RF-01).
    registrar(pagina, datos.ISMAEL, "ismael@upb.example")
    expect(pagina.get_by_role("alert")).to_have_text("ya tienes una cuenta")
