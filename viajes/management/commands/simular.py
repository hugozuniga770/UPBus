"""Corre un escenario del simulador (T23) desde la terminal.

Uso:
    python manage.py simular --lista
    python manage.py simular recorrido --ruta sur --velocidad 10
    python manage.py simular no_se_presenta --ruta sur --parada "Banco Ganadero"

Usa los mismos servicios que la app. Los viajes simulados no enseñan horas (C-27).
"""
from django.core.management.base import BaseCommand, CommandError

from comun.rechazos import Rechazo
from viajes import reglas, simulador

AVISO_DE_LA_CAPA = (
    "Desde la terminal, las pantallas abiertas ven el bus cuando vuelven a consultar el viaje "
    "(cada 30 s). Para verlo moverse en vivo, inicia la simulación desde el panel Demo."
)


class Command(BaseCommand):
    help = "Simula un viaje con los mismos servicios de la app (T23)"

    def add_arguments(self, parser):
        parser.add_argument("escenario", nargs="?", help="recorrido o no_se_presenta")
        parser.add_argument("--ruta", default="sur", help="Clave de la ruta; por defecto, sur (la grabada en REG-01)")
        parser.add_argument("--horario", help="Hora de salida, por ejemplo 06:40; por defecto, el primer ingreso")
        parser.add_argument("--velocidad", type=float, default=10, help="Cuántas veces más rápido que el real (1 a 60)")
        parser.add_argument("--parada", help="Nombre de la parada del estudiante (no_se_presenta)")
        parser.add_argument("--sin-esperar", action="store_true", help="Corre sin esperas, para probar")
        parser.add_argument("--lista", action="store_true", help="Muestra los escenarios")

    def handle(self, *args, **opciones):
        if opciones["lista"] or not opciones["escenario"]:
            for clave, descripcion in simulador.ESCENARIOS.items():
                self.stdout.write(f"{clave}: {descripcion}")
            return
        try:
            if opciones["sin_esperar"]:
                reloj = simulador.RelojSinEsperas()
            else:
                reglas.verificar_velocidad(opciones["velocidad"])
                reloj = simulador.crear_reloj(opciones["velocidad"])
                self.stdout.write(AVISO_DE_LA_CAPA)
            simulador.correr(
                opciones["escenario"], opciones["ruta"], reloj=reloj, horario=opciones["horario"],
                parada=opciones["parada"], anotar=self.stdout.write,
            )
        except Rechazo as falla:
            raise CommandError(falla.causa) from falla
