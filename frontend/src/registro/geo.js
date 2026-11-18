const RADIO_DE_LA_TIERRA_M = 6_371_000;

/** Distancia en metros entre dos puntos [latitud, longitud] (haversine). */
export function distanciaEnMetros([latA, lngA], [latB, lngB]) {
  const rad = (grados) => (grados * Math.PI) / 180;
  const dLat = rad(latB - latA);
  const dLng = rad(lngB - lngA);
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(rad(latA)) * Math.cos(rad(latB)) * Math.sin(dLng / 2) ** 2;
  return 2 * RADIO_DE_LA_TIERRA_M * Math.asin(Math.sqrt(h));
}

// Igual que el servidor (rutas/reglas.py): dos paradas a menos de 50 m son la misma.
export const RADIO_DE_LLEGADA_M = 50;
