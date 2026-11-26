"""HU-06 · Ver el bus en vivo (BUS-RF-07, BUS-RF-11)."""
import asyncio
from datetime import date

import pytest
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from rutas.models import Parada, PasoPorParada
from viajes import models as modelos_viajes
from viajes.consumers import grupo_del_viaje

from .conftest import SEVILLA, punto_a

pytestmark = pytest.mark.django_db(transaction=True)


def crear_viaje_en_curso(ruta, horario, chofer, hora):
    return modelos_viajes.Viaje.objects.create(
        ruta=ruta,
        horario=horario,
        fecha=date(2026, 11, 16),
        chofer=chofer,
        estado="en_curso",
        iniciado_en=hora(16, 6, 38),
    )


def posicion(cliente, viaje, punto, momento, id_cliente="posicion-1"):
    return cliente.post(
        f"/api/viajes/{viaje.pk}/posiciones",
        {
            "id_cliente": id_cliente,
            "latitud": punto[0],
            "longitud": punto[1],
            "tomada_en": momento.isoformat(),
        },
        format="json",
    )


async def recibir_evento(capa, canal):
    return await asyncio.wait_for(capa.receive(canal), timeout=1)


def test_HU06_CA1_la_posicion_del_bus_llega_a_quienes_miran_la_ruta(
    cliente_de, marco, ruta_norte, horario_0640, hora
):
    viaje = crear_viaje_en_curso(ruta_norte, horario_0640, marco, hora)
    capa = get_channel_layer()
    canal = async_to_sync(capa.new_channel)()
    async_to_sync(capa.group_add)(grupo_del_viaje(viaje.pk), canal)

    respuesta = posicion(cliente_de(marco), viaje, SEVILLA, hora(16, 6, 52))

    assert respuesta.status_code == 201
    evento = async_to_sync(recibir_evento)(capa, canal)
    assert evento["type"] == "evento.del.viaje"
    assert evento["datos"]["tipo"] == "posicion"
    assert evento["datos"]["viaje"] == viaje.pk
    assert evento["datos"]["latitud"] == pytest.approx(SEVILLA[0])
    assert evento["datos"]["longitud"] == pytest.approx(SEVILLA[1])


def test_HU06_CA2_rechaza_posiciones_de_un_viaje_que_no_esta_en_curso(
    cliente_de, marco, ruta_norte, horario_0640, hora
):
    viaje = modelos_viajes.Viaje.objects.create(
        ruta=ruta_norte,
        horario=horario_0640,
        fecha=date(2026, 11, 16),
        chofer=marco,
        estado="terminado",
        iniciado_en=hora(16, 6, 38),
        terminado_en=hora(16, 7, 38),
    )

    respuesta = posicion(cliente_de(marco), viaje, SEVILLA, hora(16, 7, 40))

    viaje.refresh_from_db()
    assert respuesta.status_code == 400
    assert respuesta.json()["causa"] == "el viaje no está en curso"
    assert viaje.ultima_posicion_en is None


def test_HU06_CA3_pasar_a_menos_de_50_m_registra_un_paso(
    cliente_de, marco, ruta_norte, horario_0640, hora
):
    parada = Parada.objects.create(
        ruta=ruta_norte,
        nombre="Sevilla",
        latitud=SEVILLA[0],
        longitud=SEVILLA[1],
        orden=1,
    )
    viaje = crear_viaje_en_curso(ruta_norte, horario_0640, marco, hora)
    punto = punto_a(SEVILLA, metros_al_norte=30)

    primera = posicion(cliente_de(marco), viaje, punto, hora(16, 6, 58), "cerca-sevilla")
    reenvio = posicion(cliente_de(marco), viaje, punto, hora(16, 6, 58), "cerca-sevilla")

    assert (primera.status_code, reenvio.status_code) == (201, 201)
    paso = PasoPorParada.objects.get(parada=parada)
    assert paso.minutos_desde_salida == pytest.approx(18)
    assert PasoPorParada.objects.filter(parada=parada).count() == 1


def test_HU06_CA4_pasar_a_80_m_no_cuenta_como_llegada(
    cliente_de, marco, ruta_norte, horario_0640, hora
):
    Parada.objects.create(
        ruta=ruta_norte,
        nombre="Sevilla",
        latitud=SEVILLA[0],
        longitud=SEVILLA[1],
        orden=1,
    )
    viaje = crear_viaje_en_curso(ruta_norte, horario_0640, marco, hora)

    respuesta = posicion(
        cliente_de(marco),
        viaje,
        punto_a(SEVILLA, metros_al_norte=80),
        hora(16, 6, 58),
    )

    assert respuesta.status_code == 201
    assert PasoPorParada.objects.count() == 0


def test_HU06_CA5_sin_senal_se_ve_la_ultima_posicion_con_su_hora(
    cliente_de, marco, ismael, ruta_norte, horario_0640, hora
):
    viaje = crear_viaje_en_curso(ruta_norte, horario_0640, marco, hora)
    posicion(cliente_de(marco), viaje, SEVILLA, hora(16, 6, 52))

    respuesta = cliente_de(ismael).get(f"/api/viajes/{viaje.pk}")

    assert respuesta.status_code == 200
    ultima = respuesta.json()["viaje"]["ultima_posicion"]
    assert ultima["latitud"] == pytest.approx(SEVILLA[0])
    assert ultima["longitud"] == pytest.approx(SEVILLA[1])
    assert ultima["tomada_en"] == hora(16, 6, 52).isoformat()
