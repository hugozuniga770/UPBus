"""WebSocket del viaje: aquí llegarán la posición del bus y los avisos (HU-06, HU-07, HU-09).

Por ahora solo une al cliente al grupo del viaje y confirma la conexión,
para que el tiempo real esté listo antes de la HU-06.
"""
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


def grupo_del_viaje(viaje_id):
    return f"viaje_{viaje_id}"


def grupo_del_chofer(viaje_id):
    """Grupo privado del chofer del viaje y de los administradores (HU-07)."""
    return f"viaje_{viaje_id}_chofer"


class ViajeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.viaje_id = int(self.scope["url_route"]["kwargs"]["viaje_id"])
        await self.channel_layer.group_add(grupo_del_viaje(self.viaje_id), self.channel_name)
        await self.accept()
        await self.send_json({"tipo": "conectado", "viaje": self.viaje_id})

    async def disconnect(self, codigo):
        await self.channel_layer.group_discard(grupo_del_viaje(self.viaje_id), self.channel_name)

    async def evento_del_viaje(self, evento):
        """Reenvía a la pantalla lo que un servicio publicó en el grupo del viaje."""
        await self.send_json(evento["datos"])


class ChoferDelViajeConsumer(AsyncJsonWebsocketConsumer):
    """Canal privado del viaje: avisos «Voy a subir» y ubicaciones de los estudiantes (HU-07).

    Solo entran el chofer de ese viaje y los administradores (BUS-RF-08).
    """

    async def connect(self):
        self.viaje_id = int(self.scope["url_route"]["kwargs"]["viaje_id"])
        if not await self._puede_entrar():
            await self.close(code=4403)
            return
        await self.channel_layer.group_add(grupo_del_chofer(self.viaje_id), self.channel_name)
        await self.accept()
        await self.send_json({"tipo": "conectado", "viaje": self.viaje_id})

    @database_sync_to_async
    def _puede_entrar(self):
        from .models import Viaje

        usuario = self.scope.get("user")
        if usuario is None or not usuario.is_authenticated:
            return False
        viaje = Viaje.objects.filter(pk=self.viaje_id).first()
        return viaje is not None and (viaje.chofer_id == usuario.pk or usuario.es_administrador)

    async def disconnect(self, codigo):
        await self.channel_layer.group_discard(grupo_del_chofer(self.viaje_id), self.channel_name)

    async def evento_del_viaje(self, evento):
        await self.send_json(evento["datos"])
