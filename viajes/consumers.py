"""WebSocket del viaje: aquí llegarán la posición del bus y los avisos (HU-06, HU-07, HU-09).

Por ahora solo une al cliente al grupo del viaje y confirma la conexión,
para que el tiempo real esté listo antes de la HU-06.
"""
from channels.generic.websocket import AsyncJsonWebsocketConsumer


def grupo_del_viaje(viaje_id):
    return f"viaje_{viaje_id}"


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
