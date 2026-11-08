# Log de decisiones y preguntas

**Estado:** borrador vivo.  
Las decisiones confirmadas registran elecciones del equipo; las decisiones propuestas no se consideran aprobadas hasta que la estudiante las confirme. Las preguntas pendientes se identifican con `P`.

## Decisiones

| ID | Tema | Decisión / propuesta | Estado | Motivo y fuente |
|---|---|---|---|---|
| D01 | Nombre visible del proyecto | “Proyecto de sistemas distribuidos”. | Confirmada | Elección de la estudiante. |
| D02 | Nombre técnico del repositorio/carpeta | `proyecto-sistemas-distribuidos`. | Confirmada | El nombre técnico no usa espacios; el título visible conserva los espacios. |
| D03 | Descripción | “Proyecto académico de sistemas distribuidos: requisitos, análisis, póster y código, organizados con metodología SPDD”. | Confirmada | Texto elegido por la estudiante. |
| D04 | Visibilidad | Inicialmente privada; cambiada a pública el 8 de noviembre de 2026 para compartir el proyecto con Karen. | Reemplazada | La estudiante autorizó hacer público el repositorio. |
| D05 | Control y publicación de GitHub | La estudiante conserva el control del repositorio. Por petición expresa, la versión inicial se publicó en `compartir/proyecto-inicial` de `Maria-Fernanda-Ruiz/sistemasproyecto`; no se hizo push directo a `main`. La estudiante confirma que Karen (Angélica) ya es colaboradora. | Confirmada | Instrucciones de la estudiante y autorización de publicación; el acceso de Karen lo confirmó la estudiante el 8 de noviembre de 2026. |
| D06 | Integrantes | Maria Fernanda Ruiz Velasquez y Karen Angelica Sandoval Martinez. | Confirmada | La estudiante indicó los nombres completos. |
| D07 | Identificador de grupo | `g1`. | Confirmada; disponibilidad confirmada por la estudiante | La guía usa identificadores cortos como `g1` (pág. 2); el curso/equipo confirmó que este valor está disponible. |
| D08 | Pregunta experimental | Usar la pregunta de la guía: «¿Cuántos mensajes se pierden o se duplican cuando el servidor del grupo se cae durante unos segundos?» | Confirmada | Se elige una de las preguntas propuestas en la guía (pág. 5); conecta el experimento con tolerancia a fallos. |
| D09 | Hipótesis | Se espera que tras una caída temporal `g1` recupere los mensajes enviados durante la interrupción y cada mensaje aparezca una sola vez. | Confirmada como expectativa, no como resultado | Responde a “lo que el grupo espera observar” (pág. 6) y al campo hipótesis del póster (pág. 8). |
| D10 | Duración de caída | 5 segundos por repetición. | Confirmada como elección del equipo | La guía dice “unos segundos”, sin fijar duración (pág. 5). Es fácil de repetir; ajustar si el piloto no permite observar la recuperación. |
| D11 | Tasa de envío | 1 mensaje por segundo. | Confirmada como elección del equipo | La guía requiere tasa fija, sin fijar una cifra (pág. 6). A 5 segundos se esperan aproximadamente cinco mensajes durante cada caída. |
| D12 | Repeticiones | Al menos 3. | Obligatoria por la guía | Pág. 6. |
| D13 | Presentación del experimento | Tabla y gráfica, con resultados por repetición. | Confirmada | La guía acepta una tabla o una gráfica con unidades (pág. 6); el equipo eligió ambas. |
| D14 | Servidor/API | Python con FastAPI. | Confirmada; no es imposición de la guía | La guía permite cualquier lenguaje y recomienda FastAPI (pág. 9); elección del equipo. |
| D15 | Frontend | HTML, CSS y JavaScript. | Confirmada; la tecnología queda a criterio del equipo | La guía permite un cliente web (pág. 2); elección del equipo. |
| D16 | Estilo visual | Colorido, como un lobby de juego, inspirado de forma general en Roblox sin copiar su marca o recursos. | Confirmada como dirección visual | Preferencia de la estudiante. |
| D17 | Pantalla inicial y navegación | Chat al abrir; se habían propuesto vistas separadas para Estado/Logs y Experimento. | Reemplazada por D26 | La estudiante aclaró que quiere limitar el cliente a lo que pide el PDF. |
| D18 | Participantes | Sin lista lateral; mostrar nombre y grupo junto a cada mensaje. | Confirmada | La estudiante indicó que no quería la lista. La guía exige distinguir usuarios de otros grupos (pág. 4). |
| D19 | Nombre de usuario | Elegir nombre para la demo, sin contraseña. | Confirmada como decisión de interfaz | La guía pide usuarios locales, pero no define autenticación (pág. 3). |
| D20 | Actualización del chat | El frontend consulta el servidor del grupo con `GET` cada 2 segundos. | Confirmada como diseño, no como requisito del curso | Elección entre consulta periódica y WebSocket; se eligió la alternativa sencilla. |
| D21 | Persistencia | SQLite en un volumen Docker. | Confirmada | SQLite es una alternativa permitida por la guía (pág. 3); elección del equipo. |
| D22 | Materiales y límites | No se modifican las guías ni la plantilla sin aprobación previa; no se escribe código de aplicación hasta aprobar análisis y canvas. | Confirmada | Instrucciones de trabajo de la estudiante y flujo SPDD acordado. |
| D23 | Repositorio de referencia | Leer `gszhangwei/open-spdd` como referencia metodológica; no modificarlo ni copiar su proyecto de ejemplo o sus decisiones. | Confirmada | Instrucción expresa de la estudiante. |
| D24 | Documentos SPDD iniciales | Crear requisitos, análisis, canvas REASONS y este log dentro de la carpeta del proyecto. | Confirmada | La estudiante autorizó crear estos cuatro documentos iniciales. |
| D25 | Protocolo completo del central | Avanzar con el resumen de la guía y señalar lo que falta validar; no afirmar interoperabilidad comprobada sin evidencia. | Confirmada | La estudiante pidió avanzar para la entrega próxima. |
| D26 | Alcance del cliente | Limitar el frontend a un cliente web sencillo para enviar y leer mensajes de `#general`; no crear vistas adicionales de tablero. | Confirmada; reemplaza D17 | La estudiante pidió seguir el alcance del PDF (pág. 2), que admite una página web mínima. |
| D27 | Forma de trabajo del equipo | Inicialmente se propuso que ambas trabajaran juntas sin áreas separadas. | Reemplazada por D37 | La estudiante después pidió dividir las tareas pendientes. |
| D28 | Código de partida | No hay código existente; se comienza desde cero, tomando la guía como fuente de requisitos. | Confirmada | La estudiante indicó que solo dispone del PDF y los materiales compartidos. |
| D29 | Servidor emisor del experimento | Aún no se sabe si otro equipo podrá prestar su servidor para generar mensajes mientras `g1` está detenido. | Pendiente | La guía describe el envío desde otro servidor durante la caída (pág. 5); no se inventará una alternativa como si fuera el método del curso. |
| D30 | Aprobación del canvas REASONS | El equipo aprueba el canvas actual como diseño para preparar la implementación. | Confirmada el 7 de noviembre de 2026 | Aprobación expresa de la estudiante. |
| D31 | Aprobación del análisis | El equipo aprueba el análisis actualizado, con los requisitos atribuidos al PDF y sin afirmar comunicaciones directas que no ocurrieron. | Confirmada el 7 de noviembre de 2026 | Aprobación expresa de la estudiante. |
| D32 | Primera etapa local | Implementar el chat local: usuarios, mensajes, SQLite persistente y cliente web sencillo con rutas locales separadas del protocolo central. | Implementada | La estudiante aprobó la propuesta concreta de archivos y rutas antes de los cambios. |
| D33 | Federación provisional | Implementar registro, heartbeat, envío y recepción, Lamport, deduplicación, reintentos y recuperación de historial con los campos y rutas resumidos en el PDF. La respuesta de historial se trata como lista JSON directa provisional. | Implementada; requiere validación externa | La estudiante aprobó avanzar según el PDF y eligió el supuesto de respuesta directa para `GET /history`. No se afirma interoperabilidad real. |
| D34 | Entrega de documentación técnica | Añadir README de ejecución y variables de entorno y un diagrama de arquitectura; marcar en ellos las validaciones todavía pendientes. | Borradores creados | Son entregables indicados por la guía (págs. 7–8); no incluyen resultados experimentales ni de interoperabilidad no obtenidos. |
| D35 | Organización SPDD | Organizar los documentos como requisitos, análisis, prompt/canvas por historia, plantilla REASONS e índice con enlaces, siguiendo la forma documental observada en `agregador-resiliente`; no trasladar su contenido ni sus decisiones. | Confirmada el 8 de noviembre de 2026 | La estudiante autorizó adaptar la organización después de revisar ese repositorio en modo solo lectura. |
| D36 | Plan de entrega | Enumerar tareas restantes, resultados verificables, dependencias y decisiones pendientes en un plan enlazado desde el índice SPDD. La versión inicial dejó responsables sin asignar. | Confirmada el 8 de noviembre de 2026; estado de asignación reemplazado por D37 | La estudiante pidió organizar primero el trabajo y luego distribuir las tareas. |
| D37 | Reparto inicial de tareas pendientes | Maria se encarga de OpenAPI, federación, Docker, URL pública, conformidad, interoperabilidad y experimento; Karen prepara el borrador del póster y el guion. Ambas acuerdan método experimental y revisión final. | Indicado por Maria el 8 de noviembre de 2026; pendiente de confirmación de Karen | Maria pidió quedarse con la mayoría y dejar a Karen encargos claros para trabajar con su IA. |

