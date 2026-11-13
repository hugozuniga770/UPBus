# Forma de trabajo — UPBus

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Fecha: 13/11/2026
- Preguntas abiertas: [05-preguntas-abiertas.md](05-preguntas-abiertas.md) · Cambios: [cambios.md](cambios.md)

## 1. Equipo Scrum [ACUERDO]

| Rol | Quién | Responsabilidad |
|---|---|---|
| Product Owner | Hugo Zuñiga | Ordena el Product Backlog, define los criterios de aceptación y habla con estudiantes y choferes. |
| Scrum Master | Andrew | Cuida que el equipo siga Scrum, facilita los eventos y quita lo que traba al equipo. |
| Developers | Hugo Zuñiga, Sebastian Cruz, Andrew e Ismael | Construyen, prueban y revisan cada incremento. |

## 2. Sprints y eventos

La duración del sprint y las fechas hasta el 15 de diciembre se definen en P-23. [PENDIENTE]

| Evento | Cuándo | Qué sale de él |
|---|---|---|
| Sprint Planning | Al empezar cada sprint | Las historias que entran al sprint, movidas a «Por hacer» |
| Daily Scrum | Cada día hábil, 15 minutos como máximo | Qué hizo cada uno, qué hará y qué lo traba |
| Sprint Review | Al terminar el sprint | Demo de lo que funciona; el Product Owner acepta o rechaza cada historia |
| Retrospectiva | Después de la Review | Una o dos mejoras concretas para el siguiente sprint |

## 3. Tablero en GitHub Projects [PROPUESTA] · P-25

Columnas: **Backlog** → **Por hacer** → **En curso** → **En revisión** → **Hecho**.

| Etiqueta | Uso |
|---|---|
| `historia` | Issue que es una historia de usuario |
| `must`, `should`, `could` | Prioridad MoSCoW ([03-backlog.md](03-backlog.md)) |
| `backend`, `frontend` | Parte del sistema que toca |
| `docs` | Cambio solo de documentación |
| `bug` | Algo que no funciona como dice su criterio de aceptación |

Cada historia se crea con la plantilla [historia-de-usuario](../.github/ISSUE_TEMPLATE/historia-de-usuario.md) y se asigna a quien la desarrolla.

## 4. Ramas, commits y Pull Requests [PROPUESTA] · P-26

- La rama `main` está protegida: nadie sube directo, todo entra por Pull Request.
- Una rama por historia, con su número: `hu-04-bus-en-vivo`, `hu-07-voy-a-subir`.
- Los commits empiezan con la historia: `HU-04: muestra el bus en el mapa`.
- Cada Pull Request enlaza su issue (`Cierra #12`) y lo revisa otro integrante antes de unirlo.

## 5. Definition of Done [PROPUESTA] · P-28

Una historia está **Hecha** cuando:

1. Cumple todos sus criterios de aceptación.
2. Cada criterio tiene al menos una prueba automática que pasa.
3. Otro integrante revisó y aprobó el Pull Request.
4. Está unida a `main` y la integración continua pasa en verde.
5. Funciona en el navegador de un celular, no solo en la compu.
6. La documentación afectada está al día y, si algo cambió, figura en [cambios.md](cambios.md).
7. El Product Owner la aceptó en la Sprint Review.
