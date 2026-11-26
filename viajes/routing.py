from django.urls import path

from .consumers import ChoferDelViajeConsumer, ViajeConsumer

websocket_urlpatterns = [
    path("ws/viajes/<int:viaje_id>/", ViajeConsumer.as_asgi()),
    path("ws/viajes/<int:viaje_id>/chofer/", ChoferDelViajeConsumer.as_asgi()),
]
