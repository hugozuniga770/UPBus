import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { describe, expect, it } from "vitest";

import { servidorFalso } from "../pruebas/servidorFalso.js";
import { SesionProveedor } from "../sesion/SesionContexto.jsx";
import IniciarSesion from "./IniciarSesion.jsx";

describe("Iniciar sesión (HU-02)", () => {
  it("HU02-CA3 muestra el único mensaje que da el servidor, sin decir qué dato falló", async () => {
    document.cookie = "csrftoken=abc123; path=/";
    servidorFalso({
      "GET /api/sesion": [200, { usuario: null }],
      "POST /api/sesion": [400, { causa: "Código, correo o contraseña incorrectos" }],
    });
    render(
      <MemoryRouter>
        <SesionProveedor>
          <IniciarSesion />
        </SesionProveedor>
      </MemoryRouter>,
    );

    await userEvent.type(screen.getByLabelText("Código o correo"), "70004");
    await userEvent.type(screen.getByLabelText("Contraseña de UPBus"), "no-es-la-clave");
    await userEvent.click(screen.getByRole("button", { name: "Acceder" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("Código, correo o contraseña incorrectos");
  });
});
