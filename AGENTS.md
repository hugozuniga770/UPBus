# AGENTS.md — cómo trabajar en UPBus

Instrucciones para quien programa en este repositorio, persona o asistente de IA. La guía completa está en [`docs/guia-desarrollo.md`](docs/guia-desarrollo.md).

## El proyecto

UPBus conecta en tiempo real a los estudiantes y choferes de los buses de la UPB Santa Cruz. Servidor: Django 6, Django REST Framework y Channels, con SQLite. Interfaz: React 19, Vite y Tailwind 4, con Leaflet y OpenStreetMap. Todo en español.

## Antes de escribir código

1. Lee la historia (Como … quiero … para …) y sus criterios en [`docs/sesion-07-modelos.md`](docs/sesion-07-modelos.md). Cada criterio dice su tipo (funcional, regla de negocio, manejo de errores o no funcional), trae su escenario de prueba (Dado / Cuando / Entonces) y es un test con un nombre ya escrito (`test_HUxx_CAy_...`).
2. Lee el issue de la tarea: dice dónde va el código y de qué depende.
3. Mira el molde en `cuentas/` (HU-03) y `rutas/` (HU-18).

## Reglas

1. **Capas:** `views.py` recibe y responde; `servicios.py` orquesta y guarda en transacciones; `reglas.py` decide y lanza `Rechazo("causa")`. Las vistas no tocan la base ni llaman a las reglas. Las reglas no tocan la base.
2. **Rechazos con su causa exacta**, la de la sesión 7. Llegan a la interfaz como `{"causa": "..."}` (400, 403 con `SinPermiso`, 404 con `NoExiste`).
3. **Un test por criterio**, con el nombre de la sesión 7, en `tests/test_huxx_<tema>.py`. Primero el test, verlo fallar, después el código. Las pruebas de interfaz van junto a su archivo (`*.test.jsx`).
4. **Lo que manda el celular lleva `id_cliente`** y un reenvío no duplica nada.
5. **Hora de America/La_Paz** (`comun.tiempo`); en los tests, el fixture `hora`.
6. **Datos de ejemplo** de la sección 0 de `docs/sesion-06-requisitos.md`. Nunca datos reales de la clase.
7. **Nunca subas** `padron/padron.local.json`, `.env` ni `db.sqlite3`.
8. **Ramas:** una por historia, desde `develop`, y Pull Request a `develop`. Nadie sube directo a `main` ni a `develop`.
9. **Commits:** `HU-07: qué hace (#issue)`, a nombre de la persona que trabaja. No se agregan coautores de IA: el uso de IA se declara en la sección «Participación y asistencia utilizada» del documento que corresponda.
10. **Documentación:** al terminar, filas nuevas en `docs/trazabilidad.md`; si cambia algo acordado, una fila en `docs/cambios.md`.

## Comandos

```
pytest                              # servidor
cd frontend && npm test             # interfaz
cd frontend && npm run build        # compila como en la integración continua
pytest e2e                          # punta a punta en el navegador (T21): antes, npm run build
python manage.py makemigrations     # después de cambiar un modelo
python manage.py simular --lista    # escenarios del simulador (T23)
```

## Mapa

```
config/    comun/    cuentas/ (HU-01 a HU-03)    rutas/ (HU-04, HU-08, HU-18)
viajes/ (HU-05 a HU-07, HU-09, HU-10; HU-11 a HU-13 por hacer)    mensajes/ (HU-14, HU-15)
padron/    tests/    e2e/    frontend/src/{api,sesion,componentes,paginas,registro}    docs/
```
