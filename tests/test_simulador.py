"""Simulador de escenarios (T23). Pruebas de soporte: no son criterios de la sesión 7.

El simulador llama a los mismos servicios que la app, así que estas pruebas también
comprueban que las reglas aguantan un viaje entero. Los viajes simulados no enseñan
horas (C-28).
"""
from datetime import datetime
from io import StringIO
from pathlib import Path
from threading import Event

import pytest
from django.core.management import call_command

from comun.geo import distancia_en_metros
from comun.rechazos import Rechazo
from comun.tiempo import ZONA_HORARIA
from rutas.models import Parada, PasoPorParada, Ruta
from viajes import simulador
from viajes.models import AvisoDeSubida, Viaje

from .conftest import CAMPOS, LA_FONTANA, PETROL, SEVILLA

REG_01 = Path(__file__).resolve().parent.parent / "rutas/datos/registros/registro-sur-0640-2026-11-25.json"


def reloj_de_prueba():
    """Avanza el tiempo simulado sin esperar: un viaje entero corre en un instante."""
    return simulador.RelojSinEsperas(datetime(2026, 11, 26, 6, 40, tzinfo=ZONA_HORARIA))


@pytest.fixture(autouse=True)
def sin_simulaciones_anteriores():
    simulador.SIMULACIONES.clear()
    yield
    simulador.SIMULACIONES.clear()


@pytest.fixture
def ruta(ruta_norte):
    """La Ruta Norte de los ejemplos, con recorrido y cuatro paradas aprobadas."""
    ruta_norte.recorrido = [list(LA_FONTANA), list(SEVILLA), list(PETROL), list(CAMPOS)]
    ruta_norte.save(update_fields=["recorrido"])
    paradas = [("La Fontana", LA_FONTANA), ("Sevilla", SEVILLA), ("Petrol", PETROL), ("Campos", CAMPOS)]
    for orden, (nombre, punto) in enumerate(paradas, start=1):
        Parada.objects.create(ruta=ruta_norte, nombre=nombre, latitud=punto[0], longitud=punto[1], orden=orden)
    return ruta_norte


@pytest.fixture
def en_el_momento(monkeypatch):
    """El panel corre la simulación en un hilo aparte; en las pruebas, en el momento y sin esperar."""
    monkeypatch.setattr(simulador, "_en_un_hilo", lambda tarea: tarea())
    monkeypatch.setattr(simulador, "crear_reloj", lambda velocidad: reloj_de_prueba())


def test_el_trayecto_avanza_de_a_poco_y_se_detiene_en_cada_parada(ruta):
    puntos = simulador.trayecto(ruta.recorrido, list(ruta.paradas.all()))

    detenciones = list(dict.fromkeys(p.parada for p in puntos if p.parada))
    assert detenciones == ["La Fontana", "Sevilla", "Petrol", "Campos"]
    pasos = [distancia_en_metros(a.punto, b.punto) for a, b in zip(puntos, puntos[1:])]
    assert max(pasos) <= simulador.PASO_M + 0.5
    assert all(a.segundos <= b.segundos for a, b in zip(puntos, puntos[1:]))
    en_sevilla = [p.segundos for p in puntos if p.parada == "Sevilla"]
    assert en_sevilla[-1] - en_sevilla[0] == simulador.ESPERA_EN_PARADA_S


def test_el_bus_recorre_la_ruta_y_el_viaje_termina(ruta):
    resumen = simulador.correr("recorrido", ruta.clave, reloj=reloj_de_prueba())

    viaje = Viaje.objects.get(pk=resumen["viaje"])
    assert viaje.simulado
    assert viaje.estado == "terminado"
    assert viaje.posiciones.count() == resumen["posiciones"] > 0
    assert sorted(viaje.paradas_registradas.values_list("nombre", flat=True)) == ["Campos", "La Fontana", "Petrol", "Sevilla"]


def test_un_viaje_simulado_no_ensena_horas(ruta):
    simulador.correr("recorrido", ruta.clave, reloj=reloj_de_prueba())

    assert not PasoPorParada.objects.exists()


def test_el_estudiante_que_no_sube_queda_no_se_presento(ruta):
    resumen = simulador.correr("no_se_presenta", ruta.clave, reloj=reloj_de_prueba())

    aviso = AvisoDeSubida.objects.get(viaje_id=resumen["viaje"])
    assert aviso.parada.nombre == "Sevilla"
    assert aviso.estado == "no_se_presento"
    assert aviso.ubicacion_en is None
    assert resumen["ubicaciones_compartidas"] > 0
    assert any("no se presentó" in nota for nota in resumen["notas"])


