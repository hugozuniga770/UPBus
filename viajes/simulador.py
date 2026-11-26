"""Simulador de escenarios (T23).

Mueve un bus por el recorrido grabado de una ruta llamando a los **mismos servicios
que la app** (`iniciar_viaje`, `registrar_posicion`, `avisar_que_va_a_subir`…): un
escenario solo funciona si las reglas funcionan. Lo usan el comando `simular` y el
panel de demo del administrador.

Los viajes simulados quedan marcados (`Viaje.simulado`) y no enseñan horas: sus pasos
por las paradas no cambian la hora aproximada (C-27).
"""
import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import timedelta
from itertools import count
from math import ceil

from asgiref.sync import SyncToAsync, sync_to_async
from django.db import connections, transaction

from comun.geo import distancia_en_metros
from comun.rechazos import NoExiste, Rechazo
from comun.tiempo import a_hora_local, ahora as ahora_local
from cuentas import reglas as reglas_de_cuentas
from cuentas.models import Usuario
from rutas.models import Parada, Ruta
from rutas.reglas import RADIO_DE_LLEGADA_M

from . import reglas, servicios
from .models import AvisoDeSubida, Viaje

registro = logging.getLogger(__name__)

VELOCIDAD_DEL_BUS_M_S = 7.0  # unos 25 km/h en la ciudad
PASO_M = 25  # distancia entre dos posiciones enviadas
ESPERA_EN_PARADA_S = 30  # el bus se detiene a que suban
COMPARTE_CADA_S = 15  # como la pantalla «Voy a subir»
LEJOS_DE_LA_RUTA_M = 200  # una parada más lejos que esto no está sobre el recorrido

ESCENARIOS = {
    "recorrido": "El bus recorre la ruta de punta a punta.",
    "no_se_presenta": (
        "Un estudiante avisa «Voy a subir», comparte su ubicación y no sube: "
        "cuando el bus llega a la parada siguiente queda «no se presentó»."
    ),
}

CHOFER_DE_LA_SIMULACION = ("chofer.simulado@upbus.example", "Chofer de la simulación")
ESTUDIANTE_DE_LA_SIMULACION = ("estudiante.simulado@upbus.example", "Estudiante de la simulación")


# ---- Relojes ----

class RelojAcelerado:
    """El tiempo simulado corre `velocidad` veces más rápido que el real."""

    def __init__(self, velocidad):
        self.velocidad = velocidad

    def ahora(self):
        return ahora_local()

    def esperar(self, segundos, detener=None):
        espera = max(segundos, 0) / self.velocidad
        if detener is not None:
            detener.wait(espera)
        else:
            time.sleep(espera)


class RelojSinEsperas:
    """Avanza el tiempo simulado sin esperar: para las pruebas y para preparar datos."""

    def __init__(self, inicio=None):
        self.momento = inicio or ahora_local()

    def ahora(self):
        return self.momento

    def esperar(self, segundos, detener=None):
        self.momento += timedelta(seconds=max(segundos, 0))


def crear_reloj(velocidad):
    return RelojAcelerado(velocidad)


# ---- Trayecto ----

@dataclass(frozen=True)
class Punto:
    latitud: float
    longitud: float
    segundos: float  # desde la salida, en tiempo simulado
    parada: str | None = None  # el bus está detenido en esta parada

    @property
    def punto(self):
        return (self.latitud, self.longitud)


def _densificar(recorrido, paso_m):
    puntos = [tuple(recorrido[0])]
    for a, b in zip(recorrido, recorrido[1:]):
        partes = max(1, ceil(distancia_en_metros(a, b) / paso_m))
        for i in range(1, partes + 1):
            f = i / partes
            puntos.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    return puntos


def _donde_para(puntos, parada, desde):
    """El punto del recorrido donde el bus para, buscando hacia adelante desde `desde`.

    Es el primer acercamiento a menos de 50 m; si nunca pasa tan cerca, el punto más
    cercano, siempre que esté a menos de 200 m. Si no, `None`.
    """
    distancias = [distancia_en_metros(p, parada.punto) for p in puntos[desde:]]
    if not distancias:
        return None
    cerca = next((i for i, d in enumerate(distancias) if d < RADIO_DE_LLEGADA_M), None)
    if cerca is None:
        cerca = min(range(len(distancias)), key=distancias.__getitem__)
        if distancias[cerca] > LEJOS_DE_LA_RUTA_M:
            return None
    while cerca + 1 < len(distancias) and distancias[cerca + 1] < distancias[cerca]:
        cerca += 1
    return desde + cerca


