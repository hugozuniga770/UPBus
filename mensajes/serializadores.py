"""Formatos de entrada y salida de los chats."""
from rest_framework import serializers

from comun.tiempo import a_hora_local


class MensajeDirectoEntrada(serializers.Serializer):
    id_cliente = serializers.CharField(max_length=64)
    texto = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    estudiante = serializers.IntegerField(required=False, allow_null=True)
    respuesta_rapida = serializers.CharField(max_length=80, required=False, allow_blank=True)


class MensajeDeRutaEntrada(serializers.Serializer):
    id_cliente = serializers.CharField(max_length=64)
    texto = serializers.CharField(max_length=1000, allow_blank=True)


def mensaje_a_dict(mensaje):
    return {
        "id": mensaje.pk,
        "id_cliente": mensaje.id_cliente,
        "autor": {"id": mensaje.autor_id, "nombre": mensaje.autor.nombre},
        "viaje": mensaje.viaje_id,
        "estudiante": mensaje.estudiante_id,
        "ruta": mensaje.ruta_id,
        "texto": mensaje.texto,
        "enviado_en": a_hora_local(mensaje.enviado_en).isoformat(),
    }
