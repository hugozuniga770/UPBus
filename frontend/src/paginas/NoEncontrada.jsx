import { Link } from "react-router";

export default function NoEncontrada() {
  return (
    <main className="grid h-full place-items-center px-4 text-center">
      <div>
        <p className="font-titulo text-5xl font-extrabold text-upb">404</p>
        <p className="mt-2 text-suave">Esta página no existe.</p>
        <Link to="/" className="mt-4 inline-block font-semibold text-boton hover:underline">Volver al inicio</Link>
      </div>
    </main>
  );
}
