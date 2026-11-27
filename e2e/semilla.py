"""Siembra la base nueva de las pruebas de punta a punta (T21).

La corre `e2e/conftest.py` antes de levantar el servidor (`python -m e2e.semilla`).
Crea las rutas, las cuentas que no salen del padrón y el viaje programado de
Marco en la Ruta Norte, con tres paradas aprobadas. Ismael no tiene cuenta: se
registra en la prueba de cuentas.
"""
import os
from datetime import time
from io import StringIO

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.management import call_command  # noqa: E402

from comun.tiempo import ahora  # noqa: E402
from cuentas.models import Usuario  # noqa: E402
from e2e import datos  # noqa: E402
from rutas.models import Parada, Ruta  # noqa: E402
from viajes.models import Viaje  # noqa: E402


def cuenta(nombre, correo, rol, codigo=None):
    return Usuario.objects.create_user(
        correo=correo, password=datos.CONTRASENA, nombre=nombre, rol=rol, codigo=codigo
    )


def sembrar():
    call_command("migrate", verbosity=0)
    call_command("cargar_rutas", stdout=StringIO())
    cuenta("Hugo Zuñiga", "hugo.zuniga@upb.example", "administrador", datos.HUGO)
    marco = cuenta("Marco", datos.MARCO, "chofer")
    cuenta("Ana", datos.ANA, "estudiante", "70006")
    cuenta("Valeria", datos.VALERIA, "estudiante", "70007")
    cuenta("Rosa", datos.ROSA, "estudiante", "70008")

    norte = Ruta.objects.get(clave="norte")
    for orden, (nombre, latitud, longitud) in enumerate(datos.PARADAS_NORTE, start=1):
        Parada.objects.create(
            ruta=norte, nombre=nombre, latitud=latitud, longitud=longitud, orden=orden
        )
    Viaje.objects.create(
        ruta=norte,
        horario=norte.horarios.get(sentido="ingreso", salida=time(6, 40)),
        fecha=ahora().date(),
        chofer=marco,
    )


if __name__ == "__main__":
    sembrar()
