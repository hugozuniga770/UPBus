"""Formatos de entrada y salida de viajes y posiciones."""
from rest_framework import serializers

from comun.tiempo import a_hora_local


class PosicionEntrada(serializers.Serializer):
    id_cliente = serializers.CharField(max_length=64)
    latitud = serializers.FloatField()
    longitud = serializers.FloatField()
    tomada_en = serializers.DateTimeField()


def _momento(valor):
    return a_hora_local(valor).isoformat() if valor else None


def viaje_a_dict(viaje):
    ultima_posicion = None
    if viaje.ultima_posicion_en is not None:
        ultima_posicion = {
            "latitud": viaje.ultima_latitud,
            "longitud": viaje.ultima_longitud,
            "tomada_en": _momento(viaje.ultima_posicion_en),
        }
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
    }
