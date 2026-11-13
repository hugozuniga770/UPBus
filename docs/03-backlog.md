# Product Backlog — UPBus

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Dueño del backlog: Hugo Zuñiga (Product Owner)
- Fecha: 13/11/2026
- Requisitos: [02-requisitos.md](02-requisitos.md) · Preguntas: [05-preguntas-abiertas.md](05-preguntas-abiertas.md) · Cambios: [cambios.md](cambios.md)

## 1. Resumen y prioridades

La prioridad usa MoSCoW: **Must** va en el primer incremento, **Should** en los siguientes sprints y **Could** se hace si alcanza el tiempo. Las prioridades son [PROPUESTA] del Product Owner hasta que el equipo las confirme.

| Historia | Título | Rol | Prioridad | Requisitos |
|---|---|---|---|---|
| HU-01 | Registrarme con el padrón UPB | Estudiante | Must | RF-01, RN-01 |
| HU-02 | Entrar según mi rol | Todos | Must | RF-02, RNF-03 |
| HU-03 | Ver rutas y horarios | Estudiante | Must | RF-03 |
| HU-04 | Ver mi bus en vivo | Estudiante | Must | RF-05, RNF-01 |
| HU-05 | Iniciar la ruta y compartir ubicación | Chofer | Must | RF-04, RN-06 |
| HU-06 | Compartir mi ubicación | Estudiante | Must | RF-06, RNF-04 |
| HU-07 | Avisar «Voy a subir» | Estudiante | Must | RF-07, RF-13, RN-04, RNF-05 |
| HU-08 | Recibir aviso de bus cerca | Estudiante | Should | RF-08 |
| HU-09 | Chatear directo con el chofer | Estudiante y chofer | Should | RF-09, RN-05 |
| HU-10 | Chat grupal de la ruta | Estudiante y chofer | Should | RF-10 |
| HU-11 | Pagar con QR o efectivo | Estudiante y chofer | Could | RF-11, RN-02 |
| HU-12 | Gestionar rutas, paradas, horarios y choferes | Administrador | Must | RF-12, RF-13, RN-07 |

Cada criterio de aceptación tiene un identificador (por ejemplo, HU04-CA2) para poder enlazarlo después con su prueba.

## 2. Historias

### HU-01 · Registrarme con el padrón UPB

Como estudiante, quiero registrarme con mi código o correo institucional y una contraseña, para usar UPBus solo si estoy en el padrón de la UPB.

- **HU01-CA1:** Si el código o correo está en el padrón y la persona está activa, se crea la cuenta con la contraseña elegida.
- **HU01-CA2:** Si no está en el padrón o está inactiva, se muestra «No estás en el padrón de la UPB» y no se crea la cuenta.
- **HU01-CA3:** No se puede registrar dos veces el mismo código.

### HU-02 · Entrar según mi rol

Como usuario, quiero iniciar sesión y ver solo las funciones de mi rol (estudiante, chofer o administrador), para usar la aplicación según mis permisos.

- **HU02-CA1:** Se entra con código o correo, a elección del usuario, y contraseña.
- **HU02-CA2:** Cada usuario ve solo el menú de su rol; si intenta abrir una pantalla de otro rol, se le niega el acceso.
- **HU02-CA3:** Si los datos son incorrectos, se muestra un error que no dice cuál de los datos falló.

### HU-03 · Ver rutas y horarios

Como estudiante, quiero consultar las rutas, paradas y horarios de ingreso y salida, para planificar mi viaje.

- **HU03-CA1:** Se muestran todas las rutas activas con sus paradas y horarios de ingreso y salida.
- **HU03-CA2:** Un cambio del administrador en una ruta u horario se ve la próxima vez que se abre la pantalla.

### HU-04 · Ver mi bus en vivo

Como estudiante, quiero ver en un mapa dónde está mi bus en tiempo real, para llegar a tiempo a la parada.

