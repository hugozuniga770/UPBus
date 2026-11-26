"""Quién es quién en las pruebas de punta a punta (T21).

Datos de ejemplo de la sección 0 de `docs/sesion-06-requisitos.md`, nunca de la
clase: el padrón es `padron/padron.json`. Ana, Valeria y Rosa son estudiantes
ficticias, como Ana en las pruebas del servidor. La contraseña es la de
`tests/conftest.py`.
"""
from math import cos, radians

CONTRASENA = "clave-segura-123"

HUGO = "70001"  # administrador en el padrón de ejemplo
MARCO = "marco.chofer@upbus.example"  # chofer: los choferes no están en el padrón
ANA = "ana@upb.example"  # estudiante ficticia: el bus en vivo, «Voy a subir» y el panel Demo
VALERIA = "valeria@upb.example"  # estudiante ficticia: el chat directo
ROSA = "rosa@upb.example"  # estudiante ficticia: el chat de la ruta
ISMAEL = "70004"  # estudiante del padrón de ejemplo, sin cuenta: lo registra la prueba de cuentas
LUCIA = "70005"  # inactiva en el padrón de ejemplo


def punto_a(desde, metros_al_norte=0, metros_al_este=0):
    """Un punto a cierta distancia de otro, como en `tests/conftest.py`."""
    latitud = desde[0] + metros_al_norte / 111_320
    longitud = desde[1] + metros_al_este / (111_320 * cos(radians(desde[0])))
    return (latitud, longitud)


LA_FONTANA = (-17.7200, -63.1650)
# Paradas de ejemplo de la Ruta Norte, las mismas de las pruebas del servidor.
PARADAS_NORTE = [
    ("Sevilla", *punto_a(LA_FONTANA, metros_al_norte=-3_000)),
    ("Petrol", *punto_a(LA_FONTANA, metros_al_norte=-5_000, metros_al_este=1_500)),
    ("Campos", *punto_a(LA_FONTANA, metros_al_norte=-7_000, metros_al_este=2_500)),
]
# Donde el GPS del chofer pone al bus: a más de 5 km de las paradas, para que
# ninguna prueba cierre avisos porque «el bus ya pasó».
CAMPUS_UPB = punto_a(LA_FONTANA, metros_al_norte=-12_000, metros_al_este=4_000)
