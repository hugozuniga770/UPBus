"""Cada pantalla se ve bien en el celular y en la computadora (Definition of Done).

«Se ve bien» se revisa así: la página no se desplaza hacia el costado y no hay
errores de JavaScript. Las capturas quedan en `e2e/capturas/` para mirarlas.
"""
import pytest

from e2e import datos
from e2e.conftest import CAPTURAS, GPS_DEL_BUS

PANTALLAS = [
    ("ingresar", None, "/ingresar"),
    ("registrarse", None, "/registrarse"),
    ("inicio", datos.ANA, "/"),
    ("rutas", datos.ANA, "/rutas"),
    ("viajes", datos.MARCO, "/viajes"),
    ("modo-registro", datos.MARCO, "/modo-registro"),
    ("usuarios", datos.HUGO, "/usuarios"),
    ("demo", datos.HUGO, "/demo"),
]


@pytest.mark.parametrize("celular", [True, False], ids=["celular", "computadora"])
@pytest.mark.parametrize(("nombre", "persona", "ruta"), PANTALLAS, ids=[p[0] for p in PANTALLAS])
def test_se_ve_bien_en_celular_y_computadora(abrir_como, nombre, persona, ruta, celular):
    pagina = abrir_como(persona, celular=celular, geolocation=GPS_DEL_BUS, permissions=["geolocation"])
    errores = []
    pagina.on("pageerror", lambda error: errores.append(str(error)))

    pagina.goto(ruta)
    pagina.wait_for_load_state("networkidle")

    CAPTURAS.mkdir(exist_ok=True)
    pagina.screenshot(path=CAPTURAS / f"{nombre}-{'celular' if celular else 'computadora'}.png")
    ancho = pagina.evaluate("() => ({pagina: document.documentElement.scrollWidth, ventana: window.innerWidth})")
    assert ancho["pagina"] <= ancho["ventana"], f"{ruta} se desplaza hacia el costado: {ancho}"
    assert not errores, f"{ruta} tiene errores de JavaScript: {errores}"
