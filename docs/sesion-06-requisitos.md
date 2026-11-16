# Sesión 6 — Requisitos del MVP

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Integrantes: Hugo Zuñiga (Product Owner), Andrés Laura Vargas (Scrum Master) y Sebastian Cruz
- Docente: Ing. Alejandro Rodríguez (Certificación I) · Aprueba los requisitos: Hugo Zuñiga, como Product Owner
- Fecha: 13/11/2026 · Sprint 1 · Issue: por crear · Milestone: Sprint 1
- Actualizado: 16/11/2026 · entrevistas ENT-01 y ENT-02 (C-08 a C-11) y preguntas P-19 a P-24
- Plan: [Sesiones 8–9](sesion-08-09-plan.md) · Entrevistas: [entrevistas.md](entrevistas.md) · Cambios: [cambios.md](cambios.md) · Siglas: [glosario.md](glosario.md)

## 0. Cómo leer este documento

Cada requisito tiene un ID con el prefijo `BUS` (por ejemplo, `BUS-RF-09`). Dentro del documento se abrevia como RF-09.

| Marca | Significa |
|---|---|
| **[ACUERDO]** | Lo aprobó el Product Owner, o sale de la guía oficial de buses de la UPB. |
| **[PROPUESTA]** | Lo propuso el equipo y el Product Owner todavía no lo aprobó. |
| **[PROVISIONAL]** | Valor que rige mientras no se responda una pregunta abierta (P-xx, sección 6). |
| **[SIMULADO]** | En el MVP funciona con datos simulados. Se indica qué se simula y cómo sería en el servicio real. |

**Datos de los ejemplos.** Todos los criterios usan los mismos datos:

- **Ruta:** Ruta Norte, ingreso de las 06:40 desde La Fontana Family Club. Paradas de ejemplo: La Fontana (inicio, GUIA), Sevilla, Petrol y Campos (ENT-01) y Campus UPB (fin). El orden y las coordenadas de las tres intermedias son **[PROVISIONAL]** (P-18). Llegada límite a la U: 07:45 **[PROVISIONAL]** (P-06).
- **Tarifa:** 5 Bs por viaje (GUIA). 1 crédito = 1 Bs.
- **Personas** (códigos y correos de ejemplo **[PROVISIONAL]**, P-01):

| Código | Persona | Correo | En el padrón | Rol en UPBus |
|---|---|---|---|---|
| 70001 | Hugo Zuñiga | hugo.zuniga@upb.example | Activo | Administrador y estudiante |
| 70002 | Sebastian Cruz | sebastian.cruz@upb.example | Activo | Administrador y estudiante |
| 70003 | Andrés Laura Vargas | andres.laura@upb.example | Activo | Administrador y estudiante |
| 70004 | Ismael | ismael@upb.example | Activo | Estudiante |
| 70005 | Lucía Peña (ficticia) | lucia.pena@upb.example | Inactiva | — (para probar rechazos) |
| — | Marco (chofer, ficticio) | — | No está en el padrón | Chofer, cuenta creada por el administrador |

- **Hora:** todas las fechas y horas son de America/La_Paz. Cada criterio fija su «hora actual».

## 1. Fuentes

| ID | Fuente | Qué aporta |
|---|---|---|
| GUIA | Guía oficial «Buses I-26» de la UPB (PDF) | Rutas, puntos de partida, horarios, costo de 5 Bs, mínimo de 15 estudiantes, sin tiempo de espera, sin desvíos, funcionamiento por WhatsApp |
| PERFIL | Perfil de proyecto presentado el 07/11/2026 | Problema, árbol de problemas, objetivo general, objetivos específicos y las 12 historias iniciales |
| PO13 | Decisiones del Product Owner (Hugo Zuñiga), 13/11/2026 | Tecnología, roles, registro e inicio de sesión, paradas, horas aproximadas, créditos, permisos del chofer y lo que se simula |
| DOC | Indicaciones del docente comunicadas por Hugo, **fecha no registrada** | (1) Créditos en la app en lugar de pagar por QR. (2) Sin espera de 5 minutos: el bus pasa a una hora aproximada y quien no está se queda. |
| ENT | Entrevistas del 16/11/2026: ENT-01 (chofer de la Ruta Norte) y ENT-02 (estudiante de la Ruta Norte, anónima). Detalle en [entrevistas.md](entrevistas.md) | Paradas reales de la Ruta Norte, cómo se paga hoy, el dispositivo del chofer, que la ubicación se corta y cuánto espera el bus |

## 2. Alcance del MVP

**Incluye:** registro con el padrón, inicio y cierre de sesión, gestión de usuarios, rutas con paradas y horarios, viajes con el bus en vivo, «Voy a subir», ubicación del estudiante, paradas propuestas, horas aproximadas por parada, aviso de bus cerca, registro de quién subió, créditos (recarga, pago, comprobante, devolución y retiro), chat directo, chat de ruta, modificación de rutas y aviso de mínimo de estudiantes.

