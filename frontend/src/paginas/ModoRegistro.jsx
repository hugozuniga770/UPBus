import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Circle, CircleMarker, Polyline, Tooltip, useMapEvents } from "react-leaflet";

import { api } from "../api/cliente.js";
import Aviso from "../componentes/Aviso.jsx";
import Boton from "../componentes/Boton.jsx";
import Mapa from "../componentes/Mapa.jsx";
import { almacen } from "../registro/almacen.js";
import { crearCola, crearId } from "../registro/cola.js";
import { RADIO_DE_LLEGADA_M, distanciaEnMetros } from "../registro/geo.js";
import { armarRespaldo, descargarRespaldo } from "../registro/respaldo.js";

const cola = crearCola();
const SEGUNDOS_ENTRE_PUNTOS = 15;
const METROS_ENTRE_PUNTOS = 40;
const PRECISION_MAXIMA_PARA_PUNTOS_M = 100;
const ANTIGUEDAD_MAXIMA_DE_LA_POSICION_MS = 30_000;
const SENTIDO = { ingreso: "Ingreso", salida: "Salida" };

const horaCorta = (iso) => new Date(iso).toLocaleTimeString("es-BO", { hour: "2-digit", minute: "2-digit" });

function colorDePrecision(metros) {
  if (metros == null) return "text-suave";
  if (metros <= 20) return "text-[#1d7a3a]";
  if (metros <= 50) return "text-[#a15c00]";
  return "text-[#b42318]";
}

function DejarDeSeguirAlArrastrar({ alArrastrar }) {
  useMapEvents({ dragstart: alArrastrar });
  return null;
}

/**
 * HU-18 · Modo registro (BUS-RF-23).
 *
 * Un chofer o un administrador recorre la ruta y toca «Parada aquí» en cada
 * parada. Todo se guarda primero en el celular: si se corta la señal, se envía
 * cuando vuelve, y siempre se puede descargar un respaldo.
 */
