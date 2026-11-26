import { useCallback, useEffect, useState } from "react";
import { CircleMarker, Polyline, Tooltip } from "react-leaflet";

import { api } from "../api/cliente.js";
import Aviso from "../componentes/Aviso.jsx";
import Boton from "../componentes/Boton.jsx";
import Mapa from "../componentes/Mapa.jsx";
import VoyASubir from "../componentes/VoyASubir.jsx";
import { useSesion } from "../sesion/SesionContexto.jsx";

const SENTIDO = { ingreso: "Ingreso", salida: "Salida" };

/** HU-04, HU-06 y HU-08: rutas, bus en vivo, propuestas de parada y aprobación. */
export default function Rutas() {
  const sesion = useSesion();
  const esAdmin = sesion?.usuario?.rol === "administrador";

  const [rutas, setRutas] = useState([]);
  const [rutaId, setRutaId] = useState(null);
  const [horarioId, setHorarioId] = useState(null);
  const [ruta, setRuta] = useState(null);
  const [viajeActivo, setViajeActivo] = useState(null);
  const [posicionDelBus, setPosicionDelBus] = useState(null);
  const [error, setError] = useState("");
  const [aviso, setAviso] = useState("");

  // Estado para proponer una parada (HU-08)
  const [puntoPropuesto, setPuntoPropuesto] = useState(null);
  const [nombrePropuesta, setNombrePropuesta] = useState("");
  const [enviandoPropuesta, setEnviandoPropuesta] = useState(false);
  const [gestionandoParada, setGestionandoParada] = useState(null);

  useEffect(() => {
    api
      .rutas()
      .then(({ rutas: lista }) => {
        setRutas(lista);
        if (lista.length) setRutaId(lista.find((r) => r.clave === "norte")?.id ?? lista[0].id);
      })
      .catch((falla) => setError(falla.causa));
  }, []);

  const cargarRuta = useCallback((idActual, horarioActual) => {
    if (!idActual) return;
    api
      .ruta(idActual, horarioActual)
      .then(({ ruta: detalle }) => {
        setRuta(detalle);
        setHorarioId(detalle.horario_elegido);
      })
      .catch((falla) => setError(falla.causa));
  }, []);

  useEffect(() => {
    cargarRuta(rutaId, horarioId);
  }, [rutaId, horarioId, cargarRuta]);

  useEffect(() => {
    if (!rutaId) return undefined;
    let vigente = true;
    const consultarViaje = () => {
      api.viajes({ ruta: rutaId, estado: "en_curso" })
        .then(({ viajes }) => {
          if (vigente) setViajeActivo(viajes[0] ?? null);
        })
        .catch((falla) => setError(falla.causa));
    };
    consultarViaje();
    const intervalo = setInterval(consultarViaje, 30_000);
    return () => {
      vigente = false;
      clearInterval(intervalo);
    };
  }, [rutaId]);

  useEffect(() => {
    if (!viajeActivo) {
      setPosicionDelBus(null);
      return undefined;
    }
    setPosicionDelBus(viajeActivo.ultima_posicion);
    const protocolo = window.location.protocol === "https:" ? "wss:" : "ws:";
    const socket = new WebSocket(`${protocolo}//${window.location.host}/ws/viajes/${viajeActivo.id}/`);
    socket.onmessage = ({ data }) => {
      const evento = JSON.parse(data);
      if (evento.tipo === "posicion") {
        setPosicionDelBus({
          latitud: evento.latitud,
          longitud: evento.longitud,
          tomada_en: evento.tomada_en,
        });
      }
    };
    return () => socket.close();
  }, [viajeActivo]);

  const paradas = ruta?.paradas ?? [];
  const paradasPropuestas = paradas.filter((p) => p.estado === "propuesta");
  const paradasActivasIds = new Set(viajeActivo?.paradas_activas ?? []);
  const centro = paradas.length
    ? [paradas[0].latitud, paradas[0].longitud]
    : ruta?.recorrido?.length
      ? ruta.recorrido[0]
      : undefined;

  function tocarRecorrido(evento) {
    if (!evento?.latlng) return;
    setError("");
    setAviso("");
    setPuntoPropuesto([evento.latlng.lat, evento.latlng.lng]);
  }

  async function enviarPropuesta(evento) {
    evento.preventDefault();
    if (!rutaId || !puntoPropuesto) return;
    setEnviandoPropuesta(true);
    setError("");
    setAviso("");
    try {
      await api.proponerParada(rutaId, {
        nombre: nombrePropuesta.trim(),
        latitud: puntoPropuesto[0],
        longitud: puntoPropuesto[1],
      });
      setPuntoPropuesto(null);
      setNombrePropuesta("");
      setAviso("Parada propuesta enviada. Queda pendiente de aprobación.");
      cargarRuta(rutaId, horarioId);
    } catch (falla) {
      setError(falla.causa);
    } finally {
      setEnviandoPropuesta(false);
    }
  }

  async function resolverPropuesta(paradaId, accion) {
    setGestionandoParada(paradaId);
    setError("");
    setAviso("");
    try {
      if (accion === "aprobar") {
        await api.aprobarParada(paradaId);
        setAviso("Parada aprobada y añadida al recorrido.");
      } else {
        await api.rechazarParada(paradaId);
        setAviso("Parada propuesta rechazada.");
      }
      cargarRuta(rutaId, horarioId);
    } catch (falla) {
      setError(falla.causa);
    } finally {
      setGestionandoParada(null);
    }
  }

  return (
    <div className="absolute inset-0">
      <Mapa centro={centro} seguir={centro}>
        {ruta?.recorrido?.length > 1 && (
          <Polyline
            positions={ruta.recorrido}
            pathOptions={{ color: "#3c8dbc", weight: 7, opacity: 0.85 }}
            eventHandlers={{ click: tocarRecorrido }}
          />
        )}
        {paradas.map((parada) => {
          const esPropuesta = parada.estado === "propuesta";
          const estaActiva = paradasActivasIds.has(parada.id);
          const colorRelleno = esPropuesta ? "#f39c12" : estaActiva ? "#16a34a" : "#242865";
          return (
            <CircleMarker
              key={parada.id}
              center={[parada.latitud, parada.longitud]}
              radius={estaActiva ? 11 : 9}
              pathOptions={{ color: "#fff", weight: 3, fillColor: colorRelleno, fillOpacity: 1 }}
            >
              <Tooltip direction="top">
                {parada.orden}. {parada.nombre}
                {parada.hora_aproximada ? ` · ${parada.hora_aproximada}` : ""}
                {esPropuesta ? " (propuesta)" : ""}
                {estaActiva ? " · Activa" : ""}
              </Tooltip>
            </CircleMarker>
          );
        })}
        {puntoPropuesto && (
          <CircleMarker
            center={puntoPropuesto}
            radius={10}
            pathOptions={{ color: "#242865", weight: 3, fillColor: "#f39c12", fillOpacity: 0.9 }}
          >
            <Tooltip direction="top" permanent>📍 Nueva parada propuesta</Tooltip>
          </CircleMarker>
        )}
        {posicionDelBus && (
          <CircleMarker
            center={[posicionDelBus.latitud, posicionDelBus.longitud]}
            radius={12}
            pathOptions={{ color: "#fff", weight: 4, fillColor: "#009fe3", fillOpacity: 1 }}
          >
            <Tooltip direction="top" permanent>{viajeActivo?.simulado ? "🧪 Bus simulado" : "🚌 Bus en vivo"}</Tooltip>
          </CircleMarker>
        )}
      </Mapa>

      <section className="absolute inset-x-0 bottom-0 z-[1000] max-h-[55%] overflow-y-auto rounded-t-3xl bg-white p-5 shadow-[0_-8px_30px_rgba(0,0,0,0.15)] md:inset-y-4 md:left-4 md:right-auto md:max-h-none md:w-96 md:rounded-3xl">
        <div className="mx-auto mb-3 h-1.5 w-12 rounded-full bg-black/10 md:hidden" />
        {error && <div className="mb-2"><Aviso tipo="error">{error}</Aviso></div>}
        {aviso && <div className="mb-2"><Aviso tipo="alerta">{aviso}</Aviso></div>}
        <div className="flex gap-2 overflow-x-auto pb-2">
          {rutas.map((r) => (
            <button
              key={r.id}
              type="button"
              onClick={() => {
                setRutaId(r.id);
                setHorarioId(null);
                setPuntoPropuesto(null);
              }}
              className={`shrink-0 rounded-full px-3 py-1.5 text-sm font-semibold ${r.id === rutaId ? "bg-upb text-white" : "bg-fondo text-upb"}`}
            >
              {r.nombre.replace("Ruta ", "")}
            </button>
          ))}
        </div>
        {ruta && (
          <>
            <h2 className="mt-2 font-titulo text-xl font-bold text-upb">{ruta.nombre}</h2>
            <p className="text-sm text-suave">Sale de {ruta.punto_de_partida}</p>
            {ruta.nota && <div className="mt-2"><Aviso tipo="alerta">{ruta.nota}</Aviso></div>}

            {puntoPropuesto ? (
              <form onSubmit={enviarPropuesta} className="mt-3 rounded-2xl border border-acento/40 bg-acento/10 p-3">
                <p className="text-sm font-bold text-upb">Proponer parada en este punto</p>
                <p className="text-xs text-suave">
                  {puntoPropuesto[0].toFixed(5)}, {puntoPropuesto[1].toFixed(5)}
                </p>
                <input
                  type="text"
                  value={nombrePropuesta}
                  onChange={(e) => setNombrePropuesta(e.target.value)}
                  placeholder="Nombre de la parada (ej. Plaza Principal)"
                  className="mt-2 w-full rounded-xl border border-upb/20 bg-white px-3 py-2 text-sm text-tinta focus:border-boton focus:outline-none"
                />
                <div className="mt-2 flex gap-2">
                  <Boton type="submit" disabled={enviandoPropuesta} className="flex-1 text-sm">
                    {enviandoPropuesta ? "Enviando..." : "Proponer parada"}
                  </Boton>
                  <Boton
                    variante="secundario"
                    onClick={() => { setPuntoPropuesto(null); setNombrePropuesta(""); }}
                    className="text-sm"
                  >
                    Cancelar
                  </Boton>
                </div>
              </form>
            ) : (
              ruta.recorrido?.length > 1 && (
                <p className="mt-2 text-xs text-suave">
                  Toca la línea azul del recorrido en el mapa para proponer una nueva parada.
                </p>
              )
            )}

            {esAdmin && paradasPropuestas.length > 0 && (
              <div className="mt-4 rounded-2xl border border-acento/40 bg-fondo p-3">
                <h3 className="font-titulo text-sm font-bold text-upb">
                  Paradas propuestas ({paradasPropuestas.length})
                </h3>
                <ul className="mt-2 space-y-2">
                  {paradasPropuestas.map((parada) => (
                    <li key={parada.id} className="rounded-xl bg-white p-2.5 shadow-xs">
                      <p className="text-sm font-semibold text-tinta">{parada.nombre}</p>
                      <div className="mt-2 flex gap-2">
                        <Boton
                          disabled={gestionandoParada === parada.id}
                          onClick={() => resolverPropuesta(parada.id, "aprobar")}
                          className="flex-1 py-1.5 text-xs"
                        >
                          Aprobar
                        </Boton>
                        <Boton
                          variante="peligro"
                          disabled={gestionandoParada === parada.id}
                          onClick={() => resolverPropuesta(parada.id, "rechazar")}
                          className="flex-1 py-1.5 text-xs"
                        >
                          Rechazar
                        </Boton>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="mt-3 rounded-xl bg-celeste/20 px-3 py-2 text-sm text-upb">
              {viajeActivo ? (
                posicionDelBus
                  ? <>{viajeActivo.simulado ? "🧪 Bus simulado" : "🚌 Bus en vivo"} · última señal {new Date(posicionDelBus.tomada_en).toLocaleTimeString("es-BO", { hour: "2-digit", minute: "2-digit", timeZone: "America/La_Paz" })}</>
                  : <>🚌 El viaje está en curso; esperando la primera posición.</>
              ) : (
                <>No hay un bus en curso en esta ruta.</>
              )}
            </div>
            <VoyASubir rutaId={rutaId} horarioId={horarioId} paradas={paradas} />
            <div className="mt-3 flex flex-wrap gap-2">
              {ruta.horarios.map((h) => (
                <button
                  key={h.id}
                  type="button"
                  onClick={() => setHorarioId(h.id)}
                  className={`rounded-lg px-2.5 py-1 text-sm ${h.id === horarioId ? "bg-boton text-white" : "bg-fondo text-tinta"}`}
                >
                  {SENTIDO[h.sentido]} {h.salida}
                </button>
              ))}
            </div>
            <ol className="mt-4 space-y-2">
              {paradas.map((parada) => {
                const estaActiva = paradasActivasIds.has(parada.id);
                return (
                  <li key={parada.id} className="flex items-center justify-between rounded-xl bg-fondo px-3 py-2">
                    <span>
                      <span className="mr-2 font-bold text-upb">{parada.orden}</span>
                      {parada.nombre}
                      {parada.estado === "propuesta" && (
                        <span className="ml-2 text-xs font-medium text-[#7a4a00]">(propuesta)</span>
                      )}
                      {estaActiva && (
                        <span className="ml-2 rounded-full bg-green-100 px-2 py-0.5 text-xs font-semibold text-green-800">
                          Activa
                        </span>
                      )}
                    </span>
                    <span className="font-semibold text-boton">{parada.hora_aproximada ?? "—"}</span>
                  </li>
                );
              })}
            </ol>
            {!paradas.length && (
              <p className="mt-4 text-sm text-suave">
                Esta ruta todavía no tiene paradas. Se cargan con el modo registro en un viaje real.
              </p>
            )}
          </>
        )}
      </section>
    </div>
  );
}