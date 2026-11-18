"""Convierte una lista de estudiantes (Excel o CSV) en el padrón local.

Uso:
    python manage.py importar_padron lista.xlsx --administradores 70001,70002

- Escribe `padron/padron.local.json`, que Git ignora: los datos reales de la
  clase nunca se suben al repositorio público (ver `padron/LEEME.md`).
- Si un correo no es de la UPB (`@upb.edu`, `@upb.edu.bo` o un subdominio),
  se reemplaza por uno de ejemplo: `<codigo>@upb.example`.
"""
import csv
import json
import re
import unicodedata
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from cuentas.padron import PADRON_LOCAL

DOMINIO_DE_EJEMPLO = "upb.example"
DOMINIOS_UPB = ("upb.edu", "upb.edu.bo")
ENCABEZADOS = {
    "codigo": ("codigo", "cod", "codigo de estudiante", "codigo estudiante", "registro"),
    "nombre": ("nombre", "nombre completo", "estudiante", "nombres y apellidos", "apellidos y nombres"),
    "nombres": ("nombres",),
    "apellidos": ("apellidos", "apellido"),
    "correo": ("correo", "email", "e mail", "mail", "correo electronico", "correo institucional",
               "direccion de correo", "direccion de correo electronico"),
}


def normalizar(texto):
    """«Apellido(s)» → «apellido»; «Dirección de correo» → «direccion de correo»."""
    texto = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    texto = texto.lower().replace("(s)", "")
    return " ".join(re.sub(r"[^a-z0-9]+", " ", texto).split())


def es_correo_upb(correo, dominios=DOMINIOS_UPB):
    if "@" not in (correo or ""):
        return False
    dominio = correo.rsplit("@", 1)[1].strip().lower()
    return any(dominio == d or dominio.endswith("." + d) for d in dominios)


def texto_de_celda(valor):
    if valor is None:
        return ""
    if isinstance(valor, float) and valor.is_integer():
        valor = int(valor)
    return str(valor).strip()


def ubicar_columnas(fila):
    columnas = {}
    for indice, celda in enumerate(fila):
        nombre = normalizar(celda)
        for campo, opciones in ENCABEZADOS.items():
            if nombre in opciones and campo not in columnas:
                columnas[campo] = indice
    tiene_nombre = "nombre" in columnas or "nombres" in columnas
    return columnas if "codigo" in columnas and tiene_nombre else None


def convertir_filas(filas, administradores=(), dominios=DOMINIOS_UPB):
    """Devuelve `(personas, reemplazados)` a partir de las filas de la hoja."""
    filas = [list(fila) for fila in filas]
    for numero, fila in enumerate(filas[:15]):
        columnas = ubicar_columnas(fila)
        if columnas:
            break
    else:
        raise CommandError(
            "No encontré los encabezados. La hoja necesita una columna «Código» "
            "y otra «Nombre» (o «Nombres» y «Apellidos»); «Correo» es opcional."
        )

    def celda(fila, campo):
        indice = columnas.get(campo)
        return texto_de_celda(fila[indice]) if indice is not None and indice < len(fila) else ""

    personas, reemplazados, vistos = [], 0, set()
    for fila in filas[numero + 1:]:
        codigo = celda(fila, "codigo")
        if not codigo or codigo in vistos:
            continue
        vistos.add(codigo)
        nombres = celda(fila, "nombre") or celda(fila, "nombres")
        nombre = " ".join(parte for parte in (nombres, celda(fila, "apellidos")) if parte)
        correo = celda(fila, "correo").lower()
        if not es_correo_upb(correo, dominios):
            correo = f"{codigo}@{DOMINIO_DE_EJEMPLO}"
            reemplazados += 1
        personas.append(
            {
                "codigo": codigo,
                "nombre": nombre,
                "correo": correo,
                "rol": "administrador" if codigo in administradores else "estudiante",
                "activo": True,
            }
        )
    return personas, reemplazados


def leer_filas(ruta):
    if ruta.suffix.lower() == ".csv":
        with open(ruta, encoding="utf-8-sig", newline="") as archivo:
            muestra = archivo.read(2048)
            archivo.seek(0)
            dialecto = csv.Sniffer().sniff(muestra, delimiters=",;\t")
            return list(csv.reader(archivo, dialecto))
    if ruta.suffix.lower() in (".xlsx", ".xlsm"):
        from openpyxl import load_workbook

        libro = load_workbook(ruta, read_only=True, data_only=True)
        return list(libro.active.iter_rows(values_only=True))
    raise CommandError("El archivo debe ser .xlsx o .csv")


class Command(BaseCommand):
    help = "Convierte la lista de la clase (Excel o CSV) en padron/padron.local.json"

    def add_arguments(self, parser):
        parser.add_argument("archivo", type=Path)
        parser.add_argument(
            "--administradores", default="",
            help="Códigos de los integrantes del equipo, separados por comas",
        )
        parser.add_argument(
            "--dominio", action="append", default=None,
            help="Dominio de correo de la UPB que se conserva (por defecto upb.edu y upb.edu.bo)",
        )
        parser.add_argument("--salida", type=Path, default=PADRON_LOCAL)

    def handle(self, *args, **opciones):
        ruta = opciones["archivo"]
        if not ruta.exists():
            raise CommandError(f"No existe el archivo {ruta}")
        administradores = {c.strip() for c in opciones["administradores"].split(",") if c.strip()}
        dominios = tuple(opciones["dominio"] or DOMINIOS_UPB)
        personas, reemplazados = convertir_filas(leer_filas(ruta), administradores, dominios)
        faltan = administradores - {p["codigo"] for p in personas}
        opciones["salida"].parent.mkdir(parents=True, exist_ok=True)
        with open(opciones["salida"], "w", encoding="utf-8") as archivo:
            json.dump(personas, archivo, ensure_ascii=False, indent=2)
        self.stdout.write(self.style.SUCCESS(
            f"Padrón local con {len(personas)} personas en {opciones['salida']} "
            f"({reemplazados} correos reemplazados por correos de ejemplo)."
        ))
        if faltan:
            self.stdout.write(self.style.WARNING(
                "Estos códigos de administrador no están en la lista: " + ", ".join(sorted(faltan))
            ))
