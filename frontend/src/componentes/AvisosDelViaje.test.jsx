import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, it, vi } from "vitest";

import { servidorFalso } from "../pruebas/servidorFalso.js";
import AvisosDelViaje from "./AvisosDelViaje.jsx";

const ISMAEL = { id: 4, nombre: "Ismael" };

it("avisa al chofer de un mensaje nuevo aunque el chat esté cerrado", async () => {
  const sockets = [];
  vi.stubGlobal("WebSocket", class {
    constructor(url) {
      this.url = url;
      sockets.push(this);
    }

    close() {}
  });
  servidorFalso({
    "GET /api/viajes/17/avisos": [200, {
      avisos: [{
        id: 8,
        estudiante: ISMAEL,
        parada: { id: 3, nombre: "Sevilla" },
        estado: "confirmado",
        ubicacion: null,
      }],
    }],
    "GET /api/viajes/17/mensajes?estudiante=4": [200, {
      mensajes: [],
      respuestas_rapidas: ["Ya llego"],
    }],
  });

  render(<AvisosDelViaje viajeId={17} />);
  await screen.findByRole("button", { name: "Chat con Ismael" });

  act(() => sockets[0].onmessage({
    data: JSON.stringify({
      tipo: "mensaje_directo_nuevo",
      estudiante: ISMAEL.id,
    }),
  }));

  const boton = await screen.findByRole("button", { name: "Chat con Ismael · 1 nuevo" });
  await userEvent.click(boton);
  await userEvent.click(await screen.findByRole("button", { name: "Cerrar" }));
  expect(screen.getByRole("button", { name: "Chat con Ismael" })).toBeInTheDocument();
});
