import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { api } from "../api/cliente.js";
import { useSesion } from "../sesion/SesionContexto.jsx";
import Aviso from "./Aviso.jsx";

function idDeMensaje() {
  return globalThis.crypto?.randomUUID?.() ?? `mensaje-${Date.now()}-${Math.random()}`;
}

function hora(momento) {
  return new Date(momento).toLocaleTimeString("es-BO", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
    timeZone: "America/La_Paz",
  });
}

function agregarSinDuplicar(lista, mensaje) {
  return lista.some((item) => item.id === mensaje.id) ? lista : [...lista, mensaje];
}

/** HU-14: conversación privada del estudiante confirmado con el chofer. */
export default function ChatDirecto({
  viajeId,
  estudiante = null,
  esChofer = false,
  nuevos = 0,
  alCambiarAbierto = null,
}) {
  const usuario = useSesion()?.usuario;
  const participante = estudiante ?? usuario;
  const [abierto, setAbierto] = useState(false);
  const [disponible, setDisponible] = useState(null);
  const [mensajes, setMensajes] = useState([]);
  const [respuestas, setRespuestas] = useState([]);
  const [texto, setTexto] = useState("");
  const [error, setError] = useState("");
  const [enviando, setEnviando] = useState(false);
  const reenvioPendiente = useRef(null);
  const estudianteId = participante?.id;

  const etiqueta = useMemo(
    () => (esChofer ? `Chat con ${participante?.nombre ?? "estudiante"}` : "Chat con el chofer"),
    [esChofer, participante?.nombre],
  );
  const etiquetaDelBoton = nuevos > 0
    ? `${etiqueta} · ${nuevos} ${nuevos === 1 ? "nuevo" : "nuevos"}`
    : etiqueta;

  function cambiarAbierto(siguiente) {
    setAbierto(siguiente);
    alCambiarAbierto?.(siguiente);
  }

  const cargar = useCallback(async () => {
    setError("");
    try {
      const respuesta = await api.mensajesDirectos(viajeId, esChofer ? estudianteId : null);
      setMensajes(respuesta.mensajes);
      setRespuestas(respuesta.respuestas_rapidas ?? []);
      setDisponible(true);
    } catch (falla) {
      if (falla.causa === "no estás en este viaje") {
        setDisponible(false);
      } else {
        setError(falla.causa);
      }
    }
  }, [esChofer, estudianteId, viajeId]);

  useEffect(() => {
    if (!abierto) return;
    cargar();
  }, [abierto, cargar]);

  useEffect(() => {
    if (!abierto || disponible !== true || !estudianteId || typeof WebSocket !== "function") {
      return undefined;
    }
    const protocolo = window.location.protocol === "https:" ? "wss:" : "ws:";
    const socket = new WebSocket(
      `${protocolo}//${window.location.host}/ws/mensajes/viajes/${viajeId}/${estudianteId}/`,
    );
    socket.onmessage = ({ data }) => {
      const evento = JSON.parse(data);
      if (evento.tipo === "mensaje_directo") {
        setMensajes((lista) => agregarSinDuplicar(lista, evento.mensaje));
      }
    };
    return () => socket.close();
  }, [abierto, disponible, estudianteId, viajeId]);

  async function enviar(datos) {
    setEnviando(true);
    setError("");
    const contenido = datos.respuesta_rapida ?? datos.texto;
    if (reenvioPendiente.current?.contenido !== contenido) {
      reenvioPendiente.current = { id: idDeMensaje(), contenido };
    }
    try {
      const { mensaje } = await api.enviarMensajeDirecto(viajeId, {
        id_cliente: reenvioPendiente.current.id,
        ...(esChofer ? { estudiante: estudianteId } : {}),
        ...datos,
      });
      setMensajes((lista) => agregarSinDuplicar(lista, mensaje));
      setTexto("");
      reenvioPendiente.current = null;
    } catch (falla) {
      setError(falla.causa);
    } finally {
      setEnviando(false);
    }
  }

  if (!abierto) {
    return (
      <button
        type="button"
        className="mt-2 rounded-lg border border-boton px-3 py-1.5 text-sm font-semibold text-boton"
        onClick={() => cambiarAbierto(true)}
      >
        {etiquetaDelBoton}
      </button>
    );
  }

  return (
    <section className="mt-3 w-full rounded-xl border border-celeste/60 bg-white p-3" aria-label={etiqueta}>
      <div className="flex items-center justify-between gap-2">
        <h4 className="font-titulo text-sm font-bold text-upb">{etiqueta}</h4>
        <button type="button" className="text-xs text-suave underline" onClick={() => cambiarAbierto(false)}>
          Cerrar
        </button>
      </div>
      {disponible === false && (
        <p className="mt-2 text-sm text-suave">Confirma “Voy a subir” para chatear con el chofer.</p>
      )}
      {error && <div className="mt-2"><Aviso tipo="error">{error}</Aviso></div>}
      {disponible === true && (
        <>
          <div className="mt-3 max-h-48 space-y-2 overflow-y-auto" aria-live="polite">
            {mensajes.map((mensaje) => (
              <article key={mensaje.id} className="rounded-lg bg-fondo px-3 py-2 text-sm">
                <p className="text-xs text-suave">
                  <strong className="text-upb">{mensaje.autor.nombre}</strong> · {hora(mensaje.enviado_en)}
                </p>
                <p>{mensaje.texto}</p>
              </article>
            ))}
            {!mensajes.length && <p className="text-sm text-suave">Todavía no hay mensajes.</p>}
          </div>
          {esChofer ? (
            <div className="mt-3 flex flex-wrap gap-2" aria-label="Respuestas rápidas">
              {respuestas.map((respuesta) => (
                <button
                  key={respuesta}
                  type="button"
                  disabled={enviando}
                  onClick={() => enviar({ respuesta_rapida: respuesta })}
                  className="rounded-full bg-celeste/30 px-3 py-1.5 text-sm font-semibold text-upb"
                >
                  {respuesta}
                </button>
              ))}
            </div>
          ) : (
            <form
              className="mt-3 flex gap-2"
              onSubmit={(evento) => {
                evento.preventDefault();
                if (texto.trim()) enviar({ texto });
              }}
            >
              <label className="sr-only" htmlFor={`chat-directo-${viajeId}`}>Mensaje para el chofer</label>
              <input
                id={`chat-directo-${viajeId}`}
                value={texto}
                maxLength={1000}
                onChange={(evento) => setTexto(evento.target.value)}
                className="min-w-0 flex-1 rounded-lg border border-black/15 px-3 py-2 text-sm"
                placeholder="Escribe al chofer"
              />
              <button type="submit" disabled={enviando || !texto.trim()} className="rounded-lg bg-boton px-3 py-2 text-sm font-bold text-white">
                Enviar
              </button>
            </form>
          )}
        </>
      )}
    </section>
  );
}
