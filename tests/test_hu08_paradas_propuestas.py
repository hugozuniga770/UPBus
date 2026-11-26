"""HU-08 · Proponer paradas sobre el recorrido y aprobarlas (BUS-RF-10, P-07, P-28)."""
from datetime import date

import pytest

from rutas.models import Parada
from viajes.models import Viaje

from .conftest import LA_FONTANA, SEVILLA, punto_a

pytestmark = pytest.mark.django_db


@pytest.fixture
def ruta_con_recorrido(ruta_norte):
    ruta_norte.recorrido = [list(LA_FONTANA), list(SEVILLA)]
    ruta_norte.save(update_fields=["recorrido"])
    return ruta_norte


def proponer(cliente, ruta, nombre, punto):
    return cliente.post(
        f"/api/rutas/{ruta.pk}/paradas",
        {"nombre": nombre, "latitud": punto[0], "longitud": punto[1]},
        format="json",
    )


def test_HU08_CA1_propone_una_parada_sobre_la_ruta(cliente_de, ismael, ruta_con_recorrido):
    cerca_del_recorrido = punto_a(LA_FONTANA, metros_al_norte=-1_000, metros_al_este=120)

    respuesta = proponer(cliente_de(ismael), ruta_con_recorrido, "Parada El Cristo", cerca_del_recorrido)

    assert respuesta.status_code == 201
    datos = respuesta.json()["parada"]
    assert datos["nombre"] == "Parada El Cristo"
    assert datos["estado"] == "propuesta"
    parada = Parada.objects.get(pk=datos["id"])
    assert (parada.estado, parada.creada_por) == (Parada.Estado.PROPUESTA, ismael)


def test_HU08_CA2_rechaza_una_parada_lejos_del_recorrido(cliente_de, ismael, ruta_con_recorrido):
    lejos_del_recorrido = punto_a(LA_FONTANA, metros_al_norte=-1_000, metros_al_este=250)

    respuesta = proponer(cliente_de(ismael), ruta_con_recorrido, "Parada Lejana", lejos_del_recorrido)

    assert respuesta.status_code == 400
    assert "200 m" in respuesta.json()["causa"]
    assert Parada.objects.filter(ruta=ruta_con_recorrido, nombre="Parada Lejana").count() == 0


def test_HU08_CA3_una_parada_sin_nadie_no_esta_activa(
    cliente_de, ismael, marco, ruta_con_recorrido, horario_0640, hora
):
    sevilla = Parada.objects.create(
        ruta=ruta_con_recorrido, nombre="Sevilla", latitud=SEVILLA[0], longitud=SEVILLA[1], orden=1
    )
    viaje = Viaje.objects.create(
        ruta=ruta_con_recorrido,
        horario=horario_0640,
        fecha=date(2026, 11, 16),
        chofer=marco,
        estado="en_curso",
        iniciado_en=hora(16, 6, 38),
    )

    sin_nadie = cliente_de(marco).get(f"/api/viajes/{viaje.pk}").json()["viaje"]
    assert sevilla.pk not in sin_nadie["paradas_activas"]

    aviso_id = (
        cliente_de(ismael)
        .post(f"/api/viajes/{viaje.pk}/avisos", {"parada": sevilla.pk}, format="json")
        .json()["aviso"]["id"]
    )
    con_estudiante = cliente_de(marco).get(f"/api/viajes/{viaje.pk}").json()["viaje"]
    assert sevilla.pk in con_estudiante["paradas_activas"]

    cliente_de(ismael).post(f"/api/avisos/{aviso_id}/cancelar")
    tras_cancelar = cliente_de(marco).get(f"/api/viajes/{viaje.pk}").json()["viaje"]
    assert sevilla.pk not in tras_cancelar["paradas_activas"]


def test_HU08_CA4_el_administrador_aprueba_una_parada_propuesta(
    cliente_de, ismael, hugo, ruta_con_recorrido
):
    cerca = punto_a(LA_FONTANA, metros_al_norte=-1_000, metros_al_este=50)
    parada_id = proponer(cliente_de(ismael), ruta_con_recorrido, "Parada Nueva", cerca).json()["parada"]["id"]

    sin_permiso = cliente_de(ismael).post(f"/api/paradas/{parada_id}/aprobar")
    assert sin_permiso.status_code == 403

    respuesta = cliente_de(hugo).post(f"/api/paradas/{parada_id}/aprobar")
    assert respuesta.status_code == 200
    assert respuesta.json()["parada"]["estado"] == "aprobada"
    assert Parada.objects.get(pk=parada_id).estado == Parada.Estado.APROBADA