"""Formatos de entrada y salida de viajes y posiciones."""
from rest_framework import serializers

from comun.tiempo import a_hora_local


class AvisoEntrada(serializers.Serializer):
    parada = serializers.IntegerField()


class UbicacionEntrada(serializers.Serializer):
    latitud = serializers.FloatField()
    longitud = serializers.FloatField()
    tomada_en = serializers.DateTimeField()


class SimulacionEntrada(serializers.Serializer):
    escenario = serializers.CharField(max_length=30)
    ruta = serializers.IntegerField()
    velocidad = serializers.FloatField(default=10)
    parada = serializers.IntegerField(required=False, allow_null=True)


class PosicionEntrada(serializers.Serializer):
    id_cliente = serializers.CharField(max_length=64)
    latitud = serializers.FloatField()
    longitud = serializers.FloatField()
    tomada_en = serializers.DateTimeField()


def _momento(valor):
    return a_hora_local(valor).isoformat() if valor else None


def viaje_a_dict(viaje):
    from .models import AvisoDeSubida

    ultima_posicion = None
    if viaje.ultima_posicion_en is not None:
        ultima_posicion = {
            "latitud": viaje.ultima_latitud,
            "longitud": viaje.ultima_longitud,
            "tomada_en": _momento(viaje.ultima_posicion_en),
        }
    # RF-10: una parada está activa si alguien con «Voy a subir» en ella comparte su ubicación.
    paradas_activas = list(
        viaje.avisos.filter(estado=AvisoDeSubida.Estado.CONFIRMADO, ubicacion_en__isnull=False)
        .values_list("parada_id", flat=True)
        .distinct()
    )
    return {
        "id": viaje.pk,
        "ruta": {
            "id": viaje.ruta_id,
            "clave": viaje.ruta.clave,
            "nombre": viaje.ruta.nombre,
        },
        "horario": {
            "id": viaje.horario_id,
            "sentido": viaje.horario.sentido,
            "salida": viaje.horario.salida.strftime("%H:%M"),
        },
        "fecha": viaje.fecha.isoformat(),
        "chofer": {"id": viaje.chofer_id, "nombre": viaje.chofer.nombre},
        "estado": viaje.estado,
        "iniciado_en": _momento(viaje.iniciado_en),
        "terminado_en": _momento(viaje.terminado_en),
        "ultima_posicion": ultima_posicion,
        "paradas_activas": paradas_activas,
        "simulado": viaje.simulado,
    }


def aviso_a_dict(aviso, con_ubicacion=False):
    """Con la ubicación solo para el chofer del viaje y el administrador (BUS-RF-08)."""
    ubicacion = None
    if con_ubicacion and aviso.ubicacion_en is not None:
        ubicacion = {
            "latitud": aviso.ubicacion_latitud,
            "longitud": aviso.ubicacion_longitud,
            "tomada_en": _momento(aviso.ubicacion_en),
        }
    return {
        "id": aviso.pk,
        "viaje": aviso.viaje_id,
        "estudiante": {"id": aviso.estudiante_id, "nombre": aviso.estudiante.nombre},
        "parada": {"id": aviso.parada_id, "nombre": aviso.parada.nombre},
        "estado": aviso.estado,
        "creado_en": _momento(aviso.creado_en),
        "compartiendo_ubicacion": aviso.ubicacion_en is not None,
        "ubicacion": ubicacion,
    }


def simulacion_a_dict(simulacion):
    return {
        "id": simulacion.id,
        "escenario": simulacion.escenario,
        "ruta": simulacion.ruta,
        "velocidad": simulacion.velocidad,
        "estado": simulacion.estado,
        "deteniendo": simulacion.estado == "en_curso" and simulacion.detener.is_set(),
        "viaje": simulacion.viaje,
        "iniciada_en": _momento(simulacion.iniciada_en),
        "notas": list(simulacion.notas),
    }