export default function ModoRegistro() {
  const [rutas, setRutas] = useState([]);
  const [rutaId, setRutaId] = useState("");
  const [horarioId, setHorarioId] = useState("");
  const [estado, setEstado] = useState(() => almacen.leerEstado());
  const [posicion, setPosicion] = useState(null);
  const [errorGps, setErrorGps] = useState("");
  const [nombre, setNombre] = useState("");
  const [mensaje, setMensaje] = useState(null);
  const [pendientes, setPendientes] = useState(() => cola.pendientes());
  const [confirmarFin, setConfirmarFin] = useState(false);
  const [resumen, setResumen] = useState(null);
  const [enCursoEnServidor, setEnCursoEnServidor] = useState(null);
  const [seguir, setSeguir] = useState(true);
  const ultimoPunto = useRef(null);
  const puntosSinEncolar = useRef([]);

  const registro = estado?.registro ?? null;
  const marcasValidas = estado?.marcas.filter((m) => m.estado !== "rechazada") ?? [];

  // El registro en curso vive en el celular: si se recarga la página, sigue.
  useEffect(() => {
    if (estado) almacen.guardarEstado(estado);
    else almacen.borrarEstado();
  }, [estado]);

  useEffect(() => {
    api
      .rutas()
      .then(({ rutas: lista }) => {
        setRutas(lista);
        const norte = lista.find((r) => r.clave === "norte") ?? lista[0];
        if (norte) {
          setRutaId(String(norte.id));
          setHorarioId(String(norte.horarios[0]?.id ?? ""));
        }
      })
      .catch((falla) => setMensaje({ tipo: "error", texto: falla.causa }));
    if (!almacen.leerEstado()) {
      api.registroEnCurso().then(({ registro: r }) => setEnCursoEnServidor(r)).catch(() => {});
    }
  }, []);

  // GPS del dispositivo.
  useEffect(() => {
    if (!("geolocation" in navigator)) {
      setErrorGps("Este navegador no da la ubicación.");
      return undefined;
    }
    if (!window.isSecureContext) {
      setErrorGps("El GPS solo funciona con https o en localhost. Abre la página con el enlace del túnel.");
    }
    const id = navigator.geolocation.watchPosition(
      (p) => {
        setErrorGps("");
        setPosicion({
          latitud: p.coords.latitude,
          longitud: p.coords.longitude,
          precision_m: Math.round(p.coords.accuracy),
          tomado_en: new Date(p.timestamp).toISOString(),
          recibidaMs: Date.now(),
        });
      },
      (falla) =>
        setErrorGps(
          falla.code === 1
            ? "No hay permiso de ubicación. Actívalo en el candado de la barra de direcciones."
            : "No se pudo leer el GPS. Busca un lugar abierto.",
        ),
      { enableHighAccuracy: true, maximumAge: 5000, timeout: 20000 },
    );
    return () => navigator.geolocation.clearWatch(id);
  }, []);

  // Pantalla siempre encendida mientras se registra (si el navegador lo permite).
  const registroId = registro?.id;
  useEffect(() => {
    if (!registroId || !("wakeLock" in navigator)) return undefined;
    let candado = null;
    let activo = true;
    const pedir = async () => {
      try {
        candado = await navigator.wakeLock.request("screen");
      } catch {
        // Sin permiso: el chofer deja la pantalla encendida a mano.
      }
    };
    const alVolver = () => activo && document.visibilityState === "visible" && pedir();
    pedir();
    document.addEventListener("visibilitychange", alVolver);
    return () => {
      activo = false;
      document.removeEventListener("visibilitychange", alVolver);
      candado?.release().catch(() => {});
    };
  }, [registroId]);

  // Puntos del recorrido: uno cada 15 s o cada 40 m, si el GPS es preciso.
  useEffect(() => {
    if (!registroId || !posicion || posicion.precision_m > PRECISION_MAXIMA_PARA_PUNTOS_M) return;
    const anterior = ultimoPunto.current;
    if (anterior) {
      const segundos = (Date.parse(posicion.tomado_en) - Date.parse(anterior.tomado_en)) / 1000;
      const metros = distanciaEnMetros([anterior.latitud, anterior.longitud], [posicion.latitud, posicion.longitud]);
      if (segundos < 5 || (segundos < SEGUNDOS_ENTRE_PUNTOS && metros < METROS_ENTRE_PUNTOS)) return;
    }
    const punto = {
      id_cliente: crearId(),
      latitud: posicion.latitud,
      longitud: posicion.longitud,
      precision_m: posicion.precision_m,
      tomado_en: posicion.tomado_en,
    };
    ultimoPunto.current = punto;
    puntosSinEncolar.current.push(punto);
    setEstado((e) => (e ? { ...e, puntos: [...e.puntos, punto] } : e));
  }, [posicion, registroId]);

  const encolarPuntos = useCallback(() => {
    if (!registroId || puntosSinEncolar.current.length === 0) return;
    const puntos = puntosSinEncolar.current;
    puntosSinEncolar.current = [];
    cola.agregar({ id: crearId(), tipo: "puntos", registroId, datos: puntos });
  }, [registroId]);

  const sincronizar = useCallback(async () => {
    encolarPuntos();
    const resultado = await cola.enviar(async (elemento) => {
      if (elemento.tipo === "marca") {
        await api.marcar(elemento.registroId, elemento.datos);
        setEstado((e) =>
          e ? { ...e, marcas: e.marcas.map((m) => (m.id_cliente === elemento.id ? { ...m, estado: "guardada" } : m)) } : e,
        );
      } else if (elemento.tipo === "puntos") {
        await api.enviarPuntos(elemento.registroId, elemento.datos);
      } else if (elemento.tipo === "terminar") {
        const respuesta = await api.terminarRegistro(elemento.registroId);
        setResumen(respuesta.resumen);
        setEstado((e) => {
          if (e) almacen.guardarUltimo(e);
          return null;
        });
        ultimoPunto.current = null;
      }
    });
    if (resultado.ocupada) return;
    setPendientes(resultado.pendientes);
    for (const { elemento, causa } of resultado.rechazados) {
      if (elemento.tipo === "marca") {
        setEstado((e) =>
          e ? { ...e, marcas: e.marcas.map((m) => (m.id_cliente === elemento.id ? { ...m, estado: "rechazada", causa } : m)) } : e,
        );
        setMensaje({ tipo: "error", texto: causa });
      } else if (elemento.tipo === "terminar") {
        setEstado((e) => (e ? { ...e, terminando: false } : e));
        setMensaje({ tipo: "error", texto: causa });
      }
    }
  }, [encolarPuntos]);

  useEffect(() => {
    const intervalo = setInterval(sincronizar, 5000);
    window.addEventListener("online", sincronizar);
    sincronizar();
    return () => {
      clearInterval(intervalo);
      window.removeEventListener("online", sincronizar);
    };
  }, [sincronizar]);

  const rutaElegida = rutas.find((r) => String(r.id) === rutaId);

  async function iniciar() {
    setMensaje(null);
    setResumen(null);
    const horario = rutaElegida?.horarios.find((h) => String(h.id) === horarioId) ?? null;
    try {
      const { registro: r } = await api.iniciarRegistro({
        ruta: rutaElegida.id,
        horario: horario?.id ?? null,
        id_cliente: crearId(),
      });
      ultimoPunto.current = null;
      puntosSinEncolar.current = [];
      setEstado({
        registro: {
          id: r.id,
          id_cliente: r.id_cliente,
          ruta: { id: rutaElegida.id, clave: rutaElegida.clave, nombre: rutaElegida.nombre, punto_de_partida: rutaElegida.punto_de_partida },
          horario: horario ? { id: horario.id, sentido: horario.sentido, salida: horario.salida } : null,
          iniciado_en: r.iniciado_en,
        },
        marcas: [],
        puntos: [],
        terminando: false,
      });
    } catch (falla) {
      setMensaje({ tipo: "error", texto: falla.causa });
      if (falla.causa === "ya tienes un registro en curso") {
        api.registroEnCurso().then(({ registro: r }) => setEnCursoEnServidor(r)).catch(() => {});
      }
    }
  }

  async function cancelarElDelServidor() {
    try {
      await api.cancelarRegistro(enCursoEnServidor.id);
      setEnCursoEnServidor(null);
      setMensaje({ tipo: "exito", texto: "El registro anterior quedó cancelado. Ya puedes iniciar otro." });
    } catch (falla) {
      setMensaje({ tipo: "error", texto: falla.causa });
    }
  }

  function marcar() {
    setMensaje(null);
    if (!posicion || Date.now() - posicion.recibidaMs > ANTIGUEDAD_MAXIMA_DE_LA_POSICION_MS) {
      setMensaje({ tipo: "alerta", texto: "Esperando una posición reciente del GPS…" });
      return;
    }
    const punto = [posicion.latitud, posicion.longitud];
    if (marcasValidas.some((m) => distanciaEnMetros(punto, [m.latitud, m.longitud]) < RADIO_DE_LLEGADA_M)) {
      setMensaje({ tipo: "error", texto: "ya marcaste una parada a menos de 50 m" });
      return;
    }
    const numero = marcasValidas.length + 1;
    const sugerido = numero === 1 ? registro.ruta.punto_de_partida : `Parada ${numero}`;
    const datos = {
      id_cliente: crearId(),
      nombre: nombre.trim() || sugerido,
      latitud: posicion.latitud,
      longitud: posicion.longitud,
      precision_m: posicion.precision_m,
      marcada_en: new Date().toISOString(),
    };
    cola.agregar({ id: datos.id_cliente, tipo: "marca", registroId: registro.id, datos });
    setEstado((e) => ({ ...e, marcas: [...e.marcas, { ...datos, estado: "pendiente" }] }));
    setNombre("");
    setPendientes(cola.pendientes());
    sincronizar();
  }

  function terminar() {
    setConfirmarFin(false);
    encolarPuntos();
    cola.agregar({ id: `terminar-${registro.id}`, tipo: "terminar", registroId: registro.id });
    setEstado((e) => ({ ...e, terminando: true }));
    setPendientes(cola.pendientes());
    sincronizar();
  }

  function descargar() {
    const datos = estado ?? almacen.leerUltimo();
    if (datos) descargarRespaldo(armarRespaldo(datos));
  }

  const aqui = useMemo(
    () => (posicion ? [posicion.latitud, posicion.longitud] : null),
    [posicion?.latitud, posicion?.longitud],
  );
  const sugerencia = registro ? (marcasValidas.length === 0 ? registro.ruta.punto_de_partida : `Parada ${marcasValidas.length + 1}`) : "";

  return (
    <div className="absolute inset-0">
      <Mapa centro={aqui ?? undefined} zoom={16} foco={seguir && aqui ? { punto: aqui, clave: "aqui" } : null}>
        <DejarDeSeguirAlArrastrar alArrastrar={() => setSeguir(false)} />
        {estado?.puntos?.length > 1 && (
          <Polyline positions={estado.puntos.map((p) => [p.latitud, p.longitud])} pathOptions={{ color: "#3c8dbc", weight: 5 }} />
        )}
        {marcasValidas.map((m, indice) => (
          <CircleMarker
            key={m.id_cliente}
            center={[m.latitud, m.longitud]}
            radius={10}
            pathOptions={{ color: "#fff", weight: 3, fillColor: m.estado === "guardada" ? "#242865" : "#f39c12", fillOpacity: 1 }}
          >
            <Tooltip permanent direction="top" offset={[0, -8]}>{`${indice + 1}. ${m.nombre}`}</Tooltip>
          </CircleMarker>
        ))}
        {aqui && (
          <>
            <Circle center={aqui} radius={posicion.precision_m} pathOptions={{ color: "#3c8dbc", weight: 1, fillOpacity: 0.12 }} />
            <CircleMarker center={aqui} radius={8} pathOptions={{ color: "#fff", weight: 3, fillColor: "#0073b7", fillOpacity: 1 }} />
          </>
        )}
      </Mapa>

      {!seguir && aqui && (
        <button
          type="button"
          onClick={() => setSeguir(true)}
          className="absolute right-4 top-4 z-[1000] rounded-full bg-white px-4 py-2 text-sm font-semibold text-upb shadow-lg"
        >
          Centrar en mí
        </button>
      )}

      <section className="absolute inset-x-0 bottom-0 z-[1000] max-h-[62%] overflow-y-auto rounded-t-3xl bg-white p-5 shadow-[0_-8px_30px_rgba(0,0,0,0.15)] md:inset-y-4 md:left-4 md:right-auto md:max-h-none md:w-[26rem] md:rounded-3xl">
        <div className="mx-auto mb-3 h-1.5 w-12 rounded-full bg-black/10 md:hidden" />
        <div className="flex items-start justify-between gap-3">
          <div>
            <h1 className="font-titulo text-xl font-bold text-upb">Modo registro</h1>
            <p className={`text-sm font-semibold ${colorDePrecision(posicion?.precision_m)}`}>
              {posicion ? `GPS ± ${posicion.precision_m} m` : "Buscando GPS…"}
            </p>
          </div>
          <span className={`rounded-full px-3 py-1 text-xs font-semibold ${pendientes ? "bg-[#fdf1dc] text-[#7a4a00]" : "bg-[#e7f6ea] text-[#1d5b2c]"}`}>
            {pendientes ? `${pendientes} por enviar` : "Todo guardado"}
          </span>
        </div>

        <div className="mt-3 space-y-2">
          {errorGps && <Aviso tipo="alerta">{errorGps}</Aviso>}
          {mensaje && <Aviso tipo={mensaje.tipo}>{mensaje.texto}</Aviso>}
        </div>

        {!registro && (
          <div className="mt-4 space-y-4">
            {resumen && (
              <Aviso tipo="exito">
                Registro terminado: {resumen.marcas} marcas, {resumen.paradas_nuevas} paradas nuevas y{" "}
                {resumen.paradas_existentes} ya conocidas.
              </Aviso>
            )}
            {enCursoEnServidor && (
              <Aviso tipo="alerta">
                Tienes un registro sin terminar de la {enCursoEnServidor.ruta.nombre} ({horaCorta(enCursoEnServidor.iniciado_en)}).{" "}
                <button type="button" onClick={cancelarElDelServidor} className="font-semibold underline">
                  Cancelarlo
                </button>
              </Aviso>
            )}
            <label className="block">
              <span className="mb-1 block text-sm font-semibold">Ruta</span>
              <select
                value={rutaId}
                onChange={(e) => {
                  setRutaId(e.target.value);
                  const ruta = rutas.find((r) => String(r.id) === e.target.value);
                  setHorarioId(String(ruta?.horarios[0]?.id ?? ""));
                }}
                className="w-full rounded-lg border border-[#c9cfdc] bg-campo px-3 py-2.5"
              >
                {rutas.map((r) => <option key={r.id} value={r.id}>{r.nombre}</option>)}
              </select>
            </label>
            <label className="block">
              <span className="mb-1 block text-sm font-semibold">Horario</span>
              <select value={horarioId} onChange={(e) => setHorarioId(e.target.value)} className="w-full rounded-lg border border-[#c9cfdc] bg-campo px-3 py-2.5">
                {rutaElegida?.horarios.map((h) => (
                  <option key={h.id} value={h.id}>{SENTIDO[h.sentido]} {h.salida}</option>
                ))}
              </select>
            </label>
            <p className="text-sm text-suave">
              Ve al punto de salida. Toca «Iniciar» cuando el bus arranque y «Parada aquí» en cada parada, también al llegar.
            </p>
            <Boton grande className="w-full" onClick={iniciar} disabled={!rutaElegida}>
              Iniciar registro
            </Boton>
            {!resumen && almacen.leerUltimo() && (
              <Boton variante="secundario" className="w-full" onClick={descargar}>
                Descargar el respaldo del último registro
              </Boton>
            )}
            {resumen && (
              <Boton variante="secundario" className="w-full" onClick={descargar}>
                Descargar respaldo
              </Boton>
            )}
          </div>
        )}

        {registro && (
          <div className="mt-4 space-y-4">
            <div className="rounded-xl bg-fondo px-4 py-3">
              <p className="font-semibold text-upb">
                {registro.ruta.nombre}
                {registro.horario && ` · ${SENTIDO[registro.horario.sentido]} ${registro.horario.salida}`}
              </p>
              <p className="text-sm text-suave">
                Iniciado {horaCorta(registro.iniciado_en)} · {marcasValidas.length} paradas marcadas
              </p>
            </div>
            {!estado.terminando && (
              <>
                <label className="block">
                  <span className="mb-1 block text-sm font-semibold">Nombre de la parada (opcional)</span>
                  <input
                    value={nombre}
                    onChange={(e) => setNombre(e.target.value)}
                    placeholder={sugerencia}
                    className="w-full rounded-lg border border-[#c9cfdc] bg-campo px-3 py-2.5"
                  />
                </label>
                <Boton variante="acento" grande className="w-full text-xl" onClick={marcar}>
                  📍 Parada aquí
                </Boton>
              </>
            )}
            {estado.terminando && <Aviso tipo="info">Terminando… se completa en cuanto haya señal.</Aviso>}
            <ol className="space-y-2">
              {estado.marcas.map((m, indice) => (
                <li key={m.id_cliente} className="flex items-center justify-between rounded-xl border border-black/5 px-3 py-2 text-sm">
                  <span>
                    <span className="mr-2 font-bold text-upb">{indice + 1}</span>
                    {m.nombre}
                    {m.estado === "rechazada" && <span className="block text-xs text-[#b42318]">{m.causa}</span>}
                  </span>
                  <span className="text-right">
                    <span className="block font-semibold">{horaCorta(m.marcada_en)}</span>
                    <span className="text-xs text-suave">
                      {{ pendiente: "por enviar", guardada: "guardada", rechazada: "rechazada" }[m.estado]}
                    </span>
                  </span>
                </li>
              ))}
            </ol>
            {!estado.terminando && (confirmarFin ? (
              <div className="space-y-2 rounded-xl bg-fondo p-3">
                <p className="text-sm">¿Terminar el registro? Revisa que marcaste la llegada a la U.</p>
                <div className="flex gap-2">
                  <Boton className="flex-1" onClick={terminar}>Sí, terminar</Boton>
                  <Boton variante="secundario" className="flex-1" onClick={() => setConfirmarFin(false)}>Seguir</Boton>
                </div>
              </div>
            ) : (
              <div className="flex gap-2">
                <Boton className="flex-1" onClick={() => setConfirmarFin(true)} disabled={marcasValidas.length === 0}>
                  Terminar registro
                </Boton>
                <Boton variante="secundario" onClick={descargar}>Respaldo</Boton>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