- **HU04-CA1:** El bus de la ruta elegida aparece en el mapa y su posición se actualiza al menos cada 10 segundos (RNF-01).
- **HU04-CA2:** Se muestra el tiempo estimado de llegada a la parada del estudiante.
- **HU04-CA3:** Si la ruta no inició, se muestra «El bus aún no salió».

### HU-05 · Iniciar la ruta y compartir ubicación

Como chofer, quiero iniciar la ruta con un botón y que mi ubicación se comparta sola, para no depender de compartirla a mano.

- **HU05-CA1:** El botón «Iniciar ruta» empieza a compartir la ubicación sin pasos adicionales.
- **HU05-CA2:** El botón «Terminar ruta» deja de compartirla.
- **HU05-CA3:** Si se pierde la señal, el mapa de los estudiantes muestra la última ubicación conocida con su hora.

### HU-06 · Compartir mi ubicación

Como estudiante, quiero compartir mi ubicación mientras espero el bus, para que el chofer sepa que estoy llegando.

- **HU06-CA1:** La ubicación solo se comparte si el estudiante la activa.
- **HU06-CA2:** La ve únicamente el chofer de esa ruta (RNF-04).
- **HU06-CA3:** Se deja de compartir sola en los casos que se definan en P-16. [PENDIENTE]

### HU-07 · Avisar «Voy a subir»

Como estudiante, quiero avisar con un botón «Voy a subir», para que al chofer le llegue una alerta.

- **HU07-CA1:** Con un toque, al chofer le llega una alerta con el nombre del estudiante y su parada.
- **HU07-CA2:** El chofer ve cuántos estudiantes van a subir en cada parada.
- **HU07-CA3:** El estudiante puede cancelar el aviso. Hasta cuándo se define en P-14. [PENDIENTE]

### HU-08 · Recibir aviso de bus cerca

Como estudiante, quiero recibir un aviso cuando el bus esté cerca de mi parada, para no tener que revisar el chat a cada rato.

- **HU08-CA1:** Llega un aviso cuando el bus está cerca de la parada del estudiante. Cuándo es «cerca» se define en P-17. [PENDIENTE]
- **HU08-CA2:** Solo llegan avisos de la ruta y parada que el estudiante eligió.

### HU-09 · Chatear directo con el chofer

Como estudiante, quiero escribirle directamente al chofer de mi ruta, para avisarle algo sin perderme en un grupo.

- **HU09-CA1:** El estudiante puede enviar texto o un mensaje rápido («Ya estoy en la parada», «Llego en 1 min»).
- **HU09-CA2:** El chofer responde con botones rápidos (RN-05).
- **HU09-CA3:** El chat solo funciona con el chofer de la ruta activa.

### HU-10 · Chat grupal de la ruta

Como estudiante, quiero un chat grupal de mi ruta dentro de la aplicación, para reemplazar el grupo de WhatsApp.

- **HU10-CA1:** Cada ruta tiene un chat con sus estudiantes y su chofer. Quiénes pertenecen se define en P-13. [PENDIENTE]
- **HU10-CA2:** Cada mensaje muestra el nombre de quien lo envió y la hora.

### HU-11 · Pagar con QR o efectivo

Como estudiante, quiero elegir pagar con QR o en efectivo, para pagar de la forma que me resulte más cómoda.

- **HU11-CA1:** Al subir, el estudiante elige QR o efectivo.
- **HU11-CA2:** Con QR, la app muestra el QR de cobro y el chofer confirma que recibió el pago. [PROPUESTA] · [PENDIENTE P-20]
- **HU11-CA3:** Queda registro del viaje y del método de pago.

### HU-12 · Gestionar rutas, paradas, horarios y choferes

Como administrador, quiero gestionar rutas, paradas, horarios y choferes, para mantener el servicio actualizado.

- **HU12-CA1:** El administrador puede crear, editar y desactivar rutas, paradas y horarios.
- **HU12-CA2:** Puede crear cuentas de chofer y asignar cada chofer a una ruta (RN-06, RN-07).
- **HU12-CA3:** Ve cuántos estudiantes confirmaron cada viaje (RF-13).
