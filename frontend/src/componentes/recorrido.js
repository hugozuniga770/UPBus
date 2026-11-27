// Cuentas sobre el recorrido grabado de una ruta, para dibujarlo en el mapa.

// Como el simulador (viajes/simulador.py): una parada más lejos que esto no está sobre lo grabado.
export const LEJOS_DEL_RECORRIDO_M = 200;

/** Distancia aproximada en metros entre dos puntos [latitud, longitud]; basta para la ciudad. */
export function metrosEntre([latitud1, longitud1], [latitud2, longitud2]) {
  const radianes = Math.PI / 180;
  const x = (longitud2 - longitud1) * radianes * Math.cos(((latitud1 + latitud2) / 2) * radianes);
  const y = (latitud2 - latitud1) * radianes;
  return 6_371_000 * Math.hypot(x, y);
}

/**
 * Los tramos que el recorrido grabado no cubre: de la primera parada al inicio de lo
 * grabado y del final de lo grabado a la última parada, si esas paradas quedan lejos.
 * Pasa con REG-01, que empieza en Parque Urbano y no en Makro Parque. El simulador va
 * en línea recta por esos tramos, y el mapa los dibuja punteados.
 *
 * `paradas` son los puntos [latitud, longitud] de las paradas aprobadas, en orden.
 */
export function tramosSinGrabar(recorrido, paradas) {
  if (!recorrido || recorrido.length < 2 || !paradas?.length) return [];
  const lejos = (parada) => recorrido.every((punto) => metrosEntre(punto, parada) > LEJOS_DEL_RECORRIDO_M);
  const primera = paradas[0];
  const ultima = paradas[paradas.length - 1];
  const tramos = [];
  if (lejos(primera)) tramos.push([primera, recorrido[0]]);
  if (paradas.length > 1 && lejos(ultima)) tramos.push([recorrido[recorrido.length - 1], ultima]);
  return tramos;
}