def _completar_puntas(recorrido, paradas):
    """Si el recorrido grabado empieza después de la primera parada o termina antes de la
    última, el bus va en línea recta entre esa parada y el recorrido.

    Pasa con REG-01: los puntos del recorrido empiezan en Parque Urbano, no en Makro Parque.
    """
    recorrido = [tuple(p) for p in recorrido]
    if not paradas:
        return recorrido

    def lejos(parada):
        return min(distancia_en_metros(p, parada.punto) for p in recorrido) > LEJOS_DE_LA_RUTA_M

    primera, ultima = paradas[0], paradas[-1]
    if lejos(primera):
        recorrido.insert(0, primera.punto)
    if ultima is not primera and lejos(ultima):
        recorrido.append(ultima.punto)
    return recorrido


def trayecto(recorrido, paradas, paso_m=PASO_M):
    """Posiciones cada `paso_m` metros por el recorrido, con el tiempo de cada una.

    En cada parada (en su orden) el bus se detiene `ESPERA_EN_PARADA_S` segundos sobre
    la parada misma, para que el servidor registre que pasó por ella.
    """
    puntos = _densificar(_completar_puntas(recorrido, paradas), paso_m)
    paradas_en = {}
    desde = 0
    for parada in paradas:
        indice = _donde_para(puntos, parada, desde)
        if indice is not None and indice not in paradas_en:
            paradas_en[indice] = parada
            desde = indice
    resultado, segundos = [], 0.0
    for i, punto in enumerate(puntos):
        if i:
            segundos += distancia_en_metros(puntos[i - 1], punto) / VELOCIDAD_DEL_BUS_M_S
        resultado.append(Punto(punto[0], punto[1], segundos))
        parada = paradas_en.get(i)
        if parada is not None:
            llegada = segundos + distancia_en_metros(punto, parada.punto) / VELOCIDAD_DEL_BUS_M_S
            resultado.append(Punto(parada.latitud, parada.longitud, llegada, parada.nombre))
            segundos = llegada + ESPERA_EN_PARADA_S
            resultado.append(Punto(parada.latitud, parada.longitud, segundos, parada.nombre))
    return resultado


# ---- Escenarios ----

def _cuenta_de_la_simulacion(correo, nombre, rol):
    """Cuenta de demo que no puede iniciar sesión."""
    cuenta, creada = Usuario.objects.get_or_create(correo=correo, defaults={"nombre": nombre, "rol": rol})
    if creada:
        cuenta.set_unusable_password()
        cuenta.save(update_fields=["password"])
    return cuenta


def _buscar_ruta(ruta):
    if isinstance(ruta, Ruta):
        return ruta
    filtro = {"pk": int(ruta)} if str(ruta).isdigit() else {"clave": ruta}
    encontrada = Ruta.objects.filter(**filtro).first()
    if encontrada is None:
        raise NoExiste("la ruta no existe")
    return encontrada


def _elegir_horario(ruta, salida=None):
    horarios = ruta.horarios.order_by("sentido", "salida")  # «ingreso» va antes que «salida»
    if salida:
        horarios = horarios.filter(salida=salida)
    horario = horarios.first()
    if horario is None:
        raise Rechazo("la ruta no tiene ese horario" if salida else "la ruta no tiene horarios")
    return horario


def _parada_del_estudiante(paradas, elegida=None):
    """Por defecto, la segunda parada: así hay una antes y otra después."""
    reglas.verificar_hay_paradas(paradas)
    if elegida in (None, ""):
        return paradas[1] if len(paradas) >= 3 else paradas[0]
    for parada in paradas:
        if str(parada.pk) == str(elegida) or parada.nombre.lower() == str(elegida).lower():
            return parada
    raise Rechazo("esa parada no es de esta ruta")


