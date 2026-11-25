"""HU-05 · Iniciar y terminar un viaje (BUS-RF-06)."""
from datetime import date

import pytest

from viajes import models as modelos_viajes

from .conftest import crear_cuenta

pytestmark = pytest.mark.django_db


def crear_viaje(ruta, horario, chofer, estado="programado", **campos):
    return modelos_viajes.Viaje.objects.create(
        ruta=ruta,
        horario=horario,
        fecha=date(2026, 11, 16),
        chofer=chofer,
        estado=estado,
        **campos,
    )


def test_HU05_CA1_el_chofer_inicia_su_viaje(
    cliente_de, marco, ruta_norte, horario_0640, hora, monkeypatch
):
    viaje = crear_viaje(ruta_norte, horario_0640, marco)
    momento = hora(16, 6, 38)
    monkeypatch.setattr("viajes.servicios.ahora_local", lambda: momento)

    respuesta = cliente_de(marco).post(f"/api/viajes/{viaje.pk}/iniciar")

    viaje.refresh_from_db()
    assert respuesta.status_code == 200
    assert viaje.estado == "en_curso"
    assert viaje.iniciado_en == momento


def test_HU05_CA2_rechaza_un_segundo_viaje_en_curso(
    cliente_de, marco, ruta_norte, horario_0640, hora
):
    crear_viaje(
        ruta_norte,
        horario_0640,
        marco,
        estado="en_curso",
        iniciado_en=hora(16, 6, 38),
    )
    otro_horario = ruta_norte.horarios.get(sentido="ingreso", salida="11:00")
    segundo = crear_viaje(ruta_norte, otro_horario, marco)

    respuesta = cliente_de(marco).post(f"/api/viajes/{segundo.pk}/iniciar")

    segundo.refresh_from_db()
    assert respuesta.status_code == 400
    assert respuesta.json()["causa"] == "ya tienes un viaje en curso"
    assert segundo.estado == "programado"


def test_HU05_CA3_el_chofer_termina_su_viaje(
    cliente_de, marco, ruta_norte, horario_0640, hora, monkeypatch
):
    viaje = crear_viaje(
        ruta_norte,
        horario_0640,
        marco,
        estado="en_curso",
        iniciado_en=hora(16, 6, 38),
    )
    momento = hora(16, 7, 38)
    monkeypatch.setattr("viajes.servicios.ahora_local", lambda: momento)

    respuesta = cliente_de(marco).post(f"/api/viajes/{viaje.pk}/terminar")

    viaje.refresh_from_db()
    assert respuesta.status_code == 200
    assert viaje.estado == "terminado"
    assert viaje.terminado_en == momento


def test_HU05_CA4_rechaza_iniciar_un_viaje_ajeno(
    cliente_de, marco, ruta_norte, horario_0640
):
    otro_chofer = crear_cuenta("Ana Chofer", "ana.chofer@upbus.example", "chofer")
    viaje = crear_viaje(ruta_norte, horario_0640, otro_chofer)

    respuesta = cliente_de(marco).post(f"/api/viajes/{viaje.pk}/iniciar")

    viaje.refresh_from_db()
    assert respuesta.status_code == 403
    assert respuesta.json()["causa"] == "este viaje no es tuyo"
    assert viaje.estado == "programado"
