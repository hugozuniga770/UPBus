# Guía de GitHub del equipo

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Fecha: 18/11/2026 · Issue: [#4](https://github.com/hugozuniga770/UPBus/issues/4)
- Regla del Product Owner: «que siempre que hayan modificaciones sean aprobadas por mí y nadie haga pull request directo al main; siempre en sus ramas verificamos y aprobamos».

## 0. Las ramas

| Rama | Qué tiene | Quién la cambia |
|---|---|---|
| `main` | Lo entregado al cerrar cada sprint, y la documentación que aprueba el Product Owner | Solo Hugo, uniendo `develop` al cerrar el sprint |
| `develop` | Las historias terminadas y aprobadas | Nadie sube directo: entra todo por Pull Request |
| `hu-07-voy-a-subir` | Una historia en curso | Quien la toma |
| `datos-ruta-norte`, `docs-entrevista-07` | Datos o documentos sueltos | Quien los prepara |

## 1. El flujo de una tarea

1. **Andrés asigna el issue** en el Sprint Planning del sábado. Cada issue de código trae sus criterios, el nombre de cada test, dónde va el código y la Definition of Done.
2. **Rama desde `develop`:**
   ```powershell
   git checkout develop
   git pull
   git checkout -b hu-07-voy-a-subir
   ```
3. **Commits pequeños**, cada uno con su historia y su issue:
   ```
   HU-07: rechaza un segundo aviso en el mismo viaje (#9)
   ```
4. **Antes de subir:** `pytest`, `cd frontend` y `npm test`, y `git status` para ver que no entra nada privado (sección 4).
5. **Subir y abrir el Pull Request a `develop`:**
   ```powershell
   git push -u origin hu-07-voy-a-subir
   ```
   En GitHub: *Compare & pull request*, base `develop`. En la descripción: qué hace, qué criterios cubre, una captura en celular y la lista de la Definition of Done.
6. **Revisión:** Andrés revisa que estén los tests de todos los criterios; Hugo aprueba. La integración continua tiene que estar en verde.
7. **Unir:** Hugo une el Pull Request y se borra la rama. Si `develop` cambió mientras tanto, primero actualiza tu rama:
   ```powershell
   git checkout develop
   git pull
   git checkout hu-07-voy-a-subir
   git merge develop
   ```

## 2. Cada uno con su nombre

Los commits llevan el nombre y el correo de quien los hace. Configúralo una vez:

```powershell
git config --global user.name "Tu nombre completo"
git config --global user.email "el-correo-de-tu-cuenta-de-github@ejemplo.com"
```

Si usas un asistente de IA, el commit sigue siendo tuyo: no agregues coautores de IA. El uso de IA se declara en la sección «Participación y asistencia utilizada» del documento que corresponda (C-22).

## 3. Actualizar tu copia después del 18/11/2026

El 18/11/2026 se reescribió el historial de `main` para que todos los commits figuren a nombre de Hugo (C-22). Si clonaste el repositorio antes, tu `main` ya no coincide con GitHub. Para ponerte al día:

```powershell
git fetch origin
git checkout main
git reset --hard origin/main
```

`reset --hard` borra lo que tengas sin subir en `main`. Si tenías algo, guárdalo antes en una rama: `git branch respaldo-de-mi-trabajo`. Si no tenías nada propio, también sirve borrar la carpeta y clonar de nuevo.

## 4. Lo que nunca se sube

| Archivo | Por qué |
|---|---|
| `padron/padron.local.json` | La lista real de la clase: códigos de UPBnet y correos (C-20) |
| `.env` | Claves y configuración de cada computadora |
| `db.sqlite3` | La base de cada uno, con cuentas y contraseñas cifradas |
| `frontend/node_modules/`, `.venv/` | Se instalan con `npm install` y `pip install` |

Ya están en `.gitignore`. Si alguna vez aparecen en `git status`, no los agregues y avisa en el grupo.

## 5. Para Andrés: tablero y protección de ramas

**Proteger `main` y `develop`.** En GitHub: *Settings › Branches › Add branch ruleset* (o *Add rule*), para `main` y para `develop`:

- *Require a pull request before merging*, con 1 aprobación.
- *Require status checks to pass*: los dos trabajos de «Pruebas» (Servidor e Interfaz).
- *Block force pushes*.

**Tablero.** *Projects › New project › Board*, con las columnas Por hacer, En curso, En revisión y Hecho. Se agregan los issues #1 a #18 y se asigna cada uno a quien lo toma.

## 6. Participación y asistencia utilizada

- **Hugo Zuñiga:** definió la regla de ramas y aprobación.
- **Asistencia de IA:** se usó Claude (Anthropic) para escribir esta guía.
