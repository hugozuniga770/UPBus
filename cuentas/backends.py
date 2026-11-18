"""Inicio de sesión con código o correo (BUS-RF-02)."""
from django.contrib.auth.backends import ModelBackend

from .models import Usuario


def buscar_por_identificador(identificador):
    """Un correo tiene «@»; si no, es un código."""
    identificador = (identificador or "").strip()
    if not identificador:
        return None
    if "@" in identificador:
        return Usuario.objects.filter(correo__iexact=identificador).first()
    return Usuario.objects.filter(codigo=identificador).first()


class CodigoOCorreoBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if password is None:
            return None
        usuario = buscar_por_identificador(username or kwargs.get("correo"))
        if usuario is None:
            # Toma el mismo tiempo que una contraseña real, para no revelar
            # qué códigos o correos existen.
            Usuario().set_password(password)
            return None
        if usuario.check_password(password) and self.user_can_authenticate(usuario):
            return usuario
        return None
