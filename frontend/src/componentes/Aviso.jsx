const ESTILOS = {
  error: "border-[#f5c2c0] bg-[#fdecea] text-[#8a1c13]",
  exito: "border-[#b7e1c1] bg-[#e7f6ea] text-[#1d5b2c]",
  info: "border-[#bcd9f0] bg-[#e9f3fb] text-[#174d75]",
  alerta: "border-[#f7d9a4] bg-[#fdf1dc] text-[#7a4a00]",
};

export default function Aviso({ tipo = "info", children }) {
  return (
    <div role={tipo === "error" ? "alert" : "status"} className={`rounded-lg border px-3 py-2 text-sm ${ESTILOS[tipo]}`}>
      {children}
    </div>
  );
}
