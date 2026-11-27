import { useEffect, useState } from "react";

import { api } from "../api/cliente.js";
import Aviso from "../componentes/Aviso.jsx";
import Boton from "../componentes/Boton.jsx";
import Campo from "../componentes/Campo.jsx";

const VACIO = { nombre: "", correo: "", rol: "chofer", contrasena: "", codigo: "" };

/** HU-03: el administrador crea y desactiva cuentas. */
export default function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [nueva, setNueva] = useState(VACIO);
  const [mensaje, setMensaje] = useState(null);
  const [porDesactivar, setPorDesactivar] = useState(null);

  const cargar = () => api.usuarios().then(({ usuarios: lista }) => setUsuarios(lista)).catch((f) => setMensaje({ tipo: "error", texto: f.causa }));
  useEffect(() => { cargar(); }, []);

  const cambiar = (campo) => (e) => setNueva((d) => ({ ...d, [campo]: e.target.value }));

  async function crear(evento) {
    evento.preventDefault();
    try {
      await api.crearUsuario(nueva);
      setMensaje({ tipo: "exito", texto: `Cuenta de ${nueva.nombre} creada.` });
      setNueva(VACIO);
      cargar();
    } catch (falla) {
      setMensaje({ tipo: "error", texto: falla.causa });
    }
  }

  async function desactivar(usuario) {
    try {
      await api.desactivarUsuario(usuario.id);
      setMensaje({ tipo: "exito", texto: `La cuenta de ${usuario.nombre} quedó desactivada.` });
      setPorDesactivar(null);
      cargar();
    } catch (falla) {
      setMensaje({ tipo: "error", texto: falla.causa });
    }
  }

  return (
    <main className="mx-auto grid max-w-5xl gap-6 px-4 py-8 lg:grid-cols-[1fr_22rem]">
      <section className="overflow-x-auto rounded-2xl bg-white p-5 shadow-sm ring-1 ring-black/5">
        <h1 className="font-titulo text-xl font-bold text-upb">Usuarios</h1>
        <table className="mt-4 w-full min-w-[34rem] text-left text-sm">
          <thead className="text-suave">
            <tr><th className="py-2 pr-4">Nombre</th><th className="pr-4">Rol</th><th className="pr-4">Código</th><th className="pr-4">Correo</th><th /></tr>
          </thead>
          <tbody>
            {usuarios.map((u) => (
              <tr key={u.id} className={`border-t border-black/5 ${u.activa ? "" : "text-suave line-through"}`}>
                <td className="py-2 pr-4 font-semibold">{u.nombre}</td>
                <td className="pr-4 capitalize">{u.rol}</td>
                <td className="pr-4">{u.codigo ?? "—"}</td>
                <td className="pr-4">{u.correo}</td>
                <td className="text-right">
                  {u.activa && (porDesactivar === u.id ? (
                    <span className="inline-flex gap-2">
                      <Boton variante="peligro" onClick={() => desactivar(u)}>Confirmar</Boton>
                      <Boton variante="secundario" onClick={() => setPorDesactivar(null)}>No</Boton>
                    </span>
                  ) : (
                    <Boton variante="secundario" onClick={() => setPorDesactivar(u.id)}>Desactivar</Boton>
                  ))}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
      <form onSubmit={crear} className="space-y-4 rounded-2xl bg-white p-5 shadow-sm ring-1 ring-black/5">
        <h2 className="font-titulo text-lg font-bold text-upb">Crear cuenta</h2>
        <label className="block">
          <span className="mb-1 block text-sm font-semibold">Rol</span>
          <select value={nueva.rol} onChange={cambiar("rol")} className="w-full rounded-lg border border-[#c9cfdc] bg-campo px-3 py-2.5">
            <option value="chofer">Chofer</option>
            <option value="estudiante">Estudiante</option>
            <option value="administrador">Administrador</option>
          </select>
        </label>
        <Campo etiqueta="Nombre" value={nueva.nombre} onChange={cambiar("nombre")} required />
        <Campo etiqueta="Correo" type="email" value={nueva.correo} onChange={cambiar("correo")} required />
        {nueva.rol !== "chofer" && <Campo etiqueta="Código (opcional)" value={nueva.codigo} onChange={cambiar("codigo")} />}
        <Campo etiqueta="Contraseña inicial" tipo="password" value={nueva.contrasena} onChange={cambiar("contrasena")} required />
        {mensaje && <Aviso tipo={mensaje.tipo}>{mensaje.texto}</Aviso>}
        <Boton type="submit" className="w-full">Crear cuenta</Boton>
      </form>
    </main>
  );
}
