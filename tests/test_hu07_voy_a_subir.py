"""HU-07 · Avisar «Voy a subir» y compartir mi ubicación (BUS-RF-08, BUS-RF-09, BUS-RF-03).

HU07-CA6 (deja de compartir al subir) se escribe con T16, porque necesita «subió» (HU-10).
"""
from datetime import date

import pytest
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from rutas.models import Parada
from viajes.consumers import grupo_del_chofer
from viajes.models import AvisoDeSubida, Viaje

from .conftest import PETROL, SEVILLA, crear_cuenta

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture
def paradas(ruta_norte):
    sevilla = Parada.objects.create(ruta=ruta_norte, nombre="Sevilla", latitud=SEVILLA[0], longitud=SEVILLA[1], orden=1)
    petrol = Parada.objects.create(ruta=ruta_norte, nombre="Petrol", latitud=PETROL[0], longitud=PETROL[1], orden=2)
    return sevilla, petrol


@pytest.fixture
def viaje(ruta_norte, horario_0640, marco, hora):
    return Viaje.objects.create(
        ruta=ruta_norte, horario=horario_0640, fecha=date(2026, 11, 16), chofer=marco,
        estado="en_curso", iniciado_en=hora(16, 6, 38),
    )


def escuchar_al_chofer(viaje):
    capa = get_channel_layer()
    canal = async_to_sync(capa.new_channel)()
    async_to_sync(capa.group_add)(grupo_del_chofer(viaje.pk), canal)
    return lambda: async_to_sync(capa.receive)(canal)["datos"]


def avisar(cliente, viaje, parada):
    return cliente.post(f"/api/viajes/{viaje.pk}/avisos", {"parada": parada.pk}, format="json")


def posicion_del_bus(cliente, viaje, punto, momento, id_cliente):
    return cliente.post(
        f"/api/viajes/{viaje.pk}/posiciones",
        {"id_cliente": id_cliente, "latitud": punto[0], "longitud": punto[1], "tomada_en": momento.isoformat()},
        format="json",
    )


def test_HU07_CA1_avisa_que_va_a_subir(cliente_de, ismael, viaje, paradas):
    sevilla, _ = paradas
    siguiente_evento = escuchar_al_chofer(viaje)

    respuesta = avisar(cliente_de(ismael), viaje, sevilla)

    assert respuesta.status_code == 201
    assert respuesta.json()["aviso"]["estado"] == "confirmado"
    assert siguiente_evento()["mensaje"] == "Ismael va a subir en Sevilla"


def test_HU07_CA2_rechaza_un_segundo_aviso_en_el_mismo_viaje(cliente_de, ismael, viaje, paradas):
    sevilla, _ = paradas
    avisar(cliente_de(ismael), viaje, sevilla)

    respuesta = avisar(cliente_de(ismael), viaje, sevilla)

    assert respuesta.status_code == 400
    assert respuesta.json()["causa"] == "ya avisaste que vas a subir en este viaje"
    assert AvisoDeSubida.objects.filter(viaje=viaje, estudiante=ismael).count() == 1


def test_HU07_CA3_si_el_bus_pasa_y_no_subio_queda_no_se_presento(cliente_de, ismael, marco, viaje, paradas, hora):
    sevilla, petrol = paradas
    aviso_id = avisar(cliente_de(ismael), viaje, sevilla).json()["aviso"]["id"]

    posicion_del_bus(cliente_de(marco), viaje, SEVILLA, hora(16, 6, 58), "en-sevilla")
    assert AvisoDeSubida.objects.get(pk=aviso_id).estado == "confirmado"
    posicion_del_bus(cliente_de(marco), viaje, PETROL, hora(16, 7, 6), "en-petrol")

    assert AvisoDeSubida.objects.get(pk=aviso_id).estado == "no_se_presento"


