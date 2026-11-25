# Guía del modo registro: grabar una ruta desde el celular

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Fecha: 18/11/2026 · Actualizado: 25/11/2026 (C-23, C-25) · Historia HU-18 (BUS-RF-23) · Tarea T26: [#5](https://github.com/hugozuniga770/UPBus/issues/5)
- Para quién: cualquier chofer o administrador que grabe una ruta. La primera grabada fue la Ruta Sur, el 25/11 ([REG-01](viajes-grabados.md)).

## 0. Qué hace

Mientras vas en el bus, la página sigue el GPS del celular. En cada parada tocas **«📍 Parada aquí»** y se guardan la posición y la hora. Al terminar, UPBus crea las paradas de la ruta (o reconoce las que ya existen, si estás a menos de 50 m), su orden, el recorrido y la hora aproximada de cada una. Cada vez que alguien vuelve a grabar la misma ruta, las horas se ajustan con el promedio de los últimos 5 viajes.

- Si lo graba un **administrador**, las paradas nuevas quedan aprobadas y todos las ven.
- Si lo graba un **chofer**, quedan propuestas hasta que un administrador las apruebe (P-28).

## 1. Por qué hace falta un túnel

El navegador del celular solo entrega el GPS a una página segura (con `https://`). Mientras no haya hosting (P-16), la app corre en una laptop y un **túnel gratuito de Cloudflare** le da una dirección `https://….trycloudflare.com` que se abre desde el celular, con datos móviles.

La laptop tiene que quedarse **prendida, conectada a internet y sin suspenderse** durante todo el viaje.

## 2. Qué necesitas

- La laptop con el proyecto andando ([guía de desarrollo](guia-desarrollo.md)), con la rama `develop` actualizada y `python manage.py cargar_rutas` hecho.
- `cloudflared` instalado en la laptop. En Windows: `winget install --id Cloudflare.cloudflared`. En otros sistemas, la página de descargas de Cloudflare Tunnel.
- El celular con Chrome, datos móviles y batería llena (la pantalla queda encendida todo el viaje).
- Una cuenta de **administrador** (los tres integrantes lo son) o de chofer.

## 3. El día anterior: prueba completa

1. En la laptop, tres terminales:
   ```powershell
   python manage.py runserver                       # 1) el servidor
   cd frontend; npm run dev                         # 2) la interfaz
   cloudflared tunnel --url http://localhost:5173   # 3) el túnel
   ```
2. El túnel muestra una dirección como `https://palabras-al-azar.trycloudflare.com`. Ábrela en el celular. **Cambia cada vez que arrancas el túnel.**
3. Inicia sesión con tu cuenta y entra a **Modo registro**.
4. Elige la ruta y el horario, por ejemplo Ruta Norte · Ingreso 06:40, y toca **«Iniciar registro»**. Cuando el navegador pida la ubicación, toca **Permitir**.
5. Espera a que arriba diga «GPS ± … m» con un número chico (verde) y toca **«📍 Parada aquí»** una vez, para probar.
6. Como era una prueba, no la termines: cierra la página, vuelve a entrar a Modo registro y toca **«Cancelarlo»** en el aviso del registro sin terminar. Una prueba cancelada no crea paradas ni horas.

Si en el paso 4 dice «El GPS solo funciona con https o en localhost», abriste la dirección sin el túnel. Si dice «No hay permiso de ubicación», actívalo en el candado de la barra de direcciones.

## 4. En el viaje

1. Antes de salir de casa: levanta las tres terminales, abre en el celular la dirección nueva del túnel e inicia sesión.
2. En la parada inicial, toca **«Iniciar registro»** con la ruta y el horario del viaje, y marca esa primera parada en cuanto el GPS esté en verde. Las horas se cuentan desde la salida programada del horario, así que no importa si el bus sale unos minutos antes o después (C-23).
3. En cada parada, cuando el bus se detiene a recoger estudiantes, toca **«📍 Parada aquí»**. Si sabes el nombre (Sevilla, Petrol, Campos…), escríbelo antes en «Nombre de la parada»; si no, queda como «Parada 2», «Parada 3»…, y se corrige después.
4. Si aparece «ya marcaste una parada a menos de 50 m», es la misma parada: sigue.
5. No cierres la página ni bloquees el celular. Si se corta la señal, abajo dice «N por enviar»: las marcas esperan en el celular y se envían solas cuando vuelve la señal, sin duplicarse.
6. Al llegar a la U, marca la última parada (Campus UPB), toca **«Terminar registro»** y confirma con **«Sí, terminar»**. El resumen dice cuántas marcas hubo, cuántas paradas nuevas y cuántas ya conocidas.
7. Toca **«Respaldo»** (o «Descargar respaldo») y guarda el archivo `.json`.

## 5. Después del viaje

1. En **Rutas**, abre la ruta que grabaste con su horario: deberías ver las paradas en orden, cada una con su hora.
2. Para que el resto del equipo tenga las mismas paradas, sube el respaldo al repositorio:
   ```powershell
   git checkout develop
   git pull
   git checkout -b datos-ruta-sur
   # copia el respaldo descargado a rutas/datos/registros/, por ejemplo registro-sur-0640-2026-11-25.json
   git add rutas/datos/registros/
   git commit -m "T26: respaldo de la Ruta Sur, ingreso de las 06:40 (#5)"
   git push -u origin datos-ruta-sur
   ```
   y abre el Pull Request a `develop`. El respaldo tiene solo la ruta, el horario, las posiciones y las horas: no tiene datos de ninguna persona (C-25).
3. Cada integrante lo carga en su base, con su propia cuenta de administrador:
   ```powershell
   python manage.py importar_registro rutas/datos/registros/registro-sur-0640-2026-11-25.json --usuario 70001
   ```
   (con su código o su correo). Cargar el mismo respaldo dos veces se rechaza con «ese registro ya fue importado».
4. Anota el viaje en [viajes-grabados.md](viajes-grabados.md) con su número REG-xx: paradas, horas, cuántas personas subieron en cada una y cómo fue la señal y la precisión del GPS.

## 6. Si algo falla (P-29)

| Pasa | Qué hacer |
|---|---|
| La página no abre en el celular | Revisa que las tres terminales sigan corriendo. Reinicia el túnel y usa la dirección nueva. Si igual no abre: **plan B**, una captura de Maps en cada parada con la hora anotada; después un administrador carga las paradas en `/admin` › Paradas |
| Se cortó la señal en el camino | Nada: las marcas esperan y se envían solas. Si llegas a la U sin señal, toca «Terminar registro» igual: se completa en cuanto haya señal |
| La laptop se apagó o perdió internet | Sigue marcando: todo espera en el celular. Al final descarga el respaldo; cuando la laptop vuelva, se importa con `importar_registro` y completa el mismo registro |
| Marcaste una parada de más | Termina igual. Un administrador la corrige o la borra en `/admin` › Paradas |
| La precisión del GPS es mala (rojo, más de 50 m) | Espera unos segundos con el celular cerca de la ventana antes de marcar |

## 7. Participación y asistencia utilizada

- **Hugo Zuñiga:** propuso el modo registro en lugar de las capturas de Maps (C-18).
- **Sebastian Cruz:** grabó la Ruta Sur el 25/11 (T26, REG-01).
- **Asistencia de IA:** se usó Claude (Anthropic) para construir el modo registro y escribir esta guía.
