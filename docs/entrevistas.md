# Entrevistas

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Responsable: Hugo Zuñiga (Product Owner)
- Creado: 13/11/2026 · Actualizado: 26/11/2026, ENT-07 respondida por escrito y cierre de T13 (C-35, C-36). El 18/11/2026: entrevista ENT-03 a Don Iván y guía de ENT-07 ajustada (C-15 a C-17) · Issue: [#7](https://github.com/hugozuniga770/UPBus/issues/7) · Milestone: Sprint 1
- Requisitos que dependen de estas entrevistas: [sesion-06-requisitos.md](sesion-06-requisitos.md), sección 6 · Cambios: [cambios.md](cambios.md)

## 0. Cómo leer este documento

- Cada entrevista tiene un ID (ENT-01, ENT-02…).
- Las respuestas de las secciones 2 y 3 son citas de la transcripción automática. Lo que va entre corchetes lo agregamos para que se entienda; por ejemplo, la transcripción escribió «al lado» donde se dijo «a la U».
- Las transcripciones completas están en los anexos A y B.
- Si una respuesta cambia un requisito, se registra en [cambios.md](cambios.md) y en la sección 5.
- No se nombra a las personas entrevistadas, salvo Don Iván, que dio permiso (ENT-03). La encargada del servicio en la UPB (ENT-07) queda anónima.
- ENT-03 se registra solo como tabla de preguntas y respuestas, sin transcripción completa.
- ENT-07 se respondió por escrito: su tabla tiene las respuestas tal como llegaron, entre comillas.

## 1. Calendario

| ID | A quién | Rol | Fecha | Estado |
|---|---|---|---|---|
| ENT-01 | Chofer de la Ruta Norte, contratado (no es Don Iván) | Chofer | 16/11/2026 · Hecha por Hugo y Sebastian | Hecha · 5 min 41 s |
| ENT-02 | Estudiante de la Ruta Norte (anónima) | Estudiante | 16/11/2026 · Hecha por Hugo y Sebastian | Hecha · 2 min 31 s |
| ENT-03 | Don Iván, coordinador del servicio de transporte | Coordinación del servicio | 18/11/2026 · la hizo Andrés y Hugo | Hecha · 2 min 55 s grabados |
| ENT-04 a ENT-06 | Estudiantes de otras rutas (Sur, Externa, 4to Anillo–Urubó) | Estudiante | — | No se hicieron: T13 se cerró con ENT-07 (C-36) |
| ENT-07 | Encargada del servicio de buses en la UPB (anónima) | Administración (Recursos Humanos) | 26/11/2026 · por correo: Hugo le envió la guía y ella la respondió | Hecha · por escrito |

**Cambio de calendario (C-08).** El 13/11 se pensaba entrevistar a Don Iván como chofer (ENT-01) y a la administración como ENT-06. No se encontró a Don Iván, y ENT-01 se hizo con otro chofer de la Ruta Norte. Ese chofer dijo que coordina el servicio con Don Iván, así que Don Iván pasa a ser ENT-03 y es quien puede llevarnos a la administración.

**Responsable de ENT-03 y ENT-07 (C-14).** Las dos entrevistas las hace Andrés Laura Vargas, el 18/11/2026; la hora se confirma con cada persona. Hugo revisa las respuestas y decide los cambios, como Product Owner. Si la persona de la administración no está disponible ese día, ENT-07 se hace con quien indique Don Iván, dentro del Sprint 2. Al final, la encargada pidió recibir las preguntas por correo: Hugo se las envió y ella las respondió por escrito el 26/11 (C-36).

## 2. ENT-01 — Chofer de la Ruta Norte

- Fecha: 16/11/2026 · Duración: 5 min 41 s, grabada y transcrita
- Entrevistado: chofer de la Ruta Norte, contratado. No se registró su nombre.
- Entrevistó: Hugo Zuñiga y Sebastian Cruz

| # | Pregunta | Respuesta |
|---|---|---|
| 1 | ¿Qué rutas y horarios maneja? | «Solamente ruta norte.» |
| 2 | ¿Cuántos choferes y buses hay en total? | «Creo que son 3 o 4, porque hacen ruta sur, hacen este, [ruta] externa.» |
| 3 | ¿Cuántos estudiantes suben por viaje? ¿Qué viajes van más llenos? | «Como estamos a fin de año, son pocos. Al principio entraban 25, 24, 23, 22 a veces.» Los más llenos: «En la mañana y en la tarde.» |
| 4 | ¿Cuáles son las paradas reales de su ruta? | «Tenemos de Sevilla varios puntos, casi todos los de Sevilla.» «A veces suben en Petrol, […] parte de Campos.» |
| 5 | ¿Cuál es el problema más frecuente con los estudiantes? | «Eso lo dejo a criterio de cada uno.» No respondió. |
| 6 | ¿Cómo le pagan y cuándo? | «Por QR y efectivo.» En la salida, «al ingresar aquí»; en la mañana, «al finalizar». |
| 7 | ¿Qué opina de cobrar con créditos de una app y retirar el saldo al final? | «Sería bueno probar, porque hay una que salió para los transportistas.» |
| 8 | ¿Le serviría ver la ubicación de cada estudiante en tiempo real? | «Sería bien.» |
| 9 | ¿En qué dispositivo la usaría? | «En la pantalla [del bus].» Tiene Wi-Fi, se puede entrar a Chrome y «tiene GPS, tiene todo». |
| 10 | ¿Cómo sabe hoy dónde va a subir alguien? | «Porque ya están los destinos […] todos los días los mismos destinos: Sevilla, Petrol, todo eso.» |
| 11 | ¿Y si un estudiante nuevo quiere usar el bus por primera vez? | «Tendría que explicarle cómo es la movida […] y revisar los horarios, porque hay diferentes.» |
| 12 | ¿Su ubicación en tiempo real se corta? | «Hay veces se corta en tiempo real, tengo que volver a ponerlo.» |
| 13 | Si la app le sugiere cuándo parar o esperar, ¿la usaría? | «Sí, espero hasta dos minutos, luego me llaman al otro lado.» Como máximo «un minutito más». «A veces se atrasa […] pero le meto pata para llegar.» |
| 14 | ¿Qué cambios de ruta hace por su cuenta? | «Casi nunca. La misma ruta nomás, siempre.» En su zona tiene que «hacer maniobras con microlíneas […] y si no, no vas a llegar nunca». |
| 15 | ¿Quién recibe el dinero? ¿Se entrega factura? | «Yo. Bueno, la empresa da factura.» |
| 16 | ¿Para quién trabaja y con quién coordina en la UPB? | «Contratado, soy contratado.» Coordina «con Don Iván». |

**Lo que aporta ENT-01**

- Confirma el problema central: la ubicación que comparte por WhatsApp se corta y tiene que volver a ponerla (RF-07).
- Da las paradas reales de la Ruta Norte: varios puntos de Sevilla, Petrol y parte de Campos (P-18).
- Los estudiantes suben siempre en los mismos puntos, y un estudiante nuevo no tiene cómo enterarse si nadie le explica (RF-05).
- El bus tiene una pantalla con Wi-Fi, Chrome y GPS (P-20).
- Hoy espera hasta 2 minutos, y como máximo 3 (P-19). Casi nunca cambia la ruta (RF-21).
- Cobra por QR y en efectivo, y la empresa factura (P-08, P-22). Le parece bien probar los créditos.
- Coordina el servicio con Don Iván, que pasa a ser ENT-03.

## 3. ENT-02 — Estudiante de la Ruta Norte

- Fecha: 16/11/2026 · Duración: 2 min 31 s, grabada y transcrita
- Entrevistada: estudiante de la Ruta Norte (anónima)
- Entrevistaron: Hugo Zuñiga y Sebastian Cruz

| # | Pregunta | Respuesta |
|---|---|---|
| 1 | ¿Qué ruta y horarios usas? ¿Cuántas veces por semana? | «Lo ocupo 5 veces a la semana. La ruta de entrada a las 7 de la mañana norte, y a la salida a las 12 igual norte.» |
| 2 | ¿Te dejó el bus alguna vez? | «No, nunca me ha dejado el bus.» «Alguna vez, cuando hubo alguna falla o algo, me vine en taxi.» |
| 3 | ¿Qué te molesta del grupo de WhatsApp del bus? | «Nada, lo tengo silenciado.» Es cómodo, pero «mejoraría las ubicaciones de los señores». |
| 4 | ¿Alguna vez no supiste dónde estaba el bus? | «No cargaba la ubicación y le escribí a un amigo que ya estaba en el bus, que me mandó su ubicación en tiempo real.» |
| 5 | ¿Compartirías tu ubicación con el chofer mientras esperas? | «Sí.» |
| 6 | ¿Confiarías en la hora aproximada que te diera la app? | «Sí.» |
| 7 | ¿Propondrías una parada nueva? | «No.» |
| 8 | ¿Recargarías créditos en la app para pagar? | Al principio dudó: «no siempre ocupo el bus». Cuando le explicaron que recarga solo cuando quiere: «Más fácil. Sí, yo creo que sí.» |
| 9 | ¿Qué te parece que, si no estás en la parada a la hora, el bus siga sin esperar? | «Está bien que no espere […] porque después no llegamos [a la U].» |
| 10 | ¿Usarías el chat directo con el chofer? | «Lo he ocupado varias veces, sí.» |
| 11 | Si pudieras pedir una sola cosa a una app de los buses, ¿qué sería? | «Que mejoren la ubicación […] es recurrente el problema de que no carga la ubicación en algunos conductores.» |

**Lo que aporta ENT-02**

- Lo que más pediría es que la ubicación funcione: confirma que RF-07 es lo más importante.
- Ya le escribe directo al chofer por WhatsApp, así que el chat directo (RF-19) reemplaza algo que ya hace.
- Compartiría su ubicación y confiaría en la hora aproximada (RF-08, RF-11).
- Acepta que el bus no espere (RF-09) y pagar desde la app (RF-15, RF-16).
- No propondría paradas (RF-10).
- Nunca la dejó el bus. Su problema es no saber dónde está.

## 4. Lo que coincide y lo que no

| Tema | ENT-01 (chofer) | ENT-02 (estudiante) | ENT-03 (Don Iván) | Conclusión |
|---|---|---|---|---|
| Ubicación del bus | Se corta y hay que volver a ponerla | No carga en algunos choferes; es lo que más pediría | Usan el GPS de WhatsApp; el internet se corta | Es el problema principal: RF-07 va primero y debe mostrar la última posición cuando se corta la señal |
| Paradas | Siempre las mismas | No propondría paradas | Las paradas nuevas las decide la UPB | Las paradas propuestas (RF-10) valen poco por ahora |
| Espera | Espera hasta 2 minutos | Está bien que no espere | «Mayormente son 2 minutos» | Dos de tres fuentes dicen 2 minutos: hay que decidir P-19 |
| Pago | QR y efectivo; la empresa factura | Prefiere pagar desde la app | La empresa factura y la UPB paga el mes; con créditos, el dinero va al conductor | Los créditos tienen buena acogida; falta entender cómo se combinan el pago mensual y los 5 Bs (P-26) |
| Comunicación | — | Ya chatea con el chofer | — | El chat directo tiene sentido |
| Cambios de ruta | Casi nunca | — | Los decide la UPB | El chofer no debería cambiar la ruta solo (C-17) |
| Llegada a la U | — | Entra a las 7:00 | Antes de las 7:40 | La hora límite de la mañana es 07:40 (C-16) |
| Rutas activas | Cree que son 3 o 4 | — | 4: Norte, Externa, Sur y 4to Anillo–Urubó | La Híbrida de la guía no aparece (P-27) |
| Una app así | — | — | La UPB pensaba hacer una el próximo año; aceptan una prueba piloto | Hay interés real, y también la posibilidad de que la UPB haga la suya |

**Para la defensa.** El perfil presentó el problema como «me dejó el bus». Las dos entrevistas apuntan más a «no sé dónde está el bus». Es el mismo problema visto desde dos lados, pero conviene empezar la defensa por la ubicación.

## 5. Qué cambió por las entrevistas

| Entrevista | Respuesta | Requisito afectado | Cambio |
|---|---|---|---|
| ENT-01 | Coordina el servicio con Don Iván | Calendario de entrevistas | C-08: Don Iván pasa a ENT-03 |
| ENT-01 | Paradas: Sevilla, Petrol y Campos | Ejemplos de la sesión 6, P-18 | C-09: la parada inventada «Ventura Mall» se reemplaza por Sevilla |
| ENT-01 | Don Iván no es el chofer de los ejemplos | Ejemplos de la sesión 6, P-03 | C-09: el chofer de los ejemplos pasa a ser ficticio (Marco) |
| ENT-01 | La pantalla del bus tiene Wi-Fi, Chrome y GPS | Limitaciones y tabla de lo simulado | C-10, con P-20 |
| ENT-01 y ENT-02 | Espera de 2 minutos frente a no esperar | RF-09 | C-11 propuesto, con P-19; RF-09 no cambia |
| ENT-01 y ENT-02 | Ruta fija y nadie propone paradas | Recortes del plan | C-12 propuesto: RF-21 y RF-10 pasan a ser los primeros recortes |
| ENT-01 | La empresa factura; en la mañana se paga al final | RF-16, P-08, P-22 | Se agrega al requisito; P-08 queda respondida en parte |
| ENT-01 y ENT-02 | La ubicación se corta | RF-07 | Se agrega como origen; sigue siendo prioridad alta |
| ENT-03 | El bus debe estar en la U antes de las 7:40 | P-06, ejemplos de la sesión 6 | C-16: la llegada límite de la mañana pasa de 07:45 a 07:40 |
| ENT-03 | Los cambios de ruta y las paradas nuevas los decide la UPB | RF-10, RF-21 | C-17 propuesto: el chofer solo propone cambios; los aprueba el administrador |
| ENT-03 | Habilitar o cancelar una ruta lo decide la UPB | RF-22 | Confirma que la app solo avisa al administrador |
| ENT-03 | Espera de «mayormente 2 minutos» | RF-09, P-19 | Segunda fuente a favor de la tolerancia; P-19 sigue abierta |
| ENT-03 | Con créditos, el dinero va al conductor | RF-16 | Confirma el abono al chofer |
| ENT-03 | Hay 4 rutas habilitadas | Ejemplos, anexo de la sesión 6 | P-27: confirmar si la Híbrida sigue activa |
| ENT-07 | El servicio lo administra Recursos Humanos, y así debe seguir | Actores de la sesión 6 | En el servicio real, el administrador de UPBus sería Recursos Humanos (C-35) |
| ENT-07 | La ubicación de los estudiantes es sensible y no hace falta para operar el servicio | RF-08 | No se guarda un historial de ubicaciones; se mantiene que compartirla es opcional y que solo queda la última (C-35) |
| ENT-07 | La empresa fija la tarifa y la UPB prefiere no manejar pagos | RF-15, P-26 | P-26 respondida; en el servicio real los créditos los administraría la empresa |
| ENT-07 | Los retiros del chofer se coordinan con Recursos Humanos | RF-18 | Se agrega al requisito |
| ENT-07 | Padrón real con código y nombre, pedido a Sistemas por la jefatura de carrera; correo `@upb.edu` | RF-01, P-01 | P-01 respondida |
| ENT-07 | Los choferes siguen su ruta, salvo desvíos de emergencia | RF-21 | Un desvío de emergencia no es un cambio de ruta (C-35) |
| ENT-07 | Las rutas se habilitan antes del semestre, según los inscritos | RF-22, P-27 | Se agrega al requisito; el aviso por viaje solo informa |
| ENT-07 | La única condición es la hora de llegada a la U | P-19, RF-12 | P-19 respondida: la app no fija una espera |
| ENT-07 | Reclamos: no saben si el bus está cerca y no los esperan lo suficiente | RF-07, RF-09, RF-13 | Confirma el problema que resuelven el bus en vivo, «Voy a subir» y el aviso de bus cerca |
| ENT-07 | Le servirían estudiantes por ruta y puntualidad de llegada | Alcance | P-34 nueva, fuera del MVP |
| ENT-07 | Para adoptarla: una demostración completa y la información solo para la UPB | Limitaciones de la sesión 6, P-21 | Se agrega a las limitaciones; P-21 respondida en parte |

## 6. Límites de estas entrevistas

- Las dos son de la Ruta Norte. Las otras cuatro rutas pueden tener otros problemas.
- Es una persona por rol: sirven para orientar, no para decir cuántos estudiantes tienen cada problema.
- En ENT-03 no quedó grabada la respuesta sobre el rol de Don Iván.
- La transcripción es automática y tiene errores, como «al lado» por «a la U».
- En las próximas, pedir el permiso para grabar al empezar la grabación, para que quede registrado.
- ENT-07 se respondió por escrito: no hubo repreguntas, y la pregunta 6 (horas de llegada, P-06) quedó sin respuesta.
- No se entrevistó a estudiantes de otras rutas (ENT-04 a ENT-06). De la Ruta Sur se sabe lo que mostró el primer viaje grabado ([REG-01](viajes-grabados.md)).

## 7. ENT-03 — Don Iván (coordinador del servicio)

- Fecha: 18/11/2026 · Entrevistador: Hugo zuñiga y Andrés Laura Vargas · Duración grabada: 2 min 55 s
- Permiso: autorizó que se use su nombre en la documentación («Claro, no hay ningún problema»).
- La respuesta a la pregunta 1 no se grabó; se anota como la recordó el equipo.

| # | Pregunta | Respuesta |
|---|---|---|
| 1 | ¿Cuál es su rol en el servicio y con quién de la UPB coordina? | Según contó (no se grabó), trabaja para la UPB, tiene una empresa de transporte y coordina con la encargada del servicio en la UPB (ENT-07) |
| 2 | ¿Cuántos buses y choferes hay, y qué hace cada uno? | «En total, ahorita están habilitadas 4 rutas: Norte, Externa, Sur y Cuarto Anillo–Urubó». Recogen en la mañana y llevan en la tarde o en la noche |
| 3 | ¿A qué hora debe llegar cada bus a la U? | «En la mañana, el bus tiene que estar antes de las 7:40», porque las clases empiezan a las 7:45 |
| 4 | ¿Qué pasa con una ruta de menos de 15 estudiantes? ¿Quién decide? | «Los encargados son los de la UPB. Nosotros solo [sabemos lo que] nos dicen: se habilita, no se habilita o se cancela la ruta» |
| 5 | ¿Quién decide un cambio de ruta o una parada nueva? | «Los de la UPB» |
| 6 | ¿El bus espera a un estudiante que avisa que está llegando? ¿Cuánto? | «Mayormente son 2 minutos» |
| 7 | ¿Quién recibe el pago, quién factura y cómo se rinde el dinero? | «Nosotros entregamos las facturas y ellos [la UPB] son los que pagan el íntegro de todo el mes» |
| 8 | ¿Qué pantalla tienen los buses? ¿Usan Wi-Fi o GPS? | «El GPS del WhatsApp» |
| 9 | ¿Podrían usar una pantalla para ver la ubicación de cada estudiante? | «Eso se iba a hacer para el próximo año. Iba a haber una aplicación, porque a veces el internet se corta, es mala señal» |
| 10 | Si los estudiantes pagan con créditos de una app, ¿a qué cuenta debería llegar el dinero? | «El encargado de la ruta, el conductor» |
| 11 | ¿Conoce la app para transportistas que mencionó un chofer? | «Eso no. Pero para el año iba a haber varios cambios sobre el transporte» |
| 12 | ¿Se podría hacer una prueba piloto con una aplicación? | «Claro» |
| 13 | ¿Podemos usar su nombre en la documentación? | «Claro, no hay ningún problema» |

## 8. ENT-07 — Encargada del servicio en la UPB (anónima)

- Fecha: 26/11/2026 · Por correo: ella pidió recibir las preguntas por escrito; Hugo Zuñiga le envió esta guía y ella la devolvió respondida.
- Respondió la encargada del servicio, del área de Recursos Humanos de la UPB. Queda anónima.
- Las preguntas son las de la guía preparada para esta entrevista; las marcadas con ★ eran las prioritarias. Las respuestas van tal como llegaron, con la ortografía corregida.

| # | Pregunta | Respuesta |
|---|---|---|
| 1 | ★ ¿Qué área de la UPB está a cargo del servicio de buses y cuál es su rol en él? | «El área de recursos humanos»; ella está a cargo del servicio en esa área |
| 2 | ¿Cómo se contrata el servicio: con la empresa de Don Iván o con cada chofer? ¿Hasta cuándo dura el contrato? | «El contrato se hace con la empresa cuyo representante es Iván» |
| 3 | ★ Don Iván dijo que hay 4 rutas habilitadas. ¿La Ruta Híbrida sigue funcionando? ¿Cuántos buses hay? (P-27, P-18) | «Las rutas se habilitan si existe un mínimo de estudiantes interesados e inscritos en las mismas, mediante solicitud escrita se puede habilitar una nueva ruta» |
| 4 | ¿Cuántos estudiantes usan el servicio? ¿Llevan un registro por ruta y por día? | «La cantidad de estudiantes varía cada semestre. No se lleva un registro diario, solo los inscritos a las rutas de cada semestre» |
| 5 | ★ ¿Quién aprueba los cambios de ruta y las paradas nuevas? ¿Un chofer podría hacer un desvío pequeño sin pedir permiso? (RF-10, RF-21, C-17) | «La gestión de las rutas se las gestiona en base a la cantidad de estudiantes que solicitan el uso del servicio. Los choferes deben adherirse a su ruta, pero pueden hacer desvíos de emergencia por casos de fuerza mayor» |
| 6 | ¿A qué hora debe llegar cada uno de los otros horarios de ingreso? ¿Y las salidas a su punto final? (P-06) | Sin respuesta |
| 7 | ★ Con menos de 15 estudiantes, ¿cómo deciden habilitar, no habilitar o cancelar una ruta? ¿Cómo se avisa a los estudiantes? (RF-22, P-17) | «Previo al inicio del semestre los estudiantes se inscriben a una ruta, si no se llega al mínimo requerido la ruta no se habilita» |
| 8 | Los choferes esperan «mayormente 2 minutos». ¿Es una regla de la UPB o la regla es no esperar? (P-19) | «La única condicional es la hora de llegada a la universidad, los choferes pueden gestionar su tiempo para cumplir con este requisito» |
| 9 | ¿Qué reclamos reciben con más frecuencia sobre los buses? | «Los estudiantes no saben si el bus de su ruta está cerca a su ubicación y los choferes no los esperan lo suficiente» |
| 10 | ★ ¿Cómo se relaciona el pago mensual de la UPB con los 5 Bs que cada estudiante paga al chofer? (P-26, P-08, P-22) | «La universidad contrata el servicio tercerizado, pero la empresa es la que establece la tarifa para que le sea rentable» |
| 11 | Si los estudiantes recargaran créditos en una app, ¿a qué cuenta debería llegar el dinero? ¿La UPB usaría una pasarela de pagos? (RF-15, RF-16) | «Sería preferible mantener el método actual para que la universidad no maneje pagos adicionales» |
| 12 | ¿Quién debería controlar los retiros del chofer desde la app? (RF-18) | «Esa responsabilidad debe mantenerse en coordinación con Recursos Humanos» |
| 13 | ★ ¿La UPB podría darnos un padrón real o un servicio para validar estudiantes? ¿Qué datos se podrían usar? (RF-01, P-01, P-04) | «Con el código y el nombre de estudiantes podría ser suficiente, mediante su jefatura de carrera deben hacer las gestiones para que sistemas les provea los datos que necesitan» |
| 14 | ¿Qué condiciones pone la universidad para guardar la ubicación de los estudiantes y sus pagos? (riesgo 6 del plan) | «La ubicación de los estudiantes es una información sensible que no es necesaria manejar para la operación del servicio» |
| 15 | ¿Cuál es el formato del código de estudiante y el dominio del correo institucional? (P-01) | «Los códigos de estudiantes son una secuencia de números única para cada estudiante y el correo institucional es @upb.edu» |
| 16 | ★ ¿Qué tienen pensado para la aplicación de transporte del próximo año? ¿Podría UPBus servir como base o prueba? (P-21) | «Se pueden hacer tramos de prueba con la aplicación, si es completamente funcional» |
| 17 | ¿Qué reportes le servirían: estudiantes por ruta, puntualidad, pagos? | «Por ahora es suficiente con la cantidad de estudiantes por ruta y la puntualidad de la llegada de buses a la universidad» |
| 18 | ¿Quién debería ser el administrador de UPBus: alguien de la UPB, Don Iván o los dos? | «La administración del servicio debe mantenerse en recursos humanos» |
| 19 | ★ Don Iván aceptó una prueba piloto. ¿La UPB la autorizaría? ¿Qué necesitaría para aprobarla? | «Una demostración de que la aplicación funciona a cabalidad» |
| 20 | ¿Qué tendría que cumplir la app para que la UPB la adopte de verdad? | «Que la información de la UPB se mantenga para uso exclusivo de la universidad, que ninguna persona externa tenga acceso» |
| 21 | ¿Hay algo del servicio que no preguntamos y que deberíamos saber? | «Creo que tienen la información justa para realizar su proyecto» |
| 22 | ¿Podemos volver a contactarle cuando tengamos un prototipo para mostrarle? | «Cuando sea funcional, claro que sí» |

## 9. Guía para estudiantes (ENT-04 en adelante)

Al empezar: pedir permiso para grabar y aclarar que sus respuestas son anónimas.

1. ¿Qué ruta y qué horarios usas? ¿Cuántas veces por semana?
2. ¿En qué parada subes? ¿Cómo sabes a qué hora pasa el bus por ahí?
3. ¿Te dejó el bus alguna vez? ¿Qué pasó y cómo llegaste a la U?
4. ¿Qué es lo que más te molesta del grupo de WhatsApp?
5. ¿Alguna vez no supiste dónde estaba el bus? ¿Qué hiciste?
6. ¿Compartirías tu ubicación con el chofer mientras esperas? ¿Con qué condiciones?
7. Si la app te dijera la hora aproximada en que pasa el bus por tu parada, ¿confiarías en ella?
8. ¿Propondrías una parada nueva? ¿Dónde?
9. ¿Cómo pagas hoy? ¿Preferirías recargar créditos en la app o seguir en efectivo? ¿Cuánto recargarías de una vez?
10. ¿Qué te parece que, si no estás en la parada a la hora, el bus siga sin esperar?
11. ¿Usarías un chat directo con el chofer? ¿Para qué?
12. Si pudieras pedir una sola cosa a la app, ¿qué sería?

## Anexo A — Transcripción de ENT-01 (chofer de la Ruta Norte)

Transcripción automática, sin corregir. Se cambiaron los «Hablante n» por el rol de cada persona.

**[00:02] Entrevistador:** Eh, disculpe, ¿qué rutas y horarios maneja?

**[00:07] Chofer:** Solamente ruta norte.

**[00:08] Entrevistador:** Ruta norte. ¿Y cuántos choferes y buses hay en total?

**[00:13] Chofer:** Creo que son 3 o 4, porque hacen ruta sur, hacen este, curvón externo. Creo que eso nomás son.

**[00:32] Entrevistador:** ¿Los estudiantes más o menos suben por viaje? ¿Y qué rutas van más llenas y cuáles más vacías?

**[00:39] Chofer:** Al principio era, este, como estamos a fin de año, son pocos. Al principio entraban 25, 24, 23, 22 a veces.

**[00:50] Entrevistador:** ¿Y qué rutas eran las que iban más llenas?

**[00:52] Chofer:** En la mañana y en la tarde.

**[00:55] Entrevistador:** Mmm, ya. Eh, ¿cuáles son las paradas normales, o sea, reales en su ruta, más o menos? Así, solamente un aproximado de zonas.

**[01:06] Chofer:** Tenemos de Sevilla varios puntos, casi todos los de Sevilla.

**[01:11] Entrevistador:** Ok.

**[01:11] Chofer:** A veces suben en Petrol, eh, Campos, como parte de Campos.

**[01:20] Entrevistador:** Y esta, ¿qué ruta es? ¿Norte?

**[01:22] Chofer:** Norte.

**[01:22] Entrevistador:** Norte. Ok. ¿Y cuál es el problema más frecuente acerca de los estudiantes? ¿No llegan, o avisan tarde, o a veces no pagan?

**[01:34] Chofer:** Eso lo dejo a criterio de cada uno.

**[01:37] Entrevistador:** O sea, normalmente pagan por QR, efectivo?

**[01:39] Chofer:** Sí, por QR y efectivo.

**[01:41] Entrevistador:** Y a veces, o sea, ¿usted siempre revisa cuando salen directo o, o, o le pagan al ingresar acá? Por ejemplo, ahorita le deberían pagar al ingresar, asumo, ¿no?

**[01:50] Chofer:** Sí, ahorita al ingresar aquí.

**[01:51] Entrevistador:** Y si es que fuera en la mañana, ¿le pagarían al finalizar el viaje? O sea, cuando los recojan.

**[01:55] Chofer:** Sí, al finalizar.

**[01:57] Entrevistador:** Eh, ¿usted qué opina acerca de manejar créditos de la U? Y que usted directamente al final del viaje se lo retire desde su desde una aplicación, el saldo.

**[02:07] Chofer:** Ah, ¿esa aplicación que salió recién?

**[02:09] Entrevistador:** No, recién estamos diseñando una para eso.

**[02:14] Otra persona:** Buenas.

**[02:14] Entrevistador:** ¿Cuántos?

**[02:17] Chofer:** Ya. Sería bueno probar, porque hay una que salió para los transportistas.

**[02:22] Entrevistador:** ¿Qué opina usted acerca de una app que esté siempre en una página y le aparezca la ubicación de cada estudiante en tiempo real, cuando sea pasar a recoger a los estudiantes en la primera llegada?

**[02:37] Chofer:** Sería bien.

**[02:39] Entrevistador:** ¿Y usted podría tener un dispositivo móvil conectado a un cargador y siempre prendido para revisar eso, o lo va a usar en su pantallita de?

**[02:49] Chofer:** En la pantalla.

**[02:49] Entrevistador:** ¿Tiene Wi-Fi en su pantalla?

**[02:52] Chofer:** Sí, está con Wi-Fi de YouTube.

**[02:54] Entrevistador:** Ahí puede entrar a Chrome y a una página, ¿no?

**[02:57] Chofer:** Sí, se puede.

**[02:57] Entrevistador:** ¿Tiene ubicación o no?

**[03:00] Chofer:** Mmm, tiene GPS, tiene todo, tiene carteles, todo.

**[03:04] Entrevistador:** Perfecto. Eh, ¿cómo sabe hoy normalmente dónde va a subir a alguien o cuándo?

**[03:12] Chofer:** Porque ya están los destinos, digamos, ¿no? Porque todos los días los mismos destinos: Sevilla, Petrol, todo eso.

**[03:20] Entrevistador:** ¿Y qué pasaría si un nuevo estudiante, eh, de primer año, quiere usar el bus por primera vez, pero no está en su ruta normalmente y no hay mensaje y se pierde el mensaje entre varias rutas?

**[03:33] Chofer:** Tendría que explicarle cómo es la movida, ¿no?

**[03:35] Entrevistador:** Ok.

**[03:36] Chofer:** Y revisar los horarios, porque hay diferentes.

**[03:39] Entrevistador:** En cuestión de celulares y WhatsApp, eh, ah, no, ya dije un momento. Eh, ¿usted siempre comparte su ubicación en tiempo real o se le corta de vez en cuando?

**[03:48] Chofer:** Mmm, hay veces se corta en tiempo real, tengo que volver a ponerlo.

**[03:53] Entrevistador:** Ok. Si la app le mostrara, eh, ah, no, ya le apago eso. Si la app le sugiere, eh, cuándo parar o no parar o esperar por alguien, ¿la usaría?

**[04:07] Chofer:** Sí, espero hasta dos minutos, luego me llaman al otro lado y.

**[04:11] Entrevistador:** Y máximo como un minutito más, máximo.

**[04:13] Chofer:** Sí, máximo, sí. Aunque a veces se atrasa, digamos.

**[04:15] Entrevistador:** Sí, sí.

**[04:16] Chofer:** Pero le meto pata.

**[04:18] Entrevistador:** Ok.

**[04:18] Chofer:** Para llegar más o menos.

**[04:19] Entrevistador:** ¿Qué cambio de ruta hace por su cuenta?

**[04:25] Chofer:** Mmm, ¿como qué más o menos?

**[04:28] Entrevistador:** Como, por ejemplo, en la ruta sur hay un bus que normalmente tenía que ir solo por la Velarde, pero se mete una antes del cine center para recoger a dos o tres estudiantes y sigue su ruta normalmente después.

**[04:44] Chofer:** Casi nunca.

**[04:45] Entrevistador:** ¿Casi nunca?

**[04:46] Chofer:** La misma ruta nomás, siempre.

**[04:47] Entrevistador:** Pero usted podría modificar la ruta si es que algún estudiante se lo pidiera, si es que está aprobado por la administración?

**[04:55] Chofer:** Lo que pasa es que esa ruta donde yo estoy es grave la tranquilidad, porque yo cuando voy a tener que hacer maniobras con microlíneas, tenés que bajarte abajo, meterle por ahí y si no, no vas a llegar nunca.

**[05:07] Entrevistador:** Ok. Eh, ¿quién recibe el dinero, usted o su empresa? ¿Se entrega factura?

**[05:14] Chofer:** Yo. Bueno, la empresa da factura.

**[05:17] Entrevistador:** La empresa da factura y usted recibe, ¿no?

**[05:19] Chofer:** Sí.

**[05:20] Entrevistador:** Ok. ¿Trabaja para una empresa contratada por la UPB o solamente la UPB?

**[05:27] Chofer:** Contratado, soy contratado.

**[05:29] Entrevistador:** Directamente contratado. ¿Con quién coordina en la UPB?

**[05:32] Chofer:** Con Don Iván.

**[05:33] Entrevistador:** Don Iván.

**[05:34] Chofer:** Ya listo.

**[05:36] Entrevistador:** Eh, muchas gracias, eso es todo.

**[05:39] Chofer:** Ya, listo.

**[05:41] Entrevistador:** Muchas gracias, señor, muy amable. Que le vaya bien.


## Anexo B — Transcripción de ENT-02 (estudiante de la Ruta Norte, anónima)

Transcripción automática, sin corregir. Se cambiaron los «Hablante n» por el rol de cada persona.

**[00:00] Estudiante:** Ya.

**[00:01] Entrevistador 1:** ¿Qué ruta o qué horario usas normalmente, y cuántas veces por semana?

**[00:05] Estudiante:** Eh, lo ocupo 5 veces a la semana. La ruta de entrada a las 7 de la mañana norte, y a la salida a las 12 igual norte.

**[00:12] Entrevistador 1:** Eh, ¿te dejó el bus alguna vez? ¿Qué pasó y cómo llegaste al lado?

**[00:17] Estudiante:** Eh, no, nunca me ha dejado el bus.

**[00:20] Entrevistador 1:** ¿Nunca?

**[00:20] Estudiante:** Alguna vez, cuando hubo alguna falla o algo, me vine en taxi.

**[00:25] Entrevistador 1:** Ok. Eh, ¿qué es lo que más te molesta del grupo de WhatsApp del bus?

**[00:31] Estudiante:** Nada, lo tengo silenciado.

**[00:33] Entrevistador 2:** ¿Pero es cómodo para vos utilizar? ¿Es intuitivo?

**[00:36] Estudiante:** Sí. O sea, mejoraría las ubicaciones de los señores, digamos, ¿no? Pero la verdad que es bastante cómodo.

**[00:42] Entrevistador 1:** Ok. ¿Alguna vez no supiste dónde estaba el bus? ¿Y qué hiciste en ese caso?

**[00:47] Estudiante:** Eh, sí. No cargaba la ubicación y le escribí a un amigo que ya estaba en el bus, que me mandó su ubicación en tiempo real.

**[00:53] Entrevistador 1:** Ok. ¿Compartirías tu ubicación con el chofer mientras esperas, para que no haya ningún problema?

**[01:00] Estudiante:** Sí.

**[01:01] Entrevistador 1:** Ok. Si la app te dijera la hora aproximada en la que pasa el bus por tu parada, ¿confiarías en ella?

**[01:08] Estudiante:** Sí.

**[01:11] Entrevistador 1:** Eh, ¿propondrías una parada nueva y dónde sería?

**[01:17] Estudiante:** No.

**[01:17] Entrevistador 1:** ¿No? Ok. Eh, ¿cómo pagas hoy? ¿Preferirías recargar créditos en una app y poseer en efectivo y QR?

**[01:28] Estudiante:** No, preferiría que se pudiera pagar.

**[01:32] Entrevistador 2:** O sea, digamos.

**[01:33] Entrevistador 1:** O sea, es como que pagas a la app y automáticamente los créditos están ahí, solo tocás "ping".

**[01:37] Entrevistador 2:** Pagar.

**[01:37] Entrevistador 1:** Pagar desde la app.

**[01:39] Entrevistador 2:** Pagar una vez sola.

**[01:40] Estudiante:** Sí, voy. Pero es que no siempre ocupo el bus, digamos, entonces.

**[01:45] Entrevistador 1:** No, no recargas a ese rato, pero lo procuras.

**[01:47] Estudiante:** Ah, pero es lo mismo.

**[01:48] Entrevistador 1:** Es lo mismo, pero.

**[01:49] Estudiante:** Sí, pero, ajá.

**[01:50] Entrevistador 1:** Más.

**[01:50] Estudiante:** Más fácil. Sí, yo creo que sí.

**[01:53] Entrevistador 1:** Eh, ¿qué te parece que, si no estás en la parada una hora, el bus siga sin esperar?

**[02:01] Estudiante:** No, está bien que no espere, digamos, ¿no? Porque después no llegamos al lado.

**[02:05] Entrevistador 1:** ¿Usarías el chat directo con el chofer?

**[02:09] Estudiante:** Lo he ocupado varias veces, sí.

**[02:11] Entrevistador 1:** Si pudieras pedir una sola cosa en una app para los buses, ¿qué pedirías? ¿Qué sería?

**[02:21] Estudiante:** No, o sea, capaz que mejoren la ubicación, digamos, ¿no? Porque sí hay problema, hay es recurrente el problema de que no carga la ubicación en algunos conductores.

**[02:29] Entrevistador 1:** Eso es todo. Gracias.

**[02:31] Entrevistador 2:** Listo.
