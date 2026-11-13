# Decisiones — UPBus

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Fecha: 13/11/2026
- Preguntas abiertas: [05-preguntas-abiertas.md](05-preguntas-abiertas.md) · Cambios: [cambios.md](cambios.md)

Aquí se anota cada decisión técnica o de producto, con su motivo y lo que implica. Una decisión no se borra: si cambia, se agrega una nueva que la reemplaza y se registra en [cambios.md](cambios.md).

## 1. Decisiones tomadas

| ID | Fecha | Decisión | Motivo | Consecuencias |
|---|---|---|---|---|
| D-01 | 13/11/2026 | Backend en **Django** | El equipo ya lo conoce y lo usó en proyectos anteriores. | Trae listos el sistema de usuarios, el panel de administración y las migraciones. |
| D-02 | 13/11/2026 | Base de datos **SQLite** | No requiere instalar ni configurar un servidor; viene con Django. | Admite una sola escritura a la vez: alcanza para el desarrollo, las pruebas y un piloto con pocos buses. Si el servicio crece, Django permite pasar a PostgreSQL cambiando la configuración. |
| D-03 | 13/11/2026 | Frontend en **React** | Interfaz que se actualiza sin recargar la página, necesaria para el mapa y los chats. | Hay que definir cómo se comunica con Django (P-01) y cómo se mantiene la sesión (P-04). |
| D-04 | 13/11/2026 | Estilos con **Tailwind CSS** | Permite aplicar rápido la identidad visual de la UPB (RNF-07). | Los colores UPB se definen una sola vez en la configuración de Tailwind. |
| D-05 | 06/11/2026 | Primero **aplicación web**; app móvil solo si la web funciona bien | Se llega a todos desde el navegador del celular sin publicar en tiendas. | El GPS depende del navegador (P-07). |
| D-06 | 06/11/2026 | **Padrón simulado** de la UPB, consultado desde un solo módulo | No hay acceso al sistema real de la universidad. | Se puede conectar después al sistema real sin rehacer la app (RNF-08). |
| D-07 | 06/11/2026 | Tablero y backlog en **GitHub Projects**, una historia por issue | Mismo flujo que el equipo ya usó. | Detalle en [06-forma-de-trabajo.md](06-forma-de-trabajo.md). |

## 2. Decisiones pendientes

Cada una depende de una pregunta abierta. Cuando el equipo la responda, pasa a la tabla de arriba con un nuevo número D-xx.

| Tema | Pregunta | Recomendación del Product Owner |
|---|---|---|
| Cómo se conectan React y Django | P-01 | React como aplicación aparte que consume una API hecha con Django REST Framework. |
| Cómo se logra el tiempo real | P-02 | Para el MVP, que la app consulte la ubicación cada pocos segundos; WebSockets solo si hace falta después. |
| Qué mapa se usa | P-03 | Leaflet con OpenStreetMap, gratis y sin clave. |
| Cómo se mantiene la sesión | P-04 | La sesión con cookie de Django, que ya viene incluida. |
| Versiones de las herramientas | P-05 | Definirlas antes del primer commit y anotarlas en el README. |
| Dónde corre la aplicación | P-06 | Local para el desarrollo; decidir el hosting antes de la primera demo. |
