from django.contrib import admin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo", "correo", "rol", "is_active")
    list_filter = ("rol", "is_active")
    search_fields = ("nombre", "codigo", "correo")
    exclude = ("password",)
