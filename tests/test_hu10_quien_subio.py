"""HU-10 · Registro de quién subió al bus (BUS-RF-13, C-30, C-31, P-33)."""
from datetime import date

import pytest

from rutas.models import Parada
from viajes.models import AvisoDeSubida, Viaje

from .conftest import PETROL, SEVILLA, punto_a

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture
def paradas(ruta_norte):
    sevilla = Parada.objects.create(ruta=ruta_norte, nombre="Sevilla", latitud=SEVILLA[0], longitud=SEVILLA[1], orden=1)
    petrol = Parada.objects.create(ruta=ruta_norte, nombre="Petrol", latitud=PETROL[0], longitud=PETROL[1], orden=2)
    return sevilla, petrol


@pytest.fixture
def viaje(ruta_norte, horario_0640, marco, hora):
    return Viaje.objects.create(
        ruta=ruta_norte,
        horario=horario_0640,
        fecha=date(2026, 11, 16),
        chofer=marco,
        estado="en_curso",
        iniciado_en=hora(16, 6, 38),
    )


def crear_aviso(cliente, viaje, parada):
    return cliente.post(f"/api/viajes/{viaje.pk}/avisos", {"parada": parada.pk}, format="json").json()["aviso"]["id"]


def test_HU10_CA1_el_estudiante_registra_que_subio(cliente_de, ismael, viaje, paradas):
    sevilla, _ = paradas
    aviso_id = crear_aviso(cliente_de(ismael), viaje, sevilla)

    respuesta = cliente_de(ismael).post(f"/api/avisos/{aviso_id}/subio")

    assert respuesta.status_code == 200
    assert respuesta.json()["aviso"]["estado"] == "a_bordo"
    assert AvisoDeSubida.objects.get(pk=aviso_id).estado == AvisoDeSubida.Estado.A_BORDO


def test_HU10_CA2_el_chofer_registra_que_subio(cliente_de, ismael, marco, viaje, paradas):
    sevilla, _ = paradas
    aviso_id = crear_aviso(cliente_de(ismael), viaje, sevilla)

    respuesta = cliente_de(marco).post(f"/api/avisos/{aviso_id}/subio")

    assert respuesta.status_code == 200
    assert respuesta.json()["aviso"]["estado"] == "a_bordo"
    lista = cliente_de(marco).get(f"/api/viajes/{viaje.pk}/avisos").json()["avisos"]
    assert lista[0]["estado"] == "a_bordo"


def test_HU10_CA3_rechaza_subir_a_un_viaje_terminado(cliente_de, ismael, marco, viaje, paradas):
    sevilla, _ = paradas
    aviso_id = crear_aviso(cliente_de(ismael), viaje, sevilla)
    cliente_de(marco).post(f"/api/viajes/{viaje.pk}/terminar")

    respuesta = cliente_de(ismael).post(f"/api/avisos/{aviso_id}/subio")

    assert respuesta.status_code == 400
    assert AvisoDeSubida.objects.get(pk=aviso_id).estado == AvisoDeSubida.Estado.NO_SE_PRESENTO


def test_HU10_CA4_el_chofer_marca_no_se_presento(cliente_de, ismael, marco, viaje, paradas):
    sevilla, _ = paradas
    aviso_id = crear_aviso(cliente_de(ismael), viaje, sevilla)

    sin_permiso = cliente_de(ismael).post(f"/api/avisos/{aviso_id}/no-se-presento")
    assert sin_permiso.status_code == 403

    respuesta = cliente_de(marco).post(f"/api/avisos/{aviso_id}/no-se-presento")
    assert respuesta.status_code == 200
    assert respuesta.json()["aviso"]["estado"] == "no_se_presento"
    assert AvisoDeSubida.objects.get(pk=aviso_id).estado == AvisoDeSubida.Estado.NO_SE_PRESENTO


def test_HU10_CA5_queda_a_bordo_si_avanza_con_el_bus(cliente_de, ismael, marco, viaje, paradas, hora):
    """C-30, P-33: bus > 100 m lejos de la parada y 2 ubicaciones seguidas del estudiante < 50 m del bus."""
    sevilla, _ = paradas
    aviso_id = crear_aviso(cliente_de(ismael), viaje, sevilla)

    bus_lejos_1 = punto_a(SEVILLA, metros_al_norte=-150)
    bus_lejos_2 = punto_a(SEVILLA, metros_al_norte=-220)

    # Primera ubicación del estudiante junto al bus
    cliente_de(ismael).post(
        f"/api/avisos/{aviso_id}/ubicacion",
        {"latitud": bus_lejos_1[0], "longitud": bus_lejos_1[1], "tomada_en": hora(16, 7, 1).isoformat()},
        format="json",
    )
    cliente_de(marco).post(
        f"/api/viajes/{viaje.pk}/posiciones",
        {"id_cliente": "bus-1", "latitud": bus_lejos_1[0], "longitud": bus_lejos_1[1], "tomada_en": hora(16, 7, 2).isoformat()},
        format="json",
    )
    assert AvisoDeSubida.objects.get(pk=aviso_id).estado == AvisoDeSubida.Estado.CONFIRMADO

    # Segunda ubicación consecutiva del estudiante a < 50 m del bus mientras el bus ya pasó > 100 m de Sevilla
    cliente_de(ismael).post(
        f"/api/avisos/{aviso_id}/ubicacion",
        {"latitud": bus_lejos_2[0], "longitud": bus_lejos_2[1], "tomada_en": hora(16, 7, 15).isoformat()},
        format="json",
    )
    cliente_de(marco).post(
        f"/api/viajes/{viaje.pk}/posiciones",
        {"id_cliente": "bus-2", "latitud": bus_lejos_2[0], "longitud": bus_lejos_2[1], "tomada_en": hora(16, 7, 16).isoformat()},
        format="json",
    )

    aviso = AvisoDeSubida.objects.get(pk=aviso_id)
    assert aviso.estado == AvisoDeSubida.Estado.A_BORDO
    assert aviso.ubicacion_en is None