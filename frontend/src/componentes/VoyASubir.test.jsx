import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { servidorFalso } from "../pruebas/servidorFalso.js";
import { SesionContexto } from "../sesion/SesionContexto.jsx";
import AvisosDelViaje from "./AvisosDelViaje.jsx";
import VoyASubir from "./VoyASubir.jsx";

const VIAJE = {
  id: 17,
  ruta: { id: 1, clave: "norte", nombre: "Ruta Norte" },
  horario: { id: 3, sentido: "ingreso", salida: "06:40" },
  fecha: "2026-11-16",
  estado: "en_curso",
};
const PARADAS = [
  { id: 5, nombre: "Sevilla", estado: "aprobada" },
  { id: 6, nombre: "Av. Banzer y 4to anillo", estado: "propuesta" },
];

function conEstudiante(hijo) {
  const sesion = { usuario: { id: 4, nombre: "Ismael", rol: "estudiante" }, cargando: false };
  return <SesionContexto value={sesion}>{hijo}</SesionContexto>;
}

describe("Voy a subir (HU-07)", () => {
  it("HU07-CA1 avisa que va a subir en su parada y ofrece cancelar", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    servidorFalso({
      "GET /api/viajes?ruta=1": [200, { viajes: [VIAJE] }],
      "GET /api/viajes/17/mi-aviso": [200, { aviso: null }],
      "POST /api/viajes/17/avisos": [201, { aviso: { id: 9, estado: "confirmado", parada: { id: 5, nombre: "Sevilla" } } }],
    });

    render(conEstudiante(<VoyASubir rutaId={1} horarioId={3} paradas={PARADAS} />));
    const opciones = await screen.findAllByRole("option");
    expect(opciones.map((o) => o.textContent)).toEqual(["Elige tu parada", "Sevilla"]);
    await userEvent.selectOptions(screen.getByRole("combobox"), "5");
    await userEvent.click(screen.getByRole("button", { name: "Voy a subir" }));

    expect(await screen.findByText("Sevilla", { selector: "strong" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Cancelar" })).toBeInTheDocument();
  });

  it("HU07-CA2 muestra la causa si ya avisó en ese viaje", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    servidorFalso({
      "GET /api/viajes?ruta=1": [200, { viajes: [VIAJE] }],
      "GET /api/viajes/17/mi-aviso": [200, { aviso: null }],
      "POST /api/viajes/17/avisos": [400, { causa: "ya avisaste que vas a subir en este viaje" }],
    });

    render(conEstudiante(<VoyASubir rutaId={1} horarioId={3} paradas={PARADAS} />));
    await userEvent.selectOptions(await screen.findByRole("combobox"), "5");
    await userEvent.click(screen.getByRole("button", { name: "Voy a subir" }));

    expect(await screen.findByText("ya avisaste que vas a subir en este viaje")).toBeInTheDocument();
  });

  it("HU10-CA1 permite al estudiante marcar «He subido»", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    servidorFalso({
      "GET /api/viajes?ruta=1": [200, { viajes: [VIAJE] }],
      "GET /api/viajes/17/mi-aviso": [200, { aviso: { id: 9, estado: "confirmado", parada: { id: 5, nombre: "Sevilla" } } }],
      "POST /api/avisos/9/subio": [200, { aviso: { id: 9, estado: "a_bordo", parada: { id: 5, nombre: "Sevilla" } } }],
    });

    render(conEstudiante(<VoyASubir rutaId={1} horarioId={3} paradas={PARADAS} />));
    await userEvent.click(await screen.findByRole("button", { name: "He subido" }));

    expect(await screen.findByText("Ya estás a bordo. ¡Buen viaje!")).toBeInTheDocument();
  });
});

describe("Lista de abordaje del chofer (HU-10)", () => {
  it("HU10-CA2 y CA4 permiten al chofer marcar Subió y ver quién ya subió", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    const avisoConfirmado = {
      id: 9,
      estado: "confirmado",
      estudiante: { id: 4, nombre: "Ismael" },
      parada: { id: 5, nombre: "Sevilla" },
      ubicacion: null,
    };
    servidorFalso({
      "GET /api/viajes/17/avisos": [200, { avisos: [avisoConfirmado] }],
      "POST /api/avisos/9/subio": [200, { aviso: { ...avisoConfirmado, estado: "a_bordo" } }],
    });

    render(<AvisosDelViaje viajeId={17} />);
    const botonSubio = await screen.findByRole("button", { name: "Subió" });

    servidorFalso({
      "GET /api/viajes/17/avisos": [200, { avisos: [{ ...avisoConfirmado, estado: "a_bordo" }] }],
      "POST /api/avisos/9/subio": [200, { aviso: { ...avisoConfirmado, estado: "a_bordo" } }],
    });
    await userEvent.click(botonSubio);

    expect(await screen.findByText("Ya subieron (1)")).toBeInTheDocument();
    expect(screen.getByText("A bordo")).toBeInTheDocument();
  });
});