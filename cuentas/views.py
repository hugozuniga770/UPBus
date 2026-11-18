"""Vistas de las cuentas: solo reciben, llaman al servicio y responden."""
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from comun.vistas import leer

from . import servicios
from .serializadores import CuentaNuevaEntrada, RegistroEntrada, SesionEntrada, usuario_a_dict


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfVista(APIView):
    """Entrega la cookie `csrftoken` que la interfaz manda en cada escritura."""

    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"listo": True})


@method_decorator(csrf_protect, name="dispatch")
class RegistroVista(APIView):
    """HU-01. POST /api/registro"""

    permission_classes = [AllowAny]

    def post(self, request):
        datos = leer(RegistroEntrada, request.data)
        cuenta = servicios.registrar(**datos)
        return Response({"usuario": usuario_a_dict(cuenta)}, status=status.HTTP_201_CREATED)


@method_decorator(csrf_protect, name="dispatch")
class SesionVista(APIView):
    """HU-02. GET: quién soy · POST: iniciar sesión · DELETE: cerrar sesión."""

    permission_classes = [AllowAny]

    def get(self, request):
        usuario = request.user if request.user.is_authenticated else None
        return Response({"usuario": usuario_a_dict(usuario) if usuario else None})

    def post(self, request):
        datos = leer(SesionEntrada, request.data)
        usuario = servicios.autenticar(datos["identificador"], datos["contrasena"])
        login(request, usuario, backend="cuentas.backends.CodigoOCorreoBackend")
        return Response({"usuario": usuario_a_dict(usuario)})

    def delete(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsuariosVista(APIView):
    """HU-03. GET: listar · POST: crear chofer o persona (solo administrador)."""

    def get(self, request):
        cuentas = servicios.listar_cuentas(request.user)
        return Response({"usuarios": [usuario_a_dict(c) for c in cuentas]})

    def post(self, request):
        datos = leer(CuentaNuevaEntrada, request.data)
        cuenta = servicios.crear_cuenta(request.user, **datos)
        return Response({"usuario": usuario_a_dict(cuenta)}, status=status.HTTP_201_CREATED)


class UsuarioVista(APIView):
    """HU-03. DELETE /api/usuarios/<id>: desactiva la cuenta."""

    def delete(self, request, cuenta_id):
        servicios.eliminar_cuenta(request.user, cuenta_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
