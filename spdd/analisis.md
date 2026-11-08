# Análisis del proyecto

**Estado:** aprobado por la estudiante el 7 de noviembre de 2026.  
**Materiales revisados en modo de solo lectura:**

- `proyecto_final_v2 (1).pdf`: enunciado del proyecto de Sistemas Distribuidos.
- `Template SystemsFest(1) (3).pptx`: plantilla de póster.
- Referencia de lectura: `javierchacon262/agregador-resiliente` (no se modificó).

## 1. Comprensión del problema

El equipo construye su propio servidor de chat y un cliente web. El curso dispone de un servidor central. En el uso normal, el servidor de cada grupo registra su dirección en el central, envía los mensajes originados por sus usuarios y recibe mensajes que el central reenvía. El central guarda el historial global y distribuye cada mensaje a los servidores registrados, excepto al servidor de origen.

El frontend no se comunica directamente con el central. Habla con el servidor del grupo. En condiciones normales, el central entrega mensajes entrantes al servidor del grupo mediante `POST /fed/messages`; para recuperar mensajes después de una caída, el servidor del grupo consulta `GET /history?since=...`. El frontend mostrará mensajes consultando el servidor del grupo.

La guía describe una arquitectura en estrella y una sola sala global `#general`. El valor del proyecto está en la comunicación entre servidores y en manejar fallos; no es solo construir una interfaz de chat.

## 2. Hechos comprobados en la guía

- Hay un servidor central del curso y un servidor por grupo (págs. 1–2).
- Los mensajes pasan por el central; los servidores de grupo no se comunican directamente (pág. 2).
- Todos usan la sala global `#general`; no hay salas propias de cada grupo (pág. 2).
- El cliente puede ser una página web mínima. La API entre cliente y servidor del grupo es libre; la API entre servidores está definida por el curso (pág. 2).
- La guía enumera persistencia, registro, envío/recepción, reintentos, deduplicación, Lamport, detección de fallos, recuperación y logs como mínimo común (págs. 3–5).
- Se mencionan rutas HTTP y JSON, pero el resumen remite a una especificación OpenAPI completa que prevalece si hay diferencias (págs. 4–5).
- El experimento requiere al menos tres repeticiones, resultados con unidades, datos y script de medición (pág. 6).
- La guía permite usar cualquier lenguaje; recomienda Python con FastAPI, sin hacerlo obligatorio (pág. 9).

## 3. Materiales disponibles y límites de la revisión

### Guía PDF

Se revisó el texto de sus 10 páginas de contenido. Es la fuente para los requisitos enumerados en `requisitos.md`.
La guía pide citar el libro de texto en el póster (pág. 8). La estudiante compartió `Understanding Distributed Systems 2nd edition.pdf`; sus páginas preliminares identifican a Roberto Vitillo como autor, indican segunda edición y versión 2.0.0, fechada en marzo de 2022. Referencia bibliográfica provisional: Vitillo, R. (2022). *Understanding Distributed Systems: What Every Developer Should Know About Large Distributed Applications* (2.ª ed., versión 2.0.0). El formato final dependerá de las instrucciones del curso.

### Plantilla PowerPoint

La plantilla tiene una diapositiva y texto de ejemplo/indicaciones para secciones como título, autores, resumen, introducción, método, resultados, conclusiones, trabajo futuro y referencias. La guía de la actividad exige, además, pregunta e hipótesis, arquitectura, método con repeticiones, resultados con unidades, interoperabilidad y limitaciones.

Todavía no hay contenido del proyecto colocado en la plantilla, por lo que no se puede evaluar si un póster final está completo o legible. La plantilla no se modificó; su diseño, colores y elementos se deben conservar. Cualquier propuesta para editar contenido debe explicarse y aprobarse antes.

### Código y otros materiales

No se encontró código fuente, guion, resultados de experimento, bitácora ni una versión del póster con contenido entre los materiales disponibles en la carpeta de trabajo revisada. La guía OpenAPI y el script de conformidad tampoco se encontraron.

### Repositorio de referencia

`agregador-resiliente` se leyó solo como referencia de organización e interfaz. Ese proyecto agrega información de servicios externos; este proyecto es un chat distribuido que debe cumplir el protocolo del curso. Sus decisiones, código y contenido no se trasladarán al proyecto nuevo.

## 4. Decisiones confirmadas por el equipo

