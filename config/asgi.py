"""Entrada ASGI: HTTP con Django y WebSockets con Channels (BUS-RT-04)."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
aplicacion_http = get_asgi_application()

from channels.auth import AuthMiddlewareStack  # noqa: E402
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402
from channels.security.websocket import AllowedHostsOriginValidator  # noqa: E402

import mensajes.routing  # noqa: E402
import viajes.routing  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": aplicacion_http,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    viajes.routing.websocket_urlpatterns
                    + mensajes.routing.websocket_urlpatterns
                )
            )
        ),
    }
)
