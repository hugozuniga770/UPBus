"""Vistas HTTP de viajes: reciben, llaman al servicio y responden."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from comun.vistas import leer

from . import servicios
from .serializadores import PosicionEntrada, viaje_a_dict


class ViajesVista(APIView):
    def get(self, request):
        viajes = servicios.listar_viajes(
            request.user, request.query_params.get("ruta"), request.query_params.get("estado")
        )
        return Response({"viajes": [viaje_a_dict(viaje) for viaje in viajes]})


class ViajeVista(APIView):
    def get(self, request, viaje_id):
        viaje = servicios.buscar_viaje(viaje_id)
        return Response({"viaje": viaje_a_dict(viaje)})


class IniciarViajeVista(APIView):
    def post(self, request, viaje_id):
        viaje = servicios.iniciar_viaje(request.user, viaje_id)
        return Response({"viaje": viaje_a_dict(viaje)})


class TerminarViajeVista(APIView):
    def post(self, request, viaje_id):
        viaje = servicios.terminar_viaje(request.user, viaje_id)
        return Response({"viaje": viaje_a_dict(viaje)})


class PosicionesVista(APIView):
    def post(self, request, viaje_id):
        datos = leer(PosicionEntrada, request.data)
        viaje, _ = servicios.registrar_posicion(request.user, viaje_id, **datos)
        return Response({"viaje": viaje_a_dict(viaje)}, status=status.HTTP_201_CREATED)
