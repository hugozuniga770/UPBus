from django.urls import path

from . import views

urlpatterns = [
    path("sesion/csrf", views.CsrfVista.as_view(), name="csrf"),
    path("registro", views.RegistroVista.as_view(), name="registro"),
    path("sesion", views.SesionVista.as_view(), name="sesion"),
    path("usuarios", views.UsuariosVista.as_view(), name="usuarios"),
    path("usuarios/<int:cuenta_id>", views.UsuarioVista.as_view(), name="usuario"),
]
