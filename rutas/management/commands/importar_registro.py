"""Carga un respaldo del modo registro descargado desde el celular.

Uso:
    python manage.py importar_registro rutas/datos/registros/norte-0640.json --usuario 70002

Sirve cuando el recorrido se hizo sin señal o en otra computadora. Un mismo
respaldo no se importa dos veces.
"""
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from comun.rechazos import Rechazo
from cuentas.backends import buscar_por_identificador
from rutas import servicios


class Command(BaseCommand):
    help = "Importa un respaldo JSON del modo registro y lo termina"

    def add_arguments(self, parser):
        parser.add_argument("archivo", type=Path)
        parser.add_argument("--usuario", required=True, help="Código o correo de quien hizo el recorrido")

    def handle(self, *args, **opciones):
        usuario = buscar_por_identificador(opciones["usuario"])
        if usuario is None:
            raise CommandError("No existe esa cuenta. Regístrate primero o revisa el código.")
        with open(opciones["archivo"], encoding="utf-8") as archivo:
            datos = json.load(archivo)
        try:
            resumen = servicios.importar_registro(usuario, datos)
        except Rechazo as rechazo:
            raise CommandError(rechazo.causa) from rechazo
        self.stdout.write(self.style.SUCCESS(
            f"Registro importado: {resumen['marcas']} marcas, {resumen['paradas_nuevas']} paradas "
            f"nuevas y {resumen['paradas_existentes']} ya conocidas."
        ))
        for omitida in resumen["marcas_omitidas"]:
            self.stdout.write(self.style.WARNING(f"  Omitida: {omitida}"))
