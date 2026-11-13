# Preguntas abiertas — UPBus

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Fecha: 13/11/2026
- Decisiones: [04-decisiones.md](04-decisiones.md) · Cambios: [cambios.md](cambios.md)

Dudas que el equipo debe resolver. Cuando se responda una, se anota la respuesta y la fecha en la columna «Respuesta», y si cambia algo ya escrito se registra en [cambios.md](cambios.md). Las recomendaciones son solo una sugerencia para decidir más rápido.

## 1. Arquitectura y tecnología

| ID | Pregunta | Recomendación | Respuesta |
|---|---|---|---|
| P-01 | ¿React va como aplicación aparte que habla con una API de Django, o dentro de las plantillas de Django? | Aparte (por ejemplo, con Vite) y la API con Django REST Framework. | — |
| P-02 | ¿El tiempo real se hace con WebSockets (Django Channels) o con consultas cada pocos segundos? | Consultas cada 5 a 10 segundos para el MVP; es más simple y alcanza para pocos buses. | — |
| P-03 | ¿Qué mapa usamos: Leaflet con OpenStreetMap o Google Maps? | Leaflet con OpenStreetMap: es gratis y no pide tarjeta para la clave. | — |
| P-04 | ¿Cómo se mantiene la sesión entre React y Django: cookie de sesión de Django o tokens (JWT)? | Cookie de sesión de Django, que ya viene incluida. | — |
| P-05 | ¿Qué versiones de Python, Django y Node usamos? | Las mismas en los cuatro equipos; anotarlas en el README. | — |
| P-06 | ¿Dónde corre la app para las demos: en una compu local o en un hosting? | Local para desarrollar. Ojo: algunos hostings gratuitos borran el archivo de SQLite al reiniciarse. | — |
| P-07 | El GPS del chofer funciona desde el navegador solo con la página abierta y la pantalla encendida. ¿Aceptamos esa limitación en el MVP? | Sí: tablet o celular en un soporte, con cargador. | — |
| P-08 | Los avisos de bus cerca, ¿se muestran dentro de la página abierta o como notificaciones del navegador? | Dentro de la página para el MVP; las notificaciones del navegador son más complejas. | — |

## 2. Datos y padrón

| ID | Pregunta | Recomendación | Respuesta |
|---|---|---|---|
| P-09 | ¿Qué campos tiene el padrón simulado y qué formato tienen el código y el correo institucional? | Código, nombre, correo, carrera y activo ([02-requisitos.md](02-requisitos.md), sección 5). | — |
| P-10 | ¿El padrón usa personas ficticias o compañeros reales? | Ficticias, para no publicar datos de nadie en el repo. | — |
| P-11 | La guía solo trae el punto de partida y el mapa de cada ruta. ¿Quién levanta las paradas intermedias y sus coordenadas? | Pedírselas al chofer de confianza y marcarlas en el mapa. | — |
| P-12 | ¿Cargamos las cinco rutas desde el principio o solo una para el piloto? | Solo la Ruta Norte al principio; las demás cuando el flujo funcione. | — |

## 3. Reglas del producto

| ID | Pregunta | Recomendación | Respuesta |
|---|---|---|---|
| P-13 | ¿El estudiante se inscribe a rutas fijas o elige su ruta cada día? Define quién está en cada chat de ruta. | Se inscribe a una o más rutas y puede cambiarlas. | — |
| P-14 | «Voy a subir», ¿se marca para un viaje concreto (fecha y horario)? ¿Hasta cuándo se puede cancelar? ¿Qué pasa si marca y no sube? | Por viaje; se puede cancelar hasta que el bus pase por la parada; no subir no tiene sanción en el MVP. | — |
| P-15 | Si no llegan a 15 confirmaciones, ¿la app solo avisa al administrador o cancela el viaje sola? ¿Con cuánta anticipación? | Solo avisa al administrador; la decisión la toma una persona. | — |
| P-16 | ¿Cuándo se deja de compartir sola la ubicación del estudiante? | Al subir al bus, cuando el bus pasa su parada o a los 20 minutos. | — |
| P-17 | ¿Cuándo es «bus cerca»: por tiempo (por ejemplo, 5 minutos) o por distancia (por ejemplo, 500 m)? | Por distancia en el MVP, porque es más fácil de calcular bien. | — |
| P-18 | En el chat de la ruta, ¿solo texto o también fotos y audios? ¿El administrador puede moderar? | Solo texto en el MVP; el administrador puede borrar mensajes. | — |
| P-19 | En el chat directo, ¿el chofer puede escribir primero? ¿Qué mensajes rápidos tendrá cada uno? | Sí puede escribir primero; definir 3 o 4 mensajes rápidos con el chofer de confianza. | — |
| P-20 | En el pago con QR, ¿el QR es del bus o del chofer? ¿El estudiante y el administrador ven un historial de pagos? | QR del bus cargado por el administrador; el chofer confirma; historial visible para ambos. | — |
| P-21 | ¿Incluimos el reporte de faltas de comportamiento que menciona el reglamento (maltrato de asientos, falta de respeto al chofer)? | Dejarlo fuera del MVP. | — |

## 4. Equipo y forma de trabajo

| ID | Pregunta | Recomendación | Respuesta |
|---|---|---|---|
| P-22 | ¿Cuáles son los nombres completos de Andrew e Ismael para la documentación? | — | — |
| P-23 | ¿Cuánto dura cada sprint y qué se entrega al ingeniero antes del 15 de diciembre? | Sprints de una semana para tener varias revisiones. | — |
| P-24 | ¿Quién valida los requisitos: el ingeniero, como cliente, o el Product Owner? | Confirmarlo con el ingeniero en la próxima clase. | — |
| P-25 | ¿Qué columnas y etiquetas tendrá el tablero de GitHub Projects? | Las de [06-forma-de-trabajo.md](06-forma-de-trabajo.md). | — |
| P-26 | ¿Trabajamos con una rama por historia y Pull Request revisado por otro integrante? | Sí, con `main` protegida. | — |
| P-27 | ¿Qué pruebas y qué integración continua usamos? | Pruebas de Django en el backend, Vitest en el frontend y GitHub Actions. | — |
| P-28 | ¿Aprobamos la Definition of Done propuesta? | La de [06-forma-de-trabajo.md](06-forma-de-trabajo.md). | — |
