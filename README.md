# UPBus — Buses UPB en tiempo real (UPB Santa Cruz)

- Materia: Certificación I · Docente: Ing. Alejandro Rodríguez
- Equipo (Grupo 7): Hugo Zuñiga (Product Owner), Andrew (Scrum Master), Sebastian Cruz e Ismael. Los cuatro son Developers.
- Tecnología acordada: Django con SQLite en el backend; React con Tailwind CSS en el frontend ([decisiones](docs/04-decisiones.md))
- Estado: documentación inicial. Todavía no hay código.

## 1. Qué es

Aplicación web que conecta en tiempo real a los estudiantes y a los choferes de los buses de la UPB Santa Cruz. Hoy el servicio se coordina por grupos de WhatsApp: el chofer comparte su ubicación a mano, el bus no espera y nadie sabe quién está por llegar a la parada. UPBus reemplaza esos grupos por un mapa en vivo, avisos y chat dentro de la app.

**Objetivo del producto:** que ningún estudiante de la UPB Santa Cruz pierda el bus por falta de información.

La visión completa, el problema y el alcance están en [01-vision.md](docs/01-vision.md).

## 2. Qué va a permitir

| Historia | Qué permite | Rol |
|---|---|---|
| HU-01 | Registrarse con el código o correo del padrón UPB y una contraseña | Estudiante |
| HU-02 | Entrar y ver solo las funciones de su rol | Todos |
| HU-03 | Ver rutas, paradas y horarios de ingreso y salida | Estudiante |
| HU-04 | Ver el bus en vivo en el mapa | Estudiante |
| HU-05 | Iniciar la ruta y compartir la ubicación automáticamente | Chofer |
| HU-06 | Compartir su ubicación mientras espera | Estudiante |
| HU-07 | Avisar «Voy a subir» con una alerta al chofer | Estudiante |
| HU-08 | Recibir un aviso cuando el bus está cerca | Estudiante |
| HU-09 | Chatear directo con el chofer | Estudiante y chofer |
| HU-10 | Usar el chat grupal de la ruta | Estudiante y chofer |
| HU-11 | Pagar con QR o en efectivo | Estudiante y chofer |
| HU-12 | Gestionar rutas, paradas, horarios y choferes | Administrador |

Criterios de aceptación y prioridades: [03-backlog.md](docs/03-backlog.md). Requisitos y reglas: [02-requisitos.md](docs/02-requisitos.md).

## 3. Documentación

| Documento | Para qué sirve |
|---|---|
| [01-vision.md](docs/01-vision.md) | Problema, usuarios, objetivo del producto y alcance del MVP |
| [02-requisitos.md](docs/02-requisitos.md) | Requisitos funcionales y no funcionales, reglas del negocio y padrón simulado |
| [03-backlog.md](docs/03-backlog.md) | Product Backlog: historias de usuario con criterios de aceptación |
| [04-decisiones.md](docs/04-decisiones.md) | Decisiones técnicas tomadas y por tomar |
| [05-preguntas-abiertas.md](docs/05-preguntas-abiertas.md) | Dudas que el equipo debe resolver (P-01 a P-28) |
| [06-forma-de-trabajo.md](docs/06-forma-de-trabajo.md) | Scrum, tablero, ramas y Definition of Done |
| [cambios.md](docs/cambios.md) | Registro de todo cambio a algo ya acordado |
| [glosario.md](docs/glosario.md) | Significado de las siglas (RF, HU, CA, P-xx…) |

## 4. Cómo ponerlo a andar

Pendiente. Esta sección se escribe cuando exista el primer código y estén resueltas las preguntas P-01, P-05 y P-06 ([preguntas abiertas](docs/05-preguntas-abiertas.md)).

## 5. Cómo trabajamos

Cada historia de usuario es un issue en GitHub Projects, creado con la plantilla [historia-de-usuario](.github/ISSUE_TEMPLATE/historia-de-usuario.md). El tablero, las ramas y la Definition of Done están en [06-forma-de-trabajo.md](docs/06-forma-de-trabajo.md).