def test_HU07_CA4_puede_cancelar_antes_de_que_pase_el_bus(cliente_de, ismael, marco, viaje, paradas):
    sevilla, _ = paradas
    aviso_id = avisar(cliente_de(ismael), viaje, sevilla).json()["aviso"]["id"]

    respuesta = cliente_de(ismael).post(f"/api/avisos/{aviso_id}/cancelar")

    assert respuesta.status_code == 200
    assert respuesta.json()["aviso"]["estado"] == "cancelado"
    assert cliente_de(marco).get(f"/api/viajes/{viaje.pk}/avisos").json()["avisos"] == []


def test_HU07_CA5_el_chofer_ve_la_ubicacion_compartida(cliente_de, ismael, marco, hugo, viaje, paradas, hora):
    sevilla, _ = paradas
    otra_estudiante = crear_cuenta("Ana", "ana@upb.example", "estudiante", "70006")
    aviso_id = avisar(cliente_de(ismael), viaje, sevilla).json()["aviso"]["id"]
    cerca_de_sevilla = (SEVILLA[0] + 0.001, SEVILLA[1])

    cliente_de(ismael).post(
        f"/api/avisos/{aviso_id}/ubicacion",
        {"latitud": cerca_de_sevilla[0], "longitud": cerca_de_sevilla[1], "tomada_en": hora(16, 6, 50).isoformat()},
        format="json",
    )

    del_chofer = cliente_de(marco).get(f"/api/viajes/{viaje.pk}/avisos").json()["avisos"]
    del_administrador = cliente_de(hugo).get(f"/api/viajes/{viaje.pk}/avisos").json()["avisos"]
    de_otra_estudiante = cliente_de(otra_estudiante).get(f"/api/viajes/{viaje.pk}/avisos")
    assert del_chofer[0]["ubicacion"]["latitud"] == pytest.approx(cerca_de_sevilla[0])
    assert del_administrador[0]["ubicacion"] is not None
    assert de_otra_estudiante.status_code == 403
    assert de_otra_estudiante.json()["causa"] == "solo el chofer de este viaje puede ver quién va a subir"

def test_HU07_CA6_deja_de_compartir_al_subir(cliente_de, ismael, viaje, paradas, hora):
    sevilla, _ = paradas
    aviso_id = avisar(cliente_de(ismael), viaje, sevilla).json()["aviso"]["id"]
    cliente_de(ismael).post(
        f"/api/avisos/{aviso_id}/ubicacion",
        {"latitud": SEVILLA[0], "longitud": SEVILLA[1], "tomada_en": hora(16, 6, 50).isoformat()},
        format="json",
    )
    assert AvisoDeSubida.objects.get(pk=aviso_id).ubicacion_en is not None

    respuesta = cliente_de(ismael).post(f"/api/avisos/{aviso_id}/subio")

    assert respuesta.status_code == 200
    aviso = AvisoDeSubida.objects.get(pk=aviso_id)
    assert (aviso.estado, aviso.ubicacion_latitud, aviso.ubicacion_longitud, aviso.ubicacion_en) == (
        "a_bordo", None, None, None
    )

def test_HU07_CA7_un_administrador_tambien_puede_avisar(cliente_de, hugo, viaje, paradas):
    sevilla, _ = paradas

    respuesta = avisar(cliente_de(hugo), viaje, sevilla)

    assert respuesta.status_code == 201
    assert respuesta.json()["aviso"]["estado"] == "confirmado"


def test_al_terminar_el_viaje_nadie_sigue_esperando_ni_compartiendo(cliente_de, ismael, marco, viaje, paradas, hora):
    """Completa HU05-CA3: al terminar, se cierran los avisos y las ubicaciones del viaje."""
    sevilla, _ = paradas
    aviso_id = avisar(cliente_de(ismael), viaje, sevilla).json()["aviso"]["id"]
    cliente_de(ismael).post(
        f"/api/avisos/{aviso_id}/ubicacion",
        {"latitud": SEVILLA[0], "longitud": SEVILLA[1], "tomada_en": hora(16, 6, 50).isoformat()},
        format="json",
    )

    cliente_de(marco).post(f"/api/viajes/{viaje.pk}/terminar")

    aviso = AvisoDeSubida.objects.get(pk=aviso_id)
    assert (aviso.estado, aviso.ubicacion_en) == ("no_se_presento", None)
