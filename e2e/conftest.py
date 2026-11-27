"""Pruebas de punta a punta (T21): la app real en un navegador, con varias cuentas a la vez.

Levanta el servidor de verdad (Django con Daphne, WebSockets incluidos) sobre una
base nueva sembrada por `semilla.py`, con la interfaz ya construida, y maneja
Chromium con Playwright. Cómo correrlas: `docs/guia-desarrollo.md`, sección 2.
"""
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import expect, sync_playwright

from e2e import datos

RAIZ = Path(__file__).resolve().parent.parent
CAPTURAS = Path(__file__).resolve().parent / "capturas"
CELULAR = {"viewport": {"width": 390, "height": 844}, "is_mobile": True, "has_touch": True}
COMPUTADORA = {"viewport": {"width": 1280, "height": 800}}
GPS_DEL_BUS = {"latitude": datos.CAMPUS_UPB[0], "longitude": datos.CAMPUS_UPB[1]}

expect.set_options(timeout=10_000)


def _puerto_libre():
    with socket.socket() as conexion:
        conexion.bind(("127.0.0.1", 0))
        return conexion.getsockname()[1]


def _esperar_al_servidor(base, proceso, bitacora):
    sin_proxy = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    limite = time.monotonic() + 60
    while time.monotonic() < limite:
        if proceso.poll() is not None:
            pytest.exit(f"El servidor no arrancó:\n{bitacora.read_text()}", returncode=1)
        try:
            sin_proxy.open(f"{base}/api/sesion", timeout=2)
            return
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            time.sleep(0.3)
    proceso.kill()
    pytest.exit(f"El servidor no respondió en 60 s:\n{bitacora.read_text()}", returncode=1)


@pytest.fixture(scope="session")
def servidor(tmp_path_factory):
    """La app real en un puerto libre, sobre una base nueva sembrada."""
    if not (RAIZ / "frontend" / "dist" / "index.html").exists():
        pytest.exit(
            "Falta la interfaz construida: corre `npm run build` en frontend/ antes de `pytest e2e`.",
            returncode=1,
        )
    carpeta = tmp_path_factory.mktemp("e2e")
    entorno = {
        **os.environ,
        "DJANGO_SETTINGS_MODULE": "config.settings",
        "UPBUS_BD": str(carpeta / "e2e.sqlite3"),
        "UPBUS_PADRON": "padron/padron.json",
        "UPBUS_DEBUG": "1",
    }
    entorno.pop("DATABASE_URL", None)
    subprocess.run([sys.executable, "-m", "e2e.semilla"], cwd=RAIZ, env=entorno, check=True)

    puerto = _puerto_libre()
    bitacora = carpeta / "servidor.log"
    with open(bitacora, "w") as salida:
        proceso = subprocess.Popen(
            [sys.executable, "manage.py", "runserver", f"127.0.0.1:{puerto}", "--noreload"],
            cwd=RAIZ, env=entorno, stdout=salida, stderr=subprocess.STDOUT,
        )
    base = f"http://127.0.0.1:{puerto}"
    _esperar_al_servidor(base, proceso, bitacora)
    yield base
    proceso.terminate()
    try:
        proceso.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proceso.kill()


@pytest.fixture(scope="session")
def navegador():
    with sync_playwright() as playwright:
        chromium = playwright.chromium.launch()
        yield chromium
        chromium.close()


def nuevo_contexto(navegador, servidor, celular=True, **opciones):
    return navegador.new_context(
        base_url=servidor,
        locale="es-BO",
        timezone_id="America/La_Paz",
        **(CELULAR if celular else COMPUTADORA),
        **opciones,
    )


def entrar(pagina, identificador):
    """Inicia sesión desde la pantalla de la app, como lo haría la persona."""
    pagina.goto("/ingresar")
    pagina.get_by_label("Código o correo").fill(identificador)
    pagina.get_by_label("Contraseña de UPBus").fill(datos.CONTRASENA)
    pagina.get_by_role("button", name="Acceder").click()
    expect(pagina.get_by_role("heading", name="Hola", exact=False)).to_be_visible()


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    reporte = yield
    setattr(item, f"reporte_{reporte.when}", reporte)
    return reporte


def _capturar_si_fallo(request, paginas):
    reporte = getattr(request.node, "reporte_call", None)
    if reporte is None or not reporte.failed:
        return
    CAPTURAS.mkdir(exist_ok=True)
    for numero, pagina in enumerate(paginas, start=1):
        if not pagina.is_closed():
            pagina.screenshot(path=CAPTURAS / f"falla-{request.node.name}-{numero}.png", full_page=True)


@pytest.fixture
def abrir_como(servidor, navegador, request):
    """`abrir_como(identificador)` abre la app en un celular nuevo, con esa sesión iniciada.

    Cada llamada es otra persona con su propio navegador: así se prueba lo que
    le llega a una cuando la otra hace algo. `abrir_como(None)` abre sin sesión.
    """
    contextos = []

    def abrir(identificador=None, celular=True, **opciones):
        contexto = nuevo_contexto(navegador, servidor, celular=celular, **opciones)
        contextos.append(contexto)
        pagina = contexto.new_page()
        if identificador:
            entrar(pagina, identificador)
        return pagina

    yield abrir
    paginas = [pagina for contexto in contextos for pagina in contexto.pages]
    if "viaje_en_curso" in request.fixturenames:
        paginas.append(request.getfixturevalue("viaje_en_curso"))
    _capturar_si_fallo(request, paginas)
    for contexto in contextos:
        contexto.close()


@pytest.fixture(scope="session")
def viaje_en_curso(servidor, navegador):
    """Marco inicia su viaje de la Ruta Norte (HU-05) y deja su pantalla abierta.

    Es la pantalla del chofer para todas las pruebas: comparte el GPS del bus,
    recibe «Voy a subir» por su canal privado y abre los chats.
    """
    contexto = nuevo_contexto(
        navegador, servidor, geolocation=GPS_DEL_BUS, permissions=["geolocation"]
    )
    pagina = contexto.new_page()
    entrar(pagina, datos.MARCO)
    pagina.goto("/viajes")
    pagina.get_by_role("button", name="Iniciar viaje").click()
    expect(pagina.get_by_text("Ubicación del bus compartida en tiempo real.")).to_be_visible()
    yield pagina
    contexto.close()
