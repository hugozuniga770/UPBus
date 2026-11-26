import { Link } from "react-router";

import { useSesion } from "../sesion/SesionContexto.jsx";

const TARJETAS = {
  rutas: { titulo: "Rutas y horarios", texto: "Recorridos, paradas y la hora aproximada en cada una.", a: "/rutas", icono: "🗺️" },
  registro: { titulo: "Modo registro", texto: "Marca las paradas en un viaje real para que UPBus las aprenda.", a: "/modo-registro", icono: "📍" },
  usuarios: { titulo: "Usuarios", texto: "Crea y desactiva cuentas de choferes y estudiantes.", a: "/usuarios", icono: "👥" },
  subir: { titulo: "Voy a subir", texto: "Elige tu ruta, avisa al chofer y comparte tu ubicación.", a: "/rutas", icono: "✋" },
  creditos: { titulo: "Mis créditos", texto: "Recarga y paga tus viajes desde la app.", pendiente: "HU-11", icono: "💳" },
  viajes: { titulo: "Mis viajes", texto: "Inicia tu ruta y comparte la ubicación del bus.", a: "/viajes", icono: "🚌" },
};

const POR_ROL = {
  estudiante: ["rutas", "subir", "creditos"],
  chofer: ["viajes", "registro", "rutas"],
  administrador: ["rutas", "registro", "usuarios", "subir", "creditos"],
};

function Tarjeta({ titulo, texto, a, icono, pendiente }) {
  const contenido = (
    <>
      <span className="text-3xl" aria-hidden="true">{icono}</span>
      <span className="mt-3 block font-titulo text-lg font-bold text-upb">{titulo}</span>
      <span className="mt-1 block text-suave">{texto}</span>
      {pendiente && (
        <span className="mt-3 inline-block rounded-full bg-fondo px-2.5 py-0.5 text-xs font-semibold text-suave">
          Próximamente · {pendiente}
        </span>
      )}
    </>
  );
  const clase = "block rounded-2xl bg-white p-5 shadow-sm ring-1 ring-black/5";
  if (pendiente) return <div className={`${clase} opacity-70`}>{contenido}</div>;
  return (
    <Link to={a} className={`${clase} transition hover:-translate-y-0.5 hover:shadow-md`}>
      {contenido}
    </Link>
  );
}

/** Inicio: cada rol ve sus funciones (BUS-RF-03). */
export default function Inicio() {
  const { usuario } = useSesion();
  const primerNombre = usuario.nombre.split(" ")[0];
  return (
    <main className="mx-auto max-w-4xl px-4 py-8">
      <h1 className="font-titulo text-2xl font-extrabold text-upb">Hola, {primerNombre}</h1>
      <p className="mt-1 text-suave">¿Qué quieres hacer hoy?</p>
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {POR_ROL[usuario.rol].map((clave) => (
          <Tarjeta key={clave} {...TARJETAS[clave]} />
        ))}
      </div>
    </main>
  );
}
