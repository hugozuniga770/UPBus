# Glosario de siglas — UPBus (UPB Santa Cruz)

Busca la sigla, lee su significado y sigue.

## Ficha del documento

- Proyecto: UPBus — Buses UPB en tiempo real
- Creado: 13/11/2026 · Actualizado: 25/11/2026 (abordaje, ajustes y pago, PO25). El 18/11/2026: modo registro, padrón local y términos del código · Issue: [#1](https://github.com/hugozuniga770/UPBus/issues/1) · Milestone: Sprint 1
- Elaboración: Hugo Zuñiga, con asistencia de Claude (Anthropic)

## 0. Cómo se arma un ID

`BUS-RF-09` se lee: proyecto **BUS**, tipo **RF** (requisito funcional), número **09**. Dentro de los documentos se abrevia como RF-09.

## 1. IDs de documentación

| Sigla | Significa | Ejemplo | Dónde vive |
|---|---|---|---|
| RF | Requisito funcional: algo que la app debe hacer | RF-09, «Voy a subir» | `sesion-06-requisitos.md` |
| RC | Requisito de calidad: cómo debe hacerlo | RC-03, un rechazo no deja la operación a medias | `sesion-06-requisitos.md` |
| RT | Restricción: algo ya decidido sobre la tecnología | RT-02, SQLite | `sesion-06-requisitos.md` |
| HU | Historia de usuario | HU-07 | `sesion-07-modelos.md` |
| CA | Criterio de aceptación; cada uno es un test | HU07-CA2 | `sesion-07-modelos.md` |
| CU | Caso de uso: los pasos de una historia. Mismo número que su historia | CU-07 | `sesion-07-modelos.md`, `diagramas-secuencia.md` |
| P-xx | Pregunta abierta para el Product Owner | P-06, horas de llegada | `sesion-06-requisitos.md`, sección 6 |
| C-xx | Cambio registrado a algo ya acordado | C-02, créditos en lugar de QR | `cambios.md` |
| T-xx | Tarea del plan | T11, viajes y bus en vivo | `sesion-08-09-plan.md` |
| ENT-xx | Entrevista | ENT-01, chofer de la Ruta Norte | `entrevistas.md` |

### 1.1 Fuentes citadas en los requisitos

| Sigla | Fuente |
|---|---|
| GUIA | Guía oficial «Buses I-26» de la UPB |
| PERFIL | Perfil de proyecto presentado el 07/11/2026 |
| PO13 | Decisiones del Product Owner del 13/11/2026 |
| PO18 | Decisiones del Product Owner del 18/11/2026: modo registro, padrón de la clase y roles de la implementación |
| PO25 | Decisiones del Product Owner del 25/11/2026, al revisar las historias: pago iniciado por el estudiante, abordaje automático, ajustes de créditos y todo cambio de ruta con aprobación |
| DOC | Indicaciones del docente comunicadas por Hugo |
| ENT | Entrevistas |

### 1.2 Costos (`sesion-15-costos.md`)

| Sigla | Significa |
|---|---|
| h-p | Horas-persona: una persona trabajando una hora |
| Bs/h | Bolivianos por hora: la tarifa |
| IVA | Impuesto al Valor Agregado, 13%, incluido en el precio de la factura |
| IT | Impuesto a las Transacciones, 3% del ingreso bruto |
| SMN | Salario Mínimo Nacional: 3.300 Bs en 2026 |

## 2. Arquitectura y técnicas

| Sigla | Significa |
|---|---|
| FE | Frontend: las pantallas, hechas con React y Tailwind |
| MW | La capa del medio: el servidor Django, que recibe, aplica las reglas y responde |
| BD | La base de datos del proyecto (SQLite) |
| Padrón | La lista de personas de la universidad, de solo lectura. En el repositorio va el de ejemplo (`padron.json`); la lista de la clase va en `padron.local.json`, que no se sube |
| API | La forma en que el FE le pide datos al MW |
| DRF | Django REST Framework: la herramienta de Django para hacer la API |
| WebSocket | Conexión abierta entre el navegador y el servidor, para recibir la ubicación y los mensajes al instante |
| CI | Integración continua: GitHub corre las pruebas en cada cambio |
| CSRF | Ataque en el que otra página intenta usar tu sesión; Django lo bloquea con un token que el FE manda en cada escritura |
| HTTPS | Conexión cifrada; el navegador solo entrega el GPS a páginas con HTTPS o abiertas en la misma computadora |
| Túnel | Programa gratuito (cloudflared) que da una dirección HTTPS temporal a la app que corre en una computadora, para abrirla en el celular |
| PR | Pull Request: el pedido para unir una rama a `develop`; lo aprueba Hugo |
| Wake Lock | Permiso del navegador para que la pantalla no se apague mientras se graba un recorrido |

## 3. Las marcas entre corchetes

| Marca | Significa |
|---|---|
| [ACUERDO] | Lo aprobó el Product Owner, o sale de la guía oficial de buses |
| [PROPUESTA] | Lo propuso el equipo y el Product Owner todavía no lo aprobó |
| [PROVISIONAL] | Valor que rige mientras no se responda una pregunta P-xx |
| [SIMULADO] | En el MVP funciona con datos simulados |

## 4. Términos que no son siglas

| Término | Significa |
|---|---|
| Viaje | Una salida concreta: ruta, horario, fecha y chofer |
| «Voy a subir» | Aviso del estudiante para un viaje y una parada |
| Abordaje | Que el estudiante subió al bus. Lo marca él («He subido»), el chofer («subió») o la app, si su ubicación va con el bus. No cobra (C-30, C-31) |
| No se presentó | Estado del aviso cuando el bus llega a la parada siguiente sin que el estudiante haya subido ni cancelado |
| Ajuste | Movimiento con el que el administrador da o quita créditos a una cuenta, con un motivo (C-29) |
| Parada activa | Parada que en ese viaje tiene al menos un estudiante esperando y compartiendo su ubicación |
| Hora aproximada | Hora en que el bus suele pasar por una parada, calculada con los viajes anteriores |
| Crédito | Saldo dentro de la app; 1 crédito = 1 Bs |
| Comprobante | Registro de un pago, con su ID, la persona, el viaje, la fecha, la hora y el monto. Al final de la ruta, el chofer revisa los de su viaje |
| Rechazo | Respuesta del sistema cuando no permite una operación; siempre dice la causa |
| Sprint | Ciclo de una semana que termina con algo que funciona |
| Incremento | Lo terminado en un sprint que cumple la Definition of Done |
| MVP | Producto mínimo viable: la primera versión que ya resuelve el problema principal |
| Modo registro | Modo del chofer y del administrador para grabar paradas, horas y recorrido en un viaje real (RF-23, HU-18) |
| Registro | Una grabación del modo registro: una ruta, un horario y sus marcas |
| Marca | Lo que se guarda al tocar «Parada» en el modo registro: posición, precisión del GPS y hora |
| Paso | Una vez que el bus pasó por una parada, con los minutos desde la salida programada; con los pasos se calcula la hora aproximada |
| Salida programada | La hora de salida del horario, por ejemplo las 06:40; los minutos de cada paso se cuentan desde ella (C-23) |
| REG-xx | Un viaje real grabado con el modo registro, descrito en `viajes-grabados.md` |
| Respaldo | Archivo JSON que el celular descarga con un registro, para importarlo si algo falló (`importar_registro`) |
| Cola | Lista de marcas y puntos que esperan en el celular hasta que haya señal |
| Base del código | El punto de partida que dejó Hugo el 18/11/2026: entornos, cuentas, usuarios, rutas, modo registro y pruebas |
| `develop` | Rama donde se unen las historias terminadas; solo Hugo la une con `main` al cerrar cada sprint |
