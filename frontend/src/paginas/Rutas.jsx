import { useEffect, useState } from "react";
import { CircleMarker, Polyline, Tooltip } from "react-leaflet";

import { api } from "../api/cliente.js";
import Aviso from "../componentes/Aviso.jsx";
import Mapa from "../componentes/Mapa.jsx";

const SENTIDO = { ingreso: "Ingreso", salida: "Salida" };

/** HU-04: rutas con recorrido, paradas en orden, horarios y hora aproximada. */
export default function Rutas() {
  const [rutas, setRutas] = useState([]);
  const [rutaId, setRutaId] = useState(null);
  const [horarioId, setHorarioId] = useState(null);
  const [ruta, setRuta] = useState(null);
  const [viajeActivo, setViajeActivo] = useState(null);
  const [posicionDelBus, setPosicionDelBus] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .rutas()
      .then(({ rutas: lista }) => {
        setRutas(lista);
        if (lista.length) setRutaId(lista.find((r) => r.clave === "norte")?.id ?? lista[0].id);
      })
      .catch((falla) => setError(falla.causa));
  }, []);

  useEffect(() => {
    if (!rutaId) return;
    api
      .ruta(rutaId, horarioId)
      .then(({ ruta: detalle }) => {
        setRuta(detalle);
        setHorarioId(detalle.horario_elegido);
      })
      .catch((falla) => setError(falla.causa));
  }, [rutaId, horarioId]);

  useEffect(() => {
    if (!rutaId) return undefined;
    let vigente = true;
    api.viajes({ ruta: rutaId, estado: "en_curso" })
      .then(({ viajes }) => {
        if (vigente) setViajeActivo(viajes[0] ?? null);
      })
      .catch((falla) => setError(falla.causa));
    return () => { vigente = false; };
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
  const centro = paradas.length ? [paradas[0].latitud, paradas[0].longitud] : undefined;

  return (
    <div className="absolute inset-0">
      <Mapa centro={centro} seguir={centro}>
        {ruta?.recorrido?.length > 1 && <Polyline positions={ruta.recorrido} pathOptions={{ color: "#3c8dbc", weight: 6, opacity: 0.8 }} />}
        {paradas.map((parada) => (
          <CircleMarker
            key={parada.id}
            center={[parada.latitud, parada.longitud]}
            radius={9}
            pathOptions={{ color: "#fff", weight: 3, fillColor: parada.estado === "aprobada" ? "#242865" : "#f39c12", fillOpacity: 1 }}
          >
            <Tooltip direction="top">
              {parada.orden}. {parada.nombre}
              {parada.hora_aproximada ? ` · ${parada.hora_aproximada}` : ""}
            </Tooltip>
          </CircleMarker>
        ))}
        {posicionDelBus && (
          <CircleMarker
            center={[posicionDelBus.latitud, posicionDelBus.longitud]}
            radius={12}
            pathOptions={{ color: "#fff", weight: 4, fillColor: "#009fe3", fillOpacity: 1 }}
          >
            <Tooltip direction="top" permanent>🚌 Bus en vivo</Tooltip>
          </CircleMarker>
        )}
      </Mapa>

      <section className="absolute inset-x-0 bottom-0 z-[1000] max-h-[55%] overflow-y-auto rounded-t-3xl bg-white p-5 shadow-[0_-8px_30px_rgba(0,0,0,0.15)] md:inset-y-4 md:left-4 md:right-auto md:max-h-none md:w-96 md:rounded-3xl">
        <div className="mx-auto mb-3 h-1.5 w-12 rounded-full bg-black/10 md:hidden" />
        {error && <Aviso tipo="error">{error}</Aviso>}
        <div className="flex gap-2 overflow-x-auto pb-2">
          {rutas.map((r) => (
            <button
              key={r.id}
              type="button"
              onClick={() => { setRutaId(r.id); setHorarioId(null); }}
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
            <div className="mt-3 rounded-xl bg-celeste/20 px-3 py-2 text-sm text-upb">
              {viajeActivo ? (
                posicionDelBus
                  ? <>🚌 Bus en vivo · última señal {new Date(posicionDelBus.tomada_en).toLocaleTimeString("es-BO", { hour: "2-digit", minute: "2-digit", timeZone: "America/La_Paz" })}</>
                  : <>🚌 El viaje está en curso; esperando la primera posición.</>
              ) : (
                <>No hay un bus en curso en esta ruta.</>
              )}
            </div>
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
              {paradas.map((parada) => (
                <li key={parada.id} className="flex items-center justify-between rounded-xl bg-fondo px-3 py-2">
                  <span>
                    <span className="mr-2 font-bold text-upb">{parada.orden}</span>
                    {parada.nombre}
                    {parada.estado === "propuesta" && <span className="ml-2 text-xs text-[#7a4a00]">(propuesta)</span>}
                  </span>
                  <span className="font-semibold text-boton">{parada.hora_aproximada ?? "—"}</span>
                </li>
              ))}
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
