import L from "leaflet";
import { useEffect, useRef } from "react";
import { MapContainer, TileLayer, useMap, useMapEvents } from "react-leaflet";

// Centro de Santa Cruz de la Sierra, mientras no haya otra posición.
export const CENTRO_DE_SANTA_CRUZ = [-17.7833, -63.1821];

const SIN_RELLENO = () => ({ arribaIzquierda: [0, 0], abajoDerecha: [0, 0] });

/**
 * Mueve la cámara sin que se pierda el pedido: mientras Leaflet anima un zoom
 * ignora cualquier otro movimiento, así que se espera a que termine.
 * Devuelve la función que cancela el movimiento si todavía no se hizo.
 */
function moverLaCamara(mapa, mover) {
  let vigente = true;
  const hacer = () => {
    if (vigente) mover();
  };
  if (mapa._animatingZoom) mapa.once("zoomend", hacer);
  else hacer();
  return () => {
    vigente = false;
    mapa.off("zoomend", hacer);
  };
}

/** El centro del mapa que deja `punto` en el medio de la parte que no tapa el panel. */
function centroVisible(mapa, punto, nivel, relleno) {
  const { arribaIzquierda: [izquierda, arriba], abajoDerecha: [derecha, abajo] } = relleno();
  const enPixeles = mapa.project(punto, nivel).subtract([(izquierda - derecha) / 2, (arriba - abajo) / 2]);
  return mapa.unproject(enPixeles, nivel);
}

/**
 * Lleva la cámara a `punto` cada vez que cambia y lo deja en el medio de lo que se ve.
 * Con otra `clave` (otro foco: el bus, una parada) se acerca hasta `zoom`; mientras
 * sigue al mismo foco respeta el zoom que eligió la persona.
 */
function Centrar({ punto, clave, zoom, relleno }) {
  const mapa = useMap();
  const focoAplicado = useRef(null);
  const [latitud, longitud] = punto;
  useEffect(
    () => moverLaCamara(mapa, () => {
      const nuevoFoco = focoAplicado.current !== clave;
      focoAplicado.current = clave;
      const nivel = nuevoFoco && zoom != null ? Math.max(zoom, mapa.getZoom()) : mapa.getZoom();
      mapa.setView(centroVisible(mapa, [latitud, longitud], nivel, relleno), nivel, { animate: true });
    }),
    [mapa, latitud, longitud, clave, zoom, relleno],
  );
  return null;
}

/** Muestra todos los `puntos` (la ruta entera) cada vez que cambia `clave`. */
function Encuadrar({ puntos, clave, relleno }) {
  const mapa = useMap();
  useEffect(() => {
    if (clave == null || !puntos?.length) return undefined;
    return moverLaCamara(mapa, () => {
      const { arribaIzquierda, abajoDerecha } = relleno();
      mapa.fitBounds(L.latLngBounds(puntos), {
        paddingTopLeft: arribaIzquierda,
        paddingBottomRight: abajoDerecha,
        maxZoom: 16,
        animate: true,
      });
    });
    // Solo con otra clave: los puntos se vuelven a armar en cada actualización.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mapa, clave]);
  return null;
}

function AlArrastrar({ alArrastrar }) {
  useMapEvents({ dragstart: alArrastrar });
  return null;
}

/**
 * Mapa de OpenStreetMap con Leaflet (BUS-RT-06). La persona lo mueve y lo acerca
 * como quiera; la cámara solo se mueve sola cuando se le pide:
 *
 * - `encuadre` y `claveEncuadre`: los puntos que se muestran enteros cada vez que cambia
 *   la clave (al elegir una ruta o con «Toda la ruta»). Sin clave, no hace nada.
 * - `foco`: `{ punto, clave }` que la cámara sigue mientras cambia (el bus, quien graba)
 *   o centra una vez (una parada tocada); con otra clave se acerca hasta `zoomAlEnfocar`.
 * - `relleno`: una función que dice cuánto tapan el panel y los botones, para centrar
 *   y encuadrar en lo que se ve.
 * - `alArrastrar`: se llama cuando la persona mueve el mapa con el dedo o el mouse.
 */
export default function Mapa({
  centro,
  zoom = 13,
  foco,
  zoomAlEnfocar,
  encuadre,
  claveEncuadre,
  relleno = SIN_RELLENO,
  alArrastrar,
  children,
}) {
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
      {encuadre && <Encuadrar puntos={encuadre} clave={claveEncuadre} relleno={relleno} />}
      {foco && <Centrar punto={foco.punto} clave={foco.clave} zoom={zoomAlEnfocar} relleno={relleno} />}
      {alArrastrar && <AlArrastrar alArrastrar={alArrastrar} />}
      {children}
    </MapContainer>
  );
}
