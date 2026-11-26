/// <reference types="vitest/config" />
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// Django corre en el puerto 8000. Vite le pasa /api, /admin y /ws, así la
// interfaz y el servidor comparten el mismo origen (cookie de sesión y CSRF).
const SERVIDOR = process.env.UPBUS_SERVIDOR ?? "http://127.0.0.1:8000";

export default defineConfig(({ command }) => ({
  // En producción Django/WhiteNoise publica el resultado de Vite aquí.
  // En desarrollo se conserva `/` para que el proxy de `/static` no intercepte Vite.
  base: command === "build" ? "/static/frontend/" : "/",
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    // Para probar desde el celular con un túnel HTTPS (docs/guia-modo-registro.md).
    allowedHosts: [".trycloudflare.com"],
    proxy: {
      "/api": SERVIDOR,
      "/admin": SERVIDOR,
      "/static": SERVIDOR,
      "/ws": { target: SERVIDOR.replace(/^http/, "ws"), ws: true },
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: "./src/pruebas/configuracion.js",
    css: false,
    restoreMocks: true,
    unstubGlobals: true,
  },
}));
