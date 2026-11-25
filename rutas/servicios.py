"""Servicios de rutas y del modo registro: leen, preguntan a las reglas y guardan."""
from collections import defaultdict

from django.db import transaction
from django.utils.dateparse import parse_datetime

from comun.rechazos import NoExiste, Rechazo
from comun.tiempo import ZONA_HORARIA, ahora as ahora_local

from . import reglas
from .models import (
    Horario,
    MarcaDeParada,
    Parada,
    PasoPorParada,
    PuntoDeRegistro,
    RegistroDeRecorrido,
    Ruta,
)


# ---- HU-04: ver rutas, paradas y horarios (BUS-RF-05) ----

def listar_rutas():
    return Ruta.objects.filter(activa=True).prefetch_related("horarios")


def buscar_ruta(ruta_id):
    ruta = Ruta.objects.filter(pk=ruta_id).prefetch_related("horarios").first()
    if ruta is None:
        raise NoExiste("la ruta no existe")
    return ruta


def buscar_horario(horario_id):
    if horario_id in (None, ""):
        return None
    horario = Horario.objects.filter(pk=horario_id).first()
    if horario is None:
        raise NoExiste("el horario no existe")
    return horario


def paradas_visibles(ruta, usuario):
    """Las aprobadas para todos; las propuestas también para choferes y administradores."""
    paradas = ruta.paradas.exclude(estado=Parada.Estado.RECHAZADA)
    if getattr(usuario, "rol", None) not in ("chofer", "administrador"):
        paradas = paradas.filter(estado=Parada.Estado.APROBADA)
    return list(paradas.order_by("orden", "id"))


def minutos_aprendidos(parada, horario):
    """Promedio de los últimos pasos (RF-11). Primero los del mismo horario;
    si no hay, los del mismo sentido."""
    pasos = PasoPorParada.objects.filter(parada=parada)
    del_horario = pasos.filter(horario=horario).values_list("minutos_desde_salida", flat=True)
    promedio = reglas.promedio_de_los_ultimos(del_horario)
    if promedio is None:
        del_sentido = pasos.filter(horario__sentido=horario.sentido).values_list(
            "minutos_desde_salida", flat=True
        )
        promedio = reglas.promedio_de_los_ultimos(del_sentido)
    return promedio


def horas_aproximadas(paradas, horario):
    if horario is None:
        return {parada.pk: None for parada in paradas}
    return {
        parada.pk: reglas.hora_aproximada(horario.salida, minutos_aprendidos(parada, horario))
        for parada in paradas
    }


def ver_ruta(ruta_id, horario_id, usuario):
    """La ruta con sus paradas en orden y la hora aproximada de cada una."""
    ruta = buscar_ruta(ruta_id)
    horario = buscar_horario(horario_id) or ruta.horarios.order_by("sentido", "salida").first()
    reglas.verificar_horario_de_la_ruta(horario, ruta)
    paradas = paradas_visibles(ruta, usuario)
    return ruta, horario, paradas, horas_aproximadas(paradas, horario)


# ---- Pasos por las paradas (RF-11), compartido con los viajes de HU-06 ----

def registrar_paso(parada, horario, minutos_desde_salida, ocurrido_en, registro=None):
    return PasoPorParada.objects.create(
        parada=parada,
        horario=horario,
        registro=registro,
        minutos_desde_salida=minutos_desde_salida,
        ocurrido_en=ocurrido_en,
    )


def reordenar_paradas(ruta):
    """El orden de las paradas sale de los minutos aprendidos en el sentido de ingreso."""
    paradas = list(ruta.paradas.exclude(estado=Parada.Estado.RECHAZADA))
    pasos = PasoPorParada.objects.filter(parada__ruta=ruta)
    if pasos.filter(horario__sentido=Horario.Sentido.INGRESO).exists():
        pasos = pasos.filter(horario__sentido=Horario.Sentido.INGRESO)
    minutos = defaultdict(list)
    for parada_id, valor in pasos.values_list("parada_id", "minutos_desde_salida"):
        minutos[parada_id].append(valor)

    def clave(parada):
        valores = minutos.get(parada.pk)
        promedio = sum(valores) / len(valores) if valores else None
        return (promedio is None, promedio or 0, parada.orden, parada.pk)

    for posicion, parada in enumerate(sorted(paradas, key=clave), start=1):
        parada.orden = posicion
    Parada.objects.bulk_update(paradas, ["orden"])


