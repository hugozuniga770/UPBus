/**
 * Respaldo del modo registro: un archivo JSON con todo lo marcado.
 * Se importa en el servidor con `python manage.py importar_registro`.
 * No lleva datos de quien graba: se sube al repositorio, que es público (C-25).
 */
export function armarRespaldo(estado) {
  const { registro, marcas, puntos } = estado;
  return {
    formato: "upbus-registro",
    version: 1,
    id_cliente: registro.id_cliente,
    ruta: { clave: registro.ruta.clave, nombre: registro.ruta.nombre },
    horario: registro.horario ? { sentido: registro.horario.sentido, salida: registro.horario.salida } : null,
    iniciado_en: registro.iniciado_en,
    marcas: marcas
      .filter((m) => m.estado !== "rechazada")
      .map(({ id_cliente, nombre, latitud, longitud, precision_m, marcada_en }) => ({
        id_cliente, nombre, latitud, longitud, precision_m, marcada_en,
      })),
    puntos,
  };
}

export function nombreDelRespaldo(respaldo) {
  const fecha = respaldo.iniciado_en.slice(0, 10);
  const hora = respaldo.horario?.salida?.replace(":", "") ?? "sin-horario";
  return `registro-${respaldo.ruta.clave}-${hora}-${fecha}.json`;
}

export function descargarRespaldo(respaldo) {
  const archivo = new Blob([JSON.stringify(respaldo, null, 2)], { type: "application/json" });
  const enlace = document.createElement("a");
  enlace.href = URL.createObjectURL(archivo);
  enlace.download = nombreDelRespaldo(respaldo);
  document.body.append(enlace);
  enlace.click();
  enlace.remove();
  URL.revokeObjectURL(enlace.href);
}
