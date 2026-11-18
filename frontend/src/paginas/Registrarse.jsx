import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router";

import { api } from "../api/cliente.js";
import Aviso from "../componentes/Aviso.jsx";
import Boton from "../componentes/Boton.jsx";
import Campo from "../componentes/Campo.jsx";
import PantallaDeAcceso from "../componentes/PantallaDeAcceso.jsx";
import { useSesion } from "../sesion/SesionContexto.jsx";

/** HU-01: crear la cuenta con el código y el correo del padrón. */
export default function Registrarse() {
  const { usuario, ingresar } = useSesion();
  const navegar = useNavigate();
  const [datos, setDatos] = useState({ codigo: "", correo: "", contrasena: "", confirmacion: "" });
  const [error, setError] = useState("");
  const [enviando, setEnviando] = useState(false);

  if (usuario) return <Navigate to="/" replace />;

  const cambiar = (campo) => (evento) => setDatos((d) => ({ ...d, [campo]: evento.target.value }));

  async function enviar(evento) {
    evento.preventDefault();
    setError("");
    setEnviando(true);
    try {
      await api.registrarse({ ...datos, codigo: datos.codigo.trim(), correo: datos.correo.trim() });
      await ingresar(datos.codigo.trim(), datos.contrasena);
      navegar("/", { replace: true });
    } catch (falla) {
      setError(falla.causa ?? "No se pudo crear la cuenta");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <PantallaDeAcceso titulo="Crear tu cuenta">
      <form onSubmit={enviar} className="space-y-4">
        <Campo etiqueta="Código de estudiante" inputMode="numeric" value={datos.codigo} onChange={cambiar("codigo")} required />
        <Campo etiqueta="Correo institucional" type="email" value={datos.correo} onChange={cambiar("correo")} autoComplete="email" required />
        <Campo
          etiqueta="Nueva contraseña para UPBus"
          tipo="password"
          value={datos.contrasena}
          onChange={cambiar("contrasena")}
          autoComplete="new-password"
          ayuda="Al menos 8 caracteres. No uses tu contraseña de UPBnet."
          required
        />
        <Campo etiqueta="Repite la contraseña" tipo="password" value={datos.confirmacion} onChange={cambiar("confirmacion")} autoComplete="new-password" required />
        {error && <Aviso tipo="error">{error}</Aviso>}
        <Boton type="submit" disabled={enviando} className="w-full">
          {enviando ? "Creando…" : "Crear cuenta"}
        </Boton>
      </form>
      <p className="text-center text-sm text-suave">
        ¿Ya tienes cuenta?{" "}
        <Link to="/ingresar" className="font-semibold text-boton hover:underline">
          Inicia sesión
        </Link>
      </p>
    </PantallaDeAcceso>
  );
}
