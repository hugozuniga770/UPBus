import { describe, expect, it } from "vitest";

import { metrosEntre, tramosSinGrabar } from "./recorrido.js";

// Puntos de REG-01 (Ruta Sur, 25/11): lo grabado empieza en Parque Urbano, no en Makro Parque.
const MAKRO_PARQUE = [-17.76349, -63.14769];
const PARQUE_URBANO = [-17.79876, -63.17019];
const RECORRIDO = [[-17.7981, -63.1674], [-17.79879, -63.16962], [-17.79804, -63.17496]];

describe("Tramos sin grabar del recorrido (soporte de HU-06)", () => {
  it("mide distancias en metros como el servidor (comun.geo: 4589 m de Makro Parque a Parque Urbano)", () => {
    expect(Math.abs(metrosEntre(MAKRO_PARQUE, PARQUE_URBANO) - 4589)).toBeLessThan(5);
  });

  it("une con un tramo la primera parada que queda lejos de lo grabado (REG-01)", () => {
    expect(tramosSinGrabar(RECORRIDO, [MAKRO_PARQUE, PARQUE_URBANO])).toEqual([[MAKRO_PARQUE, RECORRIDO[0]]]);
  });

  it("no agrega tramos si las paradas están sobre lo grabado, ni sin recorrido", () => {
    expect(tramosSinGrabar(RECORRIDO, [PARQUE_URBANO, RECORRIDO[2]])).toEqual([]);
    expect(tramosSinGrabar([], [MAKRO_PARQUE])).toEqual([]);
  });
});
