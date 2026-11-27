"""HU-10 · Registro de quién subió al bus (BUS-RF-13, C-30, C-31, P-33)."""
import asyncio
from datetime import date

import pytest
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from rutas.models import Parada
from viajes.consumers import grupo_del_chofer
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


def escuchar_al_chofer(viaje):
    capa = get_channel_layer()
    canal = async_to_sync(capa.new_channel)()
    async_to_sync(capa.group_add)(grupo_del_chofer(viaje.pk), canal)

    async def drenar():
        eventos = []
        while True:
            try:
                eventos.append((await asyncio.wait_for(capa.receive(canal), timeout=0.05))["datos"])
            except TimeoutError:
                return eventos

    return lambda: async_to_sync(drenar)()


def compartir(cliente, aviso_id, punto, momento):
    return cliente.post(
        f"/api/avisos/{aviso_id}/ubicacion",
        {"latitud": punto[0], "longitud": punto[1], "tomada_en": momento.isoformat()},
        format="json",
    )


def posicion_del_bus(cliente, viaje, punto, momento, id_cliente):
    return cliente.post(
        f"/api/viajes/{viaje.pk}/posiciones",
        {"id_cliente": id_cliente, "latitud": punto[0], "longitud": punto[1], "tomada_en": momento.isoformat()},
        format="json",
    )


def crear_aviso(cliente, viaje, parada):
    return cliente.post(f"/api/viajes/{viaje.pk}/avisos", {"parada": parada.pk}, format="json").json()["aviso"]["id"]


def test_HU10_CA1_el_estudiante_registra_que_subio(cliente_de, ismael, viaje, paradas):
    sevilla, _ = paradas
    aviso_id = crear_aviso(cliente_de(ismael), viaje, sevilla)
    al_chofer = escuchar_al_chofer(viaje)

    respuesta = cliente_de(ismael).post(f"/api/avisos/{aviso_id}/subio")

    assert respuesta.status_code == 200
    assert respuesta.json()["aviso"]["estado"] == "a_bordo"
    assert AvisoDeSubida.objects.get(pk=aviso_id).estado == AvisoDeSubida.Estado.A_BORDO
    assert "Ismael: ha subido" in [evento.get("mensaje") for evento in al_chofer()]
    # Subir no cobra (C-31): los créditos llegan con T17 y lo comprueban sus tests.


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
    assert respuesta.json() == {"causa": "el viaje ya terminó"}
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
    """C-30, P-33: con el bus a más de 100 m de Sevilla, dos ubicaciones seguidas de Ismael a menos de 50 m del bus."""
    sevilla, _ = paradas
    aviso_id = crear_aviso(cliente_de(ismael), viaje, sevilla)
    compartir(cliente_de(ismael), aviso_id, SEVILLA, hora(16, 6, 50))

    # El bus ya pasó por Sevilla y está a 150 m.
    bus_1 = punto_a(SEVILLA, metros_al_norte=-150)
    posicion_del_bus(cliente_de(marco), viaje, bus_1, hora(16, 7, 0), "bus-1")

    # Una sola ubicación de Ismael junto al bus: sigue Confirmado [PROVISIONAL].
    compartir(cliente_de(ismael), aviso_id, punto_a(bus_1, metros_al_este=10), hora(16, 7, 2))
    assert AvisoDeSubida.objects.get(pk=aviso_id).estado == AvisoDeSubida.Estado.CONFIRMADO

    # Una posición nueva del bus no cuenta como otra ubicación de Ismael.
    bus_2 = punto_a(SEVILLA, metros_al_norte=-180)
    posicion_del_bus(cliente_de(marco), viaje, bus_2, hora(16, 7, 5), "bus-2")
    assert AvisoDeSubida.objects.get(pk=aviso_id).estado == AvisoDeSubida.Estado.CONFIRMADO

    # La segunda ubicación seguida junto al bus: queda A bordo y deja de compartir.
    compartir(cliente_de(ismael), aviso_id, punto_a(bus_2, metros_al_este=10), hora(16, 7, 7))
    aviso = AvisoDeSubida.objects.get(pk=aviso_id)
    assert aviso.estado == AvisoDeSubida.Estado.A_BORDO
    assert aviso.ubicacion_en is None