def preparar(escenario, ruta, horario=None, parada=None):
    """Valida todo lo que se puede validar antes de mover el bus."""
    reglas.verificar_escenario(escenario, ESCENARIOS)
    ruta = _buscar_ruta(ruta)
    reglas.verificar_recorrido(ruta.recorrido)
    paradas = list(ruta.paradas.filter(estado=Parada.Estado.APROBADA).order_by("orden", "id"))
    espera_en = _parada_del_estudiante(paradas, parada) if escenario == "no_se_presenta" else None
    return ruta, _elegir_horario(ruta, horario), paradas, espera_en


def _iniciar_viaje_simulado(ruta, horario, chofer, momento):
    """Termina lo que haya quedado de una simulación anterior y arranca un viaje nuevo."""
    for anterior in Viaje.objects.filter(chofer=chofer, estado=Viaje.Estado.EN_CURSO, simulado=True):
        servicios.terminar_viaje(chofer, anterior.pk, ahora=momento)
    with transaction.atomic():
        viaje = Viaje.objects.create(
            ruta=ruta, horario=horario, fecha=a_hora_local(momento).date(), chofer=chofer, simulado=True
        )
        return servicios.iniciar_viaje(chofer, viaje.pk, ahora=momento)


def correr(escenario, ruta, *, reloj, horario=None, parada=None, detener=None, anotar=None, al_iniciar=None):
    """Corre un escenario de punta a punta y devuelve un resumen."""
    ruta, horario, paradas, espera_en = preparar(escenario, ruta, horario, parada)
    chofer = _cuenta_de_la_simulacion(*CHOFER_DE_LA_SIMULACION, Usuario.Rol.CHOFER)
    notas = []

    def nota(texto):
        notas.append(texto)
        if anotar is not None:
            anotar(texto)

    viaje = _iniciar_viaje_simulado(ruta, horario, chofer, reloj.ahora())
    if al_iniciar is not None:
        al_iniciar(viaje)
    nota(f"Viaje simulado {viaje.pk}: {ruta.nombre}, {horario.sentido} de las {horario.salida:%H:%M}")

    aviso = estudiante = None
    if espera_en is not None:
        estudiante = _cuenta_de_la_simulacion(*ESTUDIANTE_DE_LA_SIMULACION, Usuario.Rol.ESTUDIANTE)
        aviso = servicios.avisar_que_va_a_subir(estudiante, viaje.pk, espera_en.pk)
        nota(f"{estudiante.nombre} va a subir en {espera_en.nombre}")
        donde_espera = (espera_en.latitud + 10 / 111_320, espera_en.longitud)  # a 10 m de la parada

    enviadas = compartidas = 0
    detenida = False
    compartida_en = ultima_parada = None
    anterior = 0.0
    for numero, punto in enumerate(trayecto(ruta.recorrido, paradas)):
        if detener is not None and detener.is_set():
            detenida = True
            break
        reloj.esperar(punto.segundos - anterior, detener)
        anterior = punto.segundos
        if detener is not None and detener.is_set():
            detenida = True
            break
        momento = reloj.ahora()
        if aviso is not None and (compartida_en is None or punto.segundos - compartida_en >= COMPARTE_CADA_S):
            aviso.refresh_from_db(fields=["estado"])
            if aviso.estado == AvisoDeSubida.Estado.CONFIRMADO:
                servicios.compartir_ubicacion(estudiante, aviso.pk, *donde_espera, momento)
                compartidas += 1
                compartida_en = punto.segundos
            else:
                nota(f"{estudiante.nombre}: {aviso.get_estado_display().lower()}")
                aviso = None
        servicios.registrar_posicion(chofer, viaje.pk, f"simulador-{viaje.pk}-{numero}", punto.latitud, punto.longitud, momento)
        enviadas += 1
        if punto.parada and punto.parada != ultima_parada:
            ultima_parada = punto.parada
            nota(f"El bus está en {punto.parada}")

    viaje.refresh_from_db(fields=["estado"])
    if viaje.estado == Viaje.Estado.EN_CURSO:
        servicios.terminar_viaje(chofer, viaje.pk, ahora=reloj.ahora())
    if aviso is not None:
        aviso.refresh_from_db(fields=["estado"])
        nota(f"{estudiante.nombre}: {aviso.get_estado_display().lower()}, al terminar el viaje")
    nota(("Simulación detenida" if detenida else "Viaje terminado") + f": {enviadas} posiciones enviadas")
    return {
        "viaje": viaje.pk,
        "posiciones": enviadas,
        "ubicaciones_compartidas": compartidas,
        "detenida": detenida,
        "notas": notas,
    }


