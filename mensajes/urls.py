"""Rutas HTTP de los chats."""
from django.urls import path

from . import views

urlpatterns = [
    path(
        "viajes/<int:viaje_id>/mensajes",
        views.MensajesDirectosVista.as_view(),
        name="mensajes-directos",
    ),
    path(
        "rutas/<int:ruta_id>/miembro",
        views.MiembroDeRutaVista.as_view(),
        name="miembro-de-ruta",
    ),
    path(
        "rutas/<int:ruta_id>/mensajes",
        views.MensajesDeRutaVista.as_view(),
        name="mensajes-de-ruta",
    ),
]
