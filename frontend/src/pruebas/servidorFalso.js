import { vi } from "vitest";

/** Reemplaza `fetch` con respuestas fijas: { "POST /api/sesion": [400, { causa }] }. */
export function servidorFalso(respuestas) {
  const falso = vi.fn(async (url, opciones = {}) => {
    const clave = `${opciones.method ?? "GET"} ${url}`;
    const [estado, cuerpo] = respuestas[clave] ?? [404, { causa: `sin respuesta para ${clave}` }];
    return { ok: estado < 400, status: estado, json: async () => cuerpo };
  });
  vi.stubGlobal("fetch", falso);
  return falso;
}
