"""Rutas HTTP de los viajes."""
from django.urls import path

from . import views

urlpatterns = [
    path("viajes", views.ViajesVista.as_view(), name="viajes"),
    path("viajes/<int:viaje_id>", views.ViajeVista.as_view(), name="viaje"),
    path("viajes/<int:viaje_id>/iniciar", views.IniciarViajeVista.as_view(), name="iniciar-viaje"),
    path("viajes/<int:viaje_id>/terminar", views.TerminarViajeVista.as_view(), name="terminar-viaje"),
    path("viajes/<int:viaje_id>/posiciones", views.PosicionesVista.as_view(), name="posiciones-viaje"),
]
