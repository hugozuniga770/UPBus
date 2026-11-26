# UPBus — Buses UPB en tiempo real (UPB Santa Cruz)

- Integrantes: Hugo Zuñiga (Product Owner), Andrés Laura Vargas (Scrum Master, dirige la implementación) y Sebastian Cruz
- Docente: Ing. Alejandro Rodríguez (Certificación I)
- Tecnología: Python con Django, Django REST Framework y Django Channels; SQLite; React con Tailwind CSS
- Método: Scrum, con sprints de una semana ([plan](docs/sesion-08-09-plan.md))
- Estado: Sprint 2. La **base del código** (registro, inicio de sesión, usuarios, rutas en el mapa y modo registro, con sus pruebas) está en `develop` y en `main`. Las tareas se repartieron el 18/11 y cada una tiene su issue asignado. La primera ruta real, la Ruta Sur, se grabó el 25/11 ([REG-01](docs/viajes-grabados.md)).

## 1. Qué hace

Conecta en tiempo real a los estudiantes y a los choferes de los buses de la UPB Santa Cruz, para que nadie pierda el bus por falta de información. Reemplaza los grupos de WhatsApp por un mapa en vivo, avisos, chat y pago con créditos.

| Historia | Qué permite | Rol |
|---|---|---|
| HU-01 | Registrarse con el código y el correo del padrón | Estudiante |
| HU-02 | Iniciar y cerrar sesión con código o correo | Todos |
| HU-03 | Crear y eliminar choferes y personas | Administrador |
| HU-04 | Ver rutas, paradas y horarios en el mapa | Todos |
| HU-05 | Iniciar y terminar su viaje | Chofer |
| HU-06 | Ver el bus en vivo y la hora aproximada en su parada | Estudiante |
| HU-07 | Avisar «Voy a subir» y compartir su ubicación | Estudiante |
| HU-08 | Proponer una parada | Estudiante y chofer |
| HU-09 | Recibir el aviso de bus cerca | Estudiante |
| HU-10 | Registrar quién subió | Estudiante y chofer |
| HU-11 | Recargar créditos | Estudiante |
| HU-12 | Pagar el viaje y ver el comprobante | Estudiante y chofer |
| HU-13 | Retirar su saldo | Chofer |
| HU-14 | Chatear directo con el chofer | Estudiante y chofer |
| HU-15 | Usar el chat de la ruta | Estudiante y chofer |
| HU-16 | Modificar una ruta | Chofer y administrador |
| HU-17 | Ver los confirmados y recibir el aviso de mínimo | Chofer y administrador |
| HU-18 | Grabar paradas y horas en un viaje real (modo registro) | Chofer y administrador |

En el MVP la ubicación del bus y de los estudiantes, la recarga de créditos, el retiro y el padrón son **simulados**. Las paradas y sus horas no: se graban con el GPS real en el modo registro. El detalle está en la [sección 2 de los requisitos](docs/sesion-06-requisitos.md).

## 2. Documentación

