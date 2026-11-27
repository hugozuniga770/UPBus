import { useCallback, useEffect, useState } from "react";

import { api } from "../api/cliente.js";
import Aviso from "./Aviso.jsx";
import Boton from "./Boton.jsx";
import ChatDirecto from "./ChatDirecto.jsx";

function hora(momento) {
  return new Date(momento).toLocaleTimeString("es-BO", { hour: "2-digit", minute: "2-digit", timeZone: "America/La_Paz" });
}

/**
 * HU-07, HU-09 y HU-10 para el chofer:
 * - Recibe avisos «Voy a subir» y ubicaciones.
 * - Recibe sugerencias de seguir de largo si nadie espera y va atrasado (RF-12).
 * - Registra «Subió» o «No se presentó» y muestra quién ya subió.
 */
export default function AvisosDelViaje({ viajeId }) {
  const [avisos, setAvisos] = useState([]);
  const [ultimaAlerta, setUltimaAlerta] = useState("");
  const [sugerenciaSeguir, setSugerenciaSeguir] = useState("");
  const [ocupadoId, setOcupadoId] = useState(null);
  const [error, setError] = useState("");

  const consultar = useCallback(() => {
    api.avisosDelViaje(viajeId)
      .then(({ avisos: lista }) => setAvisos(lista))
      .catch((falla) => setError(falla.causa));
  }, [viajeId]);

  useEffect(() => {
    consultar();
    const intervalo = setInterval(consultar, 30_000);

    let socket = null;
    if (typeof WebSocket !== "undefined") {
      const protocolo = window.location.protocol === "https:" ? "wss:" : "ws:";
      socket = new WebSocket(`${protocolo}//${window.location.host}/ws/viajes/${viajeId}/chofer/`);
      socket.onmessage = ({ data }) => {
        const evento = JSON.parse(data);
        if (evento.tipo === "aviso" || evento.tipo === "aviso_actualizado") setUltimaAlerta(evento.mensaje);
        if (evento.tipo === "sugerencia_saltar") setSugerenciaSeguir(evento.mensaje);
        if (["aviso", "aviso_cerrado", "aviso_actualizado", "ubicacion"].includes(evento.tipo)) {
          consultar();
        }
      };
    }
    return () => {
      clearInterval(intervalo);
      socket?.close();
    };
  }, [viajeId, consultar]);

  async function gestionarAviso(avisoId, accion) {
    setOcupadoId(avisoId);
    setError("");
    try {
      if (accion === "subio") {
        await api.marcarSubio(avisoId);
      } else {
        await api.marcarNoSePresento(avisoId);
      }
      consultar();
    } catch (falla) {
      setError(falla.causa);
    } finally {
      setOcupadoId(null);
    }
  }

  const esperando = avisos.filter((a) => a.estado === "confirmado");
  const aBordo = avisos.filter((a) => a.estado === "a_bordo");

  return (
    <div className="mt-4 border-t border-black/5 pt-4">
      <h3 className="font-titulo text-base font-bold text-upb">Pasajeros del viaje</h3>
      {ultimaAlerta && <div className="mt-2"><Aviso tipo="exito">🙋 {ultimaAlerta}</Aviso></div>}
      {sugerenciaSeguir && (
        <div className="mt-2 rounded-xl border border-acento/50 bg-acento/15 px-3 py-2.5 text-sm text-tinta">
          <div className="flex items-start justify-between gap-2">
            <span>⏭️ {sugerenciaSeguir}</span>
            <button
              type="button"
              onClick={() => setSugerenciaSeguir("")}
              className="shrink-0 text-xs font-semibold text-upb underline"
            >
              Entendido
            </button>
          </div>
        </div>
      )}
      {error && <div className="mt-2"><Aviso tipo="error">{error}</Aviso></div>}

      <div className="mt-3">
        <h4 className="text-xs font-bold uppercase tracking-wide text-suave">
          Van a subir ({esperando.length})
        </h4>
        <ul className="mt-2 space-y-2">
          {esperando.map((aviso) => (
            <li key={aviso.id} className="rounded-xl bg-fondo px-3 py-2.5 text-sm">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span><strong>{aviso.estudiante.nombre}</strong> · {aviso.parada.nombre}</span>
                <span className="text-suave">
                  {aviso.ubicacion ? (
                    <a
                      className="text-boton underline"
                      href={`https://www.openstreetmap.org/?mlat=${aviso.ubicacion.latitud}&mlon=${aviso.ubicacion.longitud}#map=18/${aviso.ubicacion.latitud}/${aviso.ubicacion.longitud}`}
                      target="_blank"
                      rel="noreferrer"
                    >
                      📍 ubicación de las {hora(aviso.ubicacion.tomada_en)}
                    </a>
                  ) : (
                    "esperando"
                  )}
                </span>
              </div>
              <div className="mt-2 flex flex-wrap gap-2">
                <Boton
                  disabled={ocupadoId === aviso.id}
                  onClick={() => gestionarAviso(aviso.id, "subio")}
                  className="py-1.5 text-xs"
                >
                  Subió
                </Boton>
                <Boton
                  variante="secundario"
                  disabled={ocupadoId === aviso.id}
                  onClick={() => gestionarAviso(aviso.id, "no_se_presento")}
                  className="py-1.5 text-xs"
                >
                  No se presentó
                </Boton>
              </div>
              <ChatDirecto viajeId={viajeId} estudiante={aviso.estudiante} esChofer />
            </li>
          ))}
        </ul>
        {!esperando.length && <p className="mt-2 text-sm text-suave">Nadie está esperando en paradas ahora.</p>}
      </div>

      {aBordo.length > 0 && (
        <div className="mt-4">
          <h4 className="text-xs font-bold uppercase tracking-wide text-green-800">
            Ya subieron ({aBordo.length})
          </h4>
          <ul className="mt-2 space-y-1.5">
            {aBordo.map((aviso) => (
              <li key={aviso.id} className="flex items-center justify-between rounded-xl bg-green-50 px-3 py-2 text-sm text-green-900">
                <span><strong>{aviso.estudiante.nombre}</strong> · {aviso.parada.nombre}</span>
                <span className="rounded-full bg-green-200/70 px-2 py-0.5 text-xs font-semibold">A bordo</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
