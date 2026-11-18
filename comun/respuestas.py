"""Convierte los errores en respuestas JSON con la forma `{"causa": "..."}`."""
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .rechazos import Rechazo


def manejar_excepcion(exc, context):
    if isinstance(exc, Rechazo):
        return Response({"causa": exc.causa}, status=exc.codigo_http)

    respuesta = exception_handler(exc, context)
    if respuesta is None:
        return None
    if isinstance(exc, (exceptions.NotAuthenticated, exceptions.AuthenticationFailed)):
        causa = "debes iniciar sesión"
    elif isinstance(exc, exceptions.PermissionDenied):
        causa = "no tienes permiso para hacer esto"
    elif isinstance(exc, exceptions.ValidationError):
        campos = ", ".join(exc.detail.keys()) if isinstance(exc.detail, dict) else ""
        causa = f"faltan datos o tienen un formato no válido: {campos}".rstrip(": ")
    else:
        causa = str(getattr(exc, "detail", "no se pudo completar la operación"))
    respuesta.data = {"causa": causa, "detalle": respuesta.data}
    return respuesta


def falla_csrf(request, reason=""):
    """Responde en JSON cuando falta o venció el token CSRF (BUS-RT-05)."""
    from django.http import JsonResponse

    return JsonResponse(
        {"causa": "la página perdió su token de seguridad: recárgala e intenta de nuevo"},
        status=403,
    )
