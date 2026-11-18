"""Servicios de las cuentas: leen lo necesario, preguntan a las reglas y guardan."""
from django.contrib.auth import authenticate
from django.db import transaction
from django.db.models import Q

from comun.rechazos import NoExiste

from . import reglas
from .models import Usuario
from .padron import buscar_por_codigo


def ya_tiene_cuenta(persona):
    return Usuario.objects.filter(
        Q(codigo=str(persona["codigo"])) | Q(correo__iexact=persona["correo"])
    ).exists()


def cuenta_desde_el_padron(persona):
    rol = reglas.rol_desde_el_padron(persona)
    es_admin = rol == Usuario.Rol.ADMINISTRADOR
    return Usuario(
        correo=Usuario.objects.normalize_email(persona["correo"]).lower(),
        codigo=str(persona["codigo"]),
        nombre=persona["nombre"],
        rol=rol,
        # Los integrantes del equipo entran también al panel de Django.
        is_staff=es_admin,
        is_superuser=es_admin,
    )


@transaction.atomic
def registrar(codigo, correo, contrasena, confirmacion):
    """HU-01: crea la cuenta de una persona que está en el padrón."""
    persona = buscar_por_codigo(codigo)
    reglas.verificar_persona_en_padron(persona)
    reglas.verificar_correo_del_padron(persona, correo)
    reglas.verificar_persona_activa(persona)
    reglas.verificar_sin_cuenta(ya_tiene_cuenta(persona))
    reglas.verificar_contrasenas_iguales(contrasena, confirmacion)
    cuenta = cuenta_desde_el_padron(persona)
    reglas.verificar_contrasena(contrasena, cuenta)
    cuenta.set_password(contrasena)
    cuenta.save()
    return cuenta


def autenticar(identificador, contrasena):
    """HU-02: devuelve la cuenta si el código o correo y la contraseña coinciden.

    No consulta el padrón: solo la BD. La vista inicia la sesión.
    """
    usuario = authenticate(None, username=identificador, password=contrasena)
    reglas.verificar_credenciales(usuario)
    return usuario


def listar_cuentas(administrador):
    reglas.verificar_es_administrador(administrador)
    return Usuario.objects.order_by("-is_active", "rol", "nombre")


@transaction.atomic
def crear_cuenta(administrador, nombre, correo, rol, contrasena, codigo=None):
    """HU-03: el administrador crea un chofer o una persona nueva."""
    reglas.verificar_es_administrador(administrador)
    reglas.verificar_rol_valido(rol)
    correo = Usuario.objects.normalize_email(correo).lower()
    reglas.verificar_correo_libre(Usuario.objects.filter(correo__iexact=correo).exists())
    codigo = (codigo or "").strip() or None
    if codigo:
        reglas.verificar_codigo_libre(Usuario.objects.filter(codigo=codigo).exists())
    cuenta = Usuario(correo=correo, nombre=nombre.strip(), rol=rol, codigo=codigo)
    reglas.verificar_contrasena(contrasena, cuenta)
    cuenta.set_password(contrasena)
    cuenta.save()
    return cuenta


def buscar_cuenta(cuenta_id):
    cuenta = Usuario.objects.filter(pk=cuenta_id).first()
    if cuenta is None:
        raise NoExiste("la cuenta no existe")
    return cuenta


@transaction.atomic
def eliminar_cuenta(administrador, cuenta_id):
    """HU-03: la cuenta se desactiva, no se borra (P-23), para no perder comprobantes."""
    reglas.verificar_es_administrador(administrador)
    cuenta = buscar_cuenta(cuenta_id)
    reglas.verificar_no_es_uno_mismo(administrador, cuenta)
    cuenta.is_active = False
    cuenta.save(update_fields=["is_active"])
    return cuenta
