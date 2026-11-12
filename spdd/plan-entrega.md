# Plan para terminar y presentar el proyecto

Este plan convierte los requisitos de la guía en tareas verificables. El estado
se basa en lo comprobado hasta ahora; no se presentan como hechas la
interoperabilidad real ni las mediciones del experimento.

**Forma de trabajo:** el proyecto se realiza en equipo. Las tareas y los
aportes son compartidos; este plan no asigna tareas, méritos ni cargas por
persona ni propone áreas individuales. La coordinación se acuerda en equipo.

## Tareas pendientes y en curso

| ID | Tarea | Resultado comprobable | Depende de | Estado | Equipo |
|---|---|---|---|---|---|
| T01 | Conseguir la especificación OpenAPI y el script oficial de conformidad. | Archivos oficiales guardados en el proyecto y fuente registrada. | Solicitar al curso o localizar los materiales. | Pendiente (P02) | Equipo |
| T02 | Comparar el contrato oficial con la federación implementada. | Lista de diferencias; canvas actualizado antes de cualquier cambio de comportamiento. | T01 | Pendiente | Equipo |
| T03 | Construir y levantar el proyecto con Docker. | `docker compose up --build` construyó la imagen; `GET /` respondió HTTP 200 y `/fed/health` devolvió `{"server":"g1","lamport":0}` en modo local. | Docker Desktop disponible. | Completada; central no configurado | Equipo |
| T04 | Preparar la URL pública y la configuración del central. | Central puede alcanzar las rutas del servidor; configuración sin secretos en Git. | Instrucciones y URL del curso (P05). | Pendiente | Equipo |
| T05 | Ejecutar conformidad e interoperabilidad real. | Salida del script oficial y bitácora de mensajes entre grupos, incluyendo recuperación y duplicados observados. | T01, T02, T04 y otro grupo disponible | Pendiente | Equipo |
| T06 | Acordar cómo se hará el experimento y cómo se contará cada resultado. | Borrador de método y conteo preparado; falta confirmación del equipo y conseguir un servidor emisor. | Disponibilidad de servidor emisor (P03) y aprobación del criterio propuesto (P04) | Borrador preparado; no aprobado | Equipo |
| T07 | Preparar y ejecutar el script del experimento. | Script, datos brutos y resultados de al menos tres repeticiones, con unidades. | T06; conservar los parámetros aprobados D10–D13 salvo que el equipo los cambie | Pendiente | Equipo |
| T08 | Crear tabla y gráfica a partir de los datos observados. | Tabla y gráfica reproducibles, sin resultados estimados presentados como reales. | T07 | Pendiente | Equipo |
| T09 | Preparar el borrador de contenido del póster y revisar la plantilla original. | Borrador claro que cubre los requisitos; deja marcadores para resultados aún no medidos. No reemplaza ni rediseña la plantilla. | Requisitos del póster; versión final depende de T05 y T08 | Pendiente | Equipo |
| T10 | Preparar el guion minuto a minuto y el plan de demostración. | Guion de hasta 10 minutos que indica qué se dice y qué se muestra; marca como pendiente toda demo no verificada. | Requisitos de la sustentación; versión final depende de T03, T05 y T08 | Pendiente | Equipo |
| T11 | Hacer revisión final de entregables y repositorio. | Lista de requisitos con evidencia o pendiente explícito; archivos finales publicados en una rama revisable. | T01–T10 | Pendiente | Equipo |

## Borrador del experimento (pendiente de confirmación)

La guía propone enviar mensajes desde otro servidor mientras `g1` está caído
(pág. 5). Por ahora no hay otro grupo disponible para prestar ese servidor.
Por tanto, este es solo un plan: todavía no se puede ejecutar ni presentar
resultados.

1. El servidor emisor conserva la lista de IDs de los mensajes enviados.
2. Se envía 1 mensaje por segundo y se detiene `g1` durante 5 segundos.
3. Se vuelve a iniciar `g1` y se espera el log que indica que terminó la
   recuperación del historial.
