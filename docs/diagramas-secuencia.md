# Diagramas de secuencia de los casos de uso

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Fecha: 16/11/2026 · Sprint 1 · Issue: [#3](https://github.com/hugozuniga770/UPBus/issues/3) · Milestone: Sprint 1
- Actualizado: 25/11/2026 · revisión del Product Owner (PO25): abordaje automático, pago iniciado por el estudiante, ajustes de créditos y todo cambio de ruta con aprobación (C-29 a C-32). El 18/11/2026: se agrega CU-18, el modo registro (C-18)
- Estado: **[PROPUESTA]**. Muestran cómo pensamos construir cada caso de uso; los nombres de las funciones se confirman en la [sesión 13–14](sesion-13-14-diseno.md).
- Requisitos: [Sesión 6](sesion-06-requisitos.md) · Cambios: [cambios.md](cambios.md) · Siglas: [glosario.md](glosario.md)

## 0. Cómo leer los diagramas

- **Mismo número, misma funcionalidad:** CU-07 es el caso de uso de HU-07. Sus pasos detallados van en la sesión 7.
- Los participantes son las capas del proyecto, como en el proyecto de reserva de salas:

| Participante | Qué es | Dónde estará |
|---|---|---|
| FE | Las pantallas, en el navegador (celular, computadora o la pantalla del bus) | `frontend/` (React con Tailwind) |
| Vista | Recibe la petición y responde JSON | `views.py` de cada app (Django REST Framework) |
| Servicios | Orquesta: lee lo necesario, pregunta a las reglas y guarda | `servicios.py` |
| Reglas | Decide si se permite y con qué causa se rechaza. No toca la base | `reglas.py` |
| Padrón | Lista de la universidad, de solo lectura | `padron/padron.json` (ejemplo) o `padron/padron.local.json` (la clase, fuera del repositorio), leído solo por `cuentas/padron.py` |
| BD | La base de datos | SQLite, a través de los modelos (`models.py`) |
| Canal | Envía al instante la ubicación, los avisos y los mensajes | Django Channels (WebSocket) |

- Las vistas nunca llaman a las reglas ni guardan en la BD: todo pasa por los servicios.
- Un **rechazo** (`Rechazo` con su causa) no guarda nada y la vista responde con la causa (BUS-RC-01, BUS-RC-03).
- Datos de los ejemplos: los de la sección 0 de los requisitos (Ismael 70004, parada Sevilla de la Ruta Norte, chofer Marco, administrador Hugo).

## 1. CU-01 — Registrarse (HU-01)

```mermaid
sequenceDiagram
    actor E as Ismael
    participant FE
    participant V as Vista
    participant S as Servicios
    participant R as Reglas
    participant P as Padrón
    participant B as BD
    E->>FE: Código 70004, correo y contraseña dos veces
    FE->>V: POST /api/registro
    V->>S: registrar(codigo, correo, contrasena, confirmacion)
    S->>P: buscar_por_codigo(70004)
    P-->>S: persona o nada
    S->>B: ya tiene cuenta?
    B-->>S: no
    S->>R: verificar_persona_en_padron, correo, activa, sin_cuenta, contrasenas_iguales, contrasena
    alt Todo se cumple
        R-->>S: sin rechazo
        S->>B: crear la cuenta con rol estudiante
        S-->>V: cuenta
        V-->>FE: 201 Cuenta creada
    else Rechazo
        R-->>S: Rechazo con la causa
        S-->>V: Rechazo
        V-->>FE: 400 con la causa, por ejemplo persona no activa en el padrón
    end
```

## 2. CU-02 — Iniciar y cerrar sesión (HU-02)

```mermaid
sequenceDiagram
    actor U as Usuario
    participant FE
    participant V as Vista
    participant S as Servicios
    participant B as BD
    U->>FE: Código o correo, y contraseña
    FE->>V: POST /api/sesion
    V->>S: iniciar_sesion(identificador, contrasena)
    S->>B: buscar la cuenta por código o por correo
    alt Cuenta y contraseña correctas
        S-->>V: cuenta con su rol
        V-->>FE: 200 y cookie de sesión. El FE muestra las pantallas del rol
    else Algo no coincide
        S-->>V: Rechazo
        V-->>FE: 400 Código, correo o contraseña incorrectos
    end
    U->>FE: Cerrar sesión
    FE->>V: DELETE /api/sesion
    V-->>FE: 204. La cookie deja de valer
```

El inicio de sesión no consulta el padrón: solo la BD.

## 3. CU-03 — Gestionar usuarios (HU-03)

```mermaid
sequenceDiagram
    actor A as Hugo (administrador)
    participant FE
    participant V as Vista
    participant S as Servicios
    participant R as Reglas
    participant B as BD
    A->>FE: Crear la cuenta de chofer de Marco
    FE->>V: POST /api/usuarios
    V->>S: crear_cuenta(administrador, datos, rol=chofer)
    S->>R: verificar_es_administrador
    S->>B: existe una cuenta con ese correo?
    S->>R: verificar_correo_libre
    alt Sin rechazo
        S->>B: crear la cuenta de chofer
        V-->>FE: 201 Cuenta creada
    else Rechazo
        V-->>FE: 400 o 403 con la causa
    end
    A->>FE: Eliminar una cuenta
    FE->>V: DELETE /api/usuarios/id
    V->>S: eliminar_cuenta(administrador, id)
    S->>B: desactivar la cuenta (P-23), sin borrar viajes ni comprobantes
    V-->>FE: 204
```

## 4. CU-04 — Ver rutas, paradas y horarios (HU-04)

```mermaid
sequenceDiagram
    actor U as Usuario
    participant FE
    participant V as Vista
    participant S as Servicios
    participant B as BD
    U->>FE: Abre la Ruta Norte
    FE->>V: GET /api/rutas/norte
    V->>S: ver_ruta(norte)
    S->>B: recorrido, paradas en orden, horarios y horas aproximadas
    B-->>S: datos
    S-->>V: ruta
    V-->>FE: 200 con la ruta. El FE la dibuja en el mapa (Leaflet)
```

Es una consulta: no cambia nada en la BD (BUS-RC-02).

## 5. CU-05 — Iniciar el viaje y compartir la ubicación (HU-05)

```mermaid
sequenceDiagram
    actor C as Marco (chofer)
    participant FE
    participant V as Vista
    participant S as Servicios
    participant R as Reglas
    participant B as BD
    participant W as Canal
    C->>FE: Iniciar ruta (Ruta Norte 06:40)
    FE->>V: POST /api/viajes/id/iniciar
    V->>S: iniciar_viaje(chofer, viaje, ahora)
    S->>B: el viaje y si el chofer tiene otro en curso
    S->>R: verificar_es_su_viaje, verificar_programado, verificar_sin_viaje_en_curso
    alt Sin rechazo
        S->>B: viaje En curso, con su hora de inicio
        V-->>FE: 200
        loop Cada 5 a 10 segundos
            FE->>W: posición del bus (GPS o simulada)
            W->>S: registrar_ubicacion_bus(viaje, posición, ahora)
            S->>B: guardar la última posición
            S->>W: enviar a quienes miran la ruta
        end
    else Rechazo
        V-->>FE: 400 con la causa, por ejemplo ya tienes un viaje en curso
    end
    C->>FE: Terminar ruta
    FE->>V: POST /api/viajes/id/terminar
    V->>S: terminar_viaje(chofer, viaje, ahora)
    S->>B: viaje Terminado. Se cierran los avisos y las ubicaciones de estudiantes
```

## 6. CU-06 — Ver el bus en vivo y la hora aproximada (HU-06)

```mermaid
sequenceDiagram
    actor E as Ismael
    participant FE
    participant V as Vista
    participant S as Servicios
    participant B as BD
    participant W as Canal
    E->>FE: Abre el mapa de la Ruta Norte
    FE->>V: GET /api/viajes/id/estado
    V->>S: estado_del_viaje(viaje)
    S->>B: última posición y hora aproximada de cada parada
    alt Viaje En curso
        V-->>FE: 200 con la posición y la hora aproximada en Sevilla
        FE->>W: suscribirse al viaje
        loop Mientras el viaje está En curso
            W-->>FE: nueva posición del bus
            FE->>FE: mueve el bus en el mapa
        end
    else Viaje Programado
        V-->>FE: 200 El bus aún no salió
    end
```

## 7. CU-07 — «Voy a subir» y compartir la ubicación (HU-07)

```mermaid
sequenceDiagram
    actor E as Ismael
    participant FE
    participant V as Vista
    participant S as Servicios
    participant R as Reglas
    participant B as BD
    participant W as Canal
    actor C as Marco (chofer)
    E->>FE: Voy a subir en Sevilla
    FE->>V: POST /api/viajes/id/avisos
    V->>S: avisar_que_sube(estudiante, viaje, parada, ahora)
    S->>B: el viaje y si ya avisó en este viaje
    S->>R: verificar_viaje_abierto, verificar_un_aviso_por_viaje, verificar_bus_no_paso_la_parada
    alt Sin rechazo
        S->>B: aviso Confirmado
        S->>W: alerta al chofer
        W-->>C: Ismael va a subir en Sevilla
        V-->>FE: 201
        loop Mientras espera
            FE->>W: ubicación de Ismael (GPS o simulada)
            W->>S: registrar_ubicacion_estudiante
            S->>W: solo al chofer de ese viaje
        end
    else Rechazo
        V-->>FE: 400 Ya avisaste que vas a subir en este viaje
    end
    Note over S,B: Si el bus llega a Petrol, la parada siguiente, y Ismael no subió ni canceló, cerrar_avisos_pasados deja el aviso como No se presentó (P-33)
```

## 8. CU-08 — Proponer una parada (HU-08)

```mermaid
sequenceDiagram
    actor E as Estudiante o chofer
    participant FE
    participant V as Vista
    participant S as Servicios
    participant R as Reglas
    participant B as BD
    E->>FE: Marca un punto en el mapa de la ruta
    FE->>V: POST /api/rutas/norte/paradas-propuestas
    V->>S: proponer_parada(usuario, ruta, punto)
    S->>B: recorrido de la ruta
    S->>R: verificar_sobre_la_ruta (a menos de 200 m)
    alt Sin rechazo
        S->>B: parada Propuesta
        V-->>FE: 201
    else Rechazo
        V-->>FE: 400 La parada debe estar sobre la ruta
    end
```

Una parada solo se enciende en un viaje si alguien espera en ella con su ubicación compartida (RF-10).

## 9. CU-09 — Aviso de bus cerca (HU-09)

```mermaid
sequenceDiagram
    participant W as Canal
    participant S as Servicios
    participant R as Reglas
    participant B as BD
    actor E as Ismael
    W->>S: registrar_ubicacion_bus(viaje, posición, ahora)
    S->>B: avisos Confirmados del viaje y sus paradas
    loop Por cada aviso sin notificar
        S->>R: esta_cerca(posición, parada) a 500 m o menos
        alt Está cerca
            S->>B: marcar el aviso como notificado
            S->>W: Tu bus está cerca
            W-->>E: aviso en la app abierta
        end
    end
    S->>R: llego_a_la_parada (a menos de 50 m)
    S->>B: guardar la hora real de paso, para la hora aproximada (RF-11)
```

## 10. CU-10 y CU-12 — Registrar quién subió y pagar el viaje (HU-10, HU-12)

Subir y pagar son dos pasos distintos (C-31): registrar que subió no cobra.

```mermaid
sequenceDiagram
    actor E as Ismael
    participant FE
    participant V as Vista
    participant S as Servicios
    participant R as Reglas
    participant B as BD
    participant W as Canal
    actor C as Marco (chofer)
    alt Ismael toca He subido, o Marco marca subió
        FE->>V: POST /api/avisos/id/subio
        V->>S: registrar_abordaje(usuario, aviso, ahora)
        S->>R: verificar_viaje_en_curso, verificar_aviso_confirmado
    else Ismael comparte su ubicación y va en el bus
        FE->>V: POST /api/avisos/id/ubicacion
        V->>S: compartir_ubicacion(usuario, aviso, posición)
        S->>R: va_en_el_bus (el bus a más de 100 m de Sevilla y dos ubicaciones seguidas a menos de 50 m del bus)
    end
    S->>B: aviso A bordo, sin cobro, con quién lo marcó
    S->>W: Ismael ha subido
    W-->>C: aparece en su lista
    Note over S,B: Al quedar A bordo se deja de compartir la ubicación de Ismael
```

```mermaid
sequenceDiagram
    actor E as Ismael
    participant FE
    participant V as Vista
    participant S as Servicios
    participant R as Reglas
    participant B as BD
    actor C as Marco (chofer)
    E->>FE: Pagar el viaje con 5 créditos
    FE->>V: POST /api/viajes/id/pagos con id_cliente
    V->>S: pagar_viaje(estudiante, viaje, id_cliente, ahora)
    S->>B: viaje, saldo de Ismael y si ya pagó
    S->>R: verificar_viaje_en_curso, verificar_no_pago_antes, verificar_saldo (5 o más)
    alt Sin rechazo
        S->>B: en una sola transacción, cobro de 5, abono al chofer y comprobante
        V-->>FE: 201 con el comprobante
    else Saldo insuficiente
        V-->>FE: 400 Saldo insuficiente, paga en efectivo
    end
    Note over C,B: Al final de la ruta, como hoy
    C->>FE: Comprobantes de mi viaje, busca 70004 o Ismael
    FE->>V: GET /api/viajes/id/pagos con la búsqueda
    V->>S: pagos_del_viaje(chofer, viaje, busqueda)
    V-->>FE: lista con pagado o pagó en efectivo, y el total
    C->>FE: Ismael pagó en efectivo
    FE->>V: POST /api/viajes/id/pagos/efectivo
    V->>S: marcar_pago_en_efectivo(chofer, viaje, estudiante)
    S->>B: pago en efectivo, sin movimiento de créditos
```

Un reenvío del mismo pago (mismo `id_cliente`) devuelve el mismo comprobante, y un segundo pago del mismo viaje se rechaza por «ya pagaste este viaje»: nunca se cobra dos veces (BUS-RC-03).

## 11. CU-11 — Recargar créditos (HU-11)

```mermaid
sequenceDiagram
    actor E as Ismael
    actor A as Hugo (administrador)
    participant FE
    participant V as Vista
    participant S as Servicios
    participant R as Reglas
    participant B as BD
    E->>FE: Recargar 20 Bs
    FE->>V: POST /api/recargas
    V->>S: pedir_recarga(estudiante, monto)
    S->>R: verificar_monto (5 o más, múltiplo de 5)
    alt Monto válido
        S->>B: recarga Pendiente
        V-->>FE: 201
    else Rechazo
        V-->>FE: 400 El monto debe ser múltiplo de 5
    end
    Note over A,B: SIMULADO. En el servicio real aprueba la pasarela de pagos
    A->>FE: Aprobar la recarga
    FE->>V: POST /api/recargas/id/aprobar
    V->>S: aprobar_recarga(administrador, recarga)
    S->>R: verificar_es_administrador, verificar_pendiente
    S->>B: recarga Aprobada y movimiento de +20 créditos
    V-->>FE: 200
    Note over A,B: Ajuste del administrador (C-29)
    A->>FE: Dar 50 créditos a Ismael, motivo demo
    FE->>V: POST /api/ajustes
    V->>S: ajustar_creditos(administrador, estudiante, monto, motivo)
    S->>R: verificar_es_administrador, verificar_saldo_no_negativo
    S->>B: movimiento de ajuste con su motivo y quién lo hizo
    V-->>FE: 201
```

## 12. CU-13 — Retirar el saldo del chofer (HU-13)

```mermaid
sequenceDiagram
    actor C as Marco (chofer)
    participant FE
    participant V as Vista
    participant S as Servicios
    participant R as Reglas
    participant B as BD
    C->>FE: Retirar 40 Bs
    FE->>V: POST /api/retiros
    V->>S: retirar_saldo(chofer, monto)
    S->>B: saldo = suma de sus movimientos
    S->>R: verificar_saldo_suficiente
    alt Sin rechazo
        S->>B: movimiento de retiro (SIMULADO)
        V-->>FE: 201
    else Rechazo
        V-->>FE: 400 Saldo insuficiente
    end
```

## 13. CU-14 — Chat directo con el chofer (HU-14)

```mermaid
sequenceDiagram
    actor E as Ismael
    participant FE
    participant W as Canal
    participant S as Servicios
    participant R as Reglas
    participant B as BD
    actor C as Marco (chofer)
    E->>FE: Ya estoy en la parada
    FE->>W: mensaje directo del viaje
    W->>S: enviar_mensaje_directo(estudiante, viaje, texto)
    S->>B: el aviso de Ismael en ese viaje
    S->>R: verificar_esta_en_el_viaje
    alt Sin rechazo
        S->>B: guardar el mensaje con nombre y hora
        S->>W: al chofer
        W-->>C: Ismael. Ya estoy en la parada
        C->>W: respuesta rápida Te espero 1 min
        W-->>FE: respuesta del chofer
    else Rechazo
        W-->>FE: No estás en este viaje
    end
```

## 14. CU-15 — Chat de la ruta (HU-15)

```mermaid
sequenceDiagram
    actor E as Ismael
    participant FE
    participant W as Canal
    participant S as Servicios
    participant R as Reglas
    participant B as BD
    actor M as Miembros de la Ruta Norte
    E->>FE: Escribe en el chat de la Ruta Norte
    FE->>W: mensaje de ruta
    W->>S: enviar_mensaje_ruta(estudiante, ruta, texto)
    S->>R: verificar_es_miembro_de_la_ruta
    alt Sin rechazo
        S->>B: guardar el mensaje
        S->>W: a todos los miembros
        W-->>M: mensaje con nombre y hora
    else Rechazo
        W-->>FE: No eres parte de esta ruta
    end
```

## 15. CU-16 — Modificar una ruta (HU-16)

```mermaid
sequenceDiagram
    actor C as Marco (chofer)
    actor A as Hugo (administrador)
    participant FE
    participant V as Vista
    participant S as Servicios
    participant R as Reglas
    participant B as BD
    C->>FE: Mueve un punto del recorrido
    FE->>V: POST /api/rutas/norte/cambios
    V->>S: proponer_cambio_ruta(usuario, ruta, cambio)
    S->>R: verificar_puede_editar, verificar_no_cambia_llegada_a_la_U
    alt Lo propone el chofer
        S->>B: cambio Pendiente, la ruta sigue igual
        V-->>FE: 202 Pendiente de aprobación
        A->>FE: Aprobar
        FE->>V: POST /api/cambios/id/aprobar
        V->>S: aprobar_cambio(administrador, cambio)
        S->>B: aplicar el cambio
    else Lo hace un administrador
        S->>B: aplicar el cambio
        V-->>FE: 200 Cambio aplicado
    else Rechazo
        V-->>FE: 403 No puedes cambiar la hora de llegada a la U
    end
```

## 16. CU-17 — Confirmados y aviso de mínimo (HU-17)

```mermaid
sequenceDiagram
    participant T as Tarea programada
    participant S as Servicios
    participant R as Reglas
    participant B as BD
    participant W as Canal
    actor A as Hugo (administrador)
    T->>S: revisar_minimo(ahora), cada minuto
    S->>B: viajes que salen dentro de 30 minutos y sus confirmados
    loop Por cada viaje
        S->>R: hay_menos_del_minimo(confirmados, 15)
        alt Menos de 15 y sin aviso previo
            S->>B: marcar el viaje como avisado
            S->>W: aviso al administrador
            W-->>A: Ruta Norte 06:40 tiene 9 confirmados
        end
    end
    Note over S,B: La app no cancela el viaje. Decide una persona
```

## 17. CU-18 — Modo registro de paradas y horas (HU-18)

Agregado el 18/11/2026 (C-18). A diferencia de los demás, este caso de uso ya está construido en la base del código, así que los nombres son los reales.

```mermaid
sequenceDiagram
    actor C as Sebastian (administrador) o Marco (chofer)
    participant FE as FE (celular)
    participant V as Vista
    participant S as Servicios
    participant R as Reglas
    participant B as BD
    C->>FE: Modo registro · Ruta Norte 06:40
    FE->>V: POST /api/registros
    V->>S: iniciar_registro(usuario, ruta, horario)
    S->>R: verificar_puede_registrar, verificar_horario_de_la_ruta, verificar_sin_registro_en_curso
    S->>B: registro En curso
    V-->>FE: 201 con el registro
    loop Cada 15 segundos o 40 m
        FE->>V: POST /api/registros/id/puntos (lo que espera en la cola)
        V->>S: agregar_puntos(usuario, registro, puntos)
        S->>B: guardar los puntos nuevos, sin repetir los que ya estaban
    end
    C->>FE: toca «Parada» en Sevilla
    Note over FE: La marca entra a la cola del celular con su id_cliente. Sin señal, espera y se reintenta
    FE->>V: POST /api/registros/id/marcas
    V->>S: marcar_parada(usuario, registro, id_cliente, posición, hora)
    S->>B: ¿ya existe una marca con ese id_cliente?
    alt Es un reenvío
        V-->>FE: 201 con la misma marca, sin duplicarla
    else Es nueva
        S->>R: verificar_lejos_de_las_otras_marcas (50 m)
        S->>B: guardar la marca
        V-->>FE: 201
    end
    C->>FE: Terminar
    FE->>V: POST /api/registros/id/terminar
    V->>S: terminar_registro(usuario, registro)
    S->>R: verificar_hay_marcas
    loop Por cada marca, desde la primera (la salida)
        S->>R: parada_mas_cercana (menos de 50 m)
        alt Hay una parada cerca
            S->>B: un paso por esa parada (registrar_paso)
        else No hay
            S->>R: estado_de_una_parada_nueva: aprobada o propuesta
            S->>B: parada nueva y su paso
        end
    end
    S->>B: orden de las paradas y, si la ruta no tenía, su recorrido
    V-->>FE: 200 con el resumen: marcas, paradas nuevas y ya conocidas
```

## 18. Simulador de escenarios (T23)

No es un caso de uso del usuario: es la herramienta de la demo y de las pruebas. Lo importante es que **llama a los mismos servicios que la app**, así que un escenario solo funciona si las reglas funcionan. Cómo se usa: [guía del simulador](guia-simulador.md).

```mermaid
sequenceDiagram
    actor D as Administrador (panel Demo o terminal)
    participant Sim as Simulador
    participant S as Servicios
    participant B as BD
    participant W as Canal
    participant FE as Pantallas abiertas
    D->>Sim: no_se_presenta en la Ruta Sur, velocidad 10
    Sim->>S: iniciar_viaje(chofer de la simulación, viaje simulado)
    Sim->>S: avisar_que_va_a_subir(estudiante de la simulación, Parque Urbano)
    loop Cada 25 m del recorrido grabado, con el reloj acelerado
        Sim->>S: compartir_ubicacion(estudiante, junto a su parada), cada 15 s
        Sim->>S: registrar_posicion(chofer, posición, ahora)
        S->>B: guarda la posición, sin pasos que enseñen horas (C-28)
        S->>W: nueva posición
        W-->>FE: el bus simulado se mueve
    end
    Note over Sim,S: Ismael nunca sube. Cuando el bus llega a Petrol, cerrar_avisos_pasados lo marca No se presentó
    Note over S,B: Los pasos de un viaje simulado no cambian las horas aproximadas (C-28)
    Sim->>S: terminar_viaje(Marco)
```

## 19. Participación y asistencia utilizada

- **Hugo Zuñiga (Product Owner):** pidió los diagramas y los aprueba.
- **Asistencia de IA:** se usó Claude (Anthropic) para proponer las secuencias a partir de los requisitos y de la organización por capas del proyecto de referencia, el 18/11/2026 para dibujar la de CU-18 desde el código de la base y el 25/11/2026 para rehacer las de CU-10, CU-11, CU-12 y CU-16 con las decisiones del Product Owner (PO25).