**Actores:** estudiante, chofer y administrador. Un administrador también puede usar las funciones de estudiante, porque también lo es **[ACUERDO, PO13]**.

### Qué puede hacer cada rol

| Función | Estudiante | Chofer | Administrador |
|---|---|---|---|
| Ver rutas, paradas, horarios y el bus en vivo | Sí | Sí | Sí |
| «Voy a subir», compartir ubicación, «He subido» | Sí | No | Sí (como estudiante) |
| Proponer una parada | Sí | Sí | Sí |
| Ver sus viajes asignados, iniciarlos y terminarlos | No | Sí, solo los suyos | No |
| Ver estudiantes confirmados y su ubicación | No | Solo durante su viaje | Sí |
| Marcar «subió» o «no se presentó» | No | Solo en su viaje | No |
| Recargar créditos y pagar el viaje | Sí | No | Sí (como estudiante) |
| Ver los pagos de un viaje | Los suyos | Solo los de su viaje | Todos |
| Retirar saldo | No | Sí, el suyo | No |
| Chat directo y chat de la ruta | Sí | Solo de su viaje y su ruta | Sí |
| Modificar una ruta | No | Cambios pequeños (RF-21) | Sí |
| Crear y eliminar choferes y personas | No | No | Sí |
| Aprobar recargas (simulado) y cambios grandes de ruta | No | No | Sí |

El chofer **no** puede ver otros viajes, ver datos de estudiantes fuera de su viaje ni gestionar usuarios **[ACUERDO, PO13]**.

### Lo que se simula en el MVP (declarado)

| Qué | Cómo funciona en el MVP | Cómo sería en el servicio real |
|---|---|---|
| Ubicación del bus | Un simulador recorre la ruta y envía posiciones como si fuera el dispositivo del chofer | La pantalla del bus, que tiene Wi-Fi, Chrome y GPS (ENT-01), o el celular del chofer con cargador; en los dos casos, con la página siempre abierta |
| Ubicación del estudiante | Posiciones simuladas (por ahora, las de Ismael) | El GPS del celular del estudiante |
| Recarga de créditos | El estudiante pide la recarga y un administrador la aprueba | Una pasarela de pagos cobra a una cuenta de empresa; cuando aprueba el pago, se cargan los créditos |
| Retiro del chofer | Se registra el retiro y el saldo baja | Transferencia a la cuenta del chofer |
| Padrón de la UPB | Un archivo con los integrantes e Ismael | La base de datos oficial de la universidad |

### Limitaciones del MVP (declaradas)

- La app es web. El GPS real del chofer exige la página abierta y la pantalla encendida; no se hace una app nativa **[ACUERDO, PO13]**. Según ENT-01, el bus tiene una pantalla con Wi-Fi, Chrome y GPS en la que el chofer podría dejar la página abierta (P-20).
- El bus no espera: no existe un tiempo de espera configurable **[ACUERDO, DOC]** (P-19).
- Los avisos se muestran dentro de la app abierta; no se envían por WhatsApp, correo ni SMS **[PROPUESTA]**.
- El chat es solo de texto **[PROVISIONAL]** (P-10).

**Fuera del MVP:** aplicación móvil nativa, pasarela de pagos real, facturación e impuestos (P-08), faltas de comportamiento del reglamento y conexión con el sistema real de la UPB.

## 3. Requisitos funcionales

### BUS-RF-01 — Registro con el padrón

- Origen: PERFIL; PO13 («tal como el de Raúl»). Prioridad: alta.
- Estado: **[ACUERDO]** (PO13). El padrón es **[SIMULADO]**.
- Requisito: una persona sin cuenta escribe su código **y** su correo. El sistema los busca en el padrón y, si cumplen todo, la persona elige su contraseña, la escribe dos veces y se crea su cuenta. Se rechaza si:
  1. el código no existe en el padrón («código no encontrado en el padrón»);
  2. el correo no es el de ese código («el correo no corresponde a ese código»);
  3. la persona está inactiva («persona no activa en el padrón»);
  4. la persona ya tiene cuenta («ya tienes una cuenta»);
  5. la contraseña y su confirmación no coinciden («las contraseñas no coinciden»). Se comprueba antes que las reglas de contraseña de Django.

  El padrón es de solo lectura: el sistema nunca lo modifica y no guarda contraseñas en él **[PROVISIONAL]** (P-04).
- Criterio de aceptación:
  - Aceptación: Ismael (70004, ismael@upb.example), sin cuenta, se registra con una contraseña válida. Se crea su cuenta con rol estudiante y el padrón no cambia.
  - Rechazo: Lucía (70005, inactiva) intenta registrarse. Se rechaza por «persona no activa en el padrón» y no se crea ninguna cuenta.
  - Rechazo: Ismael escribe dos contraseñas distintas. Se rechaza por «las contraseñas no coinciden» y no se crea ninguna cuenta.

### BUS-RF-02 — Inicio y cierre de sesión con código o correo

