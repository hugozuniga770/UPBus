import { useCallback, useEffect, useRef, useState } from "react";

import { api } from "../api/cliente.js";
import Aviso from "./Aviso.jsx";

function idDeMensaje() {
  return globalThis.crypto?.randomUUID?.() ?? `mensaje-ruta-${Date.now()}-${Math.random()}`;
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

/** HU-15: chat común de quienes eligieron la ruta. */
export default function ChatDeRuta({ rutaId, nombreRuta }) {
  const [membresia, setMembresia] = useState(null);
  const [mensajes, setMensajes] = useState([]);
  const [texto, setTexto] = useState("");
  const [error, setError] = useState("");
  const [ocupado, setOcupado] = useState(false);
  const reenvioPendiente = useRef(null);

  const cargarMensajes = useCallback(async () => {
    try {
      const respuesta = await api.mensajesDeRuta(rutaId);
      setMensajes(respuesta.mensajes);
    } catch (falla) {
      setError(falla.causa);
    }
  }, [rutaId]);

  useEffect(() => {
    let vigente = true;
    setMembresia(null);
    setMensajes([]);
    setError("");
    api.membresiaDeRuta(rutaId)
      .then((respuesta) => vigente && setMembresia(respuesta))
      .catch((falla) => vigente && setError(falla.causa));
    return () => { vigente = false; };
  }, [rutaId]);

  useEffect(() => {
    if (!membresia?.puede_entrar) return undefined;
    cargarMensajes();
    if (typeof WebSocket !== "function") return undefined;
    const protocolo = window.location.protocol === "https:" ? "wss:" : "ws:";
    const socket = new WebSocket(`${protocolo}//${window.location.host}/ws/mensajes/rutas/${rutaId}/`);
    socket.onmessage = ({ data }) => {
      const evento = JSON.parse(data);
      if (evento.tipo === "mensaje_de_ruta") {
        setMensajes((lista) => agregarSinDuplicar(lista, evento.mensaje));
      }
    };
    return () => socket.close();
  }, [cargarMensajes, membresia?.puede_entrar, rutaId]);

  async function elegir() {
    setOcupado(true);
    setError("");
    try {
      await api.elegirRuta(rutaId);
      setMembresia({ es_miembro: true, puede_entrar: true });
    } catch (falla) {
      setError(falla.causa);
    } finally {
      setOcupado(false);
    }
  }

  async function enviar(evento) {
    evento.preventDefault();
    if (!texto.trim()) return;
    setOcupado(true);
    setError("");
    if (reenvioPendiente.current?.texto !== texto) {
      reenvioPendiente.current = { id: idDeMensaje(), texto };
    }
    try {
      const { mensaje } = await api.enviarMensajeDeRuta(rutaId, {
        id_cliente: reenvioPendiente.current.id,
        texto,
      });
      setMensajes((lista) => agregarSinDuplicar(lista, mensaje));
      setTexto("");
      reenvioPendiente.current = null;
    } catch (falla) {
      setError(falla.causa);
    } finally {
      setOcupado(false);
    }
  }

  return (
    <section className="mt-4 rounded-2xl bg-fondo p-3" aria-label={`Chat de ${nombreRuta}`}>
      <h3 className="font-titulo text-base font-bold text-upb">Chat de {nombreRuta}</h3>
      <p className="text-xs text-suave">Solo texto · visible para quienes eligieron esta ruta.</p>
      {error && <div className="mt-2"><Aviso tipo="error">{error}</Aviso></div>}
      {membresia && !membresia.puede_entrar && (
        <button
          type="button"
          disabled={ocupado}
          onClick={elegir}
          className="mt-3 w-full rounded-lg bg-boton px-3 py-2 text-sm font-bold text-white"
        >
          Elegir {nombreRuta} y abrir el chat
        </button>
      )}
      {membresia?.puede_entrar && (
        <>
          <div className="mt-3 max-h-48 space-y-2 overflow-y-auto" aria-live="polite">
            {mensajes.map((mensaje) => (
              <article key={mensaje.id} className="rounded-lg bg-white px-3 py-2 text-sm shadow-sm">
                <p className="text-xs text-suave">
                  <strong className="text-upb">{mensaje.autor.nombre}</strong> · {hora(mensaje.enviado_en)}
                </p>
                <p>{mensaje.texto}</p>
              </article>
            ))}
            {!mensajes.length && <p className="text-sm text-suave">Todavía no hay mensajes.</p>}
          </div>
          <form className="mt-3 flex gap-2" onSubmit={enviar}>
            <label className="sr-only" htmlFor={`chat-ruta-${rutaId}`}>Mensaje para {nombreRuta}</label>
            <input
              id={`chat-ruta-${rutaId}`}
              value={texto}
              maxLength={1000}
              onChange={(evento) => setTexto(evento.target.value)}
              className="min-w-0 flex-1 rounded-lg border border-black/15 bg-white px-3 py-2 text-sm"
              placeholder="Escribe en la ruta"
            />
            <button type="submit" disabled={ocupado || !texto.trim()} className="rounded-lg bg-boton px-3 py-2 text-sm font-bold text-white">
              Enviar
            </button>
          </form>
        </>
      )}
    </section>
  );
}
