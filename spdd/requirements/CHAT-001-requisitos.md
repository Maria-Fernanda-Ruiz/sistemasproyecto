# Requisitos del proyecto

**Estado:** borrador para revisión de la estudiante y su equipo.  
**Fuente principal:** `proyecto_final_v2 (1).pdf` (páginas numeradas del 1 al 10).

Este documento resume lo que pide la guía con palabras sencillas. Los requisitos del curso se distinguen de las decisiones de diseño que el equipo puede escoger.

## Requisitos obligatorios de la guía

| ID | Requisito | Fuente |
|---|---|---|
| R01 | El proyecto consiste en un chat distribuido: el servidor del grupo se comunica con el servidor central del curso. El central reenvía mensajes entre los servidores registrados. | Págs. 1–2 |
| R02 | La sala compartida del curso es `#general`. La guía no contempla salas privadas o salas independientes por grupo. | Pág. 2 |
| R03 | El grupo entrega un cliente sencillo para enviar y leer mensajes; puede ser una línea de comandos o una página web mínima. La API entre cliente y servidor del grupo es libre, pero la API entre servidores no. | Pág. 2 |
| R04 | El sistema completo debe levantarse con `docker compose up` en un equipo limpio. La configuración, incluido el nombre del grupo y las URL necesarias, debe pasarse mediante variables de entorno. | Pág. 3 |
| R05 | Los usuarios y el historial deben persistir después de reiniciar el sistema. La guía permite SQLite en un volumen, Redis con persistencia o PostgreSQL. | Pág. 3 |
| R06 | Se deben poder crear usuarios locales del grupo y permitirles enviar y leer mensajes de `#general`. | Pág. 3 |
| R07 | Al arrancar, el servidor del grupo se registra en el central y renueva su registro periódicamente. La URL del central se configura; no debe quedar escrita directamente en el código. | Pág. 3 |
| R08 | El servidor del grupo envía mensajes de sus usuarios al central y recibe mensajes reenviados por el central conforme al protocolo del curso. | Págs. 3–5 |
| R09 | La entrega es al menos una vez: ante fallas de red o respuestas 5xx se reintenta con espera exponencial. Los mensajes repetidos se deduplican por su `id`; las respuestas 4xx no se reintentan y se registran. | Págs. 3 y 5 |
| R10 | Los mensajes llevan reloj de Lamport. Al enviar se incrementa el reloj; al recibir se actualiza con `max(local, recibido) + 1`. El historial se presenta ordenado por `(lamport, origin)`, no por la hora física. | Págs. 3 y 5 |
| R11 | El servidor consulta la salud del central. Si no responde después del número configurable de intentos, lo marca como caído, conserva mensajes pendientes y los envía cuando vuelve. | Pág. 3 |
| R12 | Al arrancar o recuperarse de una caída, el servidor solicita al central el historial posterior a su marca de Lamport mediante `GET /history?since={lamport}`. | Pág. 4 |
| R13 | El cliente debe distinguir visualmente a usuarios de otros grupos. La guía ejemplifica usuarios como `ana@g3`. | Págs. 4–5 |
| R14 | Debe haber logs legibles de mensajes enviados, recibidos, reintentados y descartados. La guía recomienda que cada registro incluya el ID y la marca de Lamport. | Págs. 4 y 10 |
| R15 | El experimento debe elegir una pregunta de la guía, expresar qué espera observar, realizar al menos 3 repeticiones, reportar el resultado de cada una y presentar tabla o gráfica con unidades. El script de medición y los datos también se entregan. | Págs. 5–6 |
| R16 | En la interoperabilidad se prueba que los grupos conversen en `#general` y que un servidor que cae recupere los mensajes sin duplicarlos. Se lleva una bitácora de lo que funcionó y falló. | Pág. 7 |
| R17 | El repositorio debe incluir código del servidor y cliente, `docker-compose.yml`, README con instrucciones y variables de entorno, diagrama de arquitectura, script y datos del experimento, salida de conformidad, bitácora de interoperabilidad e historial de commits. | Págs. 7–8 |
| R18 | El póster vertical debe incluir título, integrantes y grupo; pregunta e hipótesis; arquitectura; método y repeticiones; resultados con unidades; interoperabilidad; limitaciones y conclusiones; referencias, incluido el libro de texto. Debe ser breve y legible. | Pág. 8 |
| R19 | La sustentación dura como máximo 10 minutos e incluye presentación del póster y una demostración; idealmente se provoca un fallo y se muestra la recuperación. | Pág. 8 |
| R20 | Se permite cualquier lenguaje o framework si funciona en contenedores y cumple la especificación. Python con FastAPI se recomienda en la guía, pero no es obligatorio. Cada integrante debe poder explicar el código entregado. | Pág. 9 |
| R21 | No se debe compartir código entre grupos. | Pág. 9 |

