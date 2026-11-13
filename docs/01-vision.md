# Visión del producto — UPBus

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Equipo: Grupo 7 · Product Owner: Hugo Zuñiga · Scrum Master: Andrew
- Docente: Ing. Alejandro Rodríguez (Certificación I)
- Fecha: 13/11/2026
- Siglas y marcas ([ACUERDO], [PROPUESTA], [PENDIENTE]): [glosario.md](glosario.md)

## 1. El problema

La UPB Santa Cruz ofrece buses que salen cada día desde distintos puntos de la ciudad hacia el campus y de regreso. Según la guía oficial del servicio (Buses I-26):

| Sentido | Ruta | Punto de partida | Horarios |
|---|---|---|---|
| Ingreso | Norte | La Fontana Family Club (norte, anillo) | 06:40, 11:00, 13:00, 15:30 |
| Ingreso | Sur | Makro Parque (Av. Makro Parques) | 06:40, 11:00 |
| Ingreso | Externa | Gladymar (Av. Canal Cotoca, 2do anillo) | 06:40 |
| Ingreso | 4to Anillo | Farmacorp (4to anillo, Alemana) | 06:40 |
| Salida | Norte, Sur y Externa | Campus UPB | 12:15, 19:00, 21:15 |
| Salida | 4to Anillo | Campus UPB | 12:15 |
| Salida | Híbrida | Campus UPB | 14:30 |

Cómo funciona hoy:

1. El estudiante se une al grupo de WhatsApp de su ruta.
2. Al iniciar la ruta, el chofer comparte su ubicación en tiempo real. El primer día, el estudiante envía su nombre y la parada en la que sube.
3. El estudiante paga 5 Bs en efectivo al chofer en cada viaje.

Normas del servicio: la ruta sigue funcionando solo con al menos 15 estudiantes, no hay tiempo de espera y el bus no se desvía por pedido de un estudiante.

**Problema central:** la coordinación del servicio es informal y no tiene seguimiento en tiempo real. El chofer no sabe quién está por llegar, los mensajes se pierden en grupos saturados y la ubicación del bus depende de que el chofer la comparta. El árbol de problemas completo está en el informe del perfil de proyecto.

## 2. Objetivo del producto (Product Goal)

Que ningún estudiante de la UPB Santa Cruz pierda el bus por falta de información, conectando en tiempo real a estudiantes y choferes. [ACUERDO]

## 3. Usuarios

| Rol | Quién es | Qué necesita |
|---|---|---|
| Estudiante | Estudiante activo de la UPB Santa Cruz que usa los buses | Saber dónde está el bus, avisar que va a subir, hablar con el chofer y pagar |
| Chofer | Conductor de la empresa que presta el servicio | Compartir su ubicación sin esfuerzo, saber quién lo espera y recibir avisos sin escribir mientras maneja |
| Administrador | Persona de la UPB a cargo del servicio | Mantener rutas, paradas, horarios y choferes al día, y saber cuántos estudiantes usan cada viaje |

Los tres usan la misma aplicación; lo que cada uno ve depende de su rol (control de acceso por roles). [ACUERDO]

## 4. Alcance

**Entra en el producto** [ACUERDO]: registro validado contra un padrón simulado de la UPB, mapa con el bus en vivo, ubicación compartida del estudiante, «Voy a subir», avisos de bus cerca, chat directo con el chofer, chat grupal por ruta que reemplaza a WhatsApp, pago con QR o en efectivo y panel de administración.

**Orden de entrega** [PROPUESTA]: las prioridades MoSCoW de cada historia están en [03-backlog.md](03-backlog.md). El pago con QR va al final y, en su primera versión, solo muestra el QR del bus y el chofer confirma el pago a mano.

**No entra por ahora** [ACUERDO]:

- Aplicación móvil nativa: primero será web; si funciona bien, se evaluará una app.
- Conexión con el sistema real de la UPB: se usa un padrón simulado, preparado para conectarse después ([02-requisitos.md](02-requisitos.md), sección 5).

**No entra por ahora** [PROPUESTA]: conexión directa con bancos para el pago con QR.
