import { Link, Outlet, useNavigate } from "react-router";

import { useSesion } from "../sesion/SesionContexto.jsx";
import Logo from "./Logo.jsx";

const NOMBRE_DEL_ROL = { estudiante: "Estudiante", chofer: "Chofer", administrador: "Administrador" };

/** Barra superior y contenido de las pantallas con sesión. */
export default function Plantilla() {
  const { usuario, salir } = useSesion();
  const navegar = useNavigate();

  async function cerrarSesion() {
    await salir();
    navegar("/ingresar", { replace: true });
  }

  return (
    <div className="flex h-full flex-col">
      <header className="z-[1100] flex h-14 shrink-0 items-center justify-between bg-upb px-4 text-white shadow">
        <Link to="/" aria-label="Inicio">
          <Logo claro tamano={30} />
        </Link>
        <div className="flex items-center gap-3 text-sm">
          <span className="hidden text-right leading-tight sm:block">
            <span className="block font-semibold">{usuario.nombre}</span>
            <span className="block text-celeste">{NOMBRE_DEL_ROL[usuario.rol]}</span>
          </span>
          <button
            type="button"
            onClick={cerrarSesion}
            className="rounded-lg border border-white/30 px-3 py-1.5 hover:bg-white/10"
          >
            Salir
          </button>
        </div>
      </header>
      <div className="relative min-h-0 flex-1">
        <Outlet />
      </div>
    </div>
  );
}