def test_rechaza_una_ruta_sin_recorrido(ruta_norte):
    with pytest.raises(Rechazo, match="la ruta no tiene recorrido: grábala con el modo registro"):
        simulador.correr("recorrido", ruta_norte.clave, reloj=reloj_de_prueba())

    assert not Viaje.objects.exists()


def test_al_detenerla_el_viaje_simulado_termina(ruta):
    detener = Event()
    detener.set()

    resumen = simulador.correr("recorrido", ruta.clave, reloj=reloj_de_prueba(), detener=detener)

    assert resumen["detenida"]
    assert Viaje.objects.get(pk=resumen["viaje"]).estado == "terminado"


def test_el_comando_simula_la_ruta_sur_grabada_sin_cambiar_sus_horas(cliente_de, sebastian):
    call_command("cargar_rutas", stdout=StringIO())
    call_command("importar_registro", str(REG_01), "--usuario", "70002", stdout=StringIO())
    ruta_sur = Ruta.objects.get(clave="sur")

    def horas():
        respuesta = cliente_de(sebastian).get(f"/api/rutas/{ruta_sur.pk}")
        return [p["hora_aproximada"] for p in respuesta.json()["ruta"]["paradas"]]

    antes = horas()
    salida = StringIO()
    call_command("simular", "no_se_presenta", "--ruta", "sur", "--sin-esperar", stdout=salida)

    assert "no se presentó" in salida.getvalue()
    viaje = Viaje.objects.get(simulado=True)
    assert viaje.estado == "terminado"
    assert viaje.paradas_registradas.count() == ruta_sur.paradas.count() == 9
    assert horas() == antes


def test_el_administrador_corre_un_escenario_desde_el_panel(cliente_de, hugo, ruta, en_el_momento):
    respuesta = cliente_de(hugo).post(
        "/api/simulaciones", {"escenario": "recorrido", "ruta": ruta.pk, "velocidad": 10}, format="json"
    )

    assert respuesta.status_code == 202
    panel = cliente_de(hugo).get("/api/simulaciones").json()
    assert [e["clave"] for e in panel["escenarios"]] == ["recorrido", "no_se_presenta"]
    simulacion = panel["simulaciones"][0]
    assert simulacion["estado"] == "terminada"
    assert Viaje.objects.get(pk=simulacion["viaje"]).simulado


def test_solo_el_administrador_usa_el_panel(cliente_de, ismael, ruta):
    respuesta = cliente_de(ismael).post(
        "/api/simulaciones", {"escenario": "recorrido", "ruta": ruta.pk}, format="json"
    )

    assert respuesta.status_code == 403
    assert respuesta.json() == {"causa": "solo el administrador puede hacer esto"}
    assert cliente_de(ismael).get("/api/simulaciones").status_code == 403


def test_el_panel_rechaza_una_ruta_sin_recorrido(cliente_de, hugo, ruta_norte, en_el_momento):
    respuesta = cliente_de(hugo).post(
        "/api/simulaciones", {"escenario": "recorrido", "ruta": ruta_norte.pk}, format="json"
    )

    assert respuesta.status_code == 400
    assert respuesta.json() == {"causa": "la ruta no tiene recorrido: grábala con el modo registro"}
    assert not Viaje.objects.exists()


def test_el_panel_detiene_la_simulacion_y_no_deja_correr_dos(cliente_de, hugo, ruta, monkeypatch):
    monkeypatch.setattr(simulador, "_en_un_hilo", lambda tarea: None)  # queda en curso
    datos = {"escenario": "recorrido", "ruta": ruta.pk}
    simulacion_id = cliente_de(hugo).post("/api/simulaciones", datos, format="json").json()["simulacion"]["id"]

    segunda = cliente_de(hugo).post("/api/simulaciones", datos, format="json")
    respuesta = cliente_de(hugo).post(f"/api/simulaciones/{simulacion_id}/detener")

    assert segunda.status_code == 400
    assert segunda.json() == {"causa": "ya hay una simulación en curso: detenla primero"}
    assert respuesta.status_code == 200
    assert simulador.SIMULACIONES[simulacion_id].detener.is_set()
