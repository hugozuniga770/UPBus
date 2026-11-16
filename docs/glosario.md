# Glosario de siglas — UPBus (UPB Santa Cruz)

Busca la sigla, lee su significado y sigue.

## Ficha del documento

- Proyecto: UPBus — Buses UPB en tiempo real
- Creado: 13/11/2026 · Issue: por crear · Milestone: Sprint 1
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
| Padrón | La lista de personas de la universidad, de solo lectura |
| API | La forma en que el FE le pide datos al MW |
| DRF | Django REST Framework: la herramienta de Django para hacer la API |
| WebSocket | Conexión abierta entre el navegador y el servidor, para recibir la ubicación y los mensajes al instante |
| CI | Integración continua: GitHub corre las pruebas en cada cambio |

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
| Parada activa | Parada que en ese viaje tiene al menos un estudiante esperando y compartiendo su ubicación |
| Hora aproximada | Hora en que el bus suele pasar por una parada, calculada con los viajes anteriores |
| Crédito | Saldo dentro de la app; 1 crédito = 1 Bs |
| Comprobante | Registro de un pago, con su ID, la persona, el viaje, la fecha, la hora y el monto |
| Rechazo | Respuesta del sistema cuando no permite una operación; siempre dice la causa |
| Sprint | Ciclo de una semana que termina con algo que funciona |
| Incremento | Lo terminado en un sprint que cumple la Definition of Done |
| MVP | Producto mínimo viable: la primera versión que ya resuelve el problema principal |
