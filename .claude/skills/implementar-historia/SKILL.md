---
name: implementar-historia
description: Implementa una historia de UPBus (HU-xx) o una tarea del plan (T11, T14…) con el molde del proyecto, empezando por los tests de sus criterios de la sesión 7. Úsalo cuando pidan implementar, continuar o revisar una historia o un issue de código de UPBus.
---

# Implementar una historia de UPBus

Sigue estos pasos en orden. Las reglas generales están en `AGENTS.md` y el detalle en `docs/guia-desarrollo.md`.

## 1. Entender qué se pide

- Busca la historia en `docs/sesion-07-modelos.md`: su frase (Como … quiero … para …), su requisito y sus criterios, cada uno con su tipo, su escenario de prueba (Dado / Cuando / Entonces) y el nombre de su test.
- Un criterio de manejo de errores o una regla de negocio casi siempre es un `Rechazo` con su causa exacta; uno no funcional (seguridad, privacidad, fiabilidad) se prueba igual que los demás.
- Lee el issue de la tarea en GitHub, si lo hay: dónde va el código y de qué depende.
- Si una dependencia no está hecha (por ejemplo, HU-07 sin viajes), dilo antes de empezar.

## 2. Rama

```
git checkout develop && git pull && git checkout -b hu-xx-tema
```

## 3. Tests primero

- Crea `tests/test_huxx_<tema>.py` con `pytestmark = pytest.mark.django_db` y un test por criterio, con el nombre exacto de la sesión 7.
- Usa los fixtures de `tests/conftest.py` (`hugo`, `sebastian`, `ismael`, `marco`, `cliente_de`, `ruta_norte`, `horario_0640`, `hora`) y los puntos `LA_FONTANA`, `SEVILLA`, `PETROL`, `CAMPOS`, `CAMPUS_UPB`.
- Comprueba el código HTTP, la `causa` exacta y que un rechazo no cambió nada en la base.
- Corre `pytest` y confirma que fallan por la razón correcta.

## 4. Servidor, capa por capa

1. `models.py` según la sección 3 de `docs/sesion-13-14-diseno.md`, y `python manage.py makemigrations <app>`.
2. `reglas.py`: funciones `verificar_...` que reciben datos ya leídos y lanzan `Rechazo`, `SinPermiso` o `NoExiste` con la causa exacta.
3. `servicios.py`: leen, llaman a las reglas y guardan; `@transaction.atomic` si escriben más de una cosa; `id_cliente` si el celular puede reenviar.
4. `serializadores.py`, `views.py` y `urls.py`: la vista solo recibe, llama al servicio y responde JSON.
5. Si hay tiempo real, envía el evento al grupo del canal desde el servicio (`viajes/consumers.py`).

## 5. Interfaz

- Agrega la llamada en `frontend/src/api/cliente.js`, la pantalla en `frontend/src/paginas/` y la ruta en `App.jsx`, protegida por rol si corresponde.
- Usa los componentes de `frontend/src/componentes/`. Primero el celular.
- Si un criterio se ve en pantalla, agrega su prueba de Vitest junto a la página, con el nombre `HUxx-CAy ...`.

## 6. Comprobar

- `pytest`, `cd frontend && npm test` y `npm run build`, todo en verde.
- Mira la pantalla en tamaño celular.

## 7. Documentar y entregar

- Agrega las filas de los criterios en `docs/trazabilidad.md` y marca ✅ en `docs/sesion-07-modelos.md` (secciones 2 y 7).
- Si cambió algo acordado, una fila en `docs/cambios.md`.
- Commits `HU-xx: qué hace (#issue)`, a nombre de la persona, sin coautores de IA.
- Pull Request a `develop` con los criterios cubiertos, una captura en celular y la Definition of Done.