# ---- HU-18: modo registro (BUS-RF-23) ----

def buscar_registro(registro_id):
    registro = RegistroDeRecorrido.objects.select_related("ruta", "horario").filter(pk=registro_id).first()
    if registro is None:
        raise NoExiste("el registro no existe")
    return registro


def registro_en_curso_de(usuario):
    return RegistroDeRecorrido.objects.filter(
        usuario=usuario, estado=RegistroDeRecorrido.Estado.EN_CURSO
    ).first()


@transaction.atomic
def iniciar_registro(usuario, ruta_id, horario_id=None, id_cliente=None, ahora=None):
    reglas.verificar_puede_registrar(usuario)
    ruta = buscar_ruta(ruta_id)
    horario = buscar_horario(horario_id)
    reglas.verificar_horario_de_la_ruta(horario, ruta)
    if id_cliente:
        existente = RegistroDeRecorrido.objects.filter(id_cliente=id_cliente).first()
        if existente is not None:  # reenvío del mismo inicio
            reglas.verificar_es_su_registro(existente, usuario)
            return existente
    reglas.verificar_sin_registro_en_curso(registro_en_curso_de(usuario) is not None)
    return RegistroDeRecorrido.objects.create(
        id_cliente=id_cliente or None,
        ruta=ruta,
        horario=horario,
        usuario=usuario,
        iniciado_en=ahora or ahora_local(),
    )


def _registro_abierto_de(usuario, registro_id):
    registro = buscar_registro(registro_id)
    reglas.verificar_es_su_registro(registro, usuario)
    reglas.verificar_registro_en_curso(registro)
    return registro


@transaction.atomic
def marcar_parada(usuario, registro_id, id_cliente, latitud, longitud, marcada_en,
                  nombre="", precision_m=None):
    """«Parada aquí». Un reenvío con el mismo `id_cliente` no duplica."""
    registro = buscar_registro(registro_id)
    reglas.verificar_es_su_registro(registro, usuario)
    repetida = registro.marcas.filter(id_cliente=id_cliente).first()
    if repetida is not None:
        return repetida
    reglas.verificar_registro_en_curso(registro)
    reglas.verificar_coordenadas(latitud, longitud)
    reglas.verificar_lejos_de_las_otras_marcas((latitud, longitud), registro.marcas.all())
    return MarcaDeParada.objects.create(
        registro=registro,
        id_cliente=id_cliente,
        nombre=(nombre or "").strip(),
        latitud=latitud,
        longitud=longitud,
        precision_m=precision_m,
        marcada_en=marcada_en,
    )


@transaction.atomic
def agregar_puntos(usuario, registro_id, puntos):
    """Posiciones del recorrido. Las repetidas se ignoran."""
    registro = _registro_abierto_de(usuario, registro_id)
    ya_guardados = set(registro.puntos.values_list("id_cliente", flat=True))
    nuevos = []
    for punto in puntos:
        if punto["id_cliente"] in ya_guardados:
            continue
        reglas.verificar_coordenadas(punto["latitud"], punto["longitud"])
        ya_guardados.add(punto["id_cliente"])
        nuevos.append(PuntoDeRegistro(registro=registro, **punto))
    PuntoDeRegistro.objects.bulk_create(nuevos)
    return len(nuevos)


