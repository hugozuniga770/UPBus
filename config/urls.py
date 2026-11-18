from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("cuentas.urls")),
    path("api/", include("rutas.urls")),
    path("api/", include("viajes.urls")),
    path("api/", include("mensajes.urls")),
]
