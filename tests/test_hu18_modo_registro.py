"""HU-18 · Registrar paradas y horas en un viaje real (BUS-RF-23)."""
import uuid

import pytest

from rutas.models import MarcaDeParada, Parada

from .conftest import CAMPUS_UPB, LA_FONTANA, SEVILLA, punto_a

pytestmark = pytest.mark.django_db


def iniciar(cliente, ruta, horario):
    respuesta = cliente.post("/api/registros", {"ruta": ruta.pk, "horario": horario.pk}, format="json")
    return respuesta


def marcar(cliente, registro_id, nombre, punto, momento, id_cliente=None):
    return cliente.post(
        f"/api/registros/{registro_id}/marcas",
        {
            "id_cliente": id_cliente or str(uuid.uuid4()),
            "nombre": nombre,
            "latitud": punto[0],
            "longitud": punto[1],
            "precision_m": 8,
            "marcada_en": momento.isoformat(),
        },
        format="json",
    )


def hora_de(cliente, ruta, horario, nombre):
    paradas = cliente.get(f"/api/rutas/{ruta.pk}?horario={horario.pk}").json()["ruta"]["paradas"]
    return next(p["hora_aproximada"] for p in paradas if p["nombre"] == nombre)


def primer_registro(cliente, ruta, horario, hora):
    registro_id = iniciar(cliente, ruta, horario).json()["registro"]["id"]
    marcar(cliente, registro_id, "La Fontana", LA_FONTANA, hora(20, 6, 40))
    marcar(cliente, registro_id, "Sevilla", SEVILLA, hora(20, 6, 58))
    marcar(cliente, registro_id, "Campus UPB", CAMPUS_UPB, hora(20, 7, 35))
    return cliente.post(f"/api/registros/{registro_id}/terminar")


def test_HU18_CA1_el_primer_registro_crea_las_paradas_y_sus_horas(cliente_de, sebastian, ruta_norte, horario_0640, hora):
    cliente = cliente_de(sebastian)

    respuesta = primer_registro(cliente, ruta_norte, horario_0640, hora)

    assert respuesta.status_code == 200
    assert respuesta.json()["resumen"]["paradas_nuevas"] == 3
    paradas = list(ruta_norte.paradas.order_by("orden").values_list("nombre", "estado"))
    assert paradas == [("La Fontana", "aprobada"), ("Sevilla", "aprobada"), ("Campus UPB", "aprobada")]
    assert hora_de(cliente, ruta_norte, horario_0640, "Sevilla") == "06:58"


def test_HU18_CA2_un_segundo_registro_ajusta_la_hora_sin_duplicar_la_parada(cliente_de, sebastian, ruta_norte, horario_0640, hora):
    cliente = cliente_de(sebastian)
    primer_registro(cliente, ruta_norte, horario_0640, hora)

    registro_id = iniciar(cliente, ruta_norte, horario_0640).json()["registro"]["id"]
    marcar(cliente, registro_id, "La Fontana", LA_FONTANA, hora(23, 6, 41))
    marcar(cliente, registro_id, "Sevilla", punto_a(SEVILLA, metros_al_norte=30), hora(23, 7, 2))
    cliente.post(f"/api/registros/{registro_id}/terminar")

    assert Parada.objects.filter(ruta=ruta_norte, nombre="Sevilla").count() == 1
    assert hora_de(cliente, ruta_norte, horario_0640, "Sevilla") == "07:00"


def test_HU18_CA3_un_estudiante_no_puede_usar_el_modo_registro(cliente_de, ismael, ruta_norte, horario_0640):
    respuesta = iniciar(cliente_de(ismael), ruta_norte, horario_0640)

    assert respuesta.status_code == 403
    assert respuesta.json()["causa"] == "solo un chofer o un administrador puede usar el modo registro"


def test_HU18_CA4_rechaza_una_marca_a_menos_de_50_m_de_otra(cliente_de, sebastian, ruta_norte, horario_0640, hora):
    cliente = cliente_de(sebastian)
    registro_id = iniciar(cliente, ruta_norte, horario_0640).json()["registro"]["id"]
    marcar(cliente, registro_id, "Sevilla", SEVILLA, hora(20, 6, 58))

    respuesta = marcar(cliente, registro_id, "Sevilla 2", punto_a(SEVILLA, metros_al_este=20), hora(20, 6, 59))

    assert respuesta.status_code == 400
    assert respuesta.json()["causa"] == "ya marcaste una parada a menos de 50 m"
    assert MarcaDeParada.objects.count() == 1


def test_HU18_CA5_una_marca_reenviada_se_guarda_una_sola_vez(cliente_de, sebastian, ruta_norte, horario_0640, hora):
    cliente = cliente_de(sebastian)
    registro_id = iniciar(cliente, ruta_norte, horario_0640).json()["registro"]["id"]
    mismo_id = str(uuid.uuid4())

    primera = marcar(cliente, registro_id, "Sevilla", SEVILLA, hora(20, 6, 58), id_cliente=mismo_id)
    reenvio = marcar(cliente, registro_id, "Sevilla", SEVILLA, hora(20, 6, 58), id_cliente=mismo_id)

    assert (primera.status_code, reenvio.status_code) == (201, 201)
    assert MarcaDeParada.objects.count() == 1
