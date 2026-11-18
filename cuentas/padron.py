"""Lectura del padrón simulado de la UPB (BUS-RF-01, BUS-RC-04).

Es el único módulo que sabe de dónde sale el padrón. Para conectar UPBus al
sistema real de la universidad, solo cambia este archivo.

El padrón es de solo lectura: UPBus nunca lo modifica ni guarda contraseñas
en él.
"""
import json
from pathlib import Path

from django.conf import settings

CARPETA = Path(settings.BASE_DIR) / "padron"
PADRON_LOCAL = CARPETA / "padron.local.json"
PADRON_DE_EJEMPLO = CARPETA / "padron.json"


def ruta_del_padron():
    if settings.UPBUS_PADRON:
        return Path(settings.UPBUS_PADRON)
    return PADRON_LOCAL if PADRON_LOCAL.exists() else PADRON_DE_EJEMPLO


def leer_padron():
    with open(ruta_del_padron(), encoding="utf-8") as archivo:
        return json.load(archivo)


def buscar_por_codigo(codigo):
    codigo = (codigo or "").strip()
    for persona in leer_padron():
        if str(persona["codigo"]) == codigo:
            return persona
    return None
