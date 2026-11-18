import { Navigate, useLocation } from "react-router";

import { useSesion } from "./SesionContexto.jsx";

/**
 * Pide sesión y, si se indica, un rol. Es solo comodidad para la pantalla:
 * el servidor vuelve a comprobar el rol en cada operación (BUS-RF-03).
 */
export default function RutaProtegida({ roles, children }) {
  const { usuario, cargando } = useSesion();
  const ubicacion = useLocation();

  if (cargando) {
    return <div className="grid h-full place-items-center text-suave">Cargando…</div>;
  }
  if (!usuario) {
    return <Navigate to="/ingresar" replace state={{ desde: ubicacion.pathname }} />;
  }
  if (roles && !roles.includes(usuario.rol)) {
    return <Navigate to="/" replace />;
  }
  return children;
}
