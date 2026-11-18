"""Reglas de las cuentas: deciden y, si no se permite, lanzan `Rechazo`.

No leen ni escriben la base de datos: reciben lo que necesitan como
parámetros.
"""
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from comun.rechazos import Rechazo, SinPermiso

CREDENCIALES_INCORRECTAS = "Código, correo o contraseña incorrectos"
SOLO_ADMINISTRADOR = "solo el administrador puede hacer esto"
ROLES_QUE_CREA_EL_ADMINISTRADOR = ("estudiante", "chofer", "administrador")


# ---- HU-01: registro con el padrón (BUS-RF-01) ----

def verificar_persona_en_padron(persona):
    if persona is None:
        raise Rechazo("código no encontrado en el padrón")


def verificar_correo_del_padron(persona, correo):
    if persona["correo"].strip().lower() != (correo or "").strip().lower():
        raise Rechazo("el correo no corresponde a ese código")


def verificar_persona_activa(persona):
    if not persona.get("activo", False):
        raise Rechazo("persona no activa en el padrón")


def verificar_sin_cuenta(ya_tiene_cuenta):
    if ya_tiene_cuenta:
        raise Rechazo("ya tienes una cuenta")


def verificar_contrasenas_iguales(contrasena, confirmacion):
    if contrasena != confirmacion:
        raise Rechazo("las contraseñas no coinciden")


def verificar_contrasena(contrasena, cuenta_nueva):
    """Reglas de contraseña de Django, después de comparar las dos."""
    try:
        validate_password(contrasena, user=cuenta_nueva)
    except ValidationError as error:
        raise Rechazo(" ".join(error.messages)) from error


def rol_desde_el_padron(persona):
    return "administrador" if persona.get("rol") == "administrador" else "estudiante"


# ---- HU-02: inicio de sesión (BUS-RF-02) ----

def verificar_credenciales(usuario):
    """Un único mensaje, sin decir qué dato falló."""
    if usuario is None:
        raise Rechazo(CREDENCIALES_INCORRECTAS)


# ---- HU-03: gestión de usuarios (BUS-RF-03, BUS-RF-04) ----

def verificar_es_administrador(usuario):
    if not getattr(usuario, "es_administrador", False):
        raise SinPermiso(SOLO_ADMINISTRADOR)


def verificar_rol_valido(rol):
    if rol not in ROLES_QUE_CREA_EL_ADMINISTRADOR:
        raise Rechazo("rol no válido")


def verificar_correo_libre(existe_cuenta_con_ese_correo):
    if existe_cuenta_con_ese_correo:
        raise Rechazo("ya existe una cuenta con ese correo")


def verificar_codigo_libre(existe_cuenta_con_ese_codigo):
    if existe_cuenta_con_ese_codigo:
        raise Rechazo("ya existe una cuenta con ese código")


def verificar_no_es_uno_mismo(administrador, cuenta):
    if administrador.pk == cuenta.pk:
        raise Rechazo("no puedes eliminar tu propia cuenta")
