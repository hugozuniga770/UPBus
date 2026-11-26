import { act, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { servidorFalso } from "../pruebas/servidorFalso.js";
import Viajes from "./Viajes.jsx";

const VIAJE = {
  id: 17,
  ruta: { id: 1, clave: "norte", nombre: "Ruta Norte" },
  horario: { id: 1, sentido: "ingreso", salida: "06:40" },
  fecha: "2026-11-16",
  chofer: { id: 4, nombre: "Marco" },
  estado: "programado",
  iniciado_en: null,
  terminado_en: null,
  ultima_posicion: null,
};

describe("Viajes del chofer (HU-05)", () => {
  it("HU05-CA1 inicia el viaje asignado y ofrece terminarlo", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    const fetchFalso = servidorFalso({
      "GET /api/viajes": [200, { viajes: [VIAJE] }],
      "POST /api/viajes/17/iniciar": [
        200,
        { viaje: { ...VIAJE, estado: "en_curso", iniciado_en: "2026-11-16T06:38:00-04:00" } },
      ],
    });

    render(<Viajes />);
    await userEvent.click(await screen.findByRole("button", { name: "Iniciar viaje" }));

    expect(await screen.findByRole("button", { name: "Terminar viaje" })).toBeInTheDocument();
    expect(fetchFalso).toHaveBeenCalledWith(
      "/api/viajes/17/iniciar",
      expect.objectContaining({ method: "POST" }),
    );
  });

  it("mantiene la pantalla encendida mientras el viaje está en curso", async () => {
    const pedirCandado = vi.fn().mockResolvedValue({ release: vi.fn().mockResolvedValue(undefined) });
    vi.stubGlobal("navigator", {
      geolocation: { watchPosition: vi.fn(() => 7), clearWatch: vi.fn() },
      wakeLock: { request: pedirCandado },
    });
    servidorFalso({
      "GET /api/viajes": [200, { viajes: [{ ...VIAJE, estado: "en_curso" }] }],
    });

    render(<Viajes />);

    await waitFor(() => expect(pedirCandado).toHaveBeenCalledWith("screen"));
  });

  it("limita los envíos del GPS por tiempo y distancia", async () => {
    let recibirPosicion;
    const observar = vi.fn((alCambiar) => {
      recibirPosicion = alCambiar;
      return 8;
    });
    vi.stubGlobal("navigator", {
      geolocation: { watchPosition: observar, clearWatch: vi.fn() },
    });
    document.cookie = "csrftoken=abc123; path=/";
    const fetchFalso = servidorFalso({
      "GET /api/viajes": [200, { viajes: [{ ...VIAJE, estado: "en_curso" }] }],
      "POST /api/viajes/17/posiciones": [201, { posicion: { id: 1 } }],
    });
    render(<Viajes />);
    await screen.findByRole("button", { name: "Terminar viaje" });

    const posicion = (latitud, timestamp) => ({
      coords: { latitude: latitud, longitude: -63.1800 },
      timestamp: Date.parse(timestamp),
    });
    await act(async () => recibirPosicion(posicion(-17.7700, "2026-11-25T10:00:00-04:00")));
    await waitFor(() => {
      const envios = fetchFalso.mock.calls.filter(([url]) => url === "/api/viajes/17/posiciones");
      expect(envios).toHaveLength(1);
    });

    await act(async () => recibirPosicion(posicion(-17.77001, "2026-11-25T10:00:01-04:00")));
    await act(async () => recibirPosicion(posicion(-17.7697, "2026-11-25T10:00:06-04:00")));
    await waitFor(() => {
      const envios = fetchFalso.mock.calls.filter(([url]) => url === "/api/viajes/17/posiciones");
      expect(envios).toHaveLength(2);
    });
  });
});
