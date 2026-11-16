# Sesión 15 — Costos del proyecto

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Integrantes: Hugo Zuñiga (Product Owner), Andrés Laura Vargas (Scrum Master) y Sebastian Cruz
- Docente: Ing. Alejandro Rodríguez (Certificación I)
- Fecha: 16/11/2026 · Sprint 1 · Issue: por crear · Milestone: Sprint 1
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
| PLAN | [Sesiones 8–9](sesion-08-09-plan.md), sección 4 | Las 142 h-p estimadas por tarea |
| GUIA | Guía oficial «Buses I-26» de la UPB | Tarifa de 5 Bs por viaje, para los viajes de prueba |

## 2. Horas estimadas

| Etapa | Tareas | h-p |
|---|---|---:|
| Perfil (ya hecho) | T00 | 6 |
| Sprint 1 | T01 a T08 | 32 |
| Sprint 2 | T09 a T13, y 3 h-p de T23 | 35 |
| Sprint 3 | T14 a T16, 5 h-p de T17 y 3 h-p de T23 | 30 |
| Sprint 4 | T18 a T20, 5 h-p de T17 y 4 h-p de T23 | 26 |
| Cierre | T21, T22 y T24 | 13 |
| **Total** | | **142** |

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
| Mano de obra | 142 h-p × 54,97 Bs/h | 7.805,97 |
| Otros costos | Sección 4 | 1.283,33 |
| Subtotal | | 9.089,30 |
| Contingencia | 15% del subtotal, para imprevistos **[PROVISIONAL]** | 1.363,39 |
| **Costo total del proyecto** | Lo que cuesta hacerlo | **10.452,69** |
| Utilidad | 20% del costo total, solo si se vendiera **[PROVISIONAL]** | 2.090,54 |
| Precio sin impuestos | Costo total + utilidad | 12.543,23 |
| IVA (13%) | Incluido en el precio de la factura (L843) | 1.941,21 |
| IT (3%) | Sobre el ingreso bruto (L843) | 447,97 |
| **Precio con factura** | Precio sin impuestos ÷ (1 − 0,13 − 0,03) | **14.932,42** |

**Por qué se divide y no se multiplica.** En Bolivia el IVA va incluido en el monto de la factura y el IT se calcula sobre el ingreso bruto. Para que después de pagar los dos queden 12.543,23 Bs, la factura tiene que ser de 12.543,23 ÷ 0,84.

## 6. Escenarios de tarifa

| Escenario | Tarifa (Bs/h) | Costo total (Bs) | Precio con factura (Bs) |
|---|---:|---:|---:|
| Piso legal (salario mínimo) | 18,75 | 4.537,71 | 6.482,44 |
| **Desarrollador web** | **54,97** | **10.452,69** | **14.932,42** |
| Ingeniero de software promedio | 68,85 | 12.719,41 | 18.170,58 |

## 7. Horas y costo por persona

Las tareas compartidas se reparten por igual: las de «Hugo y Sebastian» entre dos, y las de «Los tres» entre tres.

| Persona | Horas estimadas | Costo estimado (Bs) |
|---|---:|---:|
| Hugo Zuñiga | 48,8 | 2.684,45 |
| Sebastian Cruz | 58,8 | 3.234,16 |
| Andrés Laura Vargas | 34,3 | 1.887,36 |
| **Total** | **142,0** | **7.805,97** |

El reparto no es parejo: Sebastian lleva el bus en vivo y el simulador, que es lo más pesado, y Andrés tiene menos horas estimadas. Se revisa en el Sprint Planning del Sprint 2.

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

Si se cobran los eventos de Scrum, el costo total sube a **13.297,47 Bs** y el precio con factura a **18.996,39 Bs**. No se incluyen en el precio base porque el plan estima solo el trabajo de cada tarea **[PROPUESTA]**.

## 10. Estimado contra real

Las horas reales salen de la hoja «Registro de horas»: cada integrante anota la fecha, la tarea (T01, T08…), las horas y qué hizo. Al cerrar cada sprint se copia aquí la fila.

| Etapa | h-p estimadas | h-p reales | Diferencia | Costo real (Bs) | Comentario |
|---|---:|---:|---:|---:|---|
| Perfil | 6 | — | — | — | Hecho; horas no registradas |
| Sprint 1 | 32 | — | — | — | En curso |
| Sprint 2 | 35 | — | — | — | |
| Sprint 3 | 30 | — | — | — | |
| Sprint 4 | 26 | — | — | — | |
| Cierre | 13 | — | — | — | |
| **Total** | **142** | — | — | — | |

Al 16/11/2026 no hay horas reales registradas. T00 (perfil) y T04 (entrevistas ENT-01 y ENT-02) están hechas, pero falta anotar cuánto tomaron.

## 11. Participación y asistencia utilizada

- **Hugo Zuñiga (Product Owner):** pidió el cálculo, aprueba la tarifa y los supuestos, y lleva el registro de horas.
- **Asistencia de IA:** se usó Claude (Anthropic) para buscar los sueldos de referencia y las tasas de impuestos, armar la hoja de cálculo y redactar este documento.
