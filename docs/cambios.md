# Registro de cambios

Aquí se registra todo cambio a algo ya escrito o acordado: un requisito, una historia, una regla, el diseño o el plan. Cada cambio tiene motivo, fuente y fecha, para que nada cambie en silencio.

- Requisitos: [sesion-06-requisitos.md](sesion-06-requisitos.md) · Plan: [sesion-08-09-plan.md](sesion-08-09-plan.md) · Entrevistas: [entrevistas.md](entrevistas.md) · Costos: [sesion-15-costos.md](sesion-15-costos.md)

**Estados posibles**

- **Aplicado:** el cambio ya está en el documento afectado.
- **Propuesto:** se planteó, pero el Product Owner todavía no lo aprobó.

| ID | Fecha | Qué cambia | Antes | Después | Motivo | Fuente | Estado | Afecta |
|---|---|---|---|---|---|---|---|---|
| C-01 | 13/11/2026 | Integrantes del equipo | Cuatro integrantes, con Ismael | Tres integrantes: Hugo Zuñiga, Andrés Laura Vargas y Sebastian Cruz. Ismael queda en el padrón como estudiante de prueba | Ismael dejó el grupo | PO13 | Aplicado | Encabezados, padrón de ejemplo |
| C-02 | 13/11/2026 | Forma de pago | Pago con QR o en efectivo (perfil, HU-11) | Créditos en la app o efectivo; el QR se elimina | Sugerencia del docente: recargar créditos y pagar al chofer desde la app | DOC, PO13 | Aplicado | RF-15 a RF-18 |
| C-03 | 13/11/2026 | Espera del bus | Se evaluó una espera de hasta 5 minutos | Sin espera: horas aproximadas por parada; quien no está, se queda | Indicación del docente | DOC | Aplicado | RF-09, RF-11 |
| C-04 | 13/11/2026 | Registro | Código o correo (perfil, HU-01) | Código y correo juntos, con la misma verificación del proyecto de salas; el inicio de sesión sí acepta cualquiera de los dos | Mayor seguridad | PO13 | Aplicado | RF-01, RF-02 |
| C-05 | 13/11/2026 | Backlog | 12 historias (perfil) | 17 historias (HU-01 a HU-17) | Se suman gestión de usuarios, paradas propuestas, créditos, retiro y modificación de rutas | PO13 | Aplicado | Plan, sesión 7 |
| C-06 | 13/11/2026 | Documentación | README y `docs/01` a `06` por tema | Documentos por sesión con el formato del proyecto de salas | Decisión del Product Owner | PO13 | Aplicado | Todos los documentos |
| C-07 | 14/11/2026 | Tareas del plan | T22 era despliegue y ensayo | Se agregan T23 (simulador de escenarios y panel de demo, 10 h-p, Sebastian) y T24 (guion y ensayo de la demo, 3 h-p); T22 queda solo para el despliegue | Mostrar en clase que la app funciona, con escenarios que usan los mismos servicios que la app | Decisión del Product Owner, 14/11/2026 | Aplicado | Plan, sesión 15, diagramas de secuencia |
| C-08 | 16/11/2026 | Calendario de entrevistas | ENT-01 a Don Iván como chofer; ENT-06 a la administración de la UPB | ENT-01 se hizo con otro chofer de la Ruta Norte, contratado y coordinado por Don Iván; ENT-02 con una estudiante anónima; Don Iván pasa a ENT-03; la administración se pospone hasta saber con quién hablar | No se encontró a Don Iván | ENT-01 | Aplicado | `entrevistas.md`, plan (T04, T13) |
| C-09 | 16/11/2026 | Datos de los ejemplos | Parada inventada «Ventura Mall»; chofer de los ejemplos «Iván» | Paradas Sevilla, Petrol y Campos; chofer ficticio «Marco» | Usar las paradas reales que nombró el chofer y no confundir los ejemplos con Don Iván | ENT-01 | Aplicado | Sesión 6 (sección 0 y criterios), diagramas de secuencia |
| C-10 | 16/11/2026 | Dispositivo del chofer | Celular o tablet en un soporte, con cargador | La pantalla del bus, que tiene Wi-Fi, Chrome y GPS; la vista del chofer debe funcionar en ella. Se confirma en P-20 | El chofer dijo que usaría la pantalla del bus | ENT-01 | Aplicado | Sesión 6 (limitaciones y simulado), riesgo 3 del plan |
| C-11 | 16/11/2026 | Espera del bus | Sin espera (C-03) | Posible tolerancia de hasta 2 minutos | El chofer espera hasta 2 minutos; la estudiante prefiere que no espere; el docente dijo que no se espera | ENT-01, ENT-02, DOC | Propuesto (P-19); RF-09 no cambia | RF-09 |
| C-12 | 16/11/2026 | Orden de los recortes | 1.º sugerencia de saltar parada (RF-12) | 1.º modificación de rutas por el chofer (RF-21), 2.º paradas propuestas (RF-10) | El chofer cambia de ruta «casi nunca» y los estudiantes suben siempre en los mismos puntos | ENT-01, ENT-02 | Propuesto | Plan, sección 9 |
| C-13 | 16/11/2026 | Costos | Sin cálculo de costos; el plan sumaba 123 h-p | Sesión 15 de costos y hoja «UPBus · Costos y horas»; el plan suma 142 h-p (T00 del perfil, T23 y T24) | Llevar las cuentas del proyecto en horas-persona y bolivianos | Pedido del Product Owner, 14/11/2026 | Aplicado | Plan, `sesion-15-costos.md` |
| C-14 | 17/11/2026 | Entrevistas ENT-03 y ENT-07 | Las hacía Hugo, en el Sprint 2; sin guía para la administración | Las hace Andrés Laura Vargas el 18/11/2026 (hora por confirmar); se agrega la guía de ENT-07 | Reparto de trabajo decidido por el Product Owner | Decisión del Product Owner, 17/11/2026 | Aplicado | `entrevistas.md` (secciones 1, 7 y 8), plan (T13) |
| C-15 | 18/11/2026 | Calendario de entrevistas | ENT-07 a «la administración», sin saber con quién | ENT-03 hecha con Don Iván; ENT-07 es con la encargada del servicio en la UPB, que se registra como anónima; ENT-03 se documenta solo como tabla | Don Iván indicó con quién coordina en la UPB | ENT-03, decisión del Product Owner | Aplicado | `entrevistas.md` |
| C-16 | 18/11/2026 | Llegada a la U en la mañana | 07:45 [PROVISIONAL] | 07:40 | Don Iván: «el bus tiene que estar antes de las 7:40», porque las clases empiezan a las 7:45 | ENT-03 | Aplicado | Sesión 6 (sección 0, P-06), RF-11, RF-12 |
| C-17 | 18/11/2026 | Quién modifica una ruta | El chofer aplica cambios pequeños y los grandes los aprueba el administrador (RF-21) | El chofer solo propone; todo cambio lo aprueba el administrador | Los cambios de ruta y las paradas nuevas los decide la UPB | ENT-03 | Propuesto (P-25) | RF-10, RF-21 |

Para agregar un cambio: se copia la última fila, se le da el siguiente número y se completa cada columna.
