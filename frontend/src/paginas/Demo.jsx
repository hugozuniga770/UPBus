import { useEffect, useState } from "react";

import { api } from "../api/cliente.js";
import Aviso from "../componentes/Aviso.jsx";
import Boton from "../componentes/Boton.jsx";

const ESTADO = { en_curso: "En curso", terminada: "Terminada", detenida: "Detenida", fallo: "Falló" };
const COLOR = {
  en_curso: "bg-celeste/30 text-upb",
  terminada: "bg-[#e7f6ea] text-[#1d5b2c]",
  detenida: "bg-fondo text-suave",
  fallo: "bg-[#fdecea] text-[#8a1c13]",
};
const NOMBRE_DEL_ESCENARIO = { recorrido: "Recorrido", no_se_presenta: "No se presenta" };
const campo = "mt-1 w-full rounded-xl border border-black/10 bg-white px-3 py-2.5";

/** T23: el administrador corre escenarios con los mismos servicios que la app. */
export default function Demo() {
  const [escenarios, setEscenarios] = useState([]);
  const [simulaciones, setSimulaciones] = useState([]);
  const [rutas, setRutas] = useState([]);
  const [paradas, setParadas] = useState([]);
  const [datos, setDatos] = useState({ escenario: "recorrido", ruta: "", velocidad: 10, parada: "" });
  const [mensaje, setMensaje] = useState(null);

  const cargar = () =>
    api
      .simulaciones()
      .then(({ escenarios: lista, simulaciones: corridas }) => {
        setEscenarios(lista);
        setSimulaciones(corridas);
      })
      .catch((falla) => setMensaje({ tipo: "error", texto: falla.causa }));

  useEffect(() => {
    cargar();
    api
      .rutas()
      .then(({ rutas: lista }) => {
        setRutas(lista);
        const sur = lista.find((r) => r.clave === "sur") ?? lista[0];
        if (sur) setDatos((d) => ({ ...d, ruta: String(sur.id) }));
      })
      .catch((falla) => setMensaje({ tipo: "error", texto: falla.causa }));
  }, []);

  useEffect(() => {
    if (!datos.ruta) return;
    api
      .ruta(datos.ruta)
      .then(({ ruta }) => setParadas(ruta.paradas.filter((p) => p.estado === "aprobada")))
      .catch(() => setParadas([]));
  }, [datos.ruta]);

  const hayEnCurso = simulaciones.some((s) => s.estado === "en_curso");
  const hayActiva = simulaciones.some((s) => s.estado === "en_curso" && !s.deteniendo);
  useEffect(() => {
    if (!hayEnCurso) return undefined;
    const intervalo = setInterval(cargar, 3000);
    return () => clearInterval(intervalo);
  }, [hayEnCurso]);

  const cambiar = (nombre) => (evento) => setDatos((d) => ({ ...d, [nombre]: evento.target.value }));
  const descripcion = escenarios.find((e) => e.clave === datos.escenario)?.descripcion;

  async function iniciar(evento) {
    evento.preventDefault();
    const envio = { escenario: datos.escenario, ruta: Number(datos.ruta), velocidad: Number(datos.velocidad) };
    if (datos.escenario === "no_se_presenta" && datos.parada) envio.parada = Number(datos.parada);
    try {
      const { simulacion } = await api.iniciarSimulacion(envio);
      setMensaje({
        tipo: "exito",
        texto: `Simulación ${simulacion.id} iniciada. Abre «Rutas» en otra pestaña o en el celular para ver el bus.`,
      });
      cargar();
    } catch (falla) {
      setMensaje({ tipo: "error", texto: falla.causa });
    }
  }

  async function detener(id) {
    try {
      await api.detenerSimulacion(id);
      cargar();
    } catch (falla) {
      setMensaje({ tipo: "error", texto: falla.causa });
    }
  }

  return (
    <main className="mx-auto grid max-w-5xl gap-6 px-4 py-8 lg:grid-cols-[22rem_1fr]">
      <form onSubmit={iniciar} className="h-fit space-y-4 rounded-2xl bg-white p-5 shadow-sm ring-1 ring-black/5">
        <div>
          <h1 className="font-titulo text-xl font-bold text-upb">Demo</h1>
          <p className="mt-1 text-sm text-suave">
            Mueve un bus por una ruta grabada con los mismos servicios que la app. Los viajes simulados no cambian
            las horas aproximadas.
          </p>
        </div>
        {mensaje && <Aviso tipo={mensaje.tipo}>{mensaje.texto}</Aviso>}
        <div>
          <label className="block text-sm font-semibold text-tinta">
            Escenario
            <select value={datos.escenario} onChange={cambiar("escenario")} aria-describedby="descripcion-del-escenario" className={campo}>
              {escenarios.map((e) => (
                <option key={e.clave} value={e.clave}>{NOMBRE_DEL_ESCENARIO[e.clave] ?? e.clave}</option>
              ))}
            </select>
          </label>
          {descripcion && <p id="descripcion-del-escenario" className="mt-1 text-sm text-suave">{descripcion}</p>}
        </div>
        <label className="block text-sm font-semibold text-tinta">
          Ruta
          <select value={datos.ruta} onChange={cambiar("ruta")} className={campo}>
            {rutas.map((r) => (
              <option key={r.id} value={r.id}>{r.nombre}</option>
            ))}
          </select>
        </label>
        {datos.escenario === "no_se_presenta" && (
          <label className="block text-sm font-semibold text-tinta">
            Parada del estudiante
            <select value={datos.parada} onChange={cambiar("parada")} className={campo}>
              <option value="">La segunda parada</option>
              {paradas.map((p) => (
                <option key={p.id} value={p.id}>{p.orden}. {p.nombre}</option>
              ))}
            </select>
          </label>
        )}
        <label className="block text-sm font-semibold text-tinta">
          Velocidad (veces más rápido que el real)
          <input type="number" min="1" max="60" value={datos.velocidad} onChange={cambiar("velocidad")} className={campo} />
        </label>
        <Boton type="submit" className="w-full" disabled={!datos.ruta || hayActiva}>
          Iniciar simulación
        </Boton>
        {hayActiva && <p className="text-sm text-suave">Hay una simulación en curso: espera a que termine o detenla.</p>}
      </form>

      <section className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-black/5">
        <h2 className="font-titulo text-lg font-bold text-upb">Simulaciones</h2>
        {!simulaciones.length && <p className="mt-3 text-sm text-suave">Todavía no corriste ninguna desde que arrancó el servidor.</p>}
        <ul className="mt-3 space-y-3">
          {simulaciones.map((s) => (
            <li key={s.id} className="rounded-xl bg-fondo p-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="font-semibold text-upb">
                  {s.id}. {NOMBRE_DEL_ESCENARIO[s.escenario] ?? s.escenario} · {s.ruta} · ×{s.velocidad}
                </span>
                <span className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${COLOR[s.estado]}`}>
                  {s.deteniendo ? "Deteniendo…" : ESTADO[s.estado]}
                </span>
              </div>
              {s.notas.length > 0 && (
                <ol className="mt-2 space-y-0.5 text-sm text-tinta">
                  {s.notas.slice(-5).map((nota, i) => <li key={`${s.id}-${i}`}>{nota}</li>)}
                </ol>
              )}
              {s.estado === "en_curso" && !s.deteniendo && (
                <Boton variante="secundario" className="mt-3" onClick={() => detener(s.id)}>Detener</Boton>
              )}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
