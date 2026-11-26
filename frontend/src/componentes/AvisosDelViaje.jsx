import { useEffect, useRef, useState } from "react";

import { api } from "../api/cliente.js";
import Aviso from "./Aviso.jsx";
import ChatDirecto from "./ChatDirecto.jsx";

function hora(momento) {
  return new Date(momento).toLocaleTimeString("es-BO", { hour: "2-digit", minute: "2-digit", timeZone: "America/La_Paz" });
}

/**
 * HU-07 para el chofer: le llega «Ismael va a subir en Sevilla» y ve la ubicación
 * de quien la comparte. Usa el canal privado del viaje (solo chofer y administrador).
 */
export default function AvisosDelViaje({ viajeId }) {
  const [avisos, setAvisos] = useState([]);
  const [ultimaAlerta, setUltimaAlerta] = useState("");
  const [error, setError] = useState("");
  const [nuevosPorEstudiante, setNuevosPorEstudiante] = useState({});
  const chatsAbiertos = useRef(new Set());

  function cambiarEstadoDelChat(estudianteId, abierto) {
    if (abierto) {
      chatsAbiertos.current.add(estudianteId);
      setNuevosPorEstudiante((actuales) => ({ ...actuales, [estudianteId]: 0 }));
    } else {
      chatsAbiertos.current.delete(estudianteId);
    }
  }

  useEffect(() => {
    let vigente = true;
    const consultar = () => {
      api.avisosDelViaje(viajeId)
        .then(({ avisos: lista }) => vigente && setAvisos(lista))
        .catch((falla) => vigente && setError(falla.causa));
    };
    consultar();
    const intervalo = setInterval(consultar, 30_000);

    let socket = null;
    if (typeof WebSocket !== "undefined") {
      const protocolo = window.location.protocol === "https:" ? "wss:" : "ws:";
      socket = new WebSocket(`${protocolo}//${window.location.host}/ws/viajes/${viajeId}/chofer/`);
      socket.onmessage = ({ data }) => {
        const evento = JSON.parse(data);
        if (evento.tipo === "aviso") setUltimaAlerta(evento.mensaje);
        if (evento.tipo === "mensaje_directo_nuevo") {
          const estudianteId = evento.estudiante;
          if (estudianteId && !chatsAbiertos.current.has(estudianteId)) {
            setNuevosPorEstudiante((actuales) => ({
              ...actuales,
              [estudianteId]: (actuales[estudianteId] ?? 0) + 1,
            }));
          }
        }
        if (["aviso", "aviso_cerrado", "ubicacion"].includes(evento.tipo)) consultar();
      };
    }
    return () => {
      vigente = false;
      clearInterval(intervalo);
      socket?.close();
    };
  }, [viajeId]);

  return (
    <div className="mt-4 border-t border-black/5 pt-4">
      <h3 className="font-titulo text-base font-bold text-upb">Van a subir</h3>
      {ultimaAlerta && <div className="mt-2"><Aviso tipo="exito">🙋 {ultimaAlerta}</Aviso></div>}
      {error && <div className="mt-2"><Aviso tipo="error">{error}</Aviso></div>}
      <ul className="mt-2 space-y-2">
        {avisos.map((aviso) => (
          <li key={aviso.id} className="rounded-xl bg-fondo px-3 py-2 text-sm">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <span><strong>{aviso.estudiante.nombre}</strong> · {aviso.parada.nombre}</span>
              <span className="text-suave">
                {aviso.estado === "a_bordo" && "a bordo"}
                {aviso.estado === "confirmado" && (aviso.ubicacion
                  ? <a
                      className="text-boton underline"
                      href={`https://www.openstreetmap.org/?mlat=${aviso.ubicacion.latitud}&mlon=${aviso.ubicacion.longitud}#map=18/${aviso.ubicacion.latitud}/${aviso.ubicacion.longitud}`}
                      target="_blank"
                      rel="noreferrer"
                    >
                      📍 ubicación de las {hora(aviso.ubicacion.tomada_en)}
                    </a>
                  : "esperando")}
              </span>
            </div>
            {aviso.estado === "confirmado" && (
              <ChatDirecto
                viajeId={viajeId}
                estudiante={aviso.estudiante}
                esChofer
                nuevos={nuevosPorEstudiante[aviso.estudiante.id] ?? 0}
                alCambiarAbierto={(abierto) => cambiarEstadoDelChat(aviso.estudiante.id, abierto)}
              />
            )}
          </li>
        ))}
      </ul>
      {!avisos.length && <p className="mt-2 text-sm text-suave">Nadie avisó todavía que va a subir.</p>}
    </div>
  );
}
