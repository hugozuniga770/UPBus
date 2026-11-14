# Sesiones 8 y 9 — Plan del MVP (Scrum, por sprints)

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Repositorio: [UPBus](https://github.com/hugozuniga770/UPBus)
- Integrantes: Hugo Zuñiga (Product Owner), Andrés Laura Vargas (Scrum Master) y Sebastian Cruz. Los tres son Developers.
- Docente: Ing. Alejandro Rodríguez (Certificación I)
- Fecha del plan: 13/11/2026 · Avance: jueves 19/11/2026 · Entrega final: martes 15/12/2026
- Issue: por crear · Milestone: Sprint 1
- Requisitos: [Sesión 6](sesion-06-requisitos.md) · Cambios: [cambios.md](cambios.md)

## 1. Punto de partida

- El 07/11/2026 se presentó el perfil del proyecto: problema, árbol de problemas, objetivos y 12 historias iniciales.
- El 13/11/2026 el Product Owner tomó las decisiones que originan este plan (fuente PO13 de los requisitos).
- El equipo pasó de cuatro a tres integrantes: Ismael dejó el grupo y queda en el padrón como estudiante de prueba.
- Se toma como referencia de estilo y organización el proyecto de reserva de salas (documentos por sesión, capas `views` → `servicios` → `reglas`, un test por criterio de aceptación).
- El repositorio empieza vacío: todavía no hay código.

## 2. Alcance del MVP

El alcance completo está en la [sección 2 de los requisitos](sesion-06-requisitos.md). Se entrega por incrementos:

| Sprint | Incremento que debe funcionar |
|---|---|
| Sprint 1 | Documentación base, entorno, registro con el padrón e inicio de sesión por rol |
| Sprint 2 | Gestión de usuarios, rutas con paradas y horarios en el mapa, viajes y bus en vivo (simulado) |
| Sprint 3 | «Voy a subir», ubicación del estudiante (simulada), paradas propuestas, horas aproximadas, aviso de bus cerca y registro de quién subió |
| Sprint 4 | Créditos (recarga, pago, comprobante, devolución y retiro), chats, modificación de rutas y aviso de mínimo |
| Cierre | Pruebas completas, trazabilidad, despliegue en hosting gratuito y ensayo de la defensa |

## 3. Método: Scrum

- **Sprints de una semana**, de viernes a jueves. El último tramo (11 al 15 de diciembre) es de cierre.
- **Roles:** el Product Owner ordena el backlog y aprueba; el Scrum Master cuida el método y quita lo que traba al equipo; los tres desarrollan.
- **Eventos:** Sprint Planning el viernes, Daily Scrum de 15 minutos cada día hábil, y Sprint Review y Retrospectiva el jueves.
- **Ramas:** nadie sube directo a `main`. Cada historia se trabaja en su rama (`hu-07-voy-a-subir`), entra a `develop` por Pull Request y la aprueba Hugo. Solo Hugo une `develop` con `main`, al cerrar cada sprint.
- **Commits:** cada commit cita su issue con `#n` y empieza con su historia (`HU-07: …`).
- **Cambios:** si algo ya acordado cambia, no se cambia en silencio: se registra en `docs/cambios.md` con motivo y fecha, y después se corrige.
- **Pruebas:** los criterios de aceptación se definen en la sesión 7 y cada uno es exactamente un test.
- **Definition of Done:** la historia cumple todos sus criterios; cada criterio tiene su test y pasa; el Pull Request está aprobado por Hugo; la integración continua pasa en verde; se ve bien en celular y computadora; la documentación afectada está al día.

## 4. Tareas

Las estimaciones son en horas-persona (h-p) y son **[PROPUESTA]**: no hay horas medidas de un trabajo parecido.

| ID | Trabajo | Evidencia de terminación | Esfuerzo (h-p) | Responsable | Sprint |
|---|---|---|---:|---|---|
| T01 | Plan y requisitos | `sesion-08-09-plan.md` y `sesion-06-requisitos.md` aprobados | 4 | Hugo | 1 |
| T02 | Historias, criterios y casos de uso | `sesion-07-modelos.md` aprobado | 5 | Hugo | 1 |
| T03 | Diseño y arquitectura | `sesion-13-14-diseno.md` y `sesion-12-arquitectura.md` aprobados | 5 | Hugo y Sebastian | 1 |
| T04 | Entrevista al chofer (ENT-01) | Registro en `entrevistas.md` y paradas reales cargadas | 2 | Hugo | 1 |
| T05 | Entorno del servidor | Django, DRF y Channels arrancan; SQLite creada | 3 | Andrés | 1 |
| T06 | Entorno de la interfaz | React con Tailwind arranca y habla con la API | 3 | Andrés | 1 |
| T07 | Integración continua | GitHub Actions corre pytest y Vitest por separado | 2 | Andrés | 1 |
| T08 | Padrón, registro e inicio de sesión (HU-01, HU-02) | Tests de HU-01 y HU-02 en verde; pantallas de registro e inicio de sesión | 8 | Hugo | 1 |
| T09 | Gestión de usuarios (HU-03) | El administrador crea y elimina choferes y personas | 4 | Hugo | 2 |
| T10 | Rutas, paradas y horarios (HU-04) | Comando `cargar_rutas`; las rutas se ven en el mapa | 8 | Sebastian | 2 |
| T11 | Viajes y bus en vivo (HU-05, HU-06) | El chofer inicia el viaje; el simulador mueve el bus en el mapa por WebSocket | 10 | Sebastian | 2 |
| T12 | Base visual | Estilo UPB, navegación por rol y componentes comunes | 6 | Andrés | 2 |
| T13 | Entrevistas a estudiantes y a la UPB (ENT-02 en adelante) | Registros en `entrevistas.md` y cambios derivados | 4 | Hugo | 2 |
| T14 | «Voy a subir» y ubicación del estudiante (HU-07) | Alerta al chofer; el aviso se cancela solo si no sube | 8 | Sebastian | 3 |
| T15 | Paradas propuestas y horas aproximadas (HU-08) | Paradas activas; hora aproximada por parada | 8 | Sebastian | 3 |
| T16 | Aviso de bus cerca y registro de quién subió (HU-09, HU-10) | Aviso a 500 m; «ha subido» en la lista del chofer | 6 | Andrés | 3 |
| T17 | Créditos: recarga y pago (HU-11, HU-12) | Recarga aprobada; cobro al subir; comprobante | 10 | Hugo | 3 y 4 |
| T18 | Retiro del chofer (HU-13) | El chofer retira y el saldo no queda negativo | 3 | Hugo | 4 |
| T19 | Chats (HU-14, HU-15) | Chat directo y chat de ruta por WebSocket | 8 | Andrés | 4 |
| T20 | Modificación de rutas y aviso de mínimo (HU-16, HU-17) | Cambio grande pendiente de aprobación; aviso con menos de 15 | 6 | Sebastian | 4 |
| T21 | Trazabilidad y pruebas completas | `trazabilidad.md` completa; todos los tests en verde | 5 | Los tres | Cierre |
| T22 | Despliegue y ensayo | App publicada en hosting gratuito con HTTPS; demo ensayada | 5 | Los tres | Cierre |

Esfuerzo total: **123 h-p**.

**Reparto** **[ACUERDO]** (PO13):

- **Hugo:** cuentas, padrón y créditos, además de la documentación y las entrevistas.
- **Sebastian:** rutas, viajes y mapa.
- **Andrés:** mensajes, base de la interfaz e integración continua.

## 5. Orden y dependencias

```mermaid
flowchart LR
    T01[T01 Requisitos] --> T02[T02 Historias] --> T03[T03 Diseño]
    T03 --> T05[T05 Entorno servidor] --> T08[T08 Cuentas]
    T03 --> T06[T06 Entorno interfaz] --> T12[T12 Base visual]
    T08 --> T09[T09 Usuarios] --> T10[T10 Rutas] --> T11[T11 Viajes y bus en vivo]
    T11 --> T14[T14 Voy a subir] --> T15[T15 Paradas y horas]
    T14 --> T16[T16 Aviso y abordaje] --> T17[T17 Créditos] --> T18[T18 Retiro]
    T11 --> T19[T19 Chats]
    T10 --> T20[T20 Rutas y mínimo]
    T18 --> T21[T21 Trazabilidad] --> T22[T22 Despliegue]
```

La cadena más larga es T01 → T02 → T03 → T05 → T08 → T09 → T10 → T11 → T14 → T16 → T17 → T18 → T21 → T22. Un atraso en ella atrasa la entrega.

## 6. Calendario

| Sprint | Fechas | Planning | Review y Retrospectiva |
|---|---|---|---|
| Sprint 1 | 13/11 al 19/11 | vie 13/11 | jue 19/11 (avance al docente) |
| Sprint 2 | 20/11 al 26/11 | vie 20/11 | jue 26/11 |
| Sprint 3 | 27/11 al 03/12 | vie 27/11 | jue 03/12 |
| Sprint 4 | 04/12 al 10/12 | vie 04/12 | jue 10/12 |
| Cierre | 11/12 al 15/12 | vie 11/12 | mar 15/12 (entrega final) |

```mermaid
gantt
    title UPBus — plan por sprints
    dateFormat YYYY-MM-DD
    axisFormat %d/%m
    section Sprint 1
    Documentación (T01-T03)        :2026-11-13, 5d
    Entorno y CI (T05-T07)         :2026-11-14, 4d
    Cuentas (T08)                  :2026-11-15, 5d
    Avance al docente              :milestone, 2026-11-19, 0d
    section Sprint 2
    Usuarios y rutas (T09, T10)    :2026-11-20, 4d
    Viajes y bus en vivo (T11)     :2026-11-22, 5d
    Base visual (T12)              :2026-11-20, 7d
    section Sprint 3
    Voy a subir (T14)              :2026-11-27, 4d
    Paradas y horas (T15)          :2026-11-29, 5d
    Aviso y abordaje (T16)         :2026-11-30, 4d
    section Sprint 4
    Créditos y retiro (T17, T18)   :2026-12-01, 9d
    Chats (T19)                    :2026-12-04, 6d
    Rutas y mínimo (T20)           :2026-12-06, 5d
    section Cierre
    Trazabilidad y despliegue      :2026-12-11, 4d
    Entrega final                  :milestone, 2026-12-15, 0d
```

## 7. Disponibilidad y capacidad

- Capacidad supuesta **[PROVISIONAL]**: 8 horas por persona por sprint, 24 h-p por sprint y 96 h-p en cuatro sprints, más el cierre.
- El trabajo estimado (123 h-p) **supera** esa capacidad. Por eso los recortes de la sección 9 están aprobados de antemano.
- Cada integrante confirma sus horas reales en el Sprint Planning.

## 8. Riesgos

| # | Riesgo | Señal de alerta | Respuesta |
|---|---|---|---|
| 1 | El alcance creció (créditos, paradas que aprenden, cambios de ruta) con un integrante menos | Al cerrar el Sprint 2 no funciona el bus en vivo | Aplicar los recortes de la sección 9, en orden |
| 2 | WebSockets en un hosting gratuito | El chat o el mapa no se actualizan fuera de la computadora local | Probar el despliegue en el Sprint 2, no al final |
| 3 | El GPS real no funciona con la pantalla apagada | — | Queda [SIMULADO] en el MVP y declarado como limitación |
| 4 | Las entrevistas cambian las reglas | ENT-01 contradice un acuerdo | Registrar el cambio en `cambios.md` y ajustar el backlog en el siguiente Planning |
| 5 | Los créditos tienen errores de saldo | Un test de pago falla o un saldo queda negativo | Todo movimiento se guarda completo o no se guarda; pruebas de doble envío |
| 6 | Datos personales reales en un repositorio público | Códigos o correos reales en el padrón | Usar datos de ejemplo hasta responder P-01 |

## 9. Recortes aprobados (en este orden)

**[PROPUESTA]** hasta que el Product Owner los confirme. Si falta tiempo, se recorta desde arriba:

1. Sugerencia de saltar una parada (RF-12).
2. Modificación de rutas por el chofer (RF-21): solo el administrador edita.
3. Chat de la ruta (RF-20): queda el chat directo.
4. Retiro del chofer (RF-18): solo se muestra su saldo.
5. Paradas propuestas (RF-10): solo paradas cargadas por el administrador.
6. Horas aproximadas aprendidas (RF-11): horas fijas por parada.

No se recortan: registro, inicio de sesión, bus en vivo, «Voy a subir» y registro de quién subió.

## 10. Entregables e hitos

| Hito | Fecha | Qué se muestra | Estado |
|---|---|---|---|
| Avance | 19/11/2026 | Documentación de las sesiones 6 a 14 y el incremento del Sprint 1 | Pendiente |
| Review Sprint 2 | 26/11/2026 | Bus en vivo en el mapa | Pendiente |
| Review Sprint 3 | 03/12/2026 | «Voy a subir» de punta a punta | Pendiente |
| Review Sprint 4 | 10/12/2026 | Créditos y chats | Pendiente |
| Entrega final | 15/12/2026 | App desplegada, pruebas en verde y defensa | Pendiente |

Al cerrar cada sprint se anota aquí la fecha real y el SHA del commit de cierre.

## 11. Cambios al plan

| Fecha | Cambio | Motivo |
|---|---|---|
| 13/11/2026 | Primera versión del plan | — |

## 12. Dudas abiertas

Las preguntas P-01 a P-18 están en la [sección 6 de los requisitos](sesion-06-requisitos.md). Para este plan pesan sobre todo P-06 (horas de llegada), P-16 (hosting) y P-18 (paradas reales).

## 13. Participación y asistencia utilizada

- **Hugo Zuñiga:** definió los sprints, el reparto y las fechas, y aprueba este plan.
- **Asistencia de IA:** se usó Claude (Anthropic) para proponer las tareas, las estimaciones, el orden y los riesgos a partir de las decisiones del Product Owner.
