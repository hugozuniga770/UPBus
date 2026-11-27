"""HU-08 · Proponer paradas sobre el recorrido y aprobarlas (BUS-RF-10, P-07, P-28)."""
import asyncio
from datetime import date

import pytest
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from rutas.models import Parada
from viajes.consumers import grupo_del_chofer
from viajes.models import Viaje

from .conftest import LA_FONTANA, SEVILLA, crear_cuenta, punto_a

pytestmark = pytest.mark.django_db


@pytest.fixture
def ruta_con_recorrido(ruta_norte):
    ruta_norte.recorrido = [list(LA_FONTANA), list(SEVILLA)]
    ruta_norte.save(update_fields=["recorrido"])
    return ruta_norte


def escuchar_al_chofer(viaje):
    """Devuelve una función que dice si al canal privado del chofer llegó algo."""
    capa = get_channel_layer()
    canal = async_to_sync(capa.new_channel)()
    async_to_sync(capa.group_add)(grupo_del_chofer(viaje.pk), canal)

    async def llego_algo():
        try:
            await asyncio.wait_for(capa.receive(canal), timeout=0.3)
            return True
        except asyncio.TimeoutError:
            return False

    return lambda: async_to_sync(llego_algo)()


def proponer(cliente, ruta, nombre, punto):
    return cliente.post(
        f"/api/rutas/{ruta.pk}/paradas",
        {"nombre": nombre, "latitud": punto[0], "longitud": punto[1]},
        format="json",
    )


def test_HU08_CA1_propone_una_parada_sobre_la_ruta(cliente_de, ismael, ruta_con_recorrido):
    cerca_del_recorrido = punto_a(LA_FONTANA, metros_al_norte=-1_000, metros_al_este=120)

    respuesta = proponer(cliente_de(ismael), ruta_con_recorrido, "Av. Banzer y 4to anillo", cerca_del_recorrido)

    assert respuesta.status_code == 201
    datos = respuesta.json()["parada"]
    assert datos["nombre"] == "Av. Banzer y 4to anillo"
    assert datos["estado"] == "propuesta"
    parada = Parada.objects.get(pk=datos["id"])
    assert (parada.estado, parada.creada_por) == (Parada.Estado.PROPUESTA, ismael)


def test_HU08_CA2_rechaza_una_parada_lejos_del_recorrido(cliente_de, ismael, ruta_con_recorrido):
    lejos_del_recorrido = punto_a(LA_FONTANA, metros_al_norte=-1_000, metros_al_este=250)

    respuesta = proponer(cliente_de(ismael), ruta_con_recorrido, "Parada Lejana", lejos_del_recorrido)

    assert respuesta.status_code == 400
    assert respuesta.json() == {"causa": "la parada debe estar sobre la ruta"}
    assert Parada.objects.filter(ruta=ruta_con_recorrido, nombre="Parada Lejana").count() == 0


@pytest.mark.django_db(transaction=True)
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

    llego_algo_al_chofer = escuchar_al_chofer(viaje)

    # El bus se acerca a Sevilla y nadie marcó «Voy a subir» en ella.
    cerca_de_sevilla = punto_a(SEVILLA, metros_al_norte=300)
    posicion = cliente_de(marco).post(
        f"/api/viajes/{viaje.pk}/posiciones",
        {
            "id_cliente": "posicion-1",
            "latitud": cerca_de_sevilla[0],
            "longitud": cerca_de_sevilla[1],
            "tomada_en": hora(16, 6, 45).isoformat(),
        },
        format="json",
    )
    assert posicion.status_code == 201

    sin_nadie = cliente_de(marco).get(f"/api/viajes/{viaje.pk}").json()["viaje"]
    assert sevilla.pk not in sin_nadie["paradas_activas"]
    assert not llego_algo_al_chofer()

    aviso_id = (
        cliente_de(ismael)
        .post(f"/api/viajes/{viaje.pk}/avisos", {"parada": sevilla.pk}, format="json")
        .json()["aviso"]["id"]
    )
    assert llego_algo_al_chofer()  # con alguien esperando, a Marco sí le llega su aviso (HU-07)
    sin_ubicacion = cliente_de(marco).get(f"/api/viajes/{viaje.pk}").json()["viaje"]
    assert sevilla.pk not in sin_ubicacion["paradas_activas"]

    # Activa solo mientras Ismael comparte su ubicación (RF-10).
    cliente_de(ismael).post(
        f"/api/avisos/{aviso_id}/ubicacion",
        {"latitud": SEVILLA[0], "longitud": SEVILLA[1], "tomada_en": hora(16, 6, 50).isoformat()},
        format="json",
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
    parada_id = proponer(
        cliente_de(ismael), ruta_con_recorrido, "Av. Banzer y 4to anillo", cerca
    ).json()["parada"]["id"]
    ana = crear_cuenta("Ana", "ana@upb.example", "estudiante", "70006")

    def paradas_que_ve_ana():
        ruta = cliente_de(ana).get(f"/api/rutas/{ruta_con_recorrido.pk}").json()["ruta"]
        return {parada["id"]: parada["estado"] for parada in ruta["paradas"]}

    assert parada_id not in paradas_que_ve_ana()

    sin_permiso = cliente_de(ismael).post(f"/api/paradas/{parada_id}/aprobar")
    assert sin_permiso.status_code == 403

    respuesta = cliente_de(hugo).post(f"/api/paradas/{parada_id}/aprobar")
    assert respuesta.status_code == 200
    assert respuesta.json()["parada"]["estado"] == "aprobada"
    assert Parada.objects.get(pk=parada_id).estado == Parada.Estado.APROBADA
    assert paradas_que_ve_ana()[parada_id] == "aprobada"
