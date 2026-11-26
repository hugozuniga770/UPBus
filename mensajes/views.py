"""Vistas HTTP de los chats: reciben, llaman al servicio y responden."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from comun.vistas import leer

from . import reglas, servicios
from .serializadores import MensajeDeRutaEntrada, MensajeDirectoEntrada, mensaje_a_dict


class MensajesDirectosVista(APIView):
    def get(self, request, viaje_id):
        mensajes = servicios.mensajes_directos(
            request.user, viaje_id, request.query_params.get("estudiante")
        )
        return Response({
            "mensajes": [mensaje_a_dict(mensaje) for mensaje in mensajes],
            "respuestas_rapidas": list(reglas.RESPUESTAS_RAPIDAS),
        })

    def post(self, request, viaje_id):
        datos = leer(MensajeDirectoEntrada, request.data)
        mensaje, creado = servicios.enviar_mensaje_directo(
            request.user,
            viaje_id,
            datos["id_cliente"],
            datos.get("texto", ""),
            datos.get("estudiante"),
            datos.get("respuesta_rapida"),
        )
        codigo = status.HTTP_201_CREATED if creado else status.HTTP_200_OK
        return Response({"mensaje": mensaje_a_dict(mensaje)}, status=codigo)


class MiembroDeRutaVista(APIView):
    def get(self, request, ruta_id):
        ruta, es_miembro, puede_entrar = servicios.membresia_de_ruta(
            request.user, ruta_id
        )
        return Response({
            "ruta": {"id": ruta.pk, "nombre": ruta.nombre},
            "es_miembro": es_miembro,
            "puede_entrar": puede_entrar,
        })

    def post(self, request, ruta_id):
        miembro, creado = servicios.elegir_ruta(request.user, ruta_id)
        codigo = status.HTTP_201_CREATED if creado else status.HTTP_200_OK
        return Response({
            "miembro": {
                "id": miembro.pk,
                "ruta": miembro.ruta_id,
                "usuario": miembro.usuario_id,
            }
        }, status=codigo)


class MensajesDeRutaVista(APIView):
    def get(self, request, ruta_id):
        mensajes = servicios.mensajes_de_ruta(request.user, ruta_id)
        return Response({"mensajes": [mensaje_a_dict(mensaje) for mensaje in mensajes]})

    def post(self, request, ruta_id):
        datos = leer(MensajeDeRutaEntrada, request.data)
        mensaje, creado = servicios.enviar_mensaje_de_ruta(
            request.user, ruta_id, datos["id_cliente"], datos["texto"]
        )
        codigo = status.HTTP_201_CREATED if creado else status.HTTP_200_OK
        return Response({"mensaje": mensaje_a_dict(mensaje)}, status=codigo)
