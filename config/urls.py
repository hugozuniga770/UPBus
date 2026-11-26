from django.contrib import admin
from django.urls import include, path, re_path

from config.views import interfaz

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("cuentas.urls")),
    path("api/", include("rutas.urls")),
    path("api/", include("viajes.urls")),
    path("api/", include("mensajes.urls")),
    # React resuelve sus rutas en el navegador. Las rutas reservadas del
    # servidor se excluyen para conservar sus respuestas 404 propias.
    re_path(r"^(?!api/|admin/|static/|ws/).*$", interfaz),
]
