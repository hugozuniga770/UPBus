"""Vistas de rutas y del modo registro: reciben, llaman al servicio y responden."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from comun.vistas import leer

from . import servicios
from .serializadores import (
    MarcaEntrada,
    PropuestaParadaEntrada,
    PuntosEntrada,
    RegistroNuevoEntrada,
    parada_a_dict,
    registro_a_dict,
    ruta_detallada,
    ruta_resumida,
)


class RutasVista(APIView):
    """HU-04. GET /api/rutas"""

    def get(self, request):
        return Response({"rutas": [ruta_resumida(r) for r in servicios.listar_rutas()]})


class RutaVista(APIView):
    """HU-04. GET /api/rutas/<id>?horario=<id>"""

    def get(self, request, ruta_id):
        ruta, horario, paradas, horas = servicios.ver_ruta(
            ruta_id, request.query_params.get("horario"), request.user
        )
        return Response({"ruta": ruta_detallada(ruta, horario, paradas, horas)})


class RegistrosVista(APIView):
    """HU-18. POST /api/registros: inicia un registro."""

    def post(self, request):
        datos = leer(RegistroNuevoEntrada, request.data)
        registro = servicios.iniciar_registro(
            request.user, datos["ruta"], datos.get("horario"), datos.get("id_cliente")
        )
        return Response({"registro": registro_a_dict(registro)}, status=status.HTTP_201_CREATED)


class RegistroEnCursoVista(APIView):
    """HU-18. GET /api/registros/en-curso"""

    def get(self, request):
        registro = servicios.registro_en_curso_de(request.user)
        return Response({"registro": registro_a_dict(registro) if registro else None})


class MarcasVista(APIView):
    """HU-18. POST /api/registros/<id>/marcas: «Parada aquí»."""

    def post(self, request, registro_id):
        datos = leer(MarcaEntrada, request.data)
        servicios.marcar_parada(request.user, registro_id, **datos)
        return Response({"guardada": True}, status=status.HTTP_201_CREATED)


class PuntosVista(APIView):
    """HU-18. POST /api/registros/<id>/puntos: posiciones del recorrido."""

    def post(self, request, registro_id):
        datos = leer(PuntosEntrada, request.data)
        nuevos = servicios.agregar_puntos(request.user, registro_id, datos["puntos"])
        return Response({"guardados": nuevos}, status=status.HTTP_201_CREATED)


class TerminarRegistroVista(APIView):
    """HU-18. POST /api/registros/<id>/terminar"""

    def post(self, request, registro_id):
        resumen = servicios.terminar_registro(request.user, registro_id)
        return Response({"resumen": resumen})


class CancelarRegistroVista(APIView):
    """HU-18. POST /api/registros/<id>/cancelar"""

    def post(self, request, registro_id):
        servicios.cancelar_registro(request.user, registro_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PropuestasParadaVista(APIView):
    """HU-08. POST /api/rutas/<id>/paradas: propone una parada sobre el recorrido."""

    def post(self, request, ruta_id):
        datos = leer(PropuestaParadaEntrada, request.data)
        parada = servicios.proponer_parada(
            request.user,
            ruta_id,
            datos.get("nombre", ""),
            datos["latitud"],
            datos["longitud"],
        )
        return Response({"parada": parada_a_dict(parada)}, status=status.HTTP_201_CREATED)


class AprobarParadaVista(APIView):
    """HU-08. POST /api/paradas/<id>/aprobar"""

    def post(self, request, parada_id):
        parada = servicios.aprobar_parada(request.user, parada_id)
        return Response({"parada": parada_a_dict(parada)})


class RechazarParadaVista(APIView):
    """HU-08. POST /api/paradas/<id>/rechazar"""

    def post(self, request, parada_id):
        parada = servicios.rechazar_parada(request.user, parada_id)
        return Response({"parada": parada_a_dict(parada)})
