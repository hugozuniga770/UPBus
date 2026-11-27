# Sesión 15 — Costos del proyecto

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Integrantes: Hugo Zuñiga (Product Owner), Andrés Laura Vargas (Scrum Master) y Sebastian Cruz
- Docente: Ing. Alejandro Rodríguez (Certificación I)
- Fecha: 16/11/2026 · Sprint 1 · Issue: [#1](https://github.com/hugozuniga770/UPBus/issues/1) · Milestone: Sprint 1 · Aprobado por el Product Owner el 26/11/2026 (T01)
- Actualizado: 27/11/2026 · avance del plan: 110 de 152 h-p (72 %), sección 10. El 25/11/2026: horas por persona según el reparto del 18/11 (C-26). El 18/11/2026: T25 y T26 suman 10 h-p (152 en total); la base del código cambia responsables y las tareas por asignar las reparte Andrés (C-18, C-19)
- Hoja de cálculo con las cuentas al día: «UPBus · Costos y horas» (Claude Sheets, privada del equipo)
- Plan: [Sesiones 8–9](sesion-08-09-plan.md) · Cambios: [cambios.md](cambios.md) · Siglas: [glosario.md](glosario.md)

El número 15 es el de la última sesión de esta documentación. Si el docente pide los costos en otra sesión, se renombra el archivo y se registra en [cambios.md](cambios.md).

## 0. Cómo leer este documento

- **Qué se calcula:** cuánto costaría hacer UPBus si el trabajo del equipo se pagara a precio de mercado en Bolivia. Nadie cobra: es una estimación para la defensa y para medir el proyecto.
- **Moneda:** bolivianos (Bs). **Unidad de trabajo:** horas-persona (h-p): una persona trabajando una hora.
- **Estimado y real:** lo estimado sale del plan; lo real, de las horas que cada integrante registra. Al cerrar cada sprint se comparan (sección 10).
- Los valores marcados **[PROVISIONAL]** son supuestos del equipo; se corrigen en la hoja «Supuestos» y todo se recalcula.

## 1. Fuentes

| ID | Fuente | Qué aporta |
|---|---|---|
| SAL-WEB | [TalentUp, desarrollador web en Bolivia](https://talentup.io/en/salary/Web%20Developer/Bolivia) | Sueldo base de 116.100 Bs al año |
| SAL-ING | [Nucamp, salarios tecnológicos en Bolivia 2026](https://www.nucamp.co/blog/coding-bootcamp-bolivia-bol-highest-paying-tech-companies-in-bolivia), que cita a Levels.fyi | Ingeniero de software promedio: unos 12.118 Bs al mes |
| SMN | [Decreto Supremo 5516](https://ovt.mintrabajo.gob.bo/soporte/recursos/PLANILLA%20COMPLEMENTARIA.pdf) | Salario Mínimo Nacional 2026: 3.300 Bs al mes |
| L843 | [Ley 843: IVA e IT](https://boliviaimpuestos.com/iva-it-e-iue-todo/) | IVA del 13%, incluido en el precio de la factura; IT del 3% sobre el ingreso bruto |
| PLAN | [Sesiones 8–9](sesion-08-09-plan.md), sección 4 | Las 152 h-p estimadas por tarea |
| GUIA | Guía oficial «Buses I-26» de la UPB | Tarifa de 5 Bs por viaje, para los viajes de prueba |

## 2. Horas estimadas

| Etapa | Tareas | h-p |
|---|---|---:|
| Perfil (ya hecho) | T00 | 6 |
| Sprint 1 | T01 a T10, T12 y T25 (la base adelantó T09, T10 y T12) | 58 |
| Sprint 2 | T11, T13, T26 y 3 h-p de T23 | 19 |
| Sprint 3 | T14 a T16, 5 h-p de T17 y 3 h-p de T23 | 30 |
| Sprint 4 | T18 a T20, 5 h-p de T17 y 4 h-p de T23 | 26 |
| Cierre | T21, T22 y T24 | 13 |
| **Total** | | **152** |

Hasta el 16/11 el total era 142 h-p. El 18/11 se sumaron T25, el modo registro (8 h-p), y T26, grabar la Ruta Norte (2 h-p) (C-18).

El detalle de cada tarea, su responsable y sus dependencias está en el [plan](sesion-08-09-plan.md), secciones 4 a 6, con el diagrama de Gantt.

## 3. Tarifa por hora

Una tarifa por hora es el sueldo mensual dividido entre las horas de trabajo de un mes: 8 horas × 22 días hábiles = **176 horas**.

| Escenario | Sueldo mensual (Bs) | Tarifa (Bs/h) | Fuente |
|---|---:|---:|---|
| Piso legal (salario mínimo) | 3.300 | 18,75 | SMN |
| **Desarrollador web (el que se usa)** | 9.675 | **54,97** | SAL-WEB: 116.100 ÷ 12 |
| Ingeniero de software promedio | 12.118 | 68,85 | SAL-ING |

Se usa el escenario del desarrollador web **[PROPUESTA]**: es el trabajo que hace el equipo y la fuente da un sueldo base concreto. Es un sueldo de mercado de una persona con experiencia; un estudiante cobraría menos, y por eso se muestra también el piso legal.

## 4. Otros costos

| Concepto | Cálculo | Bs |
|---|---|---:|
| Laptops (depreciación) | 3 laptops de 6.000 Bs **[PROVISIONAL]** que duran 36 meses; solo los 1,07 meses del proyecto | 533,33 |
| Internet | 150 Bs al mes por persona **[PROVISIONAL]** × 3 × 1,07 meses | 480,00 |
| Electricidad | 50 Bs al mes por persona **[PROVISIONAL]** × 3 × 1,07 meses | 160,00 |
| Viajes de prueba en el bus | 10 viajes **[PROVISIONAL]** × 5 Bs (GUIA) | 50,00 |
| Impresión de informes | 2 entregas × 30 Bs **[PROVISIONAL]** | 60,00 |
| Hosting, GitHub y GitHub Actions, mapa (Leaflet con OpenStreetMap) | Servicios gratuitos (BUS-RT-08) | 0,00 |
| Herramientas de IA | Se completa si alguien paga una suscripción para el proyecto | 0,00 |
| **Total** | | **1.283,33** |

La duración es del 13/11 al 15/12/2026: 32 días, que son 1,07 meses.

## 5. Precio del proyecto

| Concepto | Cómo se calcula | Bs |
|---|---|---:|
| Mano de obra | 152 h-p × 54,97 Bs/h | 8.355,68 |
| Otros costos | Sección 4 | 1.283,33 |
| Subtotal | | 9.639,02 |
| Contingencia | 15% del subtotal, para imprevistos **[PROVISIONAL]** | 1.445,85 |
| **Costo total del proyecto** | Lo que cuesta hacerlo | **11.084,87** |
| Utilidad | 20% del costo total, solo si se vendiera **[PROVISIONAL]** | 2.216,97 |
| Precio sin impuestos | Costo total + utilidad | 13.301,84 |
| IVA (13%) | Incluido en el precio de la factura (L843) | 2.058,62 |
| IT (3%) | Sobre el ingreso bruto (L843) | 475,07 |
| **Precio con factura** | Precio sin impuestos ÷ (1 − 0,13 − 0,03) | **15.835,52** |

**Por qué se divide y no se multiplica.** En Bolivia el IVA va incluido en el monto de la factura y el IT se calcula sobre el ingreso bruto. Para que después de pagar los dos queden 13.301,84 Bs, la factura tiene que ser de 13.301,84 ÷ 0,84.

Con 142 h-p (16/11), el costo total era 10.452,69 Bs y el precio con factura, 14.932,42 Bs.

## 6. Escenarios de tarifa

| Escenario | Tarifa (Bs/h) | Costo total (Bs) | Precio con factura (Bs) |
|---|---:|---:|---:|
| Piso legal (salario mínimo) | 18,75 | 4.753,33 | 6.790,48 |
| **Desarrollador web** | **54,97** | **11.084,87** | **15.835,52** |
| Ingeniero de software promedio | 68,85 | 13.511,21 | 19.301,73 |

## 7. Horas y costo por persona

Los responsables son los del reparto del 18/11, dirigido por Andrés (C-26). Las tareas compartidas se reparten por igual: las de «Andrés y Hugo» entre dos y las de «Los tres» entre tres.

| Persona | Tareas | Horas estimadas | Costo estimado (Bs) |
|---|---|---:|---:|
| Hugo Zuñiga | Base del código (T05 a T10, T12 y T25), T01, T02, T04, T14, T18, T21, T23 y T24 | 88,5 | 4.864,99 |
| Sebastian Cruz | T11, T17, T19, T22 y T26 | 37,0 | 2.033,95 |
| Andrés Laura Vargas | T03, T13, T15, T16 y T20 | 26,5 | 1.456,75 |
| **Total** | | **152,0** | **8.355,68** |

Hugo lleva más horas porque hizo la base del código (42 h-p estimadas) antes del reparto. Si una tarea cambia de responsable, se cambia en la hoja «Tareas» y esta tabla se recalcula sola.

## 8. Costo de operar el servicio (fuera del proyecto)

Si la UPB adoptara UPBus, el costo mensual en el piloto sería de 0 Bs en infraestructura, porque todo es gratuito (BUS-RT-08). En el servicio real habría que sumar:

- un hosting de pago cuando el uso pase el límite gratuito;
- la comisión de la pasarela de pagos por cada recarga de créditos, hoy **[SIMULADO]**;
- el mantenimiento de la aplicación.

Estos costos no entran en el precio de la sección 5.

## 9. Lo que no está incluido

| Qué | h-p | Bs a 54,97 Bs/h |
|---|---:|---:|
| Eventos de Scrum: por sprint y por persona, 1 h de Planning, 15 min de Daily × 5 días, 1 h de Review y 30 min de Retrospectiva = 3,75 h; × 3 personas × 4 sprints | 45 | 2.473,72 |
| Tiempo de aprender Django Channels, React y Tailwind | No se estimó | — |

Si se cobran los eventos de Scrum, el costo total sube a **13.929,65 Bs** y el precio con factura a **19.899,50 Bs**. No se incluyen en el precio base porque el plan estima solo el trabajo de cada tarea **[PROPUESTA]**. Las 45 h-p se calcularon con un Daily por día hábil; con las sesiones de sábado y domingo (C-19) se revisan en la Retrospectiva del Sprint 2.

## 10. Estimado contra real

Las horas reales salen de la hoja «Registro de horas»: cada integrante anota la fecha, la tarea (T01, T08…), las horas y qué hizo. Al cerrar cada sprint se copia aquí la fila.

| Etapa | h-p estimadas | h-p reales | Diferencia | Costo real (Bs) | Comentario |
|---|---:|---:|---:|---:|---|
| Perfil | 6 | — | — | — | Hecho; horas no registradas |
| Sprint 1 | 58 | — | — | — | Hecho; la base del código (42 h-p estimadas) se hizo el 18/11 |
| Sprint 2 | 19 | — | — | — | Cerrado el 26/11; además se adelantaron T14, T15, T16 y T19, de los sprints 3 y 4 |
| Sprint 3 | 30 | — | — | — | |
| Sprint 4 | 26 | — | — | — | |
| Cierre | 13 | — | — | — | |
| **Total** | **152** | — | — | — | |

Al 27/11/2026 están hechas T00 a T16, T19, T25 y T26: **110 de 152 h-p estimadas (72 %)**. Las horas reales todavía no se registraron. Al 18/11/2026 no había horas reales registradas. T00, T04 y la base del código (T05 a T10, T12 y T25) están hechas, pero falta anotar cuánto tomaron. La base se hizo con asistencia de IA: sus horas reales mostrarán cuánto bajó el esfuerzo frente a lo estimado.

## 11. Participación y asistencia utilizada

- **Hugo Zuñiga (Product Owner):** pidió el cálculo, aprueba la tarifa y los supuestos, y lleva el registro de horas.
- **Asistencia de IA:** se usó Claude (Anthropic) para buscar los sueldos de referencia y las tasas de impuestos, armar la hoja de cálculo y redactar este documento; el 18/11/2026 para sumar T25 y T26 a la hoja y recalcular los totales, el 25/11/2026 para pasar el reparto a la hoja, y el 27/11/2026 para poner al día el avance.
