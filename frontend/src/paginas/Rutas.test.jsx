import { act, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import Rutas from "./Rutas.jsx";

vi.mock("../componentes/Mapa.jsx", () => ({
  default: ({ children }) => <div>{children}</div>,
}));
vi.mock("react-leaflet", () => ({
  CircleMarker: ({ children }) => <div>{children}</div>,
  Polyline: () => null,
  Tooltip: ({ children }) => <span>{children}</span>,
}));

const RUTA = {
  id: 1,
  clave: "norte",
  nombre: "Ruta Norte",
  punto_de_partida: "La Fontana",
  nota: "",
  horarios: [{ id: 1, sentido: "ingreso", salida: "06:40" }],
};

describe("Bus en vivo de una ruta (HU-06)", () => {
  afterEach(() => vi.restoreAllMocks());

  it("vuelve a buscar el viaje en curso cada 30 segundos", async () => {
    let actualizar;
    vi.spyOn(globalThis, "setInterval").mockImplementation((funcion, milisegundos) => {
      if (milisegundos === 30_000) actualizar = funcion;
      return 27;
    });
    vi.spyOn(globalThis, "clearInterval").mockImplementation(() => {});
    let consultasDeViaje = 0;
    vi.stubGlobal("fetch", vi.fn(async (url) => {
      if (url === "/api/rutas") {
        return { ok: true, status: 200, json: async () => ({ rutas: [RUTA] }) };
      }
      if (url === "/api/rutas/1") {
        return { ok: true, status: 200, json: async () => ({ ruta: { ...RUTA, horario_elegido: 1, recorrido: [], paradas: [] } }) };
      }
      if (url === "/api/viajes?ruta=1&estado=en_curso") {
        consultasDeViaje += 1;
        const viajes = consultasDeViaje === 1
          ? []
          : [{ id: 17, estado: "en_curso", ultima_posicion: null }];
        return { ok: true, status: 200, json: async () => ({ viajes }) };
      }
      return { ok: false, status: 404, json: async () => ({ causa: `sin respuesta para ${url}` }) };
    }));
    vi.stubGlobal("WebSocket", class {
      close() {}
    });

    render(<Rutas />);
    expect(await screen.findByText("No hay un bus en curso en esta ruta.")).toBeInTheDocument();
    expect(actualizar).toBeTypeOf("function");

    await act(async () => actualizar());

    await waitFor(() => expect(screen.getByText("🚌 El viaje está en curso; esperando la primera posición.")).toBeInTheDocument());
    expect(consultasDeViaje).toBe(2);
  });
});