- Origen: PO13. Prioridad: alta.
- Estado: **[ACUERDO]** (PO13).
- Requisito: el usuario entra con su código **o** su correo, cualquiera de los dos, y su contraseña. Se comparan con su cuenta en la BD, sin consultar el padrón. Si algo falla, el mensaje es siempre «Código, correo o contraseña incorrectos», sin decir cuál. Al cerrar sesión, las operaciones vuelven a pedir inicio de sesión.
- Criterio de aceptación:
  - Situación inicial: Ismael tiene cuenta.
  - Aceptación: entra con su código 70004 y su contraseña; también entra con su correo y la misma contraseña.
  - Rechazo: con una contraseña incorrecta recibe «Código, correo o contraseña incorrectos», el mismo mensaje que con un código inexistente.

### BUS-RF-03 — Roles y permisos

- Origen: PERFIL; PO13. Prioridad: alta.
- Estado: **[ACUERDO]** (PO13).
- Requisito: cada cuenta tiene un rol: estudiante, chofer o administrador. Cada operación comprueba el rol en el servidor según la tabla de la sección 2; que un botón no aparezca no protege nada. Un administrador puede usar también las funciones de estudiante.
- Criterio de aceptación:
  - Aceptación: Hugo (administrador) marca «Voy a subir» en un viaje, igual que un estudiante.
  - Rechazo: Ismael (estudiante) intenta crear una cuenta de chofer. Se rechaza por «solo el administrador puede hacer esto» y no se crea nada.
  - Rechazo: Marco (chofer) pide los estudiantes de un viaje que no es suyo. Se rechaza por «este viaje no es tuyo».

### BUS-RF-04 — Gestión de usuarios

- Origen: PO13. Prioridad: alta.
- Estado: **[ACUERDO]** (PO13). La relación con el padrón es **[PROVISIONAL]** (P-04).
- Requisito: el administrador crea y elimina cuentas de chofer y de personas (estudiantes nuevos). Las cuentas de chofer no salen del padrón: las crea el administrador.
- Pendiente: una cuenta con viajes o movimientos de créditos se desactiva en lugar de borrarse, para no perder comprobantes **[PROPUESTA]** (P-23).
- Criterio de aceptación:
  - Aceptación: Hugo crea la cuenta de chofer de Marco; Marco puede iniciar sesión y ve solo las funciones de chofer.
  - Rechazo: Hugo intenta crear una cuenta con un correo que ya existe. Se rechaza por «ya existe una cuenta con ese correo».

### BUS-RF-05 — Rutas, paradas y horarios

- Origen: GUIA; PERFIL. Prioridad: alta.
- Estado: **[ACUERDO]** rutas, puntos de partida y horarios (GUIA). Paradas intermedias **[PROVISIONAL]** hasta la entrevista ENT-01.
- Requisito: cualquier usuario ve cada ruta en un mapa, con su recorrido, sus paradas en orden, sus horarios de ingreso y salida y la hora aproximada de paso por cada parada (RF-11). Consultar no modifica nada.
- Criterio de aceptación:
  - Aceptación: Ismael abre la Ruta Norte y ve el recorrido, las paradas La Fontana, Sevilla, Petrol, Campos y Campus UPB, y los horarios de ingreso 06:40, 11:00, 13:00 y 15:30. Nada cambia en la BD.

### BUS-RF-06 — Viaje: iniciar y terminar

- Origen: PERFIL; PO13. Prioridad: alta.
- Estado: **[ACUERDO]** (PO13).
- Requisito: un **viaje** es una salida concreta: ruta, horario, fecha y chofer. Sus estados son Programado → En curso → Terminado, o Cancelado. Solo el chofer asignado lo inicia y lo termina. Un chofer tiene un solo viaje en curso a la vez.
- Criterio de aceptación:
  - Situación inicial: Marco tiene asignado el viaje Ruta Norte 06:40 del lunes 16/11. Son las 06:38.
  - Aceptación: Marco inicia el viaje; pasa a En curso y queda la hora de inicio.
  - Rechazo: Marco intenta iniciar otro viaje sin terminar el primero. Se rechaza por «ya tienes un viaje en curso».

### BUS-RF-07 — Ubicación del bus en vivo

- Origen: PERFIL; ENT-01 («hay veces se corta en tiempo real, tengo que volver a ponerlo»); ENT-02 (lo que más pediría: «que mejoren la ubicación»). Prioridad: alta, porque es el problema central y las dos entrevistas lo confirman.
- Estado: **[ACUERDO]** (PO13). Fuente de la ubicación **[SIMULADO]**.
- Requisito: mientras el viaje está En curso, la posición del bus se guarda y se envía en tiempo real a quienes miran esa ruta. Si el viaje no está En curso, no se aceptan posiciones. Si deja de llegar la señal, se muestra la última posición con su hora.
- Criterio de aceptación:
  - Aceptación: con el viaje En curso, llega una posición del bus; queda guardada como la última y los estudiantes de la ruta la reciben.
  - Rechazo: llega una posición para un viaje Terminado. Se rechaza por «el viaje no está en curso» y no se guarda.

