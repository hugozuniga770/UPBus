# UPBus — Buses UPB en tiempo real (UPB Santa Cruz)

- Integrantes: Hugo Zuñiga (Product Owner), Andrés Laura Vargas (Scrum Master, dirige la implementación) y Sebastian Cruz
- Docente: Ing. Alejandro Rodríguez (Certificación I)
- Tecnología: Python con Django, Django REST Framework y Django Channels; SQLite; React con Tailwind CSS
- Método: Scrum, con sprints de una semana ([plan](docs/sesion-08-09-plan.md))
- Estado: Sprint 1. Requisitos, historias y plan en revisión; entrevistas ENT-01 a ENT-03 hechas. La **base del código** (registro, inicio de sesión, usuarios, rutas en el mapa y modo registro, con sus pruebas) está en la rama `develop`, por Pull Request.

## 1. Qué hace

Conecta en tiempo real a los estudiantes y a los choferes de los buses de la UPB Santa Cruz, para que nadie pierda el bus por falta de información. Reemplaza los grupos de WhatsApp por un mapa en vivo, avisos, chat y pago con créditos.

| Historia | Qué permite | Rol |
|---|---|---|
| HU-01 | Registrarse con el código y el correo del padrón | Estudiante |
| HU-02 | Iniciar y cerrar sesión con código o correo | Todos |
| HU-03 | Crear y eliminar choferes y personas | Administrador |
| HU-04 | Ver rutas, paradas y horarios en el mapa | Todos |
| HU-05 | Iniciar y terminar su viaje | Chofer |
| HU-06 | Ver el bus en vivo y la hora aproximada en su parada | Estudiante |
| HU-07 | Avisar «Voy a subir» y compartir su ubicación | Estudiante |
| HU-08 | Proponer una parada | Estudiante y chofer |
| HU-09 | Recibir el aviso de bus cerca | Estudiante |
| HU-10 | Registrar quién subió | Estudiante y chofer |
| HU-11 | Recargar créditos | Estudiante |
| HU-12 | Pagar el viaje y ver el comprobante | Estudiante y chofer |
| HU-13 | Retirar su saldo | Chofer |
| HU-14 | Chatear directo con el chofer | Estudiante y chofer |
| HU-15 | Usar el chat de la ruta | Estudiante y chofer |
| HU-16 | Modificar una ruta | Chofer y administrador |
| HU-17 | Ver los confirmados y recibir el aviso de mínimo | Chofer y administrador |
| HU-18 | Grabar paradas y horas en un viaje real (modo registro) | Chofer y administrador |

En el MVP la ubicación del bus y de los estudiantes, la recarga de créditos, el retiro y el padrón son **simulados**. Las paradas y sus horas no: se graban con el GPS real en el modo registro. El detalle está en la [sección 2 de los requisitos](docs/sesion-06-requisitos.md).

## 2. Documentación

| Documento | Contenido | Estado |
|---|---|---|
| [sesion-06-requisitos.md](docs/sesion-06-requisitos.md) | Requisitos, alcance, lo que se simula y preguntas abiertas | Listo para revisión · RF-23 el 18/11 |
| [sesion-07-modelos.md](docs/sesion-07-modelos.md) | 18 historias, 73 criterios Dado/Cuando/Entonces con el nombre de su test, casos de uso, estados y trazabilidad | Listo para revisión |
| [sesion-08-09-plan.md](docs/sesion-08-09-plan.md) | Plan por sprints, tareas, Gantt, riesgos y recortes | Listo para revisión |
| [sesion-12-arquitectura.md](docs/sesion-12-arquitectura.md) | Arquitectura y verificación de un flujo | Pendiente |
| [sesion-13-14-diseno.md](docs/sesion-13-14-diseno.md) | Datos, clases y arquitectura FE / MW / Padrón / BD | Pendiente |
| [diagramas-secuencia.md](docs/diagramas-secuencia.md) | Un diagrama de secuencia por caso de uso, CU-18 incluido | Propuesta para revisión |
| [trazabilidad.md](docs/trazabilidad.md) | Cada test con su criterio y su requisito | Pendiente |
| [entrevistas.md](docs/entrevistas.md) | Entrevistas, conclusiones y guías de las siguientes | ENT-01 a ENT-03 hechas |
| [sesion-15-costos.md](docs/sesion-15-costos.md) | Horas-persona, tarifa, precio y estimado contra real | Listo para revisión |
| [cambios.md](docs/cambios.md) | Registro de cambios | Al día |
| [glosario.md](docs/glosario.md) | Siglas y términos | Al día |

## 3. Cómo estará organizado el código

Sigue la organización del proyecto de reserva de salas: las vistas solo reciben y responden, los servicios orquestan y las reglas deciden.

```
config/            configuración de Django
cuentas/           usuario, padrón, registro e inicio de sesión
rutas/             rutas, paradas y horarios
viajes/            viajes, ubicaciones, «Voy a subir» y créditos
mensajes/          chat directo y chat de la ruta
padron/padron.json padrón simulado, de solo lectura
tests/             un test por criterio de aceptación (pytest)
frontend/          React con Tailwind y sus pruebas (Vitest)
docs/              esta documentación
```

Cada app tendrá `models.py`, `reglas.py`, `servicios.py` y `views.py`. El detalle se define en la sesión 13–14.

## 4. Cómo ponerlo a andar

El código vive en la rama `develop` hasta que se cierre el sprint. Los pasos están en la sección 4 del README de esa rama y en la [guía de desarrollo](https://github.com/hugozuniga770/UPBus/blob/develop/docs/guia-desarrollo.md). Para grabar una ruta desde el celular: [guía del modo registro](https://github.com/hugozuniga770/UPBus/blob/develop/docs/guia-modo-registro.md).

## 5. Cómo trabajamos

- Nadie sube directo a `main`: cada historia va en su rama, entra a `develop` por Pull Request y la aprueba Hugo.
- Andrés reparte las tareas en el Sprint Planning de cada sábado; las sesiones de implementación son sábado y domingo. Cada tarea tiene su issue en GitHub.
- Todo cambio a algo ya acordado se registra en [cambios.md](docs/cambios.md).
