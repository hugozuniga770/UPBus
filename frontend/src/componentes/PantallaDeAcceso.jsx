import Logo from "./Logo.jsx";

/**
 * Marco de las pantallas de acceso. Usa los colores de la UPB pero la marca
 * es UPBus: no imita la página de UPBnet, para que nadie confunda las dos ni
 * escriba aquí su contraseña de UPBnet.
 */
export default function PantallaDeAcceso({ titulo, children }) {
  return (
    <main className="flex min-h-full items-center justify-center bg-[radial-gradient(circle_at_top,#2e3478,#1a1d4a_45%,#14162f)] px-4 py-10">
      <div className="w-full max-w-sm overflow-hidden rounded-2xl bg-white shadow-2xl shadow-black/40">
        <div className="flex flex-col items-center gap-2 bg-upb px-6 py-7">
          <Logo claro tamano={44} />
          <p className="text-sm text-celeste">Los buses de la UPB, en tiempo real</p>
        </div>
        <div className="space-y-4 bg-[#eceef3] px-6 py-6">
          <h1 className="font-titulo text-lg font-bold text-upb">{titulo}</h1>
          {children}
        </div>
        <p className="bg-white px-6 py-3 text-center text-xs text-suave">
          Usa tu contraseña de UPBus, no la de UPBnet · Proyecto de Certificación I, UPB Santa Cruz
        </p>
      </div>
    </main>
  );
}
