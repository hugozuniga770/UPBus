# Trazabilidad: requisito → criterio → test → código

- Proyecto: UPBus — Buses UPB en tiempo real (UPB Santa Cruz)
- Fecha: 18/11/2026 · Actualizado: 25/11/2026 (C-23, C-25; 75 criterios desde C-29 y C-30) · Tarea T21 (empezada con la base) · Issue: [#16](https://github.com/hugozuniga770/UPBus/issues/16)
- Criterios completos: [Sesión 7](sesion-07-modelos.md) · Requisitos: [Sesión 6](sesion-06-requisitos.md)

## 0. Cómo se mantiene

- Cada criterio de la sesión 7 es un test con el mismo nombre. Cuando una historia se termina, quien la hizo agrega aquí sus filas, en el mismo Pull Request.
- «Código» nombra el servicio, la regla o la vista que cumple el criterio, para encontrarlo rápido.
- Al 25/11/2026 hay **34 de 73** criterios con su test en verde.

## 1. Criterios con su test (base del código)

| Criterio | Requisito | Test de pytest | Código | Prueba de interfaz |
|---|---|---|---|---|
| HU01-CA1 | RF-01 | `tests/test_hu01_registro.py::test_HU01_CA1_registra_cuenta_con_codigo_y_correo_del_padron` | `cuentas.servicios.registrar` | — |
| HU01-CA2 | RF-01 | `tests/test_hu01_registro.py::test_HU01_CA2_rechaza_registro_de_persona_inactiva` | `cuentas.reglas.verificar_persona_activa` | — |
| HU01-CA3 | RF-01 | `tests/test_hu01_registro.py::test_HU01_CA3_rechaza_si_las_contrasenas_no_coinciden` | `cuentas.reglas.verificar_contrasenas_iguales` | `frontend/src/paginas/Registrarse.test.jsx` |
| HU01-CA4 | RF-01, RF-03 | `tests/test_hu01_registro.py::test_HU01_CA4_la_cuenta_toma_el_rol_de_administrador_del_padron` | `cuentas.reglas.rol_desde_el_padron` | — |
| HU02-CA1 | RF-02 | `tests/test_hu02_sesion.py::test_HU02_CA1_entra_con_su_codigo` | `cuentas.backends.CodigoOCorreoBackend` | — |
| HU02-CA2 | RF-02 | `tests/test_hu02_sesion.py::test_HU02_CA2_entra_con_su_correo` | `cuentas.backends.buscar_por_identificador` | — |
| HU02-CA3 | RF-02 | `tests/test_hu02_sesion.py::test_HU02_CA3_un_solo_mensaje_si_algo_no_coincide` | `cuentas.reglas.verificar_credenciales` | `frontend/src/paginas/IniciarSesion.test.jsx` |
| HU02-CA4 | RF-02 | `tests/test_hu02_sesion.py::test_HU02_CA4_al_cerrar_sesion_vuelve_a_pedir_inicio` | `cuentas.views.SesionVista` (DELETE), `comun.respuestas.manejar_excepcion` | — |
| HU03-CA1 | RF-04 | `tests/test_hu03_usuarios.py::test_HU03_CA1_el_administrador_crea_la_cuenta_de_un_chofer` | `cuentas.servicios.crear_cuenta` | — |
| HU03-CA2 | RF-04 | `tests/test_hu03_usuarios.py::test_HU03_CA2_rechaza_un_correo_que_ya_tiene_cuenta` | `cuentas.reglas.verificar_correo_libre` | — |
| HU03-CA3 | RF-03 | `tests/test_hu03_usuarios.py::test_HU03_CA3_un_estudiante_no_puede_crear_cuentas` | `cuentas.reglas.verificar_es_administrador` | — |
| HU03-CA4 | RF-04 | `tests/test_hu03_usuarios.py::test_HU03_CA4_eliminar_desactiva_la_cuenta` | `cuentas.servicios.eliminar_cuenta` | — |
| HU04-CA1 | RF-05 | `tests/test_hu04_rutas.py::test_HU04_CA1_ve_la_ruta_con_recorrido_paradas_y_horarios` | `rutas.servicios.ver_ruta` | — |
| HU04-CA2 | RF-05 | `tests/test_hu04_rutas.py::test_HU04_CA2_el_estudiante_ve_solo_las_paradas_aprobadas` | `rutas.servicios.paradas_visibles` | — |
| HU05-CA1 | RF-06 | `tests/test_hu05_viajes.py::test_HU05_CA1_el_chofer_inicia_su_viaje` | `viajes.servicios.iniciar_viaje` | `frontend/src/paginas/Viajes.test.jsx` |
| HU05-CA2 | RF-06 | `tests/test_hu05_viajes.py::test_HU05_CA2_rechaza_un_segundo_viaje_en_curso` | `viajes.reglas.verificar_sin_viaje_en_curso` | — |
| HU05-CA3 | RF-06 | `tests/test_hu05_viajes.py::test_HU05_CA3_el_chofer_termina_su_viaje` | `viajes.servicios.terminar_viaje`, `frontend/src/paginas/Viajes.jsx` | — |
| HU05-CA4 | RF-03, RF-06 | `tests/test_hu05_viajes.py::test_HU05_CA4_rechaza_iniciar_un_viaje_ajeno` | `viajes.reglas.verificar_es_su_viaje` | — |
| HU06-CA1 | RF-07 | `tests/test_hu06_bus_en_vivo.py::test_HU06_CA1_la_posicion_del_bus_llega_a_quienes_miran_la_ruta` | `viajes.servicios.registrar_posicion`, `viajes.consumers.ViajeConsumer`, `frontend/src/paginas/Rutas.jsx` | `frontend/src/paginas/Rutas.test.jsx` |
| HU06-CA2 | RF-07 | `tests/test_hu06_bus_en_vivo.py::test_HU06_CA2_rechaza_posiciones_de_un_viaje_que_no_esta_en_curso` | `viajes.reglas.verificar_en_curso` | — |
| HU06-CA3 | RF-11 | `tests/test_hu06_bus_en_vivo.py::test_HU06_CA3_pasar_a_menos_de_50_m_registra_un_paso` | `viajes.servicios.registrar_posicion`, `rutas.servicios.registrar_paso` | — |
| HU06-CA4 | RF-11 | `tests/test_hu06_bus_en_vivo.py::test_HU06_CA4_pasar_a_80_m_no_cuenta_como_llegada` | `rutas.reglas.parada_mas_cercana` | — |
| HU06-CA5 | RF-07 | `tests/test_hu06_bus_en_vivo.py::test_HU06_CA5_sin_senal_se_ve_la_ultima_posicion_con_su_hora` | `viajes.serializadores.viaje_a_dict`, `frontend/src/paginas/Rutas.jsx` | — |
| HU07-CA1 | RF-09 | `tests/test_hu07_voy_a_subir.py::test_HU07_CA1_avisa_que_va_a_subir` | `viajes.servicios.avisar_que_va_a_subir`, `viajes.consumers.ChoferDelViajeConsumer` | `frontend/src/componentes/VoyASubir.test.jsx` |
| HU07-CA2 | RF-09 | `tests/test_hu07_voy_a_subir.py::test_HU07_CA2_rechaza_un_segundo_aviso_en_el_mismo_viaje` | `viajes.reglas.verificar_sin_aviso_activo` | `frontend/src/componentes/VoyASubir.test.jsx` |
| HU07-CA3 | RF-09 | `tests/test_hu07_voy_a_subir.py::test_HU07_CA3_si_el_bus_pasa_y_no_subio_queda_no_se_presento` | `viajes.servicios.cerrar_no_presentados` | — |
| HU07-CA4 | RF-09 | `tests/test_hu07_voy_a_subir.py::test_HU07_CA4_puede_cancelar_antes_de_que_pase_el_bus` | `viajes.servicios.cancelar_aviso` | — |
| HU07-CA5 | RF-08 | `tests/test_hu07_voy_a_subir.py::test_HU07_CA5_el_chofer_ve_la_ubicacion_compartida` | `viajes.servicios.compartir_ubicacion`, `viajes.reglas.verificar_puede_ver_avisos`, `frontend/src/componentes/AvisosDelViaje.jsx` | — |
| HU07-CA7 | RF-03, RF-09 | `tests/test_hu07_voy_a_subir.py::test_HU07_CA7_un_administrador_tambien_puede_avisar` | `viajes.reglas.verificar_puede_avisar` | — |
| HU18-CA1 | RF-23, RF-11 | `tests/test_hu18_modo_registro.py::test_HU18_CA1_el_primer_registro_crea_las_paradas_y_sus_horas` | `rutas.servicios.terminar_registro`, `rutas.reglas.hora_aproximada` | — |
| HU18-CA2 | RF-23, RF-11 | `tests/test_hu18_modo_registro.py::test_HU18_CA2_un_segundo_registro_ajusta_la_hora_sin_duplicar_la_parada` | `rutas.reglas.parada_mas_cercana`, `rutas.reglas.salida_programada`, `rutas.servicios.minutos_aprendidos` | — |
| HU18-CA3 | RF-23 | `tests/test_hu18_modo_registro.py::test_HU18_CA3_un_estudiante_no_puede_usar_el_modo_registro` | `rutas.reglas.verificar_puede_registrar` | — |
| HU18-CA4 | RF-23 | `tests/test_hu18_modo_registro.py::test_HU18_CA4_rechaza_una_marca_a_menos_de_50_m_de_otra` | `rutas.reglas.verificar_lejos_de_las_otras_marcas` | — |
| HU18-CA5 | RF-23 | `tests/test_hu18_modo_registro.py::test_HU18_CA5_una_marca_reenviada_se_guarda_una_sola_vez` | `rutas.servicios.marcar_parada` | `frontend/src/registro/cola.test.js` |

## 2. Pruebas de soporte

No son criterios: prueban herramientas que usan las historias.

| Prueba | Qué comprueba |
|---|---|
| `tests/test_soporte.py::test_importar_padron_reemplaza_los_correos_que_no_son_de_la_upb` | `importar_padron` lee la lista con el formato de la de la clase y cambia los correos que no son de la UPB por `<código>@upb.example` |
| `tests/test_soporte.py::test_importar_un_respaldo_del_modo_registro` | `importar_registro` carga un respaldo y rechaza cargarlo dos veces |
| `tests/test_soporte.py::test_el_registro_real_de_la_ruta_sur_da_las_horas_observadas` | Con el respaldo real de la Ruta Sur (REG-01), la app muestra las horas que se vieron en el bus (C-23) |
| `tests/test_soporte.py::test_el_websocket_del_viaje_confirma_la_conexion` | El canal `ws/viajes/<id>/` conecta (base de HU-06) |
| `tests/test_hu07_voy_a_subir.py::test_al_terminar_el_viaje_nadie_sigue_esperando_ni_compartiendo` | Completa HU05-CA3: al terminar el viaje, los avisos confirmados quedan «no se presentó» y se borran las ubicaciones |
| `tests/test_soporte.py::test_el_administrador_puede_programar_viajes_desde_el_panel` | El panel de Django permite listar y filtrar los viajes que programa el administrador |
| `tests/test_simulador.py` (11 pruebas) | El simulador de T23 recorre la ruta con los mismos servicios de la app y se detiene en cada parada; con la Ruta Sur grabada, «no se presenta» funciona y las horas aproximadas no cambian (C-28); el panel solo lo usa el administrador, corre una simulación a la vez y la puede detener |
| `frontend/src/api/cliente.test.js` (3 pruebas) | El cliente manda el token CSRF, entrega la causa del rechazo y marca la falta de señal como error de red |
| `frontend/src/paginas/Viajes.test.jsx` (2 pruebas de soporte) | Mientras el chofer viaja, mantiene la pantalla encendida y limita los envíos del GPS por tiempo y distancia |
| `frontend/src/registro/respaldo.test.js` (2 pruebas) | El respaldo no lleva datos de quien graba (C-25), deja fuera las marcas rechazadas y se nombra por ruta, horario y fecha |
| `frontend/src/registro/cola.test.js` (2 pruebas más) | Sin señal la cola conserva todo y lo envía en orden; lo que el servidor rechaza sale de la cola con su causa |
| `frontend/src/paginas/Demo.test.jsx` (2 pruebas) | El panel de demo manda el escenario, la ruta, la parada y la velocidad elegidos, y muestra la causa de un rechazo |

## 3. Criterios por hacer

Los 39 criterios restantes (HU07-CA6, que se escribe con T16, y HU-08 a HU-17) están en la [sesión 7](sesion-07-modelos.md), cada uno con el nombre de su test, y en el issue de su tarea. Cuando se terminan, sus filas pasan a la sección 1.

## 4. Participación y asistencia utilizada

- **Hugo Zuñiga:** dejó la base con estos tests.
- **Sebastian Cruz:** agregó la trazabilidad de HU-05 y HU-06 al implementar T11.
- **Hugo Zuñiga (26/11/2026):** agregó las pruebas de soporte del simulador (T23).
- **Asistencia de IA:** se usó Claude (Anthropic) para escribir los tests de la base y esta tabla; Sebastian usó OpenAI Codex para implementar y documentar HU-05 y HU-06 siguiendo la skill del repositorio.
- **Hugo Zuñiga (25/11/2026):** agregó la trazabilidad de HU-07 al implementar T14, con asistencia de Claude (Anthropic).
