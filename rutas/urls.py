from django.urls import path

from . import views

urlpatterns = [
    path("rutas", views.RutasVista.as_view(), name="rutas"),
    path("rutas/<int:ruta_id>", views.RutaVista.as_view(), name="ruta"),
    path("registros", views.RegistrosVista.as_view(), name="registros"),
    path("registros/en-curso", views.RegistroEnCursoVista.as_view(), name="registro-en-curso"),
    path("registros/<int:registro_id>/marcas", views.MarcasVista.as_view(), name="marcas"),
    path("registros/<int:registro_id>/puntos", views.PuntosVista.as_view(), name="puntos"),
    path("registros/<int:registro_id>/terminar", views.TerminarRegistroVista.as_view(), name="terminar-registro"),
    path("registros/<int:registro_id>/cancelar", views.CancelarRegistroVista.as_view(), name="cancelar-registro"),
    path("rutas/<int:ruta_id>/paradas", views.PropuestasParadaVista.as_view(), name="proponer-parada"),
    path("paradas/<int:parada_id>/aprobar", views.AprobarParadaVista.as_view(), name="aprobar-parada"),
    path("paradas/<int:parada_id>/rechazar", views.RechazarParadaVista.as_view(), name="rechazar-parada"),
]