### Interfaces HTTP que resume la guía

La guía presenta estas rutas del servidor central, llamadas por cada servidor de grupo:

| Método y ruta | Uso indicado en la guía |
|---|---|
| `POST /register` | Registrar o renovar un servidor. |
| `POST /messages` | Entregar un mensaje de un usuario a la sala global. |
| `GET /history?since={lamport}` | Recuperar mensajes posteriores a una marca de Lamport. |
| `GET /health` | Consultar la salud del central. |

Y estas rutas que cada servidor de grupo ofrece al central:

| Método y ruta | Uso indicado en la guía |
|---|---|
| `GET /fed/health` | Informar nombre del servidor y reloj de Lamport actual. |
| `POST /fed/messages` | Recibir un mensaje reenviado por el central. |

La guía dice que hay una especificación OpenAPI completa y que, si difiere del resumen, prevalece la especificación. Ese archivo no está entre los materiales revisados; los detalles no incluidos aquí no se deben inventar.

## Decisiones de diseño del equipo

Estas decisiones no son requisitos impuestos por la guía:

- Servidor/API en Python con FastAPI.
- Cliente web sencillo en HTML, CSS y JavaScript para enviar y leer mensajes de `#general`, como permite la guía. Se conservará el estilo colorido tipo lobby de juego elegido por el equipo, sin copiar marcas ni recursos. No se incluyen pantallas adicionales de tablero en el alcance actual.
- SQLite para usuarios e historial, guardado en un volumen Docker.
- El frontend consulta el servidor del grupo con `GET` cada 2 segundos.
- Usuarios de la demo eligen un nombre, sin contraseña.
- No habrá lista lateral de participantes; cada mensaje mostrará nombre y grupo.
- La página se limitará al cliente sencillo del chat; no se incluirán vistas adicionales de Estado/Logs o Experimento.
- Los resultados del experimento se mostrarán en tabla y gráfica.
- El identificador de grupo elegido y confirmado es `g1`.

## Referencia bibliográfica del libro de texto

El libro compartido por la estudiante confirma el título, autor, segunda edición y versión 2.0.0 fechada en marzo de 2022. Datos bibliográficos verificados en las páginas preliminares del PDF:

> Vitillo, R. (2022). *Understanding Distributed Systems: What Every Developer Should Know About Large Distributed Applications* (2.ª ed., versión 2.0.0).

La guía pide incluir el libro de texto en las referencias del póster (pág. 8). El formato final de citación debe ajustarse a las instrucciones del curso, si se proporcionan.

## Experimento elegido

- **Pregunta de la guía:** «¿Cuántos mensajes se pierden o se duplican cuando el servidor del grupo se cae durante unos segundos?» (pág. 5).
- **Hipótesis del equipo:** se espera que, tras una caída temporal, `g1` recupere los mensajes enviados durante la interrupción y cada mensaje aparezca una sola vez. Es una expectativa que se probará, no un resultado.
- **Propuesta de método:** detener `g1` durante 5 segundos mientras se envía 1 mensaje por segundo; repetir al menos 3 veces. Mostrar mensajes enviados, perdidos y duplicados por repetición en tabla y gráfica.
- Los 5 segundos y 1 mensaje por segundo son decisiones del equipo, no valores fijados por la guía.
- La disponibilidad de un servidor de otro equipo para enviar mensajes durante la caída todavía se desconoce. La topología exacta y la forma de verificar el conteo quedan pendientes de validar con el protocolo y el entorno de pruebas disponibles.

## Entrega y trabajo del equipo

Integrantes registradas al inicio del proyecto: Maria Fernanda Ruiz Velasquez y Karen Angelica Sandoval Martinez. El equipo trabaja de forma conjunta: las tareas y los aportes son compartidos y no se atribuyen ni comparan por persona. Los nombres de las personas incorporadas después se agregarán cuando el equipo los comparta. No había código previo al inicio de la implementación; el código actual se encuentra en la carpeta `app/`.

El repositorio `Maria-Fernanda-Ruiz/sistemasproyecto` es público. La versión inicial está publicada en la rama `compartir/proyecto-inicial`.

## Estado de implementación

El chat local y una integración federada provisional están implementados. Las pruebas automatizadas usan un central simulado; la conexión con el servidor central real, la conformidad con OpenAPI y la interoperabilidad todavía no están verificadas.