| Documento | Contenido | Estado |
|---|---|---|
| [sesion-06-requisitos.md](docs/sesion-06-requisitos.md) | Requisitos, alcance, lo que se simula y preguntas abiertas | Listo para revisión · RF-23 el 18/11 |
| [sesion-07-modelos.md](docs/sesion-07-modelos.md) | 18 historias, 73 criterios Dado/Cuando/Entonces con el nombre de su test, casos de uso, estados y trazabilidad | Listo para revisión |
| [sesion-08-09-plan.md](docs/sesion-08-09-plan.md) | Plan por sprints, tareas, Gantt, riesgos y recortes | Listo para revisión |
| [sesion-12-arquitectura.md](docs/sesion-12-arquitectura.md) | Arquitectura y verificación de un flujo | Pendiente |
| [sesion-13-14-diseno.md](docs/sesion-13-14-diseno.md) | Arquitectura FE / MW / Padrón / BD, datos, clases y API | Base descrita; modelos que faltan propuestos |
| [diagramas-secuencia.md](docs/diagramas-secuencia.md) | Un diagrama de secuencia por caso de uso, CU-18 incluido | Propuesta para revisión |
| [trazabilidad.md](docs/trazabilidad.md) | Cada test con su criterio, su requisito y su código | 19 de 73 criterios con test |
| [entrevistas.md](docs/entrevistas.md) | Entrevistas, conclusiones y guías de las siguientes | ENT-01 a ENT-03 hechas |
| [viajes-grabados.md](docs/viajes-grabados.md) | Viajes reales grabados con el modo registro: paradas, horas y personas que suben | REG-01 (Ruta Sur, 25/11) |
| [sesion-15-costos.md](docs/sesion-15-costos.md) | Horas-persona, tarifa, precio y estimado contra real | Listo para revisión |
| [cambios.md](docs/cambios.md) | Registro de cambios | Al día |
| [glosario.md](docs/glosario.md) | Siglas y términos | Al día |
| [guia-desarrollo.md](docs/guia-desarrollo.md) | Ponerlo a andar, comandos y cómo implementar una historia paso a paso | Al día |
| [guia-github.md](docs/guia-github.md) | Ramas, Pull Requests, commits y cómo actualizar la copia | Al día |
| [guia-modo-registro.md](docs/guia-modo-registro.md) | Grabar una ruta desde el celular con el túnel HTTPS | Al día |
| [guia-simulador.md](docs/guia-simulador.md) | Mover un bus simulado por una ruta grabada, desde el panel Demo o la terminal | Al día |
| [AGENTS.md](AGENTS.md) | Reglas cortas para quien programa, persona o asistente de IA | Al día |

## 3. Cómo está organizado el código

Sigue la organización del proyecto de reserva de salas: las vistas solo reciben y responden, los servicios orquestan y las reglas deciden.

```
config/        configuración de Django, URLs y ASGI (HTTP y WebSocket)
comun/         Rechazo, hora de La Paz, distancias y respuestas JSON
cuentas/       usuario, padrón, registro, sesión y usuarios (HU-01 a HU-03)
rutas/         rutas, horarios, paradas, horas aproximadas y modo registro (HU-04, HU-18)
viajes/        viajes, bus en vivo, «Voy a subir», abordajes y créditos (por hacer)
mensajes/      chat directo y chat de la ruta (por hacer)
padron/        padrón de ejemplo; la lista de la clase va aparte y no se sube
tests/         un test por criterio de aceptación (pytest)
frontend/      React con Tailwind y sus pruebas (Vitest)
docs/          documentación por sesión y guías
```

Cada app tiene `models.py`, `reglas.py`, `servicios.py`, `serializadores.py` y `views.py`. El detalle está en la [sesión 13–14](docs/sesion-13-14-diseno.md).

## 4. Cómo ponerlo a andar

Necesitas Python 3.13 y Node 22. En una terminal, el servidor:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1          # en Linux o macOS: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_rutas
python manage.py runserver
```

En otra terminal, la interfaz:

```powershell
cd frontend
npm install
npm run dev
```

Abre <http://localhost:5173> y regístrate con un código del padrón (de ejemplo: `70004` e `ismael@upb.example`). Pruebas: `pytest` y, en `frontend`, `npm test`. Todo lo demás está en la [guía de desarrollo](docs/guia-desarrollo.md); para el celular, en la [guía del modo registro](docs/guia-modo-registro.md).

## 5. Cómo trabajamos

- Nadie sube directo a `main`: cada historia va en su rama, entra a `develop` por Pull Request y la aprueba Hugo.
- Andrés dirige la implementación como Scrum Master: el 18/11 el equipo repartió las tareas y cada una quedó asignada en su issue de GitHub. Las sesiones de implementación son sábado y domingo.
- Todo cambio a algo ya acordado se registra en [cambios.md](docs/cambios.md).
