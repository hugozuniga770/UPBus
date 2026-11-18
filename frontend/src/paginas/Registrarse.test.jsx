import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { describe, expect, it } from "vitest";

import { servidorFalso } from "../pruebas/servidorFalso.js";
import { SesionProveedor } from "../sesion/SesionContexto.jsx";
import Registrarse from "./Registrarse.jsx";

describe("Crear cuenta (HU-01)", () => {
  it("HU01-CA3 muestra la causa cuando las contraseñas no coinciden", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    const fetchFalso = servidorFalso({
      "GET /api/sesion": [200, { usuario: null }],
      "POST /api/registro": [400, { causa: "las contraseñas no coinciden" }],
    });
    render(
      <MemoryRouter>
        <SesionProveedor>
          <Registrarse />
        </SesionProveedor>
      </MemoryRouter>,
    );

    await userEvent.type(screen.getByLabelText("Código de estudiante"), "70004");
    await userEvent.type(screen.getByLabelText("Correo institucional"), "ismael@upb.example");
    await userEvent.type(screen.getByLabelText("Nueva contraseña para UPBus"), "clave-segura-123");
    await userEvent.type(screen.getByLabelText("Repite la contraseña"), "otra-clave-456");
    await userEvent.click(screen.getByRole("button", { name: "Crear cuenta" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("las contraseñas no coinciden");
    const envio = fetchFalso.mock.calls.find(([url]) => url === "/api/registro");
    expect(JSON.parse(envio[1].body)).toMatchObject({ codigo: "70004", confirmacion: "otra-clave-456" });
  });
});
