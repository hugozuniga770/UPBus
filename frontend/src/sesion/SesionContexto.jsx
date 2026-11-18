import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

import { api } from "../api/cliente.js";

const SesionContexto = createContext(null);

/** Guarda quién inició sesión (HU-02). `usuario` es `undefined` mientras carga. */
export function SesionProveedor({ children }) {
  const [usuario, setUsuario] = useState(undefined);

  useEffect(() => {
    api
      .sesion()
      .then((respuesta) => setUsuario(respuesta.usuario))
      .catch(() => setUsuario(null));
  }, []);

  const ingresar = useCallback(async (identificador, contrasena) => {
    const respuesta = await api.ingresar(identificador, contrasena);
    setUsuario(respuesta.usuario);
    return respuesta.usuario;
  }, []);

  const salir = useCallback(async () => {
    await api.salir().catch(() => {});
    setUsuario(null);
  }, []);

  const valor = useMemo(
    () => ({ usuario, cargando: usuario === undefined, ingresar, salir }),
    [usuario, ingresar, salir],
  );
  return <SesionContexto value={valor}>{children}</SesionContexto>;
}

export function useSesion() {
  return useContext(SesionContexto);
}
