"""Configuración de UPBus.

Los valores que cambian entre computadoras se leen de variables de entorno
(ver `.env.ejemplo` y `docs/guia-desarrollo.md`). Sin variables, la
configuración sirve para desarrollar en local.
"""
import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


def _cargar_env(archivo):
    """Lee `CLAVE=valor` de `.env`, si existe, sin pisar variables ya definidas."""
    if not archivo.exists():
        return
    for linea in archivo.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        os.environ.setdefault(clave.strip(), valor.strip())


_cargar_env(BASE_DIR / ".env")


def _lista(nombre, por_defecto):
    valor = os.environ.get(nombre)
    if valor is None:
        return por_defecto
    return [parte.strip() for parte in valor.split(",") if parte.strip()]


SECRET_KEY = os.environ.get(
    "UPBUS_SECRET_KEY", "solo-para-desarrollo-cambiar-en-el-servidor"
)
DEBUG = os.environ.get("UPBUS_DEBUG", "1") == "1"

# `.trycloudflare.com` permite probar desde el celular con un túnel HTTPS
# (docs/guia-modo-registro.md).
ALLOWED_HOSTS = _lista(
    "UPBUS_ALLOWED_HOSTS", ["localhost", "127.0.0.1", ".trycloudflare.com"]
)
CSRF_TRUSTED_ORIGINS = _lista(
    "UPBUS_CSRF_TRUSTED_ORIGINS",
    [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://*.trycloudflare.com",
    ],
)

# Render informa el dominio público en esta variable. Se agrega sin tener que
# copiarlo a otra variable y sin afectar la configuración local.
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

INSTALLED_APPS = [
    "daphne",  # sirve la app por ASGI, para los WebSockets (BUS-RT-04)
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "cuentas",
    "rutas",
    "viajes",
    "mensajes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


def _base_de_datos():
    """Usa PostgreSQL en el hosting y conserva SQLite para desarrollo."""
    if url := os.environ.get("DATABASE_URL"):
        return {
            "default": dj_database_url.parse(
                url,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
    return {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.environ.get("UPBUS_BD", str(BASE_DIR / "db.sqlite3")),
        }
    }


# BUS-RT-02: SQLite en local; PostgreSQL en el contenedor efímero de Render.
DATABASES = _base_de_datos()

# Un solo proceso en desarrollo: alcanza la capa en memoria.
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

AUTH_USER_MODEL = "cuentas.Usuario"
AUTHENTICATION_BACKENDS = ["cuentas.backends.CodigoOCorreoBackend"]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# BUS-RT-07: todas las horas en America/La_Paz.
LANGUAGE_CODE = "es"
TIME_ZONE = "America/La_Paz"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"
FRONTEND_INDEX = FRONTEND_DIST / "index.html"
STATICFILES_DIRS = [("frontend", FRONTEND_DIST)] if FRONTEND_DIST.exists() else []
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# BUS-RT-05: sesión con la cookie de Django y protección CSRF.
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_FAILURE_VIEW = "comun.respuestas.falla_csrf"

if not DEBUG:
    # Render termina TLS en su proxy y envía el protocolo original en esta
    # cabecera. Django debe reconocerlo para no crear redirecciones en bucle.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    # No se incluye ni precarga el dominio padre: `onrender.com` es compartido.
    SECURE_HSTS_SECONDS = 3600
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "EXCEPTION_HANDLER": "comun.respuestas.manejar_excepcion",
    "UNAUTHENTICATED_USER": "django.contrib.auth.models.AnonymousUser",
}

# Padrón simulado (BUS-RF-01). Si existe `padron/padron.local.json`, se usa
# ese; si no, el de ejemplo. Ver `padron/LEEME.md`.
UPBUS_PADRON = os.environ.get("UPBUS_PADRON") or None

# BUS-RF-11: metros a los que el bus «llega» a una parada. Se calibra con los
# viajes de prueba sin cambiar el código (C-34).
UPBUS_RADIO_DE_LLEGADA_M = float(os.environ.get("UPBUS_RADIO_DE_LLEGADA_M", "50"))
