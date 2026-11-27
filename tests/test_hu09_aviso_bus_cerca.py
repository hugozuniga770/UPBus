"""HU-09 · Aviso «Tu bus está cerca» y sugerencia de seguir si nadie espera (BUS-RF-11, BUS-RF-12)."""
import asyncio
from datetime import date

import pytest
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from rutas.models import Parada, PasoPorParada
from viajes.consumers import grupo_del_chofer, grupo_del_viaje
from viajes.models import AvisoDeSubida, Viaje

from .conftest import PETROL, SEVILLA, punto_a

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture
def paradas(ruta_norte):
    sevilla = Parada.objects.create(ruta=ruta_norte, nombre="Sevilla", latitud=SEVILLA[0], longitud=SEVILLA[1], orden=1)
    petrol = Parada.objects.create(ruta=ruta_norte, nombre="Petrol", latitud=PETROL[0], longitud=PETROL[1], orden=2)
    return sevilla, petrol


@pytest.fixture
def viaje_en_curso(ruta_norte, horario_0640, marco, hora):
    return Viaje.objects.create(
        ruta=ruta_norte,
        horario=horario_0640,
        fecha=date(2026, 11, 16),
        chofer=marco,
        estado="en_curso",
        iniciado_en=hora(16, 6, 38),
    )


def escuchar(grupo):
    capa = get_channel_layer()
    canal = async_to_sync(capa.new_channel)()
    async_to_sync(capa.group_add)(grupo, canal)

    async def _drenar():
        eventos = []
        while True:
            try:
                mensaje = await asyncio.wait_for(capa.receive(canal), timeout=0.05)
                eventos.append(mensaje["datos"])
            except TimeoutError:
                break
        return eventos

    return canal, lambda: async_to_sync(_drenar)()


def enviar_posicion(cliente, viaje, punto, momento, id_cliente):
    return cliente.post(
        f"/api/viajes/{viaje.pk}/posiciones",
        {"id_cliente": id_cliente, "latitud": punto[0], "longitud": punto[1], "tomada_en": momento.isoformat()},
        format="json",
    )


def test_HU09_CA1_avisa_cuando_el_bus_esta_a_500_m_o_menos(
    cliente_de, ismael, marco, viaje_en_curso, paradas, hora
):
    sevilla, _ = paradas
    aviso_id = (
        cliente_de(ismael)
        .post(f"/api/viajes/{viaje_en_curso.pk}/avisos", {"parada": sevilla.pk}, format="json")
        .json()["aviso"]["id"]
    )
    _, drenar = escuchar(grupo_del_viaje(viaje_en_curso.pk))

    a_480_m = punto_a(SEVILLA, metros_al_norte=480)
    respuesta = enviar_posicion(cliente_de(marco), viaje_en_curso, a_480_m, hora(16, 6, 55), "pos-480m")

    assert respuesta.status_code == 201
    eventos = drenar()
    avisos_cerca = [e for e in eventos if e.get("tipo") == "bus_cerca"]
    assert len(avisos_cerca) == 1
    assert avisos_cerca[0]["aviso"] == aviso_id
    assert avisos_cerca[0]["mensaje"].startswith("Tu bus está cerca")
    # El canal del viaje es público: no lleva quién espera (ENT-07).
    assert "estudiante" not in avisos_cerca[0]


def test_HU09_CA2_no_avisa_a_mas_de_500_m(
    cliente_de, ismael, marco, viaje_en_curso, paradas, hora
):
    sevilla, _ = paradas
    aviso_id = (
        cliente_de(ismael)
        .post(f"/api/viajes/{viaje_en_curso.pk}/avisos", {"parada": sevilla.pk}, format="json")
        .json()["aviso"]["id"]
    )
    _, drenar = escuchar(grupo_del_viaje(viaje_en_curso.pk))

    a_520_m = punto_a(SEVILLA, metros_al_norte=520)
    enviar_posicion(cliente_de(marco), viaje_en_curso, a_520_m, hora(16, 6, 50), "pos-520m")

    eventos = drenar()
    assert not [e for e in eventos if e.get("tipo") == "bus_cerca"]
    assert AvisoDeSubida.objects.get(pk=aviso_id).aviso_cercania_enviado is False


