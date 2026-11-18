const ESTILOS = {
  primario: "bg-boton text-white hover:bg-[#00609a] disabled:bg-boton/50",
  acento: "bg-acento text-tinta hover:bg-[#e08e0b] disabled:bg-acento/50",
  secundario: "border border-upb/20 bg-white text-upb hover:bg-fondo disabled:text-upb/40",
  peligro: "bg-[#b42318] text-white hover:bg-[#912018] disabled:bg-[#b42318]/50",
};

export default function Boton({ variante = "primario", grande = false, className = "", ...props }) {
  return (
    <button
      type="button"
      className={`inline-flex items-center justify-center gap-2 rounded-xl font-semibold transition-colors disabled:cursor-not-allowed ${
        grande ? "px-6 py-4 text-lg" : "px-4 py-2.5"
      } ${ESTILOS[variante]} ${className}`}
      {...props}
    />
  );
}
