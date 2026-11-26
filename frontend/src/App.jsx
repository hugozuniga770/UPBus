import { BrowserRouter, Route, Routes } from "react-router";

import Plantilla from "./componentes/Plantilla.jsx";
import IniciarSesion from "./paginas/IniciarSesion.jsx";
import Demo from "./paginas/Demo.jsx";
import Inicio from "./paginas/Inicio.jsx";
import ModoRegistro from "./paginas/ModoRegistro.jsx";
import NoEncontrada from "./paginas/NoEncontrada.jsx";
import Registrarse from "./paginas/Registrarse.jsx";
import Rutas from "./paginas/Rutas.jsx";
import Usuarios from "./paginas/Usuarios.jsx";
import Viajes from "./paginas/Viajes.jsx";
import RutaProtegida from "./sesion/RutaProtegida.jsx";
import { SesionProveedor } from "./sesion/SesionContexto.jsx";

export default function App() {
  return (
    <BrowserRouter>
      <SesionProveedor>
        <Routes>
          <Route path="/ingresar" element={<IniciarSesion />} />
          <Route path="/registrarse" element={<Registrarse />} />
          <Route element={<RutaProtegida><Plantilla /></RutaProtegida>}>
            <Route index element={<Inicio />} />
            <Route path="rutas" element={<Rutas />} />
            <Route
              path="viajes"
              element={<RutaProtegida roles={["chofer"]}><Viajes /></RutaProtegida>}
            />
            <Route
              path="modo-registro"
              element={<RutaProtegida roles={["chofer", "administrador"]}><ModoRegistro /></RutaProtegida>}
            />
            <Route
              path="usuarios"
              element={<RutaProtegida roles={["administrador"]}><Usuarios /></RutaProtegida>}
            />
            <Route
              path="demo"
              element={<RutaProtegida roles={["administrador"]}><Demo /></RutaProtegida>}
            />
          </Route>
          <Route path="*" element={<NoEncontrada />} />
        </Routes>
      </SesionProveedor>
    </BrowserRouter>
  );
}