def test_HU09_CA3_avisa_una_sola_vez_por_viaje(
    cliente_de, ismael, marco, viaje_en_curso, paradas, hora
):
    sevilla, _ = paradas
    cliente_de(ismael).post(f"/api/viajes/{viaje_en_curso.pk}/avisos", {"parada": sevilla.pk}, format="json")
    _, drenar = escuchar(grupo_del_viaje(viaje_en_curso.pk))

    enviar_posicion(cliente_de(marco), viaje_en_curso, punto_a(SEVILLA, metros_al_norte=480), hora(16, 6, 52), "p-1")
    enviar_posicion(cliente_de(marco), viaje_en_curso, punto_a(SEVILLA, metros_al_norte=300), hora(16, 6, 55), "p-2")

    eventos = drenar()
    avisos_cerca = [e for e in eventos if e.get("tipo") == "bus_cerca"]
    assert len(avisos_cerca) == 1


def test_HU09_CA4_sugiere_seguir_si_nadie_espera(
    cliente_de, marco, ruta_norte, horario_0640, paradas, hora
):
    sevilla, _ = paradas
    # Salió a las 06:46: va 6 minutos atrasado respecto de las 06:40.
    viaje_atrasado = Viaje.objects.create(
        ruta=ruta_norte,
        horario=horario_0640,
        fecha=date(2026, 11, 16),
        chofer=marco,
        estado="en_curso",
        iniciado_en=hora(16, 6, 46),
    )
    _, drenar = escuchar(grupo_del_chofer(viaje_atrasado.pk))

    enviar_posicion(
        cliente_de(marco),
        viaje_atrasado,
        punto_a(SEVILLA, metros_al_norte=300),
        hora(16, 7, 10),
        "pos-atrasado",
    )

    eventos = drenar()
    sugerencias = [e for e in eventos if e.get("tipo") == "sugerencia_saltar"]
    assert len(sugerencias) == 1
    assert sugerencias[0]["parada"] == sevilla.pk
    assert sugerencias[0]["mensaje"] == "Nadie espera en Sevilla: puedes seguir"


def test_HU09_CA5_no_sugiere_seguir_si_alguien_viene(
    cliente_de, ismael, marco, ruta_norte, horario_0640, paradas, hora
):
    sevilla, _ = paradas
    viaje_atrasado = Viaje.objects.create(
        ruta=ruta_norte,
        horario=horario_0640,
        fecha=date(2026, 11, 16),
        chofer=marco,
        estado="en_curso",
        iniciado_en=hora(16, 6, 52),
    )
    aviso_id = (
        cliente_de(ismael)
        .post(f"/api/viajes/{viaje_atrasado.pk}/avisos", {"parada": sevilla.pk}, format="json")
        .json()["aviso"]["id"]
    )
    a_300_m_de_sevilla = punto_a(SEVILLA, metros_al_norte=-300)
    cliente_de(ismael).post(
        f"/api/avisos/{aviso_id}/ubicacion",
        {"latitud": a_300_m_de_sevilla[0], "longitud": a_300_m_de_sevilla[1], "tomada_en": hora(16, 7, 5).isoformat()},
        format="json",
    )
    _, drenar = escuchar(grupo_del_chofer(viaje_atrasado.pk))

    enviar_posicion(
        cliente_de(marco),
        viaje_atrasado,
        punto_a(SEVILLA, metros_al_norte=300),
        hora(16, 7, 10),
        "pos-con-estudiante",
    )

    eventos = drenar()
    assert not [e for e in eventos if e.get("tipo") == "sugerencia_saltar"]


def test_no_sugiere_seguir_si_el_bus_va_a_tiempo(cliente_de, marco, viaje_en_curso, paradas, horario_0640, hora):
    """Soporte de HU09-CA4: «atrasado» se mide contra la hora aproximada de la parada (RF-12, C-40)."""
    sevilla, _ = paradas
    PasoPorParada.objects.create(
        parada=sevilla, horario=horario_0640, minutos_desde_salida=20, ocurrido_en=hora(15, 7, 0)
    )
    _, drenar = escuchar(grupo_del_chofer(viaje_en_curso.pk))

    # El bus llega cerca de Sevilla a las 06:55 y su hora aproximada es 07:00: va a tiempo.
    enviar_posicion(cliente_de(marco), viaje_en_curso, punto_a(SEVILLA, metros_al_norte=300), hora(16, 6, 55), "a-tiempo")
    assert not [e for e in drenar() if e.get("tipo") == "sugerencia_saltar"]

    # A las 07:05 ya pasó su hora aproximada: ahora sí va atrasado y nadie espera.
    enviar_posicion(cliente_de(marco), viaje_en_curso, punto_a(SEVILLA, metros_al_norte=200), hora(16, 7, 5), "tarde")
    assert [e["mensaje"] for e in drenar() if e.get("tipo") == "sugerencia_saltar"] == [
        "Nadie espera en Sevilla: puedes seguir"
    ]