### BUS-RF-08 — Ubicación del estudiante

- Origen: PO13. Prioridad: alta.
- Estado: **[ACUERDO]** (PO13). Fuente de la ubicación **[SIMULADO]**.
- Requisito: el estudiante que marcó «Voy a subir» puede compartir su ubicación. La ve solo el chofer de ese viaje (y el administrador). Se deja de compartir en cualquiera de estos casos: el estudiante toca «He subido», el chofer marca «subió» o el viaje termina.
- Criterio de aceptación:
  - Aceptación: Ismael comparte su ubicación en el viaje de las 06:40; Marco la ve.
  - Límite: Marco marca «subió» a Ismael; la ubicación de Ismael deja de compartirse en ese momento.

### BUS-RF-09 — «Voy a subir»

- Origen: PERFIL; PO13; DOC. Prioridad: alta.
- Estado: **[ACUERDO]** (PO13, DOC).
- Entrevistas: ENT-02 está de acuerdo con que el bus no espere («porque después no llegamos [a la U]»). ENT-01 cuenta que hoy espera «hasta dos minutos», y como máximo uno más (P-19).
- Requisito: el estudiante marca «Voy a subir» para un viaje concreto y una parada. Al chofer le llega la alerta con su nombre y su parada. Puede cancelarlo mientras el bus no haya pasado su parada. El bus no espera: si el bus pasa la parada y el estudiante no subió ni canceló, el aviso se cancela solo y queda registrado como «no se presentó». Un estudiante tiene un solo «Voy a subir» por viaje.
- Criterio de aceptación:
  - Aceptación: Ismael marca «Voy a subir» en Sevilla para el viaje de las 06:40. Queda Confirmado y a Marco le llega «Ismael va a subir en Sevilla».
  - Rechazo: Ismael lo marca de nuevo para el mismo viaje. Se rechaza por «ya avisaste que vas a subir en este viaje».
  - Límite: el bus pasa Sevilla y sigue sin que Ismael suba. El aviso queda como «no se presentó», sin cobro.

### BUS-RF-10 — Paradas propuestas y paradas activas

- Origen: PO13. Prioridad: media.
- Estado: **[ACUERDO]** que estudiantes y choferes proponen paradas y que una parada solo está activa si hay alguien esperando (PO13). Cuándo queda guardada una parada propuesta: **[PROVISIONAL]** (P-05).
- Entrevistas: ENT-02 no propondría paradas, y ENT-01 dice que los estudiantes suben «todos los días [en] los mismos destinos». Por eso es el recorte 2 propuesto en el plan (C-12).
- Requisito: el estudiante y el chofer pueden proponer una parada sobre el recorrido de la ruta; no pueden modificar el recorrido. En cada viaje, una parada está **activa** solo si al menos un estudiante con «Voy a subir» en ella comparte su ubicación. Si no hay nadie, la parada no se enciende y no genera avisos.
- Criterio de aceptación:
  - Aceptación: Ismael propone la parada «Av. Banzer y 4to anillo» sobre el recorrido de la Ruta Norte. Queda registrada como propuesta.
  - Límite: en el viaje de las 06:40 nadie marcó Sevilla. La parada no está activa y el chofer no recibe avisos de ella.
  - Rechazo: Ismael propone una parada a más de 200 m del recorrido. Se rechaza por «la parada debe estar sobre la ruta» **[PROVISIONAL]** (P-07).

### BUS-RF-11 — Horas aproximadas por parada

- Origen: PO13; DOC. Prioridad: media.
- Estado: **[ACUERDO]** (PO13, DOC). Cantidad de viajes del promedio **[PROVISIONAL]** (P-11).
- Requisito: el bus «llega» a una parada cuando pasa a menos de 50 m. El sistema guarda la hora real de cada paso. La hora aproximada de una parada es la del primer viaje registrado y luego se ajusta con el promedio de los últimos viajes. A cada estudiante se le muestra a qué hora aproximada pasará el bus por su parada.
- Criterio de aceptación:
  - Aceptación: en el primer viaje, el bus pasa a 30 m de Sevilla a las 06:58. La hora aproximada de esa parada queda en 06:58.
  - Límite: en el segundo viaje pasa a las 07:02. La hora aproximada pasa a ser 07:00.
  - Límite: el bus pasa a 80 m de la parada. No cuenta como llegada.

### BUS-RF-12 — Sugerencia de saltar una parada

- Origen: PO13. Prioridad: baja.
- Estado: **[ACUERDO]** (PO13): la app solo avisa; el chofer decide.
- Requisito: si el bus va atrasado respecto de su hora de llegada a la U y en la siguiente parada no hay nadie confirmado ni a menos de 500 m, la app le sugiere al chofer no detenerse. Nunca decide por él.
- Criterio de aceptación:
  - Aceptación: el bus va 6 minutos atrasado y Sevilla no tiene confirmados. A Marco le aparece «Nadie espera en Sevilla: puedes seguir».
  - Límite: hay un estudiante confirmado a 300 m. No se muestra la sugerencia.

