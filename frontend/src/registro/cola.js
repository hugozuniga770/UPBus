/**
 * Cola de envíos del modo registro (HU-18).
 *
 * Todo lo que se marca se guarda primero en el celular y después se envía.
 * Si no hay señal, queda en la cola y se reintenta; cada elemento tiene un
 * `id` propio, así que un reenvío no duplica nada (BUS-RC-03).
 */
const CLAVE = "upbus.cola";

export function crearId() {
  if (globalThis.crypto?.randomUUID) return globalThis.crypto.randomUUID();
  return `id-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

export function crearCola(almacen = globalThis.localStorage) {
  let enviando = false;

  function leer() {
    try {
      return JSON.parse(almacen.getItem(CLAVE)) ?? [];
    } catch {
      return [];
    }
  }

  function guardar(elementos) {
    try {
      almacen.setItem(CLAVE, JSON.stringify(elementos));
    } catch {
      // Sin espacio o almacenamiento bloqueado: la marca sigue en pantalla.
    }
  }

  return {
    agregar(elemento) {
      const elementos = leer();
      if (!elementos.some((e) => e.id === elemento.id)) {
        elementos.push(elemento);
        guardar(elementos);
      }
      return elementos.length;
    },

    pendientes() {
      return leer().length;
    },

    /**
     * Envía en orden. Si falla la red, se detiene y conserva el resto. Si el
     * servidor rechaza un elemento, lo quita y lo informa en `rechazados`.
     */
    async enviar(enviarElemento) {
      if (enviando) return { pendientes: leer().length, rechazados: [], enviados: 0, ocupada: true };
      enviando = true;
      const rechazados = [];
      let enviados = 0;
      try {
        for (;;) {
          const [elemento] = leer();
          if (!elemento) break;
          try {
            await enviarElemento(elemento);
            enviados += 1;
          } catch (falla) {
            if (falla?.esDeRed) break;
            rechazados.push({ elemento, causa: falla?.causa ?? "rechazado por el servidor" });
          }
          guardar(leer().filter((e) => e.id !== elemento.id));
        }
      } finally {
        enviando = false;
      }
      return { pendientes: leer().length, rechazados, enviados, ocupada: false };
    },

    vaciar() {
      guardar([]);
    },
  };
}
