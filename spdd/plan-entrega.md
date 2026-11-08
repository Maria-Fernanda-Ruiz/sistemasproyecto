# Plan para terminar y presentar el proyecto

Este plan convierte los requisitos de la guía en tareas verificables. El estado
se basa en lo comprobado hasta ahora; no se presentan como hechas la
interoperabilidad real ni las mediciones del experimento.

**Forma de trabajo:** Maria y Karen trabajan en igualdad como equipo. Las
tareas de la tabla son responsabilidades compartidas; si se nombra a una
coordinadora para una tarea, será solo para organizar el avance y no significa
que esa integrante haga más trabajo. El esquema concreto de coordinación está
pendiente de que ambas lo elijan.

## Tareas pendientes y en curso

| ID | Tarea | Resultado comprobable | Depende de | Estado | Equipo |
|---|---|---|---|---|---|
| T01 | Conseguir la especificación OpenAPI y el script oficial de conformidad. | Archivos oficiales guardados en el proyecto y fuente registrada. | Solicitar al curso o localizar los materiales. | Pendiente (P02) | Ambas |
| T02 | Comparar el contrato oficial con la federación implementada. | Lista de diferencias; canvas actualizado antes de cualquier cambio de comportamiento. | T01 | Pendiente | Ambas |
| T03 | Construir y levantar el proyecto con Docker. | `docker compose up --build` funciona y el chat responde en `localhost:8000`. | Docker Desktop disponible. | Pendiente | Ambas |
| T04 | Preparar la URL pública y la configuración del central. | Central puede alcanzar las rutas del servidor; configuración sin secretos en Git. | Instrucciones y URL del curso (P05). | Pendiente | Ambas |
| T05 | Ejecutar conformidad e interoperabilidad real. | Salida del script oficial y bitácora de mensajes entre grupos, incluyendo recuperación y duplicados observados. | T01, T02, T04 y otro grupo disponible | Pendiente | Ambas |
| T06 | Acordar cómo se hará el experimento y cómo se contará cada resultado. | Emisor, topología, inicio/fin de repetición y reglas de pérdida/duplicado definidos y confirmados por ambas. | Disponibilidad de servidor emisor (P03) y criterio de conteo (P04) | Pendiente | Ambas |
| T07 | Preparar y ejecutar el script del experimento. | Script, datos brutos y resultados de al menos tres repeticiones, con unidades. | T06; conservar los parámetros aprobados D10–D13 salvo que el equipo los cambie | Pendiente | Ambas |
| T08 | Crear tabla y gráfica a partir de los datos observados. | Tabla y gráfica reproducibles, sin resultados estimados presentados como reales. | T07 | Pendiente | Ambas |
| T09 | Preparar el borrador de contenido del póster y revisar la plantilla original. | Borrador claro que cubre los requisitos; deja marcadores para resultados aún no medidos. No reemplaza ni rediseña la plantilla. | Requisitos del póster; versión final depende de T05 y T08 | Pendiente | Ambas |
| T10 | Preparar el guion minuto a minuto y el plan de demostración. | Guion de hasta 10 minutos que indica qué se dice y qué se muestra; marca como pendiente toda demo no verificada. | Requisitos de la sustentación; versión final depende de T03, T05 y T08 | Pendiente | Ambas |
| T11 | Hacer revisión final de entregables y repositorio. | Lista de requisitos con evidencia o pendiente explícito; archivos finales publicados en una rama revisable. | T01–T10 | Pendiente | Ambas |

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
| P02 | ¿Cómo conseguiremos la especificación OpenAPI y el script oficial de conformidad? | La guía dice que la especificación completa prevalece sobre su resumen. | Opciones: (A) compartirlos aquí o pegar el enlace oficial —recomendado, así comparamos el contrato exacto—; (B) pedirlos al profesor/curso y, mientras llegan, avanzar con T03 (Docker); (C) seguir solo con el resumen del PDF, opción no recomendada porque deja la federación como provisional. |
| P03 | ¿Habrá un servidor de otro grupo para emitir mensajes durante la caída? | El método del experimento de la guía depende de otro servidor. | Pendiente |
| P04 | ¿Qué regla define mensaje perdido, recuperado o duplicado y cuándo termina cada repetición? | Sin una regla acordada, los resultados no son reproducibles. | Pendiente |
| P05 | ¿Qué instrucciones y URL pública oficial se usarán para que el central alcance `g1`? | Docker por sí solo no publica el servidor en Internet. | Pendiente |
| P07 | ¿Qué resultados reales dan las repeticiones? | Se necesitan observaciones para la tabla, gráfica, conclusiones y póster. | Pendiente hasta T07 |
| P09 | ¿Qué contenido final se confirma para el guion y el póster? | No se deben completar con datos o afirmaciones no verificados. | Pendiente |
| P11 | ¿Qué esquema equilibrado de coordinación prefieren Maria y Karen? | Organiza el avance sin suponer ni documentar diferencias de contribución. | Opciones: (A) trabajar juntas en cada tarea; (B) alternar quién coordina cada tarea, manteniendo ambas como responsables —recomendado para tener seguimiento claro sin sugerir cargas distintas—; (C) preparar borradores por turnos y revisarlos juntas. Pendiente de elegir. |

El permiso de colaboradora de Karen (Angélica) ya fue confirmado por la
estudiante; no hace falta volver a solicitarlo.

Las decisiones ya confirmadas del diseño y del experimento están en
[decision-log.md](decision-log.md). Una pregunta pendiente no se transforma en
decisión hasta que Maria y Karen la confirmen.

## Encargo para compartir con la IA de Karen (borrador)

> Estoy colaborando en igualdad con Maria en el proyecto de chat distribuido
> `g1`. Queremos organizar en equipo el borrador de contenido del póster y el
> guion minuto a minuto de la sustentación, según T09 y T10 de
> `spdd/plan-entrega.md`. Primero revisa el README, los requisitos, el análisis,
> el canvas REASONS y el log de decisiones.
> Revisa la plantilla original del póster; si no está disponible en el
> repositorio, pídemela antes de diseñar. Usa solo hechos comprobados. No
> inventes resultados, interoperabilidad ni funciones; coloca marcadores como
> `[resultado pendiente]` donde falten evidencias. Conserva el diseño de la
> plantilla y no edites código. Antes de editar o crear documentos, explícame
> qué archivos propones y espera mi aprobación. Para el guion, indica por
> minuto qué se dice y qué se muestra, con duración total máxima de 10 minutos.
> Deja los documentos como borradores para que Maria y Karen los revisen; no
> hagas commit ni push sin autorización.