### BUS-RF-13 — Aviso de bus cerca

- Origen: PERFIL; PO13. Prioridad: media.
- Estado: **[ACUERDO]** 500 m (PO13).
- Requisito: el estudiante con «Voy a subir» recibe un aviso cuando el bus está a 500 m o menos de su parada. Se avisa una sola vez por viaje.
- Criterio de aceptación:
  - Aceptación: el bus queda a 480 m de Sevilla; Ismael recibe «Tu bus está cerca».
  - Límite: a 520 m no recibe aviso.

### BUS-RF-14 — Registrar quién subió

- Origen: PO13. Prioridad: alta.
- Estado: **[ACUERDO]** (PO13).
- Requisito: el abordaje se registra cuando el estudiante toca «He subido» o cuando el chofer marca «subió». En ese momento se cobra el viaje (RF-16) y al chofer le aparece el nombre con «ha subido, ha pagado», para que solo le pregunte su nombre.
- Criterio de aceptación:
  - Aceptación: Ismael, con 10 créditos, toca «He subido». Queda como A bordo, se le cobran 5 y a Marco le aparece «Ismael: ha subido, ha pagado».
  - Rechazo: Ismael toca «He subido» en un viaje Terminado. Se rechaza por «el viaje ya terminó».

### BUS-RF-15 — Recarga de créditos

- Origen: DOC; PO13. Prioridad: media.
- Estado: **[ACUERDO]** (PO13). La aprobación del pago es **[SIMULADO]**.
- Requisito: el estudiante pide una recarga eligiendo un monto. El monto mínimo es 5 Bs y solo se aceptan múltiplos de 5, sin tope **[PROVISIONAL]** (P-15). La recarga queda Pendiente hasta que se aprueba; al aprobarse, se suman los créditos. En el MVP la aprueba un administrador; en el servicio real la aprobaría la pasarela de pagos.
- Criterio de aceptación:
  - Aceptación: Ismael pide recargar 20 Bs y Hugo la aprueba. El saldo de Ismael sube 20 créditos y queda el movimiento.
  - Rechazo: Ismael pide recargar 12 Bs. Se rechaza por «el monto debe ser múltiplo de 5» y no se registra nada.
  - Límite: pide 5 Bs; se acepta.

### BUS-RF-16 — Pago del viaje y comprobante

- Origen: GUIA (5 Bs); DOC; PO13. Prioridad: media.
- Estado: **[ACUERDO]** (PO13).
- Entrevistas: hoy el chofer cobra por QR y en efectivo; en la salida le pagan al subir y en el ingreso de la mañana, al final del viaje (ENT-01, P-22). El chofer recibe el dinero y la empresa entrega la factura (ENT-01, P-08). ENT-02 prefiere pagar desde la app.
- Requisito: al registrarse el abordaje (RF-14) se cobran 5 créditos al estudiante y se suman al saldo del chofer. Cada pago genera un comprobante con ID de pago, código, correo y nombre del estudiante, ruta, viaje, fecha, hora y monto. El chofer ve los pagos de su viaje, con el total, y puede buscar uno por ID o por código. Si el estudiante no tiene saldo suficiente, queda como «paga en efectivo»: le paga al chofer al final de la ruta y el chofer lo marca **[PROVISIONAL]** (P-13). Un mismo abordaje nunca se cobra dos veces.
- Criterio de aceptación:
  - Aceptación: Ismael, con 10 créditos, sube. Queda con 5, el saldo de Marco sube 5 y existe un comprobante con su ID.
  - Límite: Ismael, con 0 créditos, sube. No se cobra y a Marco le aparece «Ismael: ha subido, paga en efectivo».
  - Rechazo: se envía dos veces el mismo «He subido». Se cobra una sola vez.

### BUS-RF-17 — Devolución por viaje cancelado

- Origen: PO13. Prioridad: baja.
- Estado: **[ACUERDO]** (PO13).
- Requisito: si un viaje se cancela después de que un estudiante pagó con créditos, se le devuelven los 5 créditos y se descuentan del saldo del chofer. La devolución queda como un movimiento propio; el pago original no se borra.
- Pendiente: si el chofer ya retiró su saldo, la devolución lo dejaría en negativo (P-24).
- Criterio de aceptación:
  - Aceptación: el viaje se cancela con el pago de Ismael hecho. Ismael recupera 5 créditos y quedan los dos movimientos: el pago y la devolución.

### BUS-RF-18 — Retiro del saldo del chofer