## Preguntas pendientes

| ID | Pregunta | Por qué importa | Estado |
|---|---|---|---|
| P01 | ¿Cómo se confirma que `g1` no está asignado a otro grupo y puede usarse? | El identificador debe distinguir al servidor del grupo. | Resuelta: la estudiante confirmó disponibilidad |
| P02 | ¿Dónde están la especificación OpenAPI completa y el script de conformidad? | La guía indica que la especificación completa prevalece sobre el resumen (pág. 4). | No disponibles entre los archivos revisados |
| P03 | ¿Podrá otro equipo prestar un servidor para enviar mensajes mientras `g1` está detenido? | La guía describe este método de experimento (pág. 5). | Pendiente; la estudiante aún no lo sabe |
| P04 | ¿Qué regla exacta usaremos para contar un mensaje como perdido, recuperado o duplicado y cuándo termina cada repetición? | Hace que el experimento sea medible y repetible. | Pendiente |
| P05 | ¿Qué mecanismo/instrucciones de Cloudflare harán alcanzable desde el central la URL de `g1`? | La guía pide configurar una URL pública para el servidor del grupo (pág. 3); Docker ejecuta los contenedores, pero no establece por sí solo el acceso público. | Pendiente; se confirmó que el curso usa Cloudflare, pero no se tienen URL ni instrucciones concretas |
| P06 | ¿Cuál es el libro de texto del curso que debe citarse en el póster? | El póster debe incluir el libro de texto (pág. 8). | Resuelta: la estudiante compartió el PDF *Understanding Distributed Systems*, 2.ª edición, de Roberto Vitillo. Referencia provisional: Vitillo, R. (2022). *Understanding Distributed Systems: What Every Developer Should Know About Large Distributed Applications* (2.ª ed., versión 2.0.0). |
| P07 | ¿Qué resultados reales producirán las tres o más repeticiones? | No pueden completarse antes de ejecutar el experimento. | Pendiente |
| P08 | ¿Qué decisiones exactas de API local y estructura de carpetas se aprueban? | Se definirán antes de implementar cada etapa. | Resuelta: API local y estructura aprobadas antes de su implementación |
| P09 | ¿Qué contenido concreto irá en el guion de sustentación y en la plantilla del póster? | No se han compartido un guion ni resultados; cualquier edición debe aprobarse antes. | Pendiente |
| P11 | ¿Karen confirma el reparto indicado por Maria? | Permite asegurar que las tareas asignadas y sus dependencias son claras para ambas integrantes. | Pendiente de compartir con Karen |

## Registro de cambios

- Se crea este log como registro vivo de decisiones y preguntas; cada aprobación o cambio se fecha para distinguir el estado actual del histórico.
- Se limita el cliente a una página sencilla de chat conforme al alcance elegido por la estudiante; la propuesta anterior de tablero queda reemplazada.
- El canvas REASONS queda aprobado.
- El análisis queda aprobado el 7 de noviembre de 2026.
- Se implementan chat local y federación provisional. Las 13 pruebas automatizadas pasan; la configuración de Compose valida, pero el build no se ejecutó porque Docker no está activo.
- README y diagrama de arquitectura disponibles. Pruebas con central simulado no equivalen a interoperabilidad con el central del curso.
- El repositorio es público y la rama `compartir/proyecto-inicial` contiene la versión inicial. La estudiante confirma que Karen (Angélica) ya es colaboradora.
- El README contiene los nombres completos de Maria Fernanda Ruiz Velasquez y Karen Angelica Sandoval Martinez.
- Se creó `plan-entrega.md` con tareas pendientes, evidencias, dependencias y responsables propuestos por Maria; el reparto queda pendiente de confirmación de Karen.
