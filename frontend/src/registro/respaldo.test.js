import { describe, expect, it } from "vitest";
import { armarRespaldo, nombreDelRespaldo } from "./respaldo.js";

const estado = {
  registro: {
    id_cliente: "r-1",
    ruta: { clave: "sur", nombre: "Ruta Sur" },
    horario: { sentido: "ingreso", salida: "06:40" },
    iniciado_en: "2026-11-25T06:46:17-04:00",
  },
  marcas: [
    { id_cliente: "m-1", nombre: "Makro Parque", latitud: -17.76, longitud: -63.15, precision_m: 20, marcada_en: "2026-11-25T10:46:29Z", estado: "guardada" },
    { id_cliente: "m-2", nombre: "Repetida", latitud: -17.76, longitud: -63.15, precision_m: 20, marcada_en: "2026-11-25T10:46:40Z", estado: "rechazada" },
  ],
  puntos: [],
};

describe("respaldo del modo registro", () => {
  it("no lleva el código ni el correo de quien graba, porque se sube al repositorio público", () => {
    const respaldo = armarRespaldo(estado);

    expect(respaldo).not.toHaveProperty("usuario");
    expect(JSON.stringify(respaldo)).not.toMatch(/correo|codigo/);
  });

  it("deja fuera las marcas rechazadas y se nombra por ruta, horario y fecha", () => {
    const respaldo = armarRespaldo(estado);

    expect(respaldo.marcas.map((m) => m.nombre)).toEqual(["Makro Parque"]);
    expect(nombreDelRespaldo(respaldo)).toBe("registro-sur-0640-2026-11-25.json");
  });
});