- Origen: DOC; PO13. Prioridad: baja.
- Estado: **[ACUERDO]** el chofer retira solo, sin aprobación (PO13). El retiro es **[SIMULADO]**.
- Requisito: el chofer retira todo o parte de su saldo. El saldo nunca queda en negativo.
- Criterio de aceptación:
  - Aceptación: Marco, con 40 Bs de saldo, retira 40. Queda en 0 y existe el movimiento de retiro.
  - Rechazo: Marco, con 40 Bs, intenta retirar 50. Se rechaza por «saldo insuficiente» y nada cambia.

### BUS-RF-19 — Chat directo

- Origen: PERFIL; PO13. Prioridad: media.
- Estado: **[ACUERDO]** (PO13). Mensajes rápidos concretos **[PROVISIONAL]** hasta ENT-01.
- Requisito: el estudiante y el chofer de un viaje pueden escribirse. El chofer dispone de respuestas rápidas para no escribir mientras maneja. El chat directo existe solo entre un estudiante con «Voy a subir» y el chofer de ese viaje.
- Criterio de aceptación:
  - Aceptación: Ismael, confirmado en el viaje, le escribe a Marco «Ya estoy en la parada»; Marco lo recibe con el nombre y la hora.
  - Rechazo: Ismael intenta escribirle al chofer de un viaje en el que no está confirmado. Se rechaza por «no estás en este viaje».

### BUS-RF-20 — Chat de la ruta

- Origen: PERFIL; PO13 («reemplazar el grupo de WhatsApp»). Prioridad: media.
- Estado: **[ACUERDO]** (PO13). Quiénes pertenecen **[PROVISIONAL]** (P-09). Solo texto **[PROVISIONAL]** (P-10).
- Requisito: cada ruta tiene un chat con los estudiantes que la eligieron y su chofer. Cada mensaje muestra quién lo envió y la hora.
- Criterio de aceptación:
  - Aceptación: Ismael, que eligió la Ruta Norte, escribe en su chat; lo ven los demás miembros.
  - Rechazo: Ismael intenta escribir en el chat de la Ruta Sur, que no eligió. Se rechaza por «no eres parte de esta ruta».

### BUS-RF-21 — Modificación de una ruta

- Origen: PO13. Prioridad: baja.
- Estado: **[ACUERDO]** quién puede y que la hora de llegada a la U no se toca (PO13). El umbral en metros es **[PROVISIONAL]** (P-07).
- Entrevistas: ENT-01 cambia de ruta «casi nunca: la misma ruta nomás, siempre», porque en esa zona no hay espacio para maniobrar. Por eso es el recorte 1 propuesto en el plan (C-12).
- Requisito: los estudiantes no modifican rutas. El chofer puede editar las paradas, sus horas y el recorrido de su ruta con cambios pequeños. Un cambio grande (mover el recorrido 2 cuadras o más, o cambiar de avenida) queda Pendiente hasta que un administrador lo aprueba o lo rechaza. Nadie más que el administrador puede cambiar la hora de llegada a la U.
- Criterio de aceptación:
  - Aceptación: Marco mueve un punto del recorrido 80 m. El cambio se aplica.
  - Límite: Marco mueve un punto 250 m. El cambio queda Pendiente y la ruta sigue igual hasta que Hugo lo aprueba.
  - Rechazo: Marco intenta cambiar la hora de llegada a la U. Se rechaza por «no puedes cambiar la hora de llegada a la U».

### BUS-RF-22 — Aviso de mínimo de estudiantes

- Origen: GUIA (mínimo 15); PO13. Prioridad: baja.
- Estado: **[ACUERDO]** la app solo avisa al administrador (PO13). Anticipación **[PROVISIONAL]** (P-17).
- Requisito: el administrador y el chofer ven cuántos estudiantes confirmaron cada viaje. Si faltando 30 minutos para la salida hay menos de 15 confirmados, el administrador recibe un aviso. La app no cancela el viaje.
- Criterio de aceptación:
  - Aceptación: a las 06:10 el viaje de las 06:40 tiene 9 confirmados; Hugo recibe el aviso y el viaje sigue Programado.
  - Límite: con 15 confirmados no hay aviso.

## 4. Requisitos de calidad

### BUS-RC-01 — El rechazo muestra la causa concreta

- Estado: **[PROPUESTA]** del equipo.
- Requisito: cada rechazo nombra su causa, con los mensajes de este documento. Un mensaje genérico como «Error» no cumple.

### BUS-RC-02 — Una consulta no modifica datos

- Estado: **[PROPUESTA]** del equipo.
- Requisito: ver rutas, el mapa, los pagos o los chats no crea, cambia ni borra nada en la BD.

### BUS-RC-03 — Un rechazo no deja la operación a medias

- Estado: **[PROPUESTA]** del equipo.
- Requisito: cuando una operación se rechaza, los datos quedan como estaban. En los créditos, un cobro, una devolución o un retiro se guardan completos o no se guardan, y un reintento no duplica el movimiento (RF-16).

### BUS-RC-04 — Lo simulado está identificado

- Estado: **[ACUERDO]** (PO13).
- Requisito: todo lo simulado lleva la marca [SIMULADO] en la documentación y está aislado en el código, para reemplazarlo sin tocar las reglas.