@transaction.atomic
def terminar_registro(usuario, registro_id, ahora=None):
    """Une cada marca a una parada (o crea una) y guarda sus pasos.

    Los minutos de cada parada se cuentan desde la salida programada del
    horario (C-23); sin horario, desde la primera marca.
    """
    registro = _registro_abierto_de(usuario, registro_id)
    marcas = list(registro.marcas.order_by("marcada_en", "id"))
    reglas.verificar_hay_marcas(len(marcas))
    ruta = registro.ruta
    salida = marcas[0].marcada_en
    if registro.horario is not None:
        salida = reglas.salida_programada(registro.horario.salida, salida)
    paradas = list(ruta.paradas.exclude(estado=Parada.Estado.RECHAZADA))
    nuevas, existentes, usadas = 0, 0, set()

    for marca in marcas:
        parada = reglas.parada_mas_cercana(marca.punto, paradas)
        if parada is None:
            parada = Parada.objects.create(
                ruta=ruta,
                nombre=marca.nombre or f"Parada {len(paradas) + 1}",
                latitud=marca.latitud,
                longitud=marca.longitud,
                orden=len(paradas) + 1,
                estado=reglas.estado_de_una_parada_nueva(usuario),
                creada_por=usuario,
            )
            paradas.append(parada)
            nuevas += 1
        else:
            existentes += 1
        marca.parada = parada
        marca.minutos_desde_salida = reglas.minutos_entre(salida, marca.marcada_en)
        marca.save(update_fields=["parada", "minutos_desde_salida"])
        if parada.pk not in usadas:  # un solo paso por parada en cada registro
            usadas.add(parada.pk)
            registrar_paso(parada, registro.horario, marca.minutos_desde_salida,
                           marca.marcada_en, registro)

    if not ruta.recorrido:
        puntos = list(registro.puntos.order_by("tomado_en").values_list("latitud", "longitud"))
        if len(puntos) >= 2:
            ruta.recorrido = [[lat, lng] for lat, lng in puntos]
            ruta.save(update_fields=["recorrido"])

    reordenar_paradas(ruta)
    registro.estado = RegistroDeRecorrido.Estado.TERMINADO
    registro.terminado_en = ahora or ahora_local()
    registro.save(update_fields=["estado", "terminado_en"])
    return {"marcas": len(marcas), "paradas_nuevas": nuevas, "paradas_existentes": existentes}


@transaction.atomic
def cancelar_registro(usuario, registro_id):
    registro = _registro_abierto_de(usuario, registro_id)
    registro.estado = RegistroDeRecorrido.Estado.CANCELADO
    registro.save(update_fields=["estado"])
    return registro


# ---- Importar un respaldo del celular (comando importar_registro) ----

def _momento(texto):
    momento = parse_datetime(texto)
    if momento is None:
        raise Rechazo(f"fecha no válida en el respaldo: {texto}")
    if momento.tzinfo is None:
        momento = momento.replace(tzinfo=ZONA_HORARIA)
    return momento


@transaction.atomic
def importar_registro(usuario, datos):
    """Carga un respaldo descargado del modo registro y lo termina."""
    if datos.get("formato") != "upbus-registro":
        raise Rechazo("el archivo no es un respaldo del modo registro")
    existente = RegistroDeRecorrido.objects.filter(id_cliente=datos["id_cliente"]).first()
    if existente is not None and existente.estado == RegistroDeRecorrido.Estado.TERMINADO:
        raise Rechazo("ese registro ya fue importado")
    ruta = Ruta.objects.filter(clave=datos["ruta"]["clave"]).first()
    if ruta is None:
        raise NoExiste(f"no existe la ruta {datos['ruta']['clave']}; corre cargar_rutas")
    horario = None
    if datos.get("horario"):
        horario = Horario.objects.filter(
            ruta=ruta, sentido=datos["horario"]["sentido"], salida=datos["horario"]["salida"]
        ).first()
    registro = existente or RegistroDeRecorrido.objects.create(
        id_cliente=datos["id_cliente"],
        ruta=ruta,
        horario=horario,
        usuario=usuario,
        iniciado_en=_momento(datos["iniciado_en"]),
    )
    omitidas = []
    for marca in datos.get("marcas", []):
        try:
            marcar_parada(
                usuario, registro.pk, marca["id_cliente"], marca["latitud"], marca["longitud"],
                _momento(marca["marcada_en"]), marca.get("nombre", ""), marca.get("precision_m"),
            )
        except Rechazo as rechazo:
            omitidas.append(f"{marca.get('nombre') or marca['id_cliente']}: {rechazo.causa}")
    agregar_puntos(usuario, registro.pk, [
        {
            "id_cliente": punto["id_cliente"],
            "latitud": punto["latitud"],
            "longitud": punto["longitud"],
            "precision_m": punto.get("precision_m"),
            "tomado_en": _momento(punto["tomado_en"]),
        }
        for punto in datos.get("puntos", [])
    ])
    resumen = terminar_registro(usuario, registro.pk)
    resumen["marcas_omitidas"] = omitidas
    return resumen
