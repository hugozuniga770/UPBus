"""Carga las rutas y los horarios de la guía oficial (rutas/datos/rutas.json).

Se puede correr varias veces: actualiza lo que existe y no toca las paradas,
que salen del modo registro (HU-18).
"""
import json
from datetime import time
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from rutas.models import Horario, Ruta

ARCHIVO = Path(__file__).resolve().parents[2] / "datos" / "rutas.json"


def a_hora(texto):
    if not texto:
        return None
    horas, minutos = texto.split(":")
    return time(int(horas), int(minutos))


class Command(BaseCommand):
    help = "Carga las rutas y horarios de la guía de buses de la UPB"

    @transaction.atomic
    def handle(self, *args, **opciones):
        with open(ARCHIVO, encoding="utf-8") as archivo:
            rutas = json.load(archivo)
        for datos in rutas:
            ruta, _ = Ruta.objects.update_or_create(
                clave=datos["clave"],
                defaults={
                    "nombre": datos["nombre"],
                    "punto_de_partida": datos["punto_de_partida"],
                    "nota": datos.get("nota", ""),
                    "activa": datos.get("activa", True),
                },
            )
            for horario in datos["horarios"]:
                Horario.objects.update_or_create(
                    ruta=ruta,
                    sentido=horario["sentido"],
                    salida=a_hora(horario["salida"]),
                    defaults={"llegada_limite": a_hora(horario.get("llegada_limite"))},
                )
            self.stdout.write(f"  {ruta.nombre}: {len(datos['horarios'])} horarios")
        self.stdout.write(self.style.SUCCESS(f"{len(rutas)} rutas cargadas."))
