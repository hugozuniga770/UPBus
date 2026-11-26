/**
 * Cliente de la API de Django.
 *
 * - Usa la cookie de sesión de Django (BUS-RT-05).
 * - En cada escritura manda el token CSRF de la cookie `csrftoken`.
 * - Todo error llega como `ErrorApi` con la causa que dio el servidor
 *   (BUS-RC-01). `esDeRed` indica que vale la pena reintentar más tarde.
 */
export class ErrorApi extends Error {
  constructor(causa, estado, esDeRed = false) {
    super(causa);
    this.causa = causa;
    this.estado = estado;
    this.esDeRed = esDeRed;
  }
}

export function leerCookie(nombre) {
  const fila = document.cookie.split("; ").find((cookie) => cookie.startsWith(`${nombre}=`));
  return fila ? decodeURIComponent(fila.slice(nombre.length + 1)) : "";
}

let pidiendoCsrf = null;

async function asegurarCsrf() {
  if (leerCookie("csrftoken")) return;
  pidiendoCsrf ??= fetch("/api/sesion/csrf", { credentials: "same-origin" }).finally(() => {
    pidiendoCsrf = null;
  });
  await pidiendoCsrf;
}

export async function pedir(metodo, ruta, datos) {
  const escribe = metodo !== "GET";
  if (escribe) {
    try {
      await asegurarCsrf();
    } catch {
      throw new ErrorApi("sin conexión con el servidor", 0, true);
    }
  }
  const cabeceras = { Accept: "application/json" };
  if (datos !== undefined) cabeceras["Content-Type"] = "application/json";
  if (escribe) cabeceras["X-CSRFToken"] = leerCookie("csrftoken");

  let respuesta;
  try {
    respuesta = await fetch(`/api${ruta}`, {
      method: metodo,
      credentials: "same-origin",
      headers: cabeceras,
      body: datos !== undefined ? JSON.stringify(datos) : undefined,
    });
  } catch {
    throw new ErrorApi("sin conexión con el servidor", 0, true);
  }
  if (respuesta.status === 204) return null;
  const cuerpo = await respuesta.json().catch(() => null);
  if (!respuesta.ok) {
    const causa = cuerpo?.causa ?? `el servidor respondió con el error ${respuesta.status}`;
    throw new ErrorApi(causa, respuesta.status, respuesta.status >= 500);
  }
  return cuerpo;
}

export const api = {
  // HU-01 y HU-02
  sesion: () => pedir("GET", "/sesion"),
  ingresar: (identificador, contrasena) => pedir("POST", "/sesion", { identificador, contrasena }),
  salir: () => pedir("DELETE", "/sesion"),
  registrarse: (datos) => pedir("POST", "/registro", datos),
  // HU-03
  usuarios: () => pedir("GET", "/usuarios"),
  crearUsuario: (datos) => pedir("POST", "/usuarios", datos),
  desactivarUsuario: (id) => pedir("DELETE", `/usuarios/${id}`),
  // HU-04
  rutas: () => pedir("GET", "/rutas"),
  ruta: (id, horario) => pedir("GET", `/rutas/${id}${horario ? `?horario=${horario}` : ""}`),
  // HU-05 y HU-06
  viajes: (filtros = {}) => {
    const consulta = new URLSearchParams(
      Object.entries(filtros).filter(([, valor]) => valor !== undefined && valor !== null && valor !== ""),
    );
    return pedir("GET", `/viajes${consulta.size ? `?${consulta}` : ""}`);
  },
  viaje: (id) => pedir("GET", `/viajes/${id}`),
  iniciarViaje: (id) => pedir("POST", `/viajes/${id}/iniciar`),
  terminarViaje: (id) => pedir("POST", `/viajes/${id}/terminar`),
  registrarPosicion: (id, posicion) => pedir("POST", `/viajes/${id}/posiciones`, posicion),

  // HU-07
  avisar: (viajeId, paradaId) => pedir("POST", `/viajes/${viajeId}/avisos`, { parada: paradaId }),
  miAviso: (viajeId) => pedir("GET", `/viajes/${viajeId}/mi-aviso`),
  avisosDelViaje: (viajeId) => pedir("GET", `/viajes/${viajeId}/avisos`),
  cancelarAviso: (avisoId) => pedir("POST", `/avisos/${avisoId}/cancelar`),
  compartirUbicacion: (avisoId, ubicacion) => pedir("POST", `/avisos/${avisoId}/ubicacion`, ubicacion),
  // HU-18
  iniciarRegistro: (datos) => pedir("POST", "/registros", datos),
  registroEnCurso: () => pedir("GET", "/registros/en-curso"),
  marcar: (registroId, marca) => pedir("POST", `/registros/${registroId}/marcas`, marca),
  enviarPuntos: (registroId, puntos) => pedir("POST", `/registros/${registroId}/puntos`, { puntos }),
  terminarRegistro: (registroId) => pedir("POST", `/registros/${registroId}/terminar`),
  cancelarRegistro: (registroId) => pedir("POST", `/registros/${registroId}/cancelar`),
};
