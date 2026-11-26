# Guía del simulador: mostrar UPBus sin esperar a un bus real

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Fecha: 26/11/2026 · Tarea T23: [#8](https://github.com/hugozuniga770/UPBus/issues/8)
- Para quién: los integrantes, para la demo en clase (T24) y para probar las historias con un viaje entero.

## 0. Qué hace

Mueve un bus por el recorrido **grabado** de una ruta (la Ruta Sur, de [REG-01](viajes-grabados.md)) y llama a los **mismos servicios que la app**: inicia el viaje, manda las posiciones del bus, avisa «Voy a subir» y comparte la ubicación del estudiante. Un escenario solo funciona si las reglas funcionan.

- El viaje queda marcado como **simulado**: en el mapa se ve «🧪 Bus simulado» en lugar de «🚌 Bus en vivo».
- Los viajes simulados **no enseñan horas**: pasar por las paradas no cambia la hora aproximada, que sale solo de viajes reales (C-27).
- El bus va a unos 25 km/h, manda una posición cada 25 m y se detiene 30 s en cada parada.
- Si el recorrido grabado empieza después de la primera parada, el bus va en línea recta hasta él. Pasa en la Ruta Sur: REG-01 tiene puntos desde Parque Urbano, no desde Makro Parque.
- Usa dos cuentas de demo que se crean solas y no pueden iniciar sesión: «Chofer de la simulación» y «Estudiante de la simulación».

## 1. Escenarios

| Escenario | Qué pasa | Historia |
|---|---|---|
| `recorrido` | El bus recorre la ruta de punta a punta | HU-05, HU-06 |
| `no_se_presenta` | Un estudiante avisa «Voy a subir» en la segunda parada (u otra que elijas), comparte su ubicación y no sube. Cuando el bus llega a la parada siguiente, queda «no se presentó» | HU-07 |

Cuando estén T16 y T17 se agregan: un estudiante que sube marcando «He subido», otro que sube solo porque su ubicación va con el bus (HU10-CA5) y el pago del viaje (HU-12).

## 2. Desde el panel Demo (para la clase)

1. Entra con una cuenta de administrador y toca **Demo** en el inicio.
2. Elige el escenario, la ruta y la velocidad (10 significa diez veces más rápido: el viaje de 44 minutos dura unos 4). En «No se presenta» puedes elegir la parada del estudiante.
3. Toca **Iniciar simulación** y abre **Rutas › Sur** en otra pestaña o en el celular: el bus se mueve en vivo.
4. El panel muestra lo que va pasando, incluido lo que le llega al chofer, como «Estudiante de la simulación va a subir en Parque Urbano». **Detener** termina el viaje simulado. Corre una simulación a la vez.

La simulación corre dentro del servidor. Por eso, si el servidor se reinicia, la lista del panel empieza vacía; el viaje que haya quedado en curso se termina solo al iniciar la siguiente simulación.

## 3. Desde la terminal

```
python manage.py simular --lista
python manage.py simular recorrido --ruta sur --velocidad 10
python manage.py simular no_se_presenta --ruta sur --parada "Banco Ganadero"
python manage.py simular recorrido --ruta sur --sin-esperar
```

- `--horario 11:00` elige otro horario; por defecto, el primer ingreso.
- `--sin-esperar` corre todo de una vez, para probar.

Desde la terminal, las pantallas abiertas ven el bus cada vez que vuelven a consultar el viaje, cada 30 s. Para verlo moverse en vivo hay que usar el panel. El motivo: la capa de WebSocket del MVP vive en la memoria del servidor (decisión de diseño, sesión 13–14) y la terminal es otro proceso.

## 4. Participación y asistencia utilizada

- **Hugo Zuñiga:** T23, el simulador y el panel de demo.
- **Asistencia de IA:** se usó Claude (Anthropic) para escribir el simulador, sus pruebas y esta guía.
