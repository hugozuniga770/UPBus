# Requisitos — UPBus

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Equipo: Grupo 7 · Product Owner: Hugo Zuñiga · Scrum Master: Andrew
- Fecha: 13/11/2026
- Visión: [01-vision.md](01-vision.md) · Backlog: [03-backlog.md](03-backlog.md) · Preguntas: [05-preguntas-abiertas.md](05-preguntas-abiertas.md) · Cambios: [cambios.md](cambios.md)

## 0. Cómo leer este documento

Cada requisito lleva una marca. Las siglas están en [glosario.md](glosario.md).

| Marca | Significa |
|---|---|
| **[ACUERDO]** | Lo decidió el equipo o sale de la guía oficial de buses de la UPB. |
| **[PROPUESTA]** | Lo propuso el Product Owner y el equipo todavía no lo confirmó. |
| **[PENDIENTE]** | Depende de una pregunta abierta (P-xx). Si la respuesta cambia algo, se registra en [cambios.md](cambios.md). |

## 1. Requisitos funcionales

| ID | Requisito | Rol | Historia | Marca |
|---|---|---|---|---|
| RF-01 | Registrarse con código o correo institucional y una contraseña, solo si la persona está activa en el padrón simulado | Estudiante | HU-01 | [ACUERDO] |
| RF-02 | Iniciar sesión con código o correo (el usuario elige cuál) y contraseña, y ver solo las funciones de su rol | Todos | HU-02 | [ACUERDO] |
| RF-03 | Consultar rutas, paradas y horarios de ingreso y salida | Estudiante | HU-03 | [ACUERDO] |
| RF-04 | Iniciar y terminar la ruta; mientras está activa, la ubicación del chofer se comparte sola | Chofer | HU-05 | [ACUERDO] |
| RF-05 | Ver el bus en vivo en el mapa, con el tiempo estimado de llegada a su parada | Estudiante | HU-04 | [ACUERDO] |
| RF-06 | Compartir su ubicación mientras espera el bus | Estudiante | HU-06 | [ACUERDO] |
| RF-07 | Avisar «Voy a subir»; al chofer le llega una alerta con el nombre y la parada | Estudiante | HU-07 | [ACUERDO] |
| RF-08 | Recibir un aviso cuando el bus está cerca de su parada | Estudiante | HU-08 | [ACUERDO] · detalle [PENDIENTE P-08, P-17] |
| RF-09 | Chat directo entre estudiante y chofer, con mensajes rápidos | Estudiante y chofer | HU-09 | [ACUERDO] |
| RF-10 | Chat grupal de cada ruta, que reemplaza al grupo de WhatsApp | Estudiante y chofer | HU-10 | [ACUERDO] |
| RF-11 | Elegir pago con QR o en efectivo y dejar registro del pago | Estudiante y chofer | HU-11 | [ACUERDO] · forma del QR [PENDIENTE P-20] |
| RF-12 | Gestionar rutas, paradas, horarios y cuentas de chofer | Administrador | HU-12 | [ACUERDO] |
| RF-13 | Ver cuántos estudiantes confirmaron cada viaje | Chofer y administrador | HU-07, HU-12 | [PROPUESTA] |

## 2. Requisitos no funcionales

| ID | Requisito | Marca |
|---|---|---|
| RNF-01 | La ubicación del bus se actualiza al menos cada 10 segundos. | [PROPUESTA] · cómo se logra [PENDIENTE P-02] |
| RNF-02 | La aplicación es web y se usa bien desde el navegador del celular (Android y iPhone) y desde tablets. | [ACUERDO] |
| RNF-03 | Las contraseñas se guardan cifradas y cada rol solo accede a sus funciones. | [ACUERDO] |
| RNF-04 | La ubicación del estudiante solo la ve el chofer de su ruta, solo mientras espera. | [PROPUESTA] · cuándo se apaga [PENDIENTE P-16] |
| RNF-05 | «Voy a subir» se activa en máximo dos toques desde que se abre la app. | [PROPUESTA] |
| RNF-06 | La aplicación funciona durante el horario del servicio (06:30 a 22:00). | [PROPUESTA] · dónde corre [PENDIENTE P-06] |
| RNF-07 | La interfaz usa los colores y el logo de la UPB y está en español. | [ACUERDO] |
| RNF-08 | El padrón se consulta desde un solo módulo, para conectarlo después al sistema real de la UPB sin rehacer la app. | [ACUERDO] |

## 3. Reglas del negocio

| ID | Regla | Marca y fuente |
|---|---|---|
| RN-01 | Solo pueden registrarse estudiantes activos del padrón de la UPB. | [ACUERDO] equipo |
| RN-02 | Cada viaje cuesta 5 Bs. El administrador puede cambiar el monto. | [ACUERDO] guía de buses · monto editable [PROPUESTA] |
| RN-03 | Una ruta sigue funcionando solo con al menos 15 estudiantes. | [ACUERDO] guía de buses · qué hace la app [PENDIENTE P-15] |
| RN-04 | El bus no espera ni se desvía. «Voy a subir» informa al chofer, pero no lo obliga a esperar. | [ACUERDO] guía de buses |
| RN-05 | El chofer no escribe mientras maneja: responde con botones rápidos cuando está detenido. | [PROPUESTA] |
| RN-06 | Cada chofer tiene una sola ruta activa a la vez. | [PROPUESTA] |
| RN-07 | Las cuentas de chofer no salen del padrón: las crea el administrador con un usuario exclusivo de chofer. | [ACUERDO] equipo |

## 4. Roles y permisos

| Función | Estudiante | Chofer | Administrador |
|---|---|---|---|
| Ver rutas, horarios y bus en vivo | Sí | Sí | Sí |
| Compartir ubicación como estudiante y «Voy a subir» | Sí | No | No |
| Iniciar y terminar ruta | No | Sí | No |
| Chat directo | Sí | Sí | No |
| Chat de la ruta | Sí | Sí | [PENDIENTE P-18] |
| Pagar / confirmar pago | Paga | Confirma | Ve el registro [PENDIENTE P-20] |
| Gestionar rutas, paradas, horarios y choferes | No | No | Sí |

## 5. Padrón simulado

El padrón imita la base de estudiantes de la UPB. UPBus solo lo consulta para validar el registro (RF-01, RN-01) y lo hace desde un único módulo (RNF-08).

Campos [PROPUESTA] · confirmar en [PENDIENTE P-09]:

| Campo | Ejemplo | Para qué |
|---|---|---|
| `codigo` | `70001` | Iniciar sesión y validar el registro |
| `nombre` | Valeria Rojas | Mostrarlo al chofer y en los chats |
| `correo` | valeria.rojas@upb.example | Iniciar sesión y validar el registro |
| `carrera` | Ingeniería de Sistemas | Información del perfil |
| `activo` | `true` | Solo los activos pueden registrarse |

Personas de ejemplo, todas ficticias [PROPUESTA] · confirmar en [PENDIENTE P-10]:

| Código | Nombre | Correo | Activo | Uso en pruebas |
|---|---|---|---|---|
| 70001 | Valeria Rojas | valeria.rojas@upb.example | Sí | Registro exitoso |
| 70002 | Mateo Suárez | mateo.suarez@upb.example | Sí | Segundo estudiante en la misma ruta |
| 70003 | Lucía Peña | lucia.pena@upb.example | No | Registro rechazado por inactiva |

El formato real del código y el dominio del correo institucional se definen en P-09. Mientras tanto se usan códigos de 5 dígitos y el dominio de ejemplo `upb.example`.
