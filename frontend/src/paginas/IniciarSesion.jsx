import { useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router";

import Aviso from "../componentes/Aviso.jsx";
import Boton from "../componentes/Boton.jsx";
import Campo from "../componentes/Campo.jsx";
import PantallaDeAcceso from "../componentes/PantallaDeAcceso.jsx";
import { useSesion } from "../sesion/SesionContexto.jsx";

/** HU-02: entrar con código o correo y contraseña. */
export default function IniciarSesion() {
  const { usuario, ingresar } = useSesion();
  const navegar = useNavigate();
  const ubicacion = useLocation();
  const [identificador, setIdentificador] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [error, setError] = useState("");
  const [enviando, setEnviando] = useState(false);

  if (usuario) return <Navigate to="/" replace />;

  async function enviar(evento) {
    evento.preventDefault();
    setError("");
    setEnviando(true);
    try {
      await ingresar(identificador.trim(), contrasena);
      navegar(ubicacion.state?.desde ?? "/", { replace: true });
    } catch (falla) {
      setError(falla.causa ?? "No se pudo iniciar sesión");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <PantallaDeAcceso titulo="Iniciar sesión">
      <form onSubmit={enviar} className="space-y-4">
        <Campo
          etiqueta="Código o correo"
          value={identificador}
          onChange={(e) => setIdentificador(e.target.value)}
          autoComplete="username"
          required
        />
        <Campo
          etiqueta="Contraseña de UPBus"
          tipo="password"
          value={contrasena}
          onChange={(e) => setContrasena(e.target.value)}
          autoComplete="current-password"
          required
        />
        {error && <Aviso tipo="error">{error}</Aviso>}
        <Boton type="submit" disabled={enviando} className="w-full">
          {enviando ? "Entrando…" : "Acceder"}
        </Boton>
      </form>
      <p className="text-center text-sm text-suave">
        ¿Primera vez?{" "}
        <Link to="/registrarse" className="font-semibold text-boton hover:underline">
          Crea tu cuenta
        </Link>
      </p>
    </PantallaDeAcceso>
  );
}
