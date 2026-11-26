"""Entrega la aplicación React compilada en el despliegue."""

from django.conf import settings
from django.http import FileResponse, Http404


def interfaz(_request):
    indice = settings.FRONTEND_INDEX
    if not indice.is_file():
        raise Http404("La interfaz todavía no fue compilada.")
    return FileResponse(indice.open("rb"), content_type="text/html; charset=utf-8")
