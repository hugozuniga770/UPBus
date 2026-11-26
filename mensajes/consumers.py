"""Canales privados del chat directo y del chat de cada ruta."""
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


def grupo_del_chat_directo(viaje_id, estudiante_id):
    return f"chat_viaje_{viaje_id}_{estudiante_id}"


def grupo_del_chat_de_ruta(ruta_id):
    return f"chat_ruta_{ruta_id}"


class ChatDirectoConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.viaje_id = int(self.scope["url_route"]["kwargs"]["viaje_id"])
        self.estudiante_id = int(self.scope["url_route"]["kwargs"]["estudiante_id"])
        if not await self._puede_entrar():
            await self.close(code=4403)
            return
        self.grupo = grupo_del_chat_directo(self.viaje_id, self.estudiante_id)
        await self.channel_layer.group_add(self.grupo, self.channel_name)
        await self.accept()
        await self.send_json({"tipo": "conectado", "chat": "directo"})

    @database_sync_to_async
    def _puede_entrar(self):
        from .servicios import puede_entrar_al_chat_directo

        usuario = self.scope.get("user")
        return bool(
            usuario
            and usuario.is_authenticated
            and puede_entrar_al_chat_directo(
                usuario, self.viaje_id, self.estudiante_id
            )
        )

    async def disconnect(self, codigo):
        if hasattr(self, "grupo"):
            await self.channel_layer.group_discard(self.grupo, self.channel_name)

    async def mensaje_del_chat(self, evento):
        await self.send_json(evento["datos"])


class ChatDeRutaConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.ruta_id = int(self.scope["url_route"]["kwargs"]["ruta_id"])
        if not await self._puede_entrar():
            await self.close(code=4403)
            return
        self.grupo = grupo_del_chat_de_ruta(self.ruta_id)
        await self.channel_layer.group_add(self.grupo, self.channel_name)
        await self.accept()
        await self.send_json({"tipo": "conectado", "chat": "ruta"})

    @database_sync_to_async
    def _puede_entrar(self):
        from .servicios import puede_entrar_al_chat_de_ruta

        usuario = self.scope.get("user")
        return bool(
            usuario
            and usuario.is_authenticated
            and puede_entrar_al_chat_de_ruta(usuario, self.ruta_id)
        )

    async def disconnect(self, codigo):
        if hasattr(self, "grupo"):
            await self.channel_layer.group_discard(self.grupo, self.channel_name)

    async def mensaje_del_chat(self, evento):
        await self.send_json(evento["datos"])
