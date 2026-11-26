from django.contrib import admin

from .models import AvisoDeSubida, Viaje


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ("ruta", "horario", "fecha", "chofer", "estado")
    list_filter = ("estado", "fecha")
    search_fields = ("ruta__nombre", "chofer__nombre", "chofer__codigo", "chofer__correo")


@admin.register(AvisoDeSubida)
class AvisoDeSubidaAdmin(admin.ModelAdmin):
    list_display = ("estudiante", "parada", "viaje", "estado", "creado_en")
    list_filter = ("estado",)
