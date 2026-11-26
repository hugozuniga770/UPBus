"""WebSockets de los chats."""
from django.urls import path

from .consumers import ChatDeRutaConsumer, ChatDirectoConsumer

websocket_urlpatterns = [
    path(
        "ws/mensajes/viajes/<int:viaje_id>/<int:estudiante_id>/",
        ChatDirectoConsumer.as_asgi(),
    ),
    path("ws/mensajes/rutas/<int:ruta_id>/", ChatDeRutaConsumer.as_asgi()),
]
