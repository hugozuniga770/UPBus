from django.contrib import admin

from .models import Horario, MarcaDeParada, Parada, PasoPorParada, RegistroDeRecorrido, Ruta


class HorarioEnLinea(admin.TabularInline):
    model = Horario
    extra = 0


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "clave", "punto_de_partida", "activa")
    inlines = [HorarioEnLinea]


@admin.register(Parada)
class ParadaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ruta", "orden", "estado", "latitud", "longitud")
    list_filter = ("ruta", "estado")


class MarcaEnLinea(admin.TabularInline):
    model = MarcaDeParada
    extra = 0
    readonly_fields = ("recibida_en",)


@admin.register(RegistroDeRecorrido)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ("id", "ruta", "horario", "usuario", "estado", "iniciado_en")
    list_filter = ("ruta", "estado")
    inlines = [MarcaEnLinea]


@admin.register(PasoPorParada)
class PasoAdmin(admin.ModelAdmin):
    list_display = ("parada", "horario", "minutos_desde_salida", "ocurrido_en")
    list_filter = ("parada__ruta",)