### BUS-RC-05 — Interfaz cuidada en celular y computadora

- Estado: **[ACUERDO]** (PO13).
- Requisito: las pantallas se ven bien en celular y en computadora, con la identidad de la UPB (inicio de sesión al estilo UPBnet) y un uso tipo Uber: mapa a pantalla completa y tarjetas que suben desde abajo.

## 5. Restricciones

| ID | Restricción | Estado |
|---|---|---|
| BUS-RT-01 | El servidor se hace con Django y Django REST Framework; las reglas de negocio, en Python | **[ACUERDO]** (PO13) |
| BUS-RT-02 | La persistencia usa SQLite | **[ACUERDO]** (PO13) |
| BUS-RT-03 | La interfaz se hace con React y Tailwind CSS, como aplicación aparte que consume la API | **[ACUERDO]** (PO13) |
| BUS-RT-04 | El tiempo real usa WebSockets (Django Channels) | **[ACUERDO]** (PO13) |
| BUS-RT-05 | La sesión se mantiene con la cookie de Django y protección CSRF | **[ACUERDO]** (PO13) |
| BUS-RT-06 | El mapa usa Leaflet con OpenStreetMap | **[ACUERDO]** (PO13) |
| BUS-RT-07 | Todas las fechas y horas se interpretan en America/La_Paz | **[ACUERDO]** (PO13) |
| BUS-RT-08 | Solo se usan servicios gratuitos, incluido el hosting | **[ACUERDO]** (PO13) |
| BUS-RT-09 | Las pruebas del servidor (pytest) y las de la interfaz (Vitest) están separadas | **[ACUERDO]** (PO13) |

## 5.1 Resumen de casos límite

| Requisito | Límite | Resultado |
|---|---|---|
| RF-09 | El bus pasa la parada y el estudiante no subió | El aviso queda como «no se presentó», sin cobro |
| RF-11 | El bus pasa a 50 m exactos de la parada | No cuenta: debe ser menos de 50 m **[PROVISIONAL]** |
| RF-13 | El bus está a 500 m exactos | Se avisa (a 501 m no) |
| RF-15 | Recarga de 5 Bs | Se acepta (4 o 12 se rechazan) |
| RF-16 | Sube con saldo 0 | No se cobra; paga en efectivo |
| RF-18 | Retira exactamente todo su saldo | Se acepta; queda en 0 |
| RF-21 | Mueve el recorrido 200 m exactos | Necesita aprobación **[PROVISIONAL]** |
| RF-22 | 15 confirmados exactos | No hay aviso (con 14 sí) |

## 6. Preguntas abiertas para el Product Owner

Mientras no haya respuesta, rige el valor provisional. Las que dependen de una entrevista indican cuál.

