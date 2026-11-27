# Guía de desarrollo

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Fecha: 18/11/2026 · Base del código · Issue: [#4](https://github.com/hugozuniga770/UPBus/issues/4)
- Para quién: cualquier integrante que va a programar una historia. Si usas un asistente de IA, que lea también [`AGENTS.md`](../AGENTS.md).
- Relacionados: [historias y criterios](sesion-07-modelos.md) · [diseño](sesion-13-14-diseno.md) · [trazabilidad](trazabilidad.md) · [GitHub](guia-github.md) · [modo registro](guia-modo-registro.md)

## 0. Qué necesitas instalado

| Programa | Versión | Para qué |
|---|---|---|
| Python | 3.13 | El servidor (Django) |
| Node.js | 22 | La interfaz (React con Vite) |
| Git | cualquiera reciente | El repositorio |
| cloudflared | cualquiera reciente | Solo para abrir la app en el celular ([guía del modo registro](guia-modo-registro.md)) |

## 1. Ponerlo a andar la primera vez

**Servidor**, en una terminal, desde la carpeta del proyecto:

```powershell
git clone https://github.com/hugozuniga770/UPBus.git
cd UPBus
git checkout develop
python -m venv .venv
.venv\Scripts\Activate.ps1          # en Linux o macOS: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_rutas
python manage.py runserver
```

En Windows, si PowerShell no deja activar el entorno, corre una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

**Interfaz**, en otra terminal:

```powershell
cd UPBus/frontend
npm install
npm run dev
```

Abre <http://localhost:5173>. Vite le pasa a Django (puerto 8000) todo lo que empieza con `/api`, `/admin`, `/static` y `/ws`, así los dos comparten el mismo origen y funcionan la cookie de sesión y el token CSRF.

**Tu cuenta.** Con el padrón de ejemplo, regístrate con `70001` y `hugo.zuniga@upb.example` (administrador) o con `70004` e `ismael@upb.example` (estudiante). Con la lista de la clase (`padron/padron.local.json`, que Hugo pasa por privado y no está en GitHub), cada uno usa su código y su correo. Cómo se arma esa lista: [`padron/LEEME.md`](../padron/LEEME.md).

## 2. Comandos

| Comando | Qué hace |
|---|---|
| `pytest` | Corre las pruebas del servidor |
| `pytest tests/test_hu18_modo_registro.py -k CA2` | Corre una sola prueba |
| `cd frontend` y `npm test` | Corre las pruebas de la interfaz (Vitest) |
| `cd frontend` y `npm run build` | Comprueba que la interfaz compila, como en la integración continua |
| `pytest e2e` | Corre las pruebas de punta a punta en el navegador (T21): levanta el servidor sobre una base nueva y prueba con varias cuentas a la vez. Antes, una sola vez: `pip install -r requirements-e2e.txt` y `python -m playwright install chromium`; y `npm run build` en `frontend/` cada vez que cambie la interfaz. Las capturas quedan en `e2e/capturas/` |
| `python manage.py makemigrations <app>` | Crea la migración después de cambiar un modelo |
| `python manage.py cargar_rutas` | Carga o actualiza las 5 rutas y sus horarios desde `rutas/datos/rutas.json`; se puede correr varias veces |
| `python manage.py importar_padron <archivo> --administradores a,b,c` | Arma `padron/padron.local.json` desde la lista de la clase (.xlsx o .csv) |
| `python manage.py importar_registro <respaldo.json> --usuario <código o correo>` | Carga un respaldo del modo registro |
| `python manage.py simular recorrido --ruta sur` | Mueve un bus simulado por la ruta grabada ([guía del simulador](guia-simulador.md)); `--lista` muestra los escenarios |

Para cambiar algo de la configuración (otra base, otro padrón, otro dominio o la distancia de llegada a las paradas, C-34), copia `.env.ejemplo` como `.env` y edítalo. `.env` no se sube.

## 3. Cómo está organizado

```
config/        configuración de Django, URLs y ASGI (HTTP y WebSocket)
comun/         lo compartido: Rechazo, hora de La Paz, distancias, respuestas JSON
cuentas/       usuario, padrón, registro, sesión y gestión de usuarios (HU-01 a HU-03)
rutas/         rutas, horarios, paradas, horas aproximadas y modo registro (HU-04, HU-18)
viajes/        viajes, bus en vivo, «Voy a subir», abordajes y créditos (por hacer)
mensajes/      chat directo y chat de la ruta (HU-14, HU-15)
padron/        padrón de ejemplo; aquí va también padron.local.json, que no se sube
tests/         un test por criterio de aceptación (pytest)
e2e/           pruebas de punta a punta en el navegador, con varias cuentas a la vez (T21)
frontend/      React con Tailwind; sus pruebas van junto a cada archivo (*.test.jsx)
docs/          documentación por sesión y guías
```

Cada app tiene las mismas capas, como el proyecto de reserva de salas:

| Archivo | Qué hace | Qué no hace |
|---|---|---|
| `views.py` | Recibe la petición, lee los datos con su serializador, llama a un servicio y responde JSON | No toca la base ni llama a las reglas |
| `servicios.py` | Orquesta: lee lo necesario, pregunta a las reglas y guarda, en una transacción | No decide reglas de negocio por su cuenta |
| `reglas.py` | Decide si algo se permite; si no, lanza `Rechazo("causa")` | No toca la base: recibe los datos ya leídos |
| `models.py` | Las tablas | No tiene reglas de negocio |
| `serializadores.py` | El formato de lo que entra y de lo que sale | — |

Un rechazo siempre lleva la causa exacta de la sesión 7 y llega a la interfaz como `{"causa": "..."}`, con 400 (regla), 403 (permiso, `SinPermiso`) o 404 (`NoExiste`). La interfaz la muestra tal cual.

Ejemplos completos para copiar el molde: `cuentas/` (HU-03, gestión de usuarios) y `rutas/` (HU-18, modo registro).

## 4. Cómo implementar una historia, paso a paso

1. **Toma el issue** que te asignó Andrés y crea tu rama desde `develop` ([guía de GitHub](guia-github.md)):
   ```powershell
   git checkout develop
   git pull
   git checkout -b hu-05-viajes
   ```
2. **Copia los criterios.** En la [sesión 7](sesion-07-modelos.md) están los criterios de tu historia con el nombre de cada test. Crea `tests/test_hu05_<tema>.py` con esos nombres.
3. **Escribe el primer test y míralo fallar.** Usa los datos y fixtures de `tests/conftest.py`: `hugo`, `sebastian`, `ismael`, `marco`, `cliente`, `cliente_de(persona)`, `ruta_norte`, `horario_0640`, `hora(dia, horas, minutos)` y los puntos `LA_FONTANA`, `SEVILLA`, `PETROL`, `CAMPOS` y `CAMPUS_UPB`.
4. **Modelo:** agrega lo que necesitas en `models.py` y crea la migración con `python manage.py makemigrations <app>`. El diseño propuesto está en la [sesión 13–14](sesion-13-14-diseno.md), sección 3.
5. **Reglas:** una función por cosa que se decide, con el mensaje exacto del documento, por ejemplo `verificar_es_su_viaje` → `«este viaje no es tuyo»`.
6. **Servicio:** lee, pregunta a las reglas y guarda. Si escribe más de una cosa, va con `@transaction.atomic`. Si recibe algo que el celular puede reenviar, usa un `id_cliente` para no duplicar, como `marcar_parada`.
7. **Vista y URL:** la vista solo recibe, llama al servicio y responde. Agrega la ruta en el `urls.py` de la app.
8. **Interfaz:** la función en `frontend/src/api/cliente.js`, la página en `frontend/src/paginas/` y la ruta en `App.jsx`. Si el criterio se ve en pantalla (un mensaje, un botón que aparece), agrega una prueba de Vitest junto a la página.
9. **Corre todo:** `pytest`, `npm test` y `npm run build`, y mira la pantalla en el celular (o con el modo celular del navegador).
10. **Documenta:** agrega las filas de tus criterios a [trazabilidad.md](trazabilidad.md). Si cambiaste algo acordado (un mensaje, una regla, un modelo propuesto), agrega una fila en [cambios.md](cambios.md).
11. **Commit y Pull Request:** `HU-05: el chofer inicia su viaje (#6)` y un Pull Request a `develop` ([guía de GitHub](guia-github.md)).

### Probar con varias cuentas en una sola laptop

Para hacer una historia no hace falta juntarse: los tests de cada criterio crean sus propias cuentas en una base de prueba, y en pantalla una sola persona puede ser estudiante, chofer y administrador a la vez.

1. **Usa el padrón de ejemplo**, para no registrar a compañeros de verdad. En `.env`, pon `UPBUS_PADRON=padron/padron.json`. Si no quieres tocar tu base, agrega `UPBUS_BD=prueba.sqlite3` y corre `python manage.py migrate` y `python manage.py cargar_rutas`.
2. **Crea las cuentas.** Regístrate como Hugo (`70001`, `hugo.zuniga@upb.example`, administrador) y como Ismael (`70004`, `ismael@upb.example`, estudiante). Con Hugo, en **Usuarios**, crea un chofer, por ejemplo Marco.
3. **La Ruta Sur grabada** se carga sola la primera vez que la simulas en **Demo** (C-37). Para verla con sus paradas en **Rutas** antes de simular: `python manage.py importar_registro rutas/datos/registros/registro-sur-0640-2026-11-25.json --usuario 70001`.
4. **Abre una ventana por cuenta.** Cada ventana guarda su propia sesión: Chrome normal con Hugo, una ventana de incógnito con Ismael y otro navegador (Edge o Firefox) con Marco, todas en `http://localhost:5173`.
5. **Mueve un bus sin salir a la calle.** Con Hugo, abre **Demo** y corre «Recorrido» o «No se presenta» en la Ruta Sur ([guía del simulador](guia-simulador.md)). Con Ismael, en **Rutas › Sur**, el viaje simulado aparece en curso: puedes marcar «Voy a subir» en una parada y ver qué pasa cuando llega el bus. En «No se presenta», el estudiante de la simulación espera en la segunda parada y comparte su ubicación.

Por ejemplo, para T15 (HU-08): Ismael propone una parada tocando el recorrido, Hugo la aprueba desde su ventana e Ismael la ve aprobada. Para la parada activa (HU08-CA3), corre «No se presenta»: la parada donde espera el estudiante de la simulación está activa y las demás no.

**Entre varias personas a la vez**, por ejemplo en la Review: una sola laptop corre el servidor y abre el túnel de la [guía del modo registro](guia-modo-registro.md). Los demás abren la dirección `https://….trycloudflare.com` en su celular o su computadora y entran con su propia cuenta. Todos usan la base de esa laptop, y el panel Demo de esa laptop mueve el bus en vivo para todos. Cuando esté el hosting (T22), la dirección pública reemplaza al túnel.

## 5. Convenciones

- **Nombres en español**, completos y sin abreviar: `verificar_sin_registro_en_curso`, `minutos_desde_salida`.
- **Hora:** todo en America/La_Paz. Usa `comun.tiempo.ahora()`; en las pruebas, el fixture `hora`.
- **Datos de ejemplo:** los de la [sección 0 de los requisitos](sesion-06-requisitos.md). Nunca datos reales de la clase en el código, en las pruebas ni en los documentos.
- **Lo simulado** (bus en vivo, ubicación del estudiante, recargas, retiros, padrón) queda aislado en su módulo, para cambiarlo sin tocar las reglas (BUS-RC-04).
- **Interfaz:** colores y componentes de `frontend/src/componentes/` (Boton, Campo, Aviso, Mapa, Plantilla). Primero el celular: mapa a pantalla completa y tarjetas que suben desde abajo, como la pantalla de rutas.

## 6. Problemas comunes

| Ves | Qué pasa | Qué hacer |
|---|---|---|
| «la página perdió su token de seguridad» | La cookie CSRF venció o cambiaste de dirección | Recarga la página |
| `DisallowedHost` | Abriste la app desde una dirección que Django no conoce | Agrégala a `UPBUS_ALLOWED_HOSTS` en `.env` |
| Un test dice `Database access not allowed` | Le falta acceso a la base | `pytestmark = pytest.mark.django_db` al inicio del archivo; las de WebSocket, `transaction=True` |
| La interfaz no habla con el servidor | Django no está corriendo en el puerto 8000 | Levanta `python manage.py runserver` antes que `npm run dev` |
| `no such table` | Faltan migraciones | `python manage.py migrate` |
| Las rutas aparecen sin paradas | Nadie grabó esa ruta en tu base | Importa el respaldo de `rutas/datos/registros/` con `importar_registro` |

## 7. Participación y asistencia utilizada

- **Hugo Zuñiga:** dejó la base del código y pidió esta guía para que el equipo pueda tomar las tareas.
- **Asistencia de IA:** se usó Claude (Anthropic) para escribir la base y esta guía; el 26/11/2026, para agregar cómo probar con varias cuentas y cómo correr las pruebas de punta a punta (T21).
