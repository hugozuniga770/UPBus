import { useEffect, useRef, useState } from "react";

import { api } from "../api/cliente.js";
import { useSesion } from "../sesion/SesionContexto.jsx";
import Aviso from "./Aviso.jsx";
import Boton from "./Boton.jsx";

const SEGUNDOS_ENTRE_UBICACIONES = 15;

/**
 * HU-07: el estudiante avisa «Voy a subir» en su parada, lo cancela mientras el bus
 * no pasó y, si quiere, comparte su ubicación con el chofer (BUS-RF-08, BUS-RF-09).
 */
export default function VoyASubir({ rutaId, horarioId, paradas }) {
  const usuario = useSesion()?.usuario;
  const puedeAvisar = ["estudiante", "administrador"].includes(usuario?.rol);
  const [viaje, setViaje] = useState(null);
  const [aviso, setAviso] = useState(null);
  const [paradaId, setParadaId] = useState("");
  const [compartiendo, setCompartiendo] = useState(false);
  const [ocupado, setOcupado] = useState(false);
  const [error, setError] = useState("");
  const ultimoEnvio = useRef(0);

  useEffect(() => {
    if (!puedeAvisar || !rutaId) return undefined;
    let vigente = true;
    const consultar = () => {
      api.viajes({ ruta: rutaId })
        .then(({ viajes }) => {
          if (!vigente) return;
          const abiertos = viajes.filter(
            (v) => ["programado", "en_curso"].includes(v.estado) && (!horarioId || v.horario.id === horarioId),
          );
          setViaje(abiertos.find((v) => v.estado === "en_curso") ?? abiertos[0] ?? null);
        })
        .catch((falla) => setError(falla.causa));
    };
    consultar();
    const intervalo = setInterval(consultar, 30_000);
    return () => {
      vigente = false;
      clearInterval(intervalo);
    };
  }, [puedeAvisar, rutaId, horarioId]);

  const viajeId = viaje?.id;
  useEffect(() => {
    setAviso(null);
    if (!viajeId) return undefined;
    let vigente = true;
    api.miAviso(viajeId)
      .then(({ aviso: actual }) => vigente && setAviso(actual))
      .catch((falla) => setError(falla.causa));
    return () => { vigente = false; };
  }, [viajeId]);

  const avisoConfirmado = aviso?.estado === "confirmado" ? aviso.id : null;
  useEffect(() => {
    if (!compartiendo || !avisoConfirmado) return undefined;
    if (!navigator.geolocation) {
      setError("Este dispositivo no permite compartir tu ubicación.");
      return undefined;
    }
    const seguimiento = navigator.geolocation.watchPosition(
      (posicion) => {
        if (posicion.timestamp - ultimoEnvio.current < SEGUNDOS_ENTRE_UBICACIONES * 1000) return;
        ultimoEnvio.current = posicion.timestamp;
        api.compartirUbicacion(avisoConfirmado, {
          latitud: posicion.coords.latitude,
          longitud: posicion.coords.longitude,
          tomada_en: new Date(posicion.timestamp).toISOString(),
        }).catch((falla) => !falla.esDeRed && setError(falla.causa));
      },
      () => setError("No se pudo leer tu ubicación. Revisa el permiso del navegador."),
      { enableHighAccuracy: true, maximumAge: 10_000, timeout: 20_000 },
    );
    return () => navigator.geolocation.clearWatch(seguimiento);
  }, [compartiendo, avisoConfirmado]);

  async function hacer(accion) {
    setOcupado(true);
    setError("");
    try {
      await accion();
    } catch (falla) {
      setError(falla.causa);
    } finally {
      setOcupado(false);
    }
  }

  if (!puedeAvisar || !viaje) return null;
  const elegibles = paradas.filter((parada) => parada.estado === "aprobada");

  return (
    <div className="mt-3 rounded-xl border border-celeste/60 px-3 py-3">
      <p className="text-sm font-semibold text-upb">
        Viaje de las {viaje.horario.salida} · {viaje.estado === "en_curso" ? "en curso" : "programado"}
      </p>
      {error && <div className="mt-2"><Aviso tipo="error">{error}</Aviso></div>}
      {aviso?.estado === "confirmado" && (
        <>
          <p className="mt-2 text-sm">Vas a subir en <strong>{aviso.parada.nombre}</strong>. El chofer ya lo sabe.</p>
          <div className="mt-3 flex flex-wrap gap-2">
            <Boton variante="secundario" onClick={() => setCompartiendo((actual) => !actual)}>
              {compartiendo ? "Dejar de compartir mi ubicación" : "Compartir mi ubicación"}
            </Boton>
            <Boton
              variante="peligro"
              disabled={ocupado}
              onClick={() => hacer(async () => {
                await api.cancelarAviso(aviso.id);
                setCompartiendo(false);
                setAviso(null);
              })}
            >
              Cancelar
            </Boton>
          </div>
        </>
      )}
      {aviso?.estado === "a_bordo" && <p className="mt-2 text-sm">Ya estás a bordo. ¡Buen viaje!</p>}
      {!aviso && (
        <div className="mt-2 flex flex-wrap items-end gap-2">
          <label className="text-sm">
            <span className="block text-suave">Tu parada</span>
            <select
              value={paradaId}
              onChange={(evento) => setParadaId(evento.target.value)}
              className="mt-1 rounded-lg bg-campo px-2 py-1.5"
            >
              <option value="">Elige tu parada</option>
              {elegibles.map((parada) => (
                <option key={parada.id} value={parada.id}>{parada.nombre}</option>
              ))}
            </select>
          </label>
          <Boton
            variante="acento"
            disabled={!paradaId || ocupado}
            onClick={() => hacer(async () => {
              const { aviso: nuevo } = await api.avisar(viaje.id, Number(paradaId));
              setAviso(nuevo);
            })}
          >
            Voy a subir
          </Boton>
        </div>
      )}
    </div>
  );
}
