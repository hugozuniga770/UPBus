import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { SesionContexto } from "../sesion/SesionContexto.jsx";
import Rutas from "./Rutas.jsx";

// El mapa de mentira muestra a qué apunta la cámara y deja simular que se arrastra.
vi.mock("../componentes/Mapa.jsx", () => ({
  default: ({ children, foco, claveEncuadre, alArrastrar }) => (
    <div
      data-testid="mapa"
      data-foco={foco ? `${foco.clave} ${foco.punto.join(",")}` : ""}
      data-encuadre={claveEncuadre ?? ""}
    >
      <button type="button" onClick={alArrastrar}>Arrastrar el mapa</button>
      {children}
    </div>
  ),
}));
vi.mock("react-leaflet", () => ({
  CircleMarker: ({ children, eventHandlers }) => <div onClick={eventHandlers?.click}>{children}</div>,
  Pane: ({ children }) => <div>{children}</div>,
  Polyline: ({ eventHandlers }) => (eventHandlers ? (
    <button
      type="button"
      onClick={() => eventHandlers.click({ latlng: { lat: -17.75, lng: -63.17 } })}
    >
      Recorrido simulado
    </button>
  ) : null),
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

  it("HU08-CA1 y HU08-CA4 propone una parada tocando el recorrido y el administrador la aprueba", async () => {
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

describe("Cámara del mapa (soporte de HU-06)", () => {
  afterEach(() => vi.restoreAllMocks());

  const PARADA = { id: 10, nombre: "Parada El Cristo", latitud: -17.75, longitud: -63.17, orden: 1, estado: "aprobada", hora_aproximada: "06:52" };

  function servidor(viajes = []) {
    vi.stubGlobal("fetch", vi.fn(async (url) => {
      if (url === "/api/rutas") {
        return { ok: true, status: 200, json: async () => ({ rutas: [RUTA] }) };
      }
      if (url.startsWith("/api/rutas/1")) {
        return {
          ok: true,
          status: 200,
          json: async () => ({
            ruta: { ...RUTA, horario_elegido: 1, recorrido: [[-17.72, -63.16], [-17.78, -63.18]], paradas: [PARADA] },
          }),
        };
      }
      if (url === "/api/viajes?ruta=1&estado=en_curso") {
        return { ok: true, status: 200, json: async () => ({ viajes }) };
      }
      return { ok: true, status: 200, json: async () => ({}) };
    }));
    vi.stubGlobal("WebSocket", class {
      close() {}
    });
  }

  it("muestra la ruta entera cuando llega y otra vez con «Toda la ruta»", async () => {
    servidor();
    render(<Rutas />);
    await screen.findByRole("heading", { name: "Ruta Norte" });
    expect(screen.getByTestId("mapa")).toHaveAttribute("data-encuadre", "1-0");

    fireEvent.click(screen.getByRole("button", { name: "🗺️ Toda la ruta" }));

    expect(screen.getByTestId("mapa")).toHaveAttribute("data-encuadre", "1-1");
  });

  it("tocar una parada, en la lista o en el mapa, lleva la cámara a esa parada", async () => {
    servidor();
    render(<Rutas />);
    await screen.findByRole("heading", { name: "Ruta Norte" });
    expect(screen.getByTestId("mapa")).toHaveAttribute("data-foco", "");

    fireEvent.click(screen.getByRole("button", { name: /Parada El Cristo/ }));
    expect(screen.getByTestId("mapa")).toHaveAttribute("data-foco", "parada-1 -17.75,-63.17");

    fireEvent.click(screen.getByText("1. Parada El Cristo · 06:52"));
    expect(screen.getByTestId("mapa")).toHaveAttribute("data-foco", "parada-2 -17.75,-63.17");
  });

  it("sigue al bus hasta que la persona mueve el mapa, y tocar el bus lo vuelve a seguir", async () => {
    servidor([{
      id: 17,
      estado: "en_curso",
      simulado: true,
      ultima_posicion: { latitud: -17.76, longitud: -63.17, tomada_en: "2026-11-27T07:00:00-04:00" },
    }]);
    render(<Rutas />);
    const seguir = await screen.findByRole("button", { name: "🚌 Seguir al bus" });
    expect(seguir).toHaveAttribute("aria-pressed", "false");

    fireEvent.click(seguir);
    expect(screen.getByRole("button", { name: "🚌 Siguiendo al bus" })).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByTestId("mapa")).toHaveAttribute("data-foco", "bus -17.76,-63.17");

    fireEvent.click(screen.getByRole("button", { name: "Arrastrar el mapa" }));
    expect(screen.getByRole("button", { name: "🚌 Seguir al bus" })).toHaveAttribute("aria-pressed", "false");
    expect(screen.getByTestId("mapa")).toHaveAttribute("data-foco", "");

    fireEvent.click(screen.getByText("🧪 Bus simulado"));
    expect(screen.getByTestId("mapa")).toHaveAttribute("data-foco", "bus -17.76,-63.17");
  });
});
