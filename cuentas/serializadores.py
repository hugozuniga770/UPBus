"""Formato de los datos que llegan y salen (no son reglas del negocio)."""
from rest_framework import serializers

from .models import Usuario


class RegistroEntrada(serializers.Serializer):
    codigo = serializers.CharField(max_length=20, trim_whitespace=True)
    correo = serializers.CharField(max_length=254, trim_whitespace=True)
    contrasena = serializers.CharField(trim_whitespace=False)
    confirmacion = serializers.CharField(trim_whitespace=False)


class SesionEntrada(serializers.Serializer):
    identificador = serializers.CharField(max_length=254, trim_whitespace=True)
    contrasena = serializers.CharField(trim_whitespace=False)


class CuentaNuevaEntrada(serializers.Serializer):
    nombre = serializers.CharField(max_length=150)
    correo = serializers.EmailField()
    rol = serializers.CharField(max_length=20)
    contrasena = serializers.CharField(trim_whitespace=False)
    codigo = serializers.CharField(max_length=20, required=False, allow_blank=True)


def usuario_a_dict(usuario):
    return {
        "id": usuario.pk,
        "nombre": usuario.nombre,
        "codigo": usuario.codigo,
        "correo": usuario.correo,
        "rol": usuario.rol,
        "activa": usuario.is_active,
        "puede_actuar_como_estudiante": usuario.puede_actuar_como_estudiante,
    }


__all__ = [
    "RegistroEntrada",
    "SesionEntrada",
    "CuentaNuevaEntrada",
    "usuario_a_dict",
    "Usuario",
]
