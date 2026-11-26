import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { servidorFalso } from "../pruebas/servidorFalso.js";
import { SesionContexto } from "../sesion/SesionContexto.jsx";
import ChatDeRuta from "./ChatDeRuta.jsx";

const ISMAEL = { id: 4, nombre: "Ismael", rol: "estudiante" };

function conEstudiante(hijo) {
  return <SesionContexto value={{ usuario: ISMAEL, cargando: false }}>{hijo}</SesionContexto>;
}

const MENSAJE = {
  id: 3,
  id_cliente: "ruta-3",
  autor: ISMAEL,
  viaje: null,
  estudiante: null,
  ruta: 1,
  texto: "¿El bus ya salió?",
  enviado_en: "2026-11-16T18:15:00-04:00",
};

describe("Chat de ruta (HU-15)", () => {
  it("HU15-CA1 permite elegir la ruta y escribir en su chat", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    servidorFalso({
      "GET /api/rutas/1/miembro": [200, { es_miembro: false, puede_entrar: false }],
      "POST /api/rutas/1/miembro": [201, { miembro: { id: 2, ruta: 1, usuario: 4 } }],
      "GET /api/rutas/1/mensajes": [200, { mensajes: [] }],
      "POST /api/rutas/1/mensajes": [201, { mensaje: MENSAJE }],
    });

    render(conEstudiante(<ChatDeRuta rutaId={1} nombreRuta="Ruta Norte" />));
    await userEvent.click(await screen.findByRole("button", { name: "Elegir Ruta Norte y abrir el chat" }));
    await userEvent.type(await screen.findByLabelText("Mensaje para Ruta Norte"), "¿El bus ya salió?");
    await userEvent.click(screen.getByRole("button", { name: "Enviar" }));

    expect(await screen.findByText("¿El bus ya salió?")).toBeInTheDocument();
    expect(screen.getByText("Ismael").parentElement).toHaveTextContent("18:15");
  });

  it("HU15-CA2 muestra la causa al rechazar una ruta ajena", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    servidorFalso({
      "GET /api/rutas/2/miembro": [200, { es_miembro: true, puede_entrar: true }],
      "GET /api/rutas/2/mensajes": [200, { mensajes: [] }],
      "POST /api/rutas/2/mensajes": [400, { causa: "no eres parte de esta ruta" }],
    });

    render(conEstudiante(<ChatDeRuta rutaId={2} nombreRuta="Ruta Sur" />));
    await userEvent.type(await screen.findByLabelText("Mensaje para Ruta Sur"), "Hola");
    await userEvent.click(screen.getByRole("button", { name: "Enviar" }));

    expect(await screen.findByText("no eres parte de esta ruta")).toBeInTheDocument();
  });
});
