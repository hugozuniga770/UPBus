import { useId, useState } from "react";

/** Campo de texto con etiqueta. Las contraseñas tienen botón para verlas. */
export default function Campo({ etiqueta, tipo = "text", ayuda, ...props }) {
  const id = useId();
  const idAyuda = `${id}-ayuda`;
  const [visible, setVisible] = useState(false);
  const esContrasena = tipo === "password";
  return (
    <div>
      <label htmlFor={id} className="mb-1 block text-sm font-semibold text-tinta">
        {etiqueta}
      </label>
      <div className="flex overflow-hidden rounded-lg border border-[#c9cfdc] bg-campo focus-within:border-boton focus-within:ring-2 focus-within:ring-boton/30">
        <input
          id={id}
          type={esContrasena && visible ? "text" : tipo}
          aria-describedby={ayuda ? idAyuda : undefined}
          className="w-full bg-transparent px-3 py-2.5 text-base outline-none"
          {...props}
        />
        {esContrasena && (
          <button
            type="button"
            onClick={() => setVisible((v) => !v)}
            className="border-l border-[#c9cfdc] bg-white px-3 text-sm text-suave hover:text-upb"
            aria-label={visible ? "Ocultar contraseña" : "Ver contraseña"}
          >
            {visible ? "Ocultar" : "Ver"}
          </button>
        )}
      </div>
      {ayuda && (
        <p id={idAyuda} className="mt-1 text-sm text-suave">
          {ayuda}
        </p>
      )}
    </div>
  );
}