- Nombre técnico propuesto para el nuevo repositorio: `proyecto-sistemas-distribuidos`; nombre visible: “Proyecto de sistemas distribuidos”.
- Descripción: “Proyecto académico de sistemas distribuidos: requisitos, análisis, póster y código, organizados con metodología SPDD”.
- Visibilidad escogida: privada.
- La estudiante quiere crear/gestionar el repositorio y sus ramas, merges y publicación desde Visual Studio Code. No se ha creado un repositorio remoto.
- Equipo de dos integrantes: la estudiante y Angélica; ambas trabajan en código.
- Código corto elegido y confirmado para el servidor: `g1`.
- Experimento: tema de pérdidas/duplicados; se usa como pregunta de borrador la pregunta de la guía (pág. 5).
- Hipótesis esperada: después de una caída temporal, `g1` recupera los mensajes enviados durante la interrupción y cada mensaje aparece una sola vez.
- Diseño del experimento: caída de 5 segundos, 1 mensaje por segundo, mínimo 3 repeticiones; resultados en tabla y gráfica.
- Cliente: una página web sencilla de chat en HTML/CSS/JavaScript, con estilo colorido tipo lobby de juego elegido por el equipo. El alcance actual se limita al cliente de chat solicitado/permitido por la guía; no se incluyen vistas adicionales de tablero de Estado/Logs o Experimento.
- En el chat se muestra nombre y grupo junto a cada mensaje; no se muestra lista de participantes.
- Los usuarios de demo eligen un nombre sin contraseña.
- El frontend consulta el servidor del grupo con `GET` cada 2 segundos.
- Persistencia con SQLite en volumen Docker.
- Backend con Python y FastAPI.
- Las decisiones anteriores no modifican requisitos impuestos por la guía; son elecciones del equipo.
- No había código previo; la etapa local inicial partió desde cero. Ambas integrantes trabajarán juntas en las etapas de programación.

## 5. Suposiciones que no se deben tratar como hechos

- Que el formato de nombre de grupo se puede cambiar: el equipo confirmó que puede usar `g1`.
- Que las rutas, cuerpos JSON, códigos de estado o mecanismos de reintento descritos en el resumen son idénticos a la especificación completa.
- Que el central y los demás grupos estarán disponibles para pruebas en cualquier momento.
- Que se puede detener solo el servidor `g1` mientras otra instancia envía mensajes al central; la topología y el generador de carga deben concretarse. Aún no se sabe si otro equipo prestará un servidor.
- Que un `GET` local cada 2 segundos es suficiente para la experiencia visual deseada; es una decisión de diseño, no una exigencia de la guía.
- Que los nombres de usuario sin contraseña cumplen las necesidades de demostración; la guía exige usuarios locales, pero no define autenticación.
- Que el modo de despliegue local permitirá al central alcanzar la URL del servidor del grupo. La guía pide configurar una URL pública, así que el acceso desde fuera del equipo debe verificarse.
- El curso usa Cloudflare, pero no se han compartido la URL ni las instrucciones específicas para publicar o exponer el servidor. Docker ejecuta el servicio en contenedores; no se asumirá que por sí solo lo vuelve accesible desde el central.

## 6. Riesgos y dependencias

1. **Interoperabilidad:** el PDF dice que el contrato OpenAPI completo prevalece sobre su resumen. Implementar los detalles sin ese archivo puede causar incompatibilidad.
2. **Acceso de red:** el central necesita llegar al servidor del grupo; Docker Compose por sí solo no garantiza que una URL local sea accesible desde el central. El curso usa Cloudflare, pero falta confirmar el mecanismo e instrucciones concretas.
3. **Experimento:** medir pérdidas y duplicados requiere identificar todos los mensajes enviados y recibidos y definir con precisión cuándo termina la recuperación.
4. **Entrega:** quedan por obtener el script de conformidad, la especificación completa y los datos reales del experimento. Tampoco se sabe aún si habrá un servidor de otro equipo disponible para el experimento.
5. **Póster:** la plantilla contiene indicaciones de redacción científica, pero no se debe reemplazar ni rediseñar. El contenido debe adaptarse conservando el diseño original.
6. **Interoperabilidad responsable:** una prueba local o simulada no debe reportarse como prueba con los servidores de otros grupos.

## 7. Próximos pasos SPDD

1. **Completado:** revisar los requisitos, el análisis y el canvas REASONS; ambos documentos de diseño quedaron aprobados.
2. **Completado:** implementar el servidor local y el cliente web sencillo, con pruebas de usuarios, mensajes, reloj local y persistencia.
3. Continuar por etapas conforme a Operations; presentar la propuesta concreta antes de cada nuevo cambio de código.
4. Validar la conexión central con las rutas resumidas en la guía y cualquier especificación oficial disponible, sin afirmar interoperabilidad no probada.
5. Ejecutar las verificaciones del curso cuando estén disponibles y registrar resultados reales, sin presentar pruebas no realizadas.
