import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

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
  it("inicia el viaje asignado y ofrece terminarlo", async () => {
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
});
