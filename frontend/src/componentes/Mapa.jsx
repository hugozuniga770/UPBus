import { useEffect } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";

// Centro de Santa Cruz de la Sierra, mientras no haya otra posición.
export const CENTRO_DE_SANTA_CRUZ = [-17.7833, -63.1821];

function Centrar({ punto, zoom }) {
  const mapa = useMap();
  useEffect(() => {
    if (punto) mapa.setView(punto, zoom ?? mapa.getZoom(), { animate: true });
  }, [mapa, punto, zoom]);
  return null;
}

/** Mapa de OpenStreetMap con Leaflet (BUS-RT-06). */
export default function Mapa({ centro, zoom = 13, seguir, children }) {
  return (
    <MapContainer
      center={centro ?? CENTRO_DE_SANTA_CRUZ}
      zoom={zoom}
      className="absolute inset-0 z-0"
      zoomControl={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {seguir && <Centrar punto={seguir} />}
      {children}
    </MapContainer>
  );
}
