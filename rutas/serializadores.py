"""Formato de entrada y salida de rutas y del modo registro."""
from rest_framework import serializers

from comun.tiempo import a_hora_local


class RegistroNuevoEntrada(serializers.Serializer):
    ruta = serializers.IntegerField()
    horario = serializers.IntegerField(required=False, allow_null=True)
    id_cliente = serializers.CharField(max_length=64, required=False, allow_blank=True)


class MarcaEntrada(serializers.Serializer):
    id_cliente = serializers.CharField(max_length=64)
    nombre = serializers.CharField(max_length=120, required=False, allow_blank=True)
    latitud = serializers.FloatField()
    longitud = serializers.FloatField()
    precision_m = serializers.FloatField(required=False, allow_null=True)
    marcada_en = serializers.DateTimeField()


class PuntoEntrada(serializers.Serializer):
    id_cliente = serializers.CharField(max_length=64)
    latitud = serializers.FloatField()
    longitud = serializers.FloatField()
    precision_m = serializers.FloatField(required=False, allow_null=True)
    tomado_en = serializers.DateTimeField()


class PuntosEntrada(serializers.Serializer):
    puntos = PuntoEntrada(many=True)


def _hora(valor):
    return valor.strftime("%H:%M") if valor else None


def horario_a_dict(horario):
    from .reglas import llegada_limite

    return {
        "id": horario.pk,
        "sentido": horario.sentido,
        "salida": _hora(horario.salida),
        "llegada_limite": _hora(llegada_limite(horario)),
        "llegada_confirmada": horario.llegada_limite is not None,
    }


def ruta_resumida(ruta):
    return {
        "id": ruta.pk,
        "clave": ruta.clave,
        "nombre": ruta.nombre,
        "punto_de_partida": ruta.punto_de_partida,
        "nota": ruta.nota,
        "horarios": [horario_a_dict(h) for h in ruta.horarios.all()],
    }


def ruta_detallada(ruta, horario, paradas, horas):
    datos = ruta_resumida(ruta)
    datos.update(
        {
            "recorrido": ruta.recorrido,
            "horario_elegido": horario.pk if horario else None,
            "paradas": [
                {
                    "id": parada.pk,
                    "nombre": parada.nombre,
                    "latitud": parada.latitud,
                    "longitud": parada.longitud,
                    "orden": parada.orden,
                    "estado": parada.estado,
                    "hora_aproximada": _hora(horas.get(parada.pk)),
                }
                for parada in paradas
            ],
        }
    )
    return datos


def registro_a_dict(registro):
    return {
        "id": registro.pk,
        "id_cliente": registro.id_cliente,
        "ruta": {"id": registro.ruta_id, "clave": registro.ruta.clave, "nombre": registro.ruta.nombre},
        "horario": horario_a_dict(registro.horario) if registro.horario else None,
        "estado": registro.estado,
        "iniciado_en": a_hora_local(registro.iniciado_en).isoformat(),
        "marcas": [
            {
                "id_cliente": marca.id_cliente,
                "nombre": marca.nombre,
                "latitud": marca.latitud,
                "longitud": marca.longitud,
                "marcada_en": a_hora_local(marca.marcada_en).isoformat(),
            }
            for marca in registro.marcas.all()
        ],
    }


class PropuestaParadaEntrada(serializers.Serializer):
    nombre = serializers.CharField(max_length=120, required=False, allow_blank=True)
    latitud = serializers.FloatField()
    longitud = serializers.FloatField()


def parada_a_dict(parada, hora_aproximada=None):
    return {
        "id": parada.pk,
        "ruta": parada.ruta_id,
        "nombre": parada.nombre,
        "latitud": parada.latitud,
        "longitud": parada.longitud,
        "orden": parada.orden,
        "estado": parada.estado,
        "creada_por": parada.creada_por.nombre if parada.creada_por else None,
        "hora_aproximada": _hora(hora_aproximada),
    }

