/** Guarda el registro en curso en el celular, para retomarlo si se recarga la página. */
const CLAVE = "upbus.modo-registro";
const CLAVE_ULTIMO = "upbus.modo-registro.ultimo";

function leer(clave) {
  try {
    return JSON.parse(localStorage.getItem(clave));
  } catch {
    return null;
  }
}

function escribir(clave, valor) {
  try {
    if (valor === null) localStorage.removeItem(clave);
    else localStorage.setItem(clave, JSON.stringify(valor));
  } catch {
    // Almacenamiento lleno o bloqueado: se sigue con lo que hay en memoria.
  }
}

export const almacen = {
  leerEstado: () => leer(CLAVE),
  guardarEstado: (estado) => escribir(CLAVE, estado),
  borrarEstado: () => escribir(CLAVE, null),
  leerUltimo: () => leer(CLAVE_ULTIMO),
  guardarUltimo: (estado) => escribir(CLAVE_ULTIMO, estado),
};
