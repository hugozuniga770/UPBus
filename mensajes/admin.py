from django.contrib import admin

from .models import Mensaje, MiembroDeRuta


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ("autor", "texto", "viaje", "ruta", "enviado_en")
    list_filter = ("enviado_en", "ruta")
    search_fields = ("autor__nombre", "texto", "id_cliente")


@admin.register(MiembroDeRuta)
class MiembroDeRutaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "ruta", "elegido_en")
    list_filter = ("ruta",)
    search_fields = ("usuario__nombre", "usuario__codigo")
