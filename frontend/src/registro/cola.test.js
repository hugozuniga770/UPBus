import { describe, expect, it, vi } from "vitest";

import { crearCola } from "./cola.js";

function almacenFalso() {
  const datos = new Map();
  return { getItem: (c) => datos.get(c) ?? null, setItem: (c, v) => datos.set(c, v) };
}

const sinSenal = () => vi.fn().mockRejectedValue(Object.assign(new Error("sin señal"), { esDeRed: true }));

describe("cola del modo registro", () => {
  it("HU18-CA5 una marca agregada dos veces queda una sola vez", () => {
    const cola = crearCola(almacenFalso());

    cola.agregar({ id: "marca-1", tipo: "marca" });
    cola.agregar({ id: "marca-1", tipo: "marca" });

    expect(cola.pendientes()).toBe(1);
  });

  it("sin señal conserva todo y lo envía, en orden, cuando vuelve", async () => {
    const cola = crearCola(almacenFalso());
    cola.agregar({ id: "a" });
    cola.agregar({ id: "b" });

    expect((await cola.enviar(sinSenal())).pendientes).toBe(2);

    const conSenal = vi.fn().mockResolvedValue(undefined);
    const resultado = await cola.enviar(conSenal);
    expect(resultado.pendientes).toBe(0);
    expect(conSenal.mock.calls.map(([e]) => e.id)).toEqual(["a", "b"]);
  });

  it("lo que el servidor rechaza sale de la cola con su causa", async () => {
    const cola = crearCola(almacenFalso());
    cola.agregar({ id: "a" });
    const rechazo = vi.fn().mockRejectedValue({ causa: "ya marcaste una parada a menos de 50 m" });

    const resultado = await cola.enviar(rechazo);

    expect(resultado.pendientes).toBe(0);
    expect(resultado.rechazados[0].causa).toBe("ya marcaste una parada a menos de 50 m");
  });
});
