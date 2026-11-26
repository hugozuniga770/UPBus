"""HU-15 · Chat de quienes eligieron una ruta."""
import pytest
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.apps import apps
from django.core.management import call_command

import mensajes.routing
from mensajes.models import MiembroDeRuta
from rutas.models import Ruta

from .conftest import crear_cuenta

pytestmark = pytest.mark.django_db(transaction=True)


def escuchar_chat(ruta):
    capa = get_channel_layer()
    canal = async_to_sync(capa.new_channel)()
    async_to_sync(capa.group_add)(f"chat_ruta_{ruta.pk}", canal)
    return lambda: async_to_sync(capa.receive)(canal)["datos"]


def test_HU15_CA1_el_miembro_escribe_en_el_chat_de_su_ruta(
    cliente_de, ismael, ruta_norte, hora, monkeypatch
):
    momento = hora(16, 18, 15)
    monkeypatch.setattr("mensajes.servicios.ahora_local", lambda: momento, raising=False)
    cliente = cliente_de(ismael)
    union = cliente.post(f"/api/rutas/{ruta_norte.pk}/miembro")
    siguiente_evento = escuchar_chat(ruta_norte)

    respuesta = cliente.post(
        f"/api/rutas/{ruta_norte.pk}/mensajes",
        {"id_cliente": "ruta-1", "texto": "¿El bus ya salió?"},
        format="json",
    )

    assert union.status_code == 201
    assert respuesta.status_code == 201
    mensaje = respuesta.json()["mensaje"]
    assert mensaje["autor"] == {"id": ismael.pk, "nombre": "Ismael"}
    assert mensaje["texto"] == "¿El bus ya salió?"
    assert mensaje["enviado_en"] == momento.isoformat()
    assert siguiente_evento() == {"tipo": "mensaje_de_ruta", "mensaje": mensaje}


def test_HU15_CA2_rechaza_escribir_en_una_ruta_ajena(
    cliente_de, ismael, ruta_norte
):
    call_command("cargar_rutas")
    ruta_sur = Ruta.objects.get(clave="sur")
    cliente = cliente_de(ismael)
    cliente.post(f"/api/rutas/{ruta_norte.pk}/miembro")

    respuesta = cliente.post(
        f"/api/rutas/{ruta_sur.pk}/mensajes",
        {"id_cliente": "ruta-ajena", "texto": "Hola"},
        format="json",
    )

    assert respuesta.status_code == 400
    assert respuesta.json()["causa"] == "no eres parte de esta ruta"
    Mensaje = apps.get_model("mensajes", "Mensaje")
    assert Mensaje.objects.count() == 0


def test_el_websocket_de_ruta_solo_acepta_a_sus_miembros(ismael, ruta_norte):
    ajena = crear_cuenta("Ana", "ana@upb.example", "estudiante", "70006")
    MiembroDeRuta.objects.create(usuario=ismael, ruta=ruta_norte)

    async def conectar(usuario):
        comunicador = WebsocketCommunicator(
            URLRouter(mensajes.routing.websocket_urlpatterns),
            f"/ws/mensajes/rutas/{ruta_norte.pk}/",
        )
        comunicador.scope["user"] = usuario
        conectado, codigo = await comunicador.connect()
        mensaje = await comunicador.receive_json_from() if conectado else None
        if conectado:
            await comunicador.disconnect()
        return conectado, codigo, mensaje

    del_miembro = async_to_sync(conectar)(ismael)
    de_la_ajena = async_to_sync(conectar)(ajena)

    assert del_miembro == (True, None, {"tipo": "conectado", "chat": "ruta"})
    assert de_la_ajena[0] is False