4. Se propone contar como **perdido** cada ID enviado durante la caída que no
   aparece en el historial de `g1` tras la recuperación.
5. Se propone contar como **duplicado** cada log «Mensaje duplicado reconocido»
   de `g1` durante esa repetición. El chat puede mostrar un solo mensaje porque
   el servidor deduplica los IDs.
6. Se guardan los IDs enviados, el historial final y los logs de cada
   repetición; se repite al menos 3 veces y se reportan resultados reales en
   tabla y gráfica.

Los pasos y las reglas de conteo son una propuesta para revisar en equipo; no
están aprobados todavía. No se modificarán ni crearán scripts de medición
hasta conseguir un emisor y confirmar el método.

## Ya completado (no repetir sin necesidad)

- Requisitos iniciales extraídos de la guía y análisis SPDD aprobados.
- Canvas REASONS aprobado antes de escribir el código de la aplicación.
- Chat local con FastAPI, cliente web y persistencia SQLite.
- Federación provisional y 13 pruebas automatizadas aprobadas con central
  simulado. Esto no demuestra interoperabilidad con el central del curso.
- README, diagrama de arquitectura y estructura de documentos SPDD.
- Rama pública `compartir/proyecto-inicial` en GitHub.

## Decisiones necesarias para cerrar el plan

| ID | Decisión o dato | Por qué hace falta | Estado |
|---|---|---|---|
| P02 | ¿Cómo conseguiremos la especificación OpenAPI y el script oficial de conformidad? | La guía dice que la especificación completa prevalece sobre su resumen. | Opciones: (A) pedirlos al profesor/curso —recomendado, para contrastar el contrato antes de afirmar interoperabilidad—; (B) mientras llegan, avanzar con el diseño del experimento y consultar si habrá un servidor emisor; (C) seguir solo con el resumen del PDF, opción no recomendada porque deja la federación como provisional. |
| P03 | ¿Habrá un servidor de otro grupo para emitir mensajes durante la caída? | El método del experimento de la guía depende de otro servidor. | No hay uno disponible por ahora; consultar más adelante |
| P04 | ¿Qué regla define mensaje perdido, recuperado o duplicado y cuándo termina cada repetición? | Sin una regla acordada, los resultados no son reproducibles. | Propuesta en el borrador anterior; falta confirmación del equipo |
| P05 | ¿Qué instrucciones y URL pública oficial se usarán para que el central alcance `g1`? | Docker por sí solo no publica el servidor en Internet. | Pendiente |
| P07 | ¿Qué resultados reales dan las repeticiones? | Se necesitan observaciones para la tabla, gráfica, conclusiones y póster. | Pendiente hasta T07 |
| P09 | ¿Qué contenido final se confirma para el guion y el póster? | No se deben completar con datos o afirmaciones no verificados. | Pendiente |
| P11 | ¿Se asignarán áreas individuales o se trabajará conjuntamente? | Evita dar a entender que los aportes o las cargas de trabajo son distintos. | Resuelta: trabajo conjunto, sin áreas asignadas individualmente (`D37`). |

Las decisiones de diseño y preguntas pendientes están en
[decision-log.md](decision-log.md). Las decisiones nuevas deben confirmarse en
equipo antes de registrarse como definitivas.

## Instrucciones para continuar el trabajo

Quien continúe el proyecto debe revisar el README, los requisitos, el análisis,
el canvas REASONS y el log de decisiones. Usar solo hechos comprobados; no
inventar resultados, interoperabilidad ni funciones. Mantener las tareas,
aportes y méritos como trabajo del equipo, sin atribuirlos ni compararlos por
persona. Antes de modificar archivos, explicar los cambios propuestos y
esperar aprobación. Dejar los documentos como borradores para revisión en
equipo y no hacer commit o push sin autorización.
