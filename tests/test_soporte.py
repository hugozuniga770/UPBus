"""Pruebas de soporte: no son criterios de aceptación.

Verifican herramientas de las que dependen el equipo y la demo: el
importador del padrón, el respaldo del modo registro (también el viaje real de la
Ruta Sur) y el WebSocket.
"""
import json
import uuid
from io import StringIO
from pathlib import Path

import pytest
from asgiref.sync import async_to_sync
from channels.testing import WebsocketCommunicator
from django.contrib import admin
from django.core.management import CommandError, call_command

from config.asgi import application
from cuentas.management.commands.importar_padron import convertir_filas
from rutas.models import Parada, Ruta
from viajes.models import Viaje

from .conftest import CAMPUS_UPB, LA_FONTANA, SEVILLA


def test_el_administrador_puede_programar_viajes_desde_el_panel():
    viaje_admin = admin.site._registry[Viaje]

    assert viaje_admin.list_display == ("ruta", "horario", "fecha", "chofer", "estado")
    assert viaje_admin.list_filter == ("estado", "fecha")


def test_importar_padron_reemplaza_los_correos_que_no_son_de_la_upb():
    """Mismo formato que la lista de la clase; las personas son ficticias."""
    filas = [
        ("Nombre", "Apellido(s)", "Dirección de correo", "Codigo"),
        ("Ana", "Rojas Paz", "ana.rojas1@upb.edu", 71001),
        ("Luis", "Vaca", "luisito@gmail.com", 71002),
        ("Eva", "Suárez", "eva.suarez1@upb.edu.bo", 71003),
    ]

    personas, reemplazados = convertir_filas(filas, administradores={"71001"})

    assert reemplazados == 1
    assert personas[0] == {"codigo": "71001", "nombre": "Ana Rojas Paz", "correo": "ana.rojas1@upb.edu",
                           "rol": "administrador", "activo": True}
    assert personas[1]["correo"] == "71002@upb.example"
    assert personas[2]["correo"] == "eva.suarez1@upb.edu.bo"


@pytest.mark.django_db
def test_importar_un_respaldo_del_modo_registro(tmp_path, sebastian, ruta_norte):
    def marca(nombre, punto, minuto):
        return {"id_cliente": str(uuid.uuid4()), "nombre": nombre, "latitud": punto[0],
                "longitud": punto[1], "precision_m": 10, "marcada_en": f"2026-11-20T06:{minuto}:00-04:00"}

    respaldo = {
        "formato": "upbus-registro", "version": 1, "id_cliente": str(uuid.uuid4()),
        "ruta": {"clave": "norte"}, "horario": {"sentido": "ingreso", "salida": "06:40"},
        "iniciado_en": "2026-11-20T06:39:00-04:00",
        "marcas": [marca("La Fontana", LA_FONTANA, 40), marca("Sevilla", SEVILLA, 58), marca("Campus UPB", CAMPUS_UPB, 59)],
        "puntos": [],
    }
    archivo = tmp_path / "respaldo.json"
    archivo.write_text(json.dumps(respaldo), encoding="utf-8")

    call_command("importar_registro", str(archivo), "--usuario", "70002", stdout=StringIO())

    assert Parada.objects.filter(ruta=ruta_norte).count() == 3
    with pytest.raises(CommandError, match="ya fue importado"):
        call_command("importar_registro", str(archivo), "--usuario", "70002", stdout=StringIO())


@pytest.mark.django_db(transaction=True)
def test_el_websocket_del_viaje_confirma_la_conexion():
    async def conectar():
        comunicador = WebsocketCommunicator(application, "/ws/viajes/7/", headers=[(b"origin", b"http://localhost")])
        conectado, _ = await comunicador.connect()
        mensaje = await comunicador.receive_json_from()
        await comunicador.disconnect()
        return conectado, mensaje

    conectado, mensaje = async_to_sync(conectar)()

    assert conectado
    assert mensaje == {"tipo": "conectado", "viaje": 7}


RUTA_SUR_25_11 = Path(__file__).resolve().parent.parent / "rutas/datos/registros/registro-sur-0640-2026-11-25.json"


def test_el_registro_real_de_la_ruta_sur_da_las_horas_observadas(cliente_de, sebastian):
    """Viaje grabado el 25/11 (REG-01): las horas de la app son las que se vieron en el bus."""
    call_command("cargar_rutas", stdout=StringIO())
    call_command("importar_registro", str(RUTA_SUR_25_11), "--usuario", "70002", stdout=StringIO())
    ruta_sur = Ruta.objects.get(clave="sur")
    ingreso_0640 = ruta_sur.horarios.get(sentido="ingreso", salida="06:40")

    paradas = cliente_de(sebastian).get(f"/api/rutas/{ruta_sur.pk}?horario={ingreso_0640.pk}").json()["ruta"]["paradas"]

    assert [(p["nombre"], p["hora_aproximada"]) for p in paradas] == [
        ("Makro Parque", "06:46"), ("Parque Urbano", "07:00"), ("Banco Ganadero", "07:02"),
        ("Cine Center", "07:04"), ("Mercado Ramafa", "07:11"), ("AMarket Santos Dumont 4to anillo", "07:14"),
        ("Hot Burguer 4to anillo", "07:15"), ("Avenida Olimpica 4to anillo", "07:17"), ("Campus UPB", "07:30"),
    ]
    assert all(p["estado"] == "aprobada" for p in paradas)
    assert len(Ruta.objects.get(clave="sur").recorrido) == 96
