# Viajes grabados con el modo registro

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Creado: 25/11/2026 · Tarea T26 · Issue: [#5](https://github.com/hugozuniga770/UPBus/issues/5)
- Qué es: cada viaje real grabado con el modo registro (HU-18, BUS-RF-23), con lo que se vio en el bus. Cada viaje tiene un identificador REG-xx y su respaldo en `rutas/datos/registros/`.
- Relacionados: [requisitos](sesion-06-requisitos.md) (RF-11, RF-23) · [guía del modo registro](guia-modo-registro.md) · [cambios](cambios.md)

## 0. Cómo se carga un viaje

Cada integrante carga el respaldo en su base con su cuenta de administrador:

```powershell
python manage.py importar_registro rutas/datos/registros/registro-sur-0640-2026-11-25.json --usuario <tu código o correo>
```

Cargar el mismo respaldo dos veces se rechaza con «ese registro ya fue importado».

## 1. REG-01 — Ruta Sur, ingreso de las 06:40, miércoles 25/11/2026

- Grabó: Sebastian Cruz, con su cuenta de administrador.
- Respaldo: [`rutas/datos/registros/registro-sur-0640-2026-11-25.json`](../rutas/datos/registros/registro-sur-0640-2026-11-25.json), 9 marcas y 96 puntos del recorrido.
- Salida programada: 06:40 desde Makro Parque, el punto de partida de la ruta. Llegada límite a la U: 07:40.

| # | Parada | Hora de la marca | Minutos desde las 06:40 | Personas que subieron | Precisión del GPS |
|---:|---|---|---:|---:|---:|
| 1 | Makro Parque | 06:46 | 6,5 | 1 | 121 m |
| 2 | Parque Urbano | 07:00 | 20,9 | 2 | 31 m |
| 3 | Banco Ganadero | 07:02 | 22,4 | 2 | 59 m |
| 4 | Cine Center | 07:04 | 24,2 | 3 | 50 m |
| 5 | Mercado Ramafa | 07:11 | 31,3 | 2 | 40 m |
| 6 | AMarket Santos Dumont (4to anillo) | 07:14 | 34,4 | 2 | 40 m |
| 7 | Hot Burguer (4to anillo) | 07:15 | 35,0 | 1 | 40 m |
| 8 | Avenida Olímpica (4to anillo) | 07:17 | 37,9 | 1 | 40 m |
| 9 | Campus UPB | 07:30 | 50,1 | — (llegada) | 50 m |
| | **Total** | | | **14** | |

Las personas que subieron las anotó Sebastian aparte: el modo registro no las cuenta (P-32). Donde no anotó «x2» o «x3» se tomó 1 persona. Mercado Ramafa figura a las 07:10 en sus notas y a las 07:11 en la marca: vale la de la marca.

### Qué mostró

1. **El recorrido tomó 44 minutos**, de las 06:46 en Makro Parque a las 07:30 en la UPB, dentro de la llegada límite de las 07:40.
2. **Las horas se miden desde la salida programada.** El bus pasó por su punto de partida a las 06:46. Con la primera versión del cálculo, que contaba los minutos desde la primera marca, la app habría mostrado cada parada 6 minutos antes de lo visto (Parque Urbano a las 06:54 en lugar de las 07:00). Desde C-23 los minutos se cuentan desde las 06:40 programadas y la hora se redondea hacia abajo, así que la app muestra lo que se vio. La prueba `test_el_registro_real_de_la_ruta_sur_da_las_horas_observadas` lo comprueba con este mismo respaldo.
3. **Subieron 14 personas en 8 paradas.** Es un solo viaje, pero queda por debajo del mínimo de 15 de RF-22: con estos números, el administrador habría recibido el aviso de mínimo.
4. **El recorrido tiene puntos desde las 07:00.** Entre Makro Parque y Parque Urbano no hay puntos, así que el mapa une esas dos paradas con una línea recta. El siguiente registro de esta ruta puede completar ese tramo.
5. **La precisión del GPS fue de 21 a 121 m.** La peor fue en Makro Parque, al empezar. Conviene esperar a que el indicador esté en verde (20 m o menos) antes de marcar la primera parada.

### Para qué se usa

- Las paradas y horas de la Ruta Sur ya están en la app para todos (HU-04).
- La Ruta Sur es la primera con paradas reales para probar «Voy a subir» (T14) y el bus en vivo (T11).
- Las personas por parada sirven de datos para los escenarios del simulador (T23) y para revisar el mínimo de RF-22.

## 2. Participación y asistencia utilizada

- **Sebastian Cruz:** grabó el viaje con el modo registro y anotó cuántas personas subieron en cada parada (T26).
- **Hugo Zuñiga:** subió el respaldo al repositorio.
- **Asistencia de IA:** se usó Claude (Anthropic) para pasar el registro a este documento y comprobar las horas con una prueba.
