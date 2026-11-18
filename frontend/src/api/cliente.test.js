import { describe, expect, it, vi } from "vitest";

import { servidorFalso } from "../pruebas/servidorFalso.js";
import { ErrorApi, api } from "./cliente.js";

describe("cliente de la API", () => {
  it("manda el token CSRF de la cookie en cada escritura (BUS-RT-05)", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    const fetchFalso = servidorFalso({ "POST /api/sesion": [200, { usuario: { nombre: "Ismael" } }] });

    await api.ingresar("70004", "clave-segura-123");

    const [url, opciones] = fetchFalso.mock.calls[0];
    expect(url).toBe("/api/sesion");
    expect(opciones.headers["X-CSRFToken"]).toBe("abc123");
  });

  it("entrega la causa del rechazo que da el servidor (BUS-RC-01)", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    servidorFalso({ "POST /api/sesion": [400, { causa: "Código, correo o contraseña incorrectos" }] });

    const falla = await api.ingresar("70004", "otra").catch((e) => e);

    expect(falla).toBeInstanceOf(ErrorApi);
    expect(falla.causa).toBe("Código, correo o contraseña incorrectos");
    expect(falla.esDeRed).toBe(false);
  });

  it("marca la falta de señal como error de red, para reintentar", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));

    const falla = await api.marcar(1, {}).catch((e) => e);

    expect(falla.esDeRed).toBe(true);
  });
});
