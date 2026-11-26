"""Pruebas de soporte para el despliegue gratuito de T22 (#17)."""
from pathlib import Path

from django.test import Client, override_settings

from config.settings import _base_de_datos


def test_T22_database_url_configura_postgresql(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://upbus:secreto@db.example:5432/upbus?sslmode=require",
    )

    base = _base_de_datos()

    assert base["default"]["ENGINE"] == "django.db.backends.postgresql"
    assert base["default"]["NAME"] == "upbus"
    assert base["default"]["USER"] == "upbus"
    assert base["default"]["CONN_MAX_AGE"] == 600


def test_T22_django_entrega_la_interfaz_compilada(tmp_path):
    indice = tmp_path / "index.html"
    indice.write_text("<main>UPBus desplegado</main>", encoding="utf-8")

    with override_settings(FRONTEND_INDEX=indice):
        respuesta = Client().get("/rutas", secure=True)

    assert respuesta.status_code == 200
    assert b"UPBus desplegado" in b"".join(respuesta.streaming_content)


def test_T22_render_no_incluye_secretos_y_arranca_con_asgi():
    raiz = Path(__file__).resolve().parent.parent
    blueprint = (raiz / "render.yaml").read_text(encoding="utf-8")
    dockerfile = (raiz / "Dockerfile").read_text(encoding="utf-8")
    dockerignore = (raiz / ".dockerignore").read_text(encoding="utf-8")

    assert "plan: free" in blueprint
    assert "generateValue: true" in blueprint
    assert "DATABASE_URL" in blueprint
    assert "secreto" not in blueprint.lower()
    assert "daphne" in dockerfile
    assert "config.asgi:application" in dockerfile
    assert "padron/padron.local.json" in dockerignore
