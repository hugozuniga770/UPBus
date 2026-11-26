import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { SesionContexto } from "../sesion/SesionContexto.jsx";
import Rutas from "./Rutas.jsx";

vi.mock("../componentes/Mapa.jsx", () => ({
  default: ({ children }) => <div>{children}</div>,
}));
vi.mock("react-leaflet", () => ({
  CircleMarker: ({ children }) => <div>{children}</div>,
  Polyline: ({ eventHandlers }) => (
    <button
      type="button"
      onClick={() => eventHandlers?.click?.({ latlng: { lat: -17.75, lng: -63.17 } })}
    >
      Recorrido simulado
    </button>
  ),
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

describe("Paradas propuestas y aprobación (HU-08)", () => {
  afterEach(() => vi.restoreAllMocks());

  it("permite proponer una parada al tocar el recorrido y aprobarla como administrador", async () => {
    document.cookie = "csrftoken=token-prueba";
    let estadoParada = "propuesta";
    const fetchMock = vi.fn(async (url, opciones) => {
      if (url === "/api/rutas") {
        return { ok: true, status: 200, json: async () => ({ rutas: [RUTA] }) };
      }
      if (url === "/api/rutas/1") {
        return {
          ok: true,
          status: 200,
          json: async () => ({
            ruta: {
              ...RUTA,
              horario_elegido: 1,
              recorrido: [[-17.72, -63.16], [-17.78, -63.18]],
              paradas: [
                { id: 10, nombre: "Parada El Cristo", latitud: -17.75, longitud: -63.17, orden: 1, estado: estadoParada, hora_aproximada: null },
              ],
            },
          }),
        };
      }
      if (url === "/api/viajes?ruta=1&estado=en_curso") {
        return { ok: true, status: 200, json: async () => ({ viajes: [] }) };
      }
      if (url === "/api/rutas/1/paradas" && opciones?.method === "POST") {
        return {
          ok: true,
          status: 201,
          json: async () => ({ parada: { id: 10, nombre: "Parada El Cristo", estado: "propuesta" } }),
        };
      }
      if (url === "/api/paradas/10/aprobar" && opciones?.method === "POST") {
        estadoParada = "aprobada";
        return {
          ok: true,
          status: 200,
          json: async () => ({ parada: { id: 10, nombre: "Parada El Cristo", estado: "aprobada" } }),
        };
      }
      return { ok: false, status: 404, json: async () => ({ causa: `sin respuesta para ${url}` }) };
    });
    vi.stubGlobal("fetch", fetchMock);
    vi.stubGlobal("WebSocket", class {
      close() {}
    });

    render(
      <SesionContexto value={{ usuario: { id: 1, nombre: "Hugo", rol: "administrador" }, cargando: false }}>
        <Rutas />
      </SesionContexto>,
    );

    const botonRecorrido = await screen.findByText("Recorrido simulado");
    fireEvent.click(botonRecorrido);

    const campoNombre = await screen.findByPlaceholderText("Nombre de la parada (ej. Plaza Principal)");
    fireEvent.change(campoNombre, { target: { value: "Parada El Cristo" } });
    fireEvent.click(screen.getByRole("button", { name: "Proponer parada" }));

    await waitFor(() => expect(screen.getByText("Parada propuesta enviada. Queda pendiente de aprobación.")).toBeInTheDocument());

    fireEvent.click(screen.getByRole("button", { name: "Aprobar" }));
    await waitFor(() => expect(screen.getByText("Parada aprobada y añadida al recorrido.")).toBeInTheDocument());
  });
});