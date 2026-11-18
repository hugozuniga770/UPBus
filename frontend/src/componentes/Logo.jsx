/** Logo de UPBus: un pin de ubicación con un bus adentro. */
export default function Logo({ claro = false, tamano = 36, conNombre = true }) {
  const fondo = claro ? "#8cc4ec" : "#242865";
  const ventana = claro ? "#242865" : "#242865";
  return (
    <span className="inline-flex items-center gap-2">
      <svg width={tamano * 0.77} height={tamano} viewBox="0 0 100 130" aria-hidden="true">
        <path d="M50 4C25.1 4 5 24.1 5 49c0 33 45 77 45 77s45-44 45-77C95 24.1 74.9 4 50 4Z" fill={fondo} />
        <rect x="27" y="22" width="46" height="48" rx="10" fill="#fff" />
        <rect x="33" y="29" width="34" height="19" rx="4" fill={ventana} />
        <circle cx="37" cy="58" r="4" fill="#f39c12" />
        <circle cx="63" cy="58" r="4" fill="#f39c12" />
        <rect x="44" y="56" width="12" height="4" rx="2" fill={ventana} />
        <rect x="31" y="68" width="9" height="8" rx="2" fill={ventana} />
        <rect x="60" y="68" width="9" height="8" rx="2" fill={ventana} />
      </svg>
      {conNombre && (
        <span
          className={`font-titulo font-extrabold tracking-tight ${claro ? "text-white" : "text-upb"}`}
          style={{ fontSize: tamano * 0.62 }}
        >
          UPB<span className={claro ? "text-celeste" : "text-boton"}>us</span>
        </span>
      )}
    </span>
  );
}