| ID | Pregunta | Valor provisional | Afecta |
|---|---|---|---|
| P-01 | ¿Qué códigos y correos reales van en el padrón? ¿El repositorio es público? | Códigos 70001 a 70005 y correos `@upb.example` | RF-01 |
| P-02 | ¿El equipo se sigue presentando como «Grupo 7»? | No se nombra el número de grupo | Encabezados |
| P-03 | ¿La cuenta del chofer lleva el nombre real de Don Iván? Respondida (ENT-01): Don Iván no es el chofer de los ejemplos; contrató al chofer entrevistado y es con quien este coordina el servicio con la UPB | Chofer de ejemplo ficticio: Marco | Ejemplos |
| P-04 | Si el administrador crea y elimina estudiantes, ¿el padrón sigue siendo de solo lectura? | Sí: el padrón no se toca; el administrador crea y elimina cuentas en la BD | RF-01, RF-04 |
| P-05 | «Solo para el primer día se guardan o no»: ¿quién decide que una parada propuesta queda guardada? | Queda guardada cuando el chofer o un administrador la aprueba; mientras tanto vale solo para ese viaje | RF-10 |
| P-06 | ¿A qué hora debe llegar a la U cada horario de ingreso? ¿Y las salidas a su punto final? Se pregunta en ENT-03 | 06:40 → 07:45; los demás, 65 minutos después de salir | RF-11, RF-12 |
| P-07 | ¿Cuántos metros son «2 cuadras»? ¿Quién decide qué es «cambio de avenida»? | 200 m; el cambio de avenida siempre pide aprobación | RF-10, RF-21 |
| P-08 | «Hablar de impuestos»: ¿se refiere a facturar los pagos o a una sanción por no presentarse? Respondida en parte (ENT-01): el chofer recibe el dinero y la empresa entrega la factura. Falta saber si habrá una sanción por no presentarse | «No se presentó» solo se registra; la app no factura | RF-09, RF-16 |
| P-09 | ¿El estudiante elige las rutas que usa? Eso define su chat de ruta | Sí: elige una o más y puede cambiarlas | RF-20 |
| P-10 | ¿El chat es solo de texto? ¿El administrador puede borrar mensajes? | Solo texto; el administrador puede borrar | RF-19, RF-20 |
| P-11 | ¿Con cuántos viajes se promedia la hora aproximada? | Los últimos 5 | RF-11 |
| P-12 | ¿El retiro del chofer tiene monto mínimo? | No | RF-18 |
| P-13 | ¿El chofer marca «pagó en efectivo» al final de la ruta? | Sí | RF-16 |
| P-14 | ¿Un administrador puede actuar también como chofer? | No: el chofer es una cuenta aparte | RF-03 |
| P-15 | ¿La recarga tiene monto máximo? | No | RF-15 |
| P-16 | ¿Qué hosting gratuito se usa? | Se decide en el Sprint 2 | RT-08 |
| P-17 | ¿Con cuánta anticipación se avisa al administrador que hay menos de 15? | 30 minutos antes de la salida | RF-22 |
| P-18 | ¿Cuáles son las paradas reales de cada ruta, su orden y sus coordenadas? Respondida en parte (ENT-01): la Ruta Norte pasa por «varios puntos de Sevilla», Petrol y parte de Campos. Faltan el orden, las coordenadas y las demás rutas (ENT-03) | Las paradas de la sección 0 | RF-05 |
| P-19 | El chofer de ENT-01 espera «hasta dos minutos», y como máximo uno más; el docente indicó que el bus no espera. ¿Se da una tolerancia de espera? | Sin espera, como indicó el docente (DOC) | RF-09 |
| P-20 | ¿Qué pantalla tiene el bus (sistema y navegador) y le da su ubicación a una página web? | Se asume que sí; se confirma con Don Iván y con una prueba en el bus | RF-07 |
| P-21 | El chofer mencionó una aplicación que «salió para los transportistas». ¿Cuál es y qué hace? | Se investiga como referencia; no cambia el alcance | Alcance |
| P-22 | ¿Cuándo se cobra? Hoy, en la salida se paga al subir y en el ingreso de la mañana, al final del viaje (ENT-01) | Con créditos se cobra al registrar que subió, en los dos sentidos; el efectivo se paga como hoy | RF-14, RF-16 |
| P-23 | Al eliminar una cuenta que tiene viajes o movimientos de créditos, ¿se borra o se desactiva? | Se desactiva, para no perder comprobantes | RF-04 |
| P-24 | Si el chofer ya retiró su saldo y se cancela un viaje, la devolución dejaría su saldo en negativo. ¿Quién la cubre? | Se permite el saldo negativo solo por una devolución, y se compensa con sus próximos cobros | RF-17, RF-18 |

## 7. Siguiente paso

- Documento siguiente: `docs/sesion-07-modelos.md`, con las historias HU-01 a HU-17, sus criterios Dado/Cuando/Entonces, los casos de uso, los estados del viaje, del «Voy a subir» y de la recarga, y la trazabilidad requisito → historia → criterio → test.
- Los criterios de este documento se reutilizan allí con los mismos datos, para que cada test salga de un criterio y no de un detalle del código.

## 8. Participación y asistencia utilizada

- **Hugo Zuñiga (Product Owner):** respondió las preguntas del 13/11/2026, definió los acuerdos, los valores provisionales y lo que se simula, y aprueba este documento.
- **Andrés Laura Vargas y Sebastian Cruz:** revisión pendiente antes del commit.
- **Asistencia de IA:** se usó Claude (Anthropic) para estudiar la estructura del proyecto de referencia (reserva de salas), ordenar las respuestas del Product Owner, proponer la estructura y redactar el borrador.
- **Hugo Zuñiga (16/11/2026):** hizo las entrevistas ENT-01 y ENT-02.
- **Asistencia de IA (16/11/2026):** se usó Claude (Anthropic) para pasar las entrevistas a este documento, cambiar los ejemplos (C-09) y redactar las preguntas P-19 a P-24.

## 9. Anexo — Datos de la guía de buses (GUIA)

| Sentido | Ruta | Punto de partida | Horarios |
|---|---|---|---|
| Ingreso | Norte | La Fontana Family Club (norte, anillo) | 06:40, 11:00, 13:00, 15:30 |
| Ingreso | Sur | Makro Parque (Av. Makro Parques) | 06:40, 11:00 |
| Ingreso | Externa | Gladymar (Av. Canal Cotoca, 2do anillo) | 06:40 |
| Ingreso | 4to Anillo | Farmacorp (4to anillo, Alemana) | 06:40 |
| Salida | Norte, Sur y Externa | Campus UPB | 12:15, 19:00, 21:15 |
| Salida | 4to Anillo | Campus UPB | 12:15 |
| Salida | Híbrida | Campus UPB | 14:30 |

Normas de uso según la guía: mínimo de 15 estudiantes para que la ruta siga funcionando; 5 Bs cada vez que se usa el bus; no hay tiempo de espera; los estudiantes deben unirse al grupo de su ruta; el bus no se desvía por pedido de un estudiante.
