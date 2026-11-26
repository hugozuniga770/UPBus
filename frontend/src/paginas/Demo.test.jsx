import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { servidorFalso } from "../pruebas/servidorFalso.js";
import Demo from "./Demo.jsx";

const ESCENARIOS = [
  { clave: "recorrido", descripcion: "El bus recorre la ruta de punta a punta." },
  { clave: "no_se_presenta", descripcion: "Un estudiante avisa y no sube." },
];
const RUTAS = [
  { id: 1, clave: "norte", nombre: "Ruta Norte", horarios: [] },
  { id: 2, clave: "sur", nombre: "Ruta Sur", horarios: [] },
];
const RUTA_SUR = {
  id: 2,
  paradas: [
    { id: 11, orden: 1, nombre: "Makro Parque", estado: "aprobada" },
    { id: 12, orden: 2, nombre: "Parque Urbano", estado: "aprobada" },
  ],
};

describe("Panel de demo (T23)", () => {
  it("inicia el escenario elegido en la Ruta Sur, con su parada y velocidad", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    const falso = servidorFalso({
      "GET /api/simulaciones": [200, { escenarios: ESCENARIOS, simulaciones: [] }],
      "GET /api/rutas": [200, { rutas: RUTAS }],
      "GET /api/rutas/2": [200, { ruta: RUTA_SUR }],
      "POST /api/simulaciones": [202, { simulacion: { id: 1, escenario: "no_se_presenta", ruta: "Ruta Sur", velocidad: 20, estado: "en_curso", deteniendo: false, viaje: 7, notas: [] } }],
    });

    render(<Demo />);
    await screen.findByRole("option", { name: "No se presenta" });
    await userEvent.selectOptions(screen.getByLabelText("Escenario"), "no_se_presenta");
    await userEvent.selectOptions(await screen.findByLabelText("Parada del estudiante"), "12");
    await userEvent.clear(screen.getByLabelText(/Velocidad/));
    await userEvent.type(screen.getByLabelText(/Velocidad/), "20");
    await userEvent.click(screen.getByRole("button", { name: "Iniciar simulación" }));

    expect(await screen.findByText(/Simulación 1 iniciada/)).toBeInTheDocument();
    const [, envio] = falso.mock.calls.find(([url, opciones]) => url === "/api/simulaciones" && opciones?.method === "POST");
    expect(JSON.parse(envio.body)).toEqual({ escenario: "no_se_presenta", ruta: 2, velocidad: 20, parada: 12 });
  });

  it("muestra la causa si la ruta no tiene recorrido", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    servidorFalso({
      "GET /api/simulaciones": [200, { escenarios: ESCENARIOS, simulaciones: [] }],
      "GET /api/rutas": [200, { rutas: RUTAS }],
      "GET /api/rutas/2": [200, { ruta: { id: 2, paradas: [] } }],
      "POST /api/simulaciones": [400, { causa: "la ruta no tiene recorrido: grábala con el modo registro" }],
    });

    render(<Demo />);
    await screen.findByRole("option", { name: "Ruta Sur" });
    await userEvent.click(screen.getByRole("button", { name: "Iniciar simulación" }));

    expect(await screen.findByText("la ruta no tiene recorrido: grábala con el modo registro")).toBeInTheDocument();
  });
});
