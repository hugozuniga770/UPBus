"""HU-14 · Chat directo entre un confirmado y el chofer de su viaje."""
from datetime import date

import pytest
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.apps import apps

import mensajes.routing
from rutas.models import Parada
from viajes.models import AvisoDeSubida, Viaje

from .conftest import SEVILLA, crear_cuenta

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture
def viaje(ruta_norte, horario_0640, marco, hora):
    return Viaje.objects.create(
        ruta=ruta_norte,
        horario=horario_0640,
        fecha=date(2026, 11, 16),
        chofer=marco,
        estado=Viaje.Estado.EN_CURSO,
        iniciado_en=hora(16, 6, 38),
    )


@pytest.fixture
def aviso_confirmado(viaje, ismael):
    parada = Parada.objects.create(
        ruta=viaje.ruta,
        nombre="Sevilla",
        latitud=SEVILLA[0],
        longitud=SEVILLA[1],
        orden=1,
    )
    return AvisoDeSubida.objects.create(
        viaje=viaje,
        estudiante=ismael,
        parada=parada,
        estado=AvisoDeSubida.Estado.CONFIRMADO,
    )


def escuchar_chat(viaje, estudiante):
    capa = get_channel_layer()
    canal = async_to_sync(capa.new_channel)()
    async_to_sync(capa.group_add)(f"chat_viaje_{viaje.pk}_{estudiante.pk}", canal)
    return lambda: async_to_sync(capa.receive)(canal)["datos"]


def test_HU14_CA1_el_confirmado_le_escribe_al_chofer(
    cliente_de, ismael, viaje, aviso_confirmado, hora, monkeypatch
):
    momento = hora(16, 6, 50)
    monkeypatch.setattr("mensajes.servicios.ahora_local", lambda: momento, raising=False)
    siguiente_evento = escuchar_chat(viaje, ismael)

    respuesta = cliente_de(ismael).post(
        f"/api/viajes/{viaje.pk}/mensajes",
        {"id_cliente": "directo-1", "texto": "Ya estoy en la parada"},
        format="json",
    )

    assert respuesta.status_code == 201
    mensaje = respuesta.json()["mensaje"]
    assert mensaje["autor"] == {"id": ismael.pk, "nombre": "Ismael"}
    assert mensaje["texto"] == "Ya estoy en la parada"
    assert mensaje["enviado_en"] == momento.isoformat()
    assert siguiente_evento() == {"tipo": "mensaje_directo", "mensaje": mensaje}

    aviso_confirmado.estado = AvisoDeSubida.Estado.CANCELADO
    aviso_confirmado.save(update_fields=["estado"])
    repetida = cliente_de(ismael).post(
        f"/api/viajes/{viaje.pk}/mensajes",
        {"id_cliente": "directo-1", "texto": "Ya estoy en la parada"},
        format="json",
    )
    Mensaje = apps.get_model("mensajes", "Mensaje")
    assert repetida.status_code == 200
    assert Mensaje.objects.filter(id_cliente="directo-1").count() == 1


def test_HU14_CA2_rechaza_escribir_sin_estar_en_el_viaje(
    cliente_de, ismael, viaje
):
    respuesta = cliente_de(ismael).post(
        f"/api/viajes/{viaje.pk}/mensajes",
        {"id_cliente": "directo-sin-aviso", "texto": "¿Ya viene?"},
        format="json",
    )

    assert respuesta.status_code == 400
    assert respuesta.json()["causa"] == "no estás en este viaje"
    Mensaje = apps.get_model("mensajes", "Mensaje")
    assert Mensaje.objects.count() == 0


def test_HU14_CA3_el_chofer_responde_con_una_respuesta_rapida(
    cliente_de, ismael, marco, viaje, aviso_confirmado
):
    cliente_de(ismael).post(
        f"/api/viajes/{viaje.pk}/mensajes",
        {"id_cliente": "pregunta-1", "texto": "Ya estoy en la parada"},
        format="json",
    )
    siguiente_evento = escuchar_chat(viaje, ismael)

    respuesta = cliente_de(marco).post(
        f"/api/viajes/{viaje.pk}/mensajes",
        {
            "id_cliente": "respuesta-1",
            "estudiante": ismael.pk,
            "respuesta_rapida": "Ya llego",
        },
        format="json",
    )

    assert respuesta.status_code == 201
    mensaje = respuesta.json()["mensaje"]
    assert mensaje["autor"] == {"id": marco.pk, "nombre": "Marco"}
    assert mensaje["texto"] == "Ya llego"
    assert siguiente_evento() == {"tipo": "mensaje_directo", "mensaje": mensaje}


def test_el_websocket_directo_solo_acepta_a_los_participantes(
    ismael, viaje, aviso_confirmado
):
    ajena = crear_cuenta("Ana", "ana@upb.example", "estudiante", "70006")

    async def conectar(usuario):
        comunicador = WebsocketCommunicator(
            URLRouter(mensajes.routing.websocket_urlpatterns),
            f"/ws/mensajes/viajes/{viaje.pk}/{ismael.pk}/",
        )
        comunicador.scope["user"] = usuario
        conectado, codigo = await comunicador.connect()
        mensaje = await comunicador.receive_json_from() if conectado else None
        if conectado:
            await comunicador.disconnect()
        return conectado, codigo, mensaje

    del_participante = async_to_sync(conectar)(ismael)
    de_la_ajena = async_to_sync(conectar)(ajena)

    assert del_participante == (True, None, {"tipo": "conectado", "chat": "directo"})
    assert de_la_ajena[0] is False
