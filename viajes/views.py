"""Vistas HTTP de viajes: reciben, llaman al servicio y responden."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from comun.vistas import leer

from . import servicios, simulador
from .serializadores import (
    AvisoEntrada,
    PosicionEntrada,
    SimulacionEntrada,
    UbicacionEntrada,
    aviso_a_dict,
    simulacion_a_dict,
    viaje_a_dict,
)


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


class AvisosVista(APIView):
    """HU-07: el estudiante avisa «Voy a subir»; el chofer ve quién va a subir y dónde está."""

    def get(self, request, viaje_id):
        avisos = servicios.avisos_del_viaje(request.user, viaje_id)
        return Response({"avisos": [aviso_a_dict(aviso, con_ubicacion=True) for aviso in avisos]})

    def post(self, request, viaje_id):
        datos = leer(AvisoEntrada, request.data)
        aviso = servicios.avisar_que_va_a_subir(request.user, viaje_id, datos["parada"])
        return Response({"aviso": aviso_a_dict(aviso)}, status=status.HTTP_201_CREATED)


class MiAvisoVista(APIView):
    def get(self, request, viaje_id):
        aviso = servicios.aviso_activo_de(request.user, viaje_id)
        return Response({"aviso": aviso_a_dict(aviso) if aviso else None})


class CancelarAvisoVista(APIView):
    def post(self, request, aviso_id):
        aviso = servicios.cancelar_aviso(request.user, aviso_id)
        return Response({"aviso": aviso_a_dict(aviso)})


class UbicacionDelAvisoVista(APIView):
    def post(self, request, aviso_id):
        datos = leer(UbicacionEntrada, request.data)
        aviso = servicios.compartir_ubicacion(request.user, aviso_id, **datos)
        return Response({"aviso": aviso_a_dict(aviso)})


class SimulacionesVista(APIView):
    """T23: panel de demo del administrador."""

    def get(self, request):
        escenarios, simulaciones = simulador.panel(request.user)
        return Response({
            "escenarios": [{"clave": clave, "descripcion": descripcion} for clave, descripcion in escenarios],
            "simulaciones": [simulacion_a_dict(s) for s in simulaciones],
        })

    def post(self, request):
        datos = leer(SimulacionEntrada, request.data)
        simulacion = simulador.iniciar_simulacion(request.user, **datos)
        return Response({"simulacion": simulacion_a_dict(simulacion)}, status=status.HTTP_202_ACCEPTED)


class DetenerSimulacionVista(APIView):
    def post(self, request, simulacion_id):
        simulacion = simulador.detener_simulacion(request.user, simulacion_id)
        return Response({"simulacion": simulacion_a_dict(simulacion)})
