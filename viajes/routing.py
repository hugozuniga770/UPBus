from django.urls import path

from .consumers import ViajeConsumer

websocket_urlpatterns = [
    path("ws/viajes/<int:viaje_id>/", ViajeConsumer.as_asgi()),
]
