import { useEffect, useMemo, useState } from "react";

import { api } from "../api/cliente.js";
import Aviso from "../componentes/Aviso.jsx";
import Boton from "../componentes/Boton.jsx";

const NOMBRE_ESTADO = {
  programado: "Programado",
  en_curso: "En curso",
  terminado: "Terminado",
  cancelado: "Cancelado",
};

function idDePosicion() {
  return globalThis.crypto?.randomUUID?.() ?? `posicion-${Date.now()}-${Math.random()}`;
}

/** HU-05 y HU-06: el chofer inicia/termina y comparte la posición del bus. */
export default function Viajes() {
  const [viajes, setViajes] = useState([]);
  const [ocupado, setOcupado] = useState(null);
  const [error, setError] = useState("");
  const [aviso, setAviso] = useState("");
  const viajeEnCurso = useMemo(
    () => viajes.find((viaje) => viaje.estado === "en_curso"),
    [viajes],
  );

  useEffect(() => {
    api.viajes().then(({ viajes: lista }) => setViajes(lista)).catch((falla) => setError(falla.causa));
  }, []);

  useEffect(() => {
    if (!viajeEnCurso) return undefined;
    if (!navigator.geolocation) {
      setAviso("Este dispositivo no permite compartir la ubicación del bus.");
      return undefined;
    }
    const seguimiento = navigator.geolocation.watchPosition(
      (posicion) => {
        api.registrarPosicion(viajeEnCurso.id, {
          id_cliente: idDePosicion(),
          latitud: posicion.coords.latitude,
          longitud: posicion.coords.longitude,
          tomada_en: new Date(posicion.timestamp).toISOString(),
        }).then(() => setAviso("Ubicación del bus compartida en tiempo real."))
          .catch((falla) => setAviso(falla.esDeRed ? "Sin señal: se conserva la última posición enviada." : falla.causa));
      },
      () => setAviso("No se pudo leer la ubicación. Revisa el permiso del navegador."),
      { enableHighAccuracy: true, maximumAge: 5_000, timeout: 15_000 },
    );
    return () => navigator.geolocation.clearWatch(seguimiento);
  }, [viajeEnCurso]);

  async function cambiarEstado(viaje, accion) {
    setOcupado(viaje.id);
    setError("");
    try {
      const { viaje: actualizado } = accion === "iniciar"
        ? await api.iniciarViaje(viaje.id)
        : await api.terminarViaje(viaje.id);
      setViajes((lista) => lista.map((item) => (item.id === actualizado.id ? actualizado : item)));
      setAviso(accion === "iniciar" ? "Viaje iniciado. Ya estás compartiendo la ubicación del bus." : "Viaje terminado.");
    } catch (falla) {
      setError(falla.causa);
    } finally {
      setOcupado(null);
    }
  }

  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="font-titulo text-2xl font-extrabold text-upb">Mis viajes</h1>
      <p className="mt-1 text-suave">Inicia tu ruta para mostrar el bus en tiempo real.</p>
      {error && <div className="mt-4"><Aviso tipo="error">{error}</Aviso></div>}
      {aviso && <div className="mt-4"><Aviso tipo="alerta">{aviso}</Aviso></div>}
      <div className="mt-6 space-y-4">
        {viajes.map((viaje) => (
          <article key={viaje.id} className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-black/5">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <h2 className="font-titulo text-lg font-bold text-upb">{viaje.ruta.nombre}</h2>
                <p className="text-suave">{viaje.fecha} · {viaje.horario.salida} · {viaje.horario.sentido}</p>
              </div>
              <span className="rounded-full bg-fondo px-3 py-1 text-sm font-semibold text-upb">
                {NOMBRE_ESTADO[viaje.estado]}
              </span>
            </div>
            {viaje.estado === "programado" && (
              <Boton className="mt-5" disabled={ocupado === viaje.id} onClick={() => cambiarEstado(viaje, "iniciar")}>
                Iniciar viaje
              </Boton>
            )}
            {viaje.estado === "en_curso" && (
              <Boton variante="peligro" className="mt-5" disabled={ocupado === viaje.id} onClick={() => cambiarEstado(viaje, "terminar")}>
                Terminar viaje
              </Boton>
            )}
          </article>
        ))}
        {!viajes.length && !error && (
          <p className="rounded-2xl bg-white p-5 text-suave shadow-sm">No tienes viajes asignados.</p>
        )}
      </div>
    </main>
  );
}
