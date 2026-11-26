import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { servidorFalso } from "../pruebas/servidorFalso.js";
import { SesionContexto } from "../sesion/SesionContexto.jsx";
import ChatDirecto from "./ChatDirecto.jsx";

const ISMAEL = { id: 4, nombre: "Ismael", rol: "estudiante" };
const MARCO = { id: 8, nombre: "Marco", rol: "chofer" };

function conSesion(usuario, hijo) {
  return <SesionContexto value={{ usuario, cargando: false }}>{hijo}</SesionContexto>;
}

function mensaje(autor, texto, id = 1) {
  return {
    id,
    id_cliente: `mensaje-${id}`,
    autor,
    viaje: 17,
    estudiante: ISMAEL.id,
    ruta: null,
    texto,
    enviado_en: "2026-11-16T06:50:00-04:00",
  };
}

describe("Chat directo (HU-14)", () => {
  it("HU14-CA1 muestra al chofer el mensaje con nombre y hora", async () => {
    servidorFalso({
      "GET /api/viajes/17/mensajes?estudiante=4": [
        200,
        { mensajes: [mensaje(ISMAEL, "Ya estoy en la parada")], respuestas_rapidas: ["Ya llego"] },
      ],
    });

    render(conSesion(MARCO, <ChatDirecto viajeId={17} estudiante={ISMAEL} esChofer />));
    await userEvent.click(screen.getByRole("button", { name: "Chat con Ismael" }));

    expect(await screen.findByText("Ya estoy en la parada")).toBeInTheDocument();
    expect(screen.getByText("Ismael").parentElement).toHaveTextContent("06:50");
  });

  it("HU14-CA2 explica que debe confirmar Voy a subir", async () => {
    servidorFalso({
      "GET /api/viajes/17/mensajes": [400, { causa: "no estás en este viaje" }],
    });

    render(conSesion(ISMAEL, <ChatDirecto viajeId={17} />));
    await userEvent.click(screen.getByRole("button", { name: "Chat con el chofer" }));

    expect(await screen.findByText("Confirma “Voy a subir” para chatear con el chofer.")).toBeInTheDocument();
  });

  it("HU14-CA3 envía una respuesta rápida sin escribir", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    const respuesta = mensaje(MARCO, "Ya llego", 2);
    const fetchFalso = servidorFalso({
      "GET /api/viajes/17/mensajes?estudiante=4": [
        200,
        { mensajes: [], respuestas_rapidas: ["Ya llego", "Te espero 1 min"] },
      ],
      "POST /api/viajes/17/mensajes": [201, { mensaje: respuesta }],
    });

    render(conSesion(MARCO, <ChatDirecto viajeId={17} estudiante={ISMAEL} esChofer />));
    await userEvent.click(screen.getByRole("button", { name: "Chat con Ismael" }));
    await userEvent.click(await screen.findByRole("button", { name: "Ya llego" }));

    expect(await screen.findByText("Ya llego", { selector: "p" })).toBeInTheDocument();
    const opciones = fetchFalso.mock.calls.find(([url, config]) => (
      url === "/api/viajes/17/mensajes" && config.method === "POST"
    ))[1];
    expect(JSON.parse(opciones.body)).toMatchObject({ estudiante: 4, respuesta_rapida: "Ya llego" });
  });
});