# ---- Panel de demo: una simulación a la vez, en un hilo del servidor ----

@dataclass
class Simulacion:
    id: int
    escenario: str
    ruta: str
    velocidad: float
    iniciada_en: object
    estado: str = "en_curso"  # en_curso, terminada, detenida o fallo
    viaje: int | None = None
    notas: list = field(default_factory=list)
    detener: threading.Event = field(default_factory=threading.Event, repr=False)


SIMULACIONES = {}
_numeros = count(1)
_candado = threading.Lock()
NOTAS_QUE_SE_GUARDAN = 12


def _en_un_hilo(tarea):
    """Corre la simulación en un hilo aparte, sin trabar el servidor.

    Bajo Daphne, el hilo se lanza desde el bucle de eventos del servidor con
    `sync_to_async`: así lo que los servicios mandan por WebSocket sale por ese mismo
    bucle, donde vive la capa de Channels en memoria, y las pantallas ven el bus en vivo.
    """
    def con_conexion_propia():
        try:
            tarea()
        finally:
            connections.close_all()

    bucle = getattr(SyncToAsync.threadlocal, "main_event_loop", None)
    if bucle is not None and bucle.is_running():
        def programar():
            bucle.create_task(sync_to_async(con_conexion_propia, thread_sensitive=False)())

        bucle.call_soon_threadsafe(programar)
    else:
        threading.Thread(target=con_conexion_propia, daemon=True, name="simulador").start()


def _anotar_en(simulacion):
    def anotar(texto):
        simulacion.notas.append(texto)
        del simulacion.notas[:-NOTAS_QUE_SE_GUARDAN]
    return anotar


def _correr_en_el_panel(simulacion, ruta, parada):
    try:
        resumen = correr(
            simulacion.escenario, ruta, reloj=crear_reloj(simulacion.velocidad), parada=parada,
            detener=simulacion.detener, anotar=_anotar_en(simulacion),
            al_iniciar=lambda viaje: setattr(simulacion, "viaje", viaje.pk),
        )
        simulacion.estado = "detenida" if resumen["detenida"] else "terminada"
    except Rechazo as falla:
        simulacion.estado = "fallo"
        _anotar_en(simulacion)(falla.causa)
    except Exception:  # un hilo que falla en silencio dejaría el panel colgado
        registro.exception("La simulación %s falló", simulacion.id)
        simulacion.estado = "fallo"
        _anotar_en(simulacion)("error inesperado: revisa el registro del servidor")


def panel(usuario):
    reglas_de_cuentas.verificar_es_administrador(usuario)
    return list(ESCENARIOS.items()), sorted(SIMULACIONES.values(), key=lambda s: s.id, reverse=True)


def iniciar_simulacion(usuario, escenario, ruta, velocidad=10, parada=None):
    reglas_de_cuentas.verificar_es_administrador(usuario)
    reglas.verificar_velocidad(velocidad)
    ruta, _, _, _ = preparar(escenario, ruta, parada=parada)
    with _candado:
        reglas.verificar_sin_simulacion_en_curso(
            any(s.estado == "en_curso" and not s.detener.is_set() for s in SIMULACIONES.values())
        )
        simulacion = Simulacion(next(_numeros), escenario, ruta.nombre, velocidad, ahora_local())
        SIMULACIONES[simulacion.id] = simulacion
    _en_un_hilo(lambda: _correr_en_el_panel(simulacion, ruta.pk, parada))
    return simulacion


def detener_simulacion(usuario, simulacion_id):
    reglas_de_cuentas.verificar_es_administrador(usuario)
    simulacion = SIMULACIONES.get(simulacion_id)
    if simulacion is None:
        raise NoExiste("la simulación no existe")
    simulacion.detener.set()
    return simulacion
