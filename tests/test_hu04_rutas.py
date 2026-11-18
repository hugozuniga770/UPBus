"""HU-04 · Ver rutas, paradas y horarios (BUS-RF-05)."""
import pytest

from rutas.models import Parada, PasoPorParada, Ruta

from .conftest import CAMPOS, CAMPUS_UPB, LA_FONTANA, PETROL, SEVILLA

pytestmark = pytest.mark.django_db


def test_HU04_CA1_ve_la_ruta_con_recorrido_paradas_y_horarios(cliente_de, ismael, ruta_norte, horario_0640):
    for orden, (nombre, punto) in enumerate(
        [("La Fontana", LA_FONTANA), ("Sevilla", SEVILLA), ("Petrol", PETROL),
         ("Campos", CAMPOS), ("Campus UPB", CAMPUS_UPB)], start=1
    ):
        Parada.objects.create(ruta=ruta_norte, nombre=nombre, latitud=punto[0], longitud=punto[1], orden=orden)
    ruta_norte.recorrido = [list(LA_FONTANA), list(CAMPUS_UPB)]
    ruta_norte.save()
    conteo_antes = (Ruta.objects.count(), Parada.objects.count(), PasoPorParada.objects.count())

    respuesta = cliente_de(ismael).get(f"/api/rutas/{ruta_norte.pk}?horario={horario_0640.pk}")

    assert respuesta.status_code == 200
    ruta = respuesta.json()["ruta"]
    assert len(ruta["recorrido"]) == 2
    assert [p["nombre"] for p in ruta["paradas"]] == ["La Fontana", "Sevilla", "Petrol", "Campos", "Campus UPB"]
    ingresos = [h["salida"] for h in ruta["horarios"] if h["sentido"] == "ingreso"]
    assert ingresos == ["06:40", "11:00", "13:00", "15:30"]
    assert (Ruta.objects.count(), Parada.objects.count(), PasoPorParada.objects.count()) == conteo_antes


def test_HU04_CA2_el_estudiante_ve_solo_las_paradas_aprobadas(cliente_de, ismael, marco, ruta_norte):
    Parada.objects.create(ruta=ruta_norte, nombre="Sevilla", latitud=SEVILLA[0], longitud=SEVILLA[1], orden=1)
    Parada.objects.create(
        ruta=ruta_norte, nombre="Av. Banzer y 4to anillo", latitud=PETROL[0], longitud=PETROL[1],
        orden=2, estado="propuesta",
    )

    del_estudiante = cliente_de(ismael).get(f"/api/rutas/{ruta_norte.pk}").json()["ruta"]["paradas"]
    del_chofer = cliente_de(marco).get(f"/api/rutas/{ruta_norte.pk}").json()["ruta"]["paradas"]

    assert [p["nombre"] for p in del_estudiante] == ["Sevilla"]
    assert [(p["nombre"], p["estado"]) for p in del_chofer] == [
        ("Sevilla", "aprobada"), ("Av. Banzer y 4to anillo", "propuesta"),
    ]
