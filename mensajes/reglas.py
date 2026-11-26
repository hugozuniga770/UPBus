"""Reglas puras de los chats: deciden, pero no consultan la base."""
from comun.rechazos import Rechazo, SinPermiso


RESPUESTAS_RAPIDAS = ("Ya llego", "Te espero 1 min", "Sube por favor")


def verificar_texto(texto):
    if not texto or not texto.strip():
        raise Rechazo("el mensaje no puede estar vacío")


def verificar_confirmado(aviso):
    if aviso is None or aviso.estado != "confirmado":
        raise Rechazo("no estás en este viaje")


def verificar_chofer_del_viaje(viaje, usuario):
    if viaje.chofer_id != usuario.pk:
        raise SinPermiso("este viaje no es tuyo")


def verificar_respuesta_rapida(respuesta):
    if respuesta not in RESPUESTAS_RAPIDAS:
        raise Rechazo("elige una respuesta rápida válida")


def verificar_mismo_reenvio(mensaje, usuario, viaje=None, estudiante=None, ruta=None):
    coincide = (
        mensaje.autor_id == usuario.pk
        and mensaje.viaje_id == getattr(viaje, "pk", None)
        and mensaje.estudiante_id == getattr(estudiante, "pk", None)
        and mensaje.ruta_id == getattr(ruta, "pk", None)
    )
    if not coincide:
        raise Rechazo("identificador de mensaje ya usado")


def verificar_puede_elegir_ruta(usuario):
    if not usuario.puede_actuar_como_estudiante:
        raise SinPermiso("solo un estudiante puede elegir una ruta")


def verificar_es_miembro_de_la_ruta(es_miembro, es_chofer_de_la_ruta, usuario):
    if not (es_miembro or es_chofer_de_la_ruta or usuario.es_administrador):
        raise Rechazo("no eres parte de esta ruta")
