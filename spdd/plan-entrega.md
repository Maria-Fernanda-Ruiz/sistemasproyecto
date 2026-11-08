# Plan para terminar y presentar el proyecto

Este plan convierte los requisitos de la guía en tareas verificables. El estado
se basa en lo comprobado hasta ahora; no se presentan como hechas la
interoperabilidad real ni las mediciones del experimento.

**Responsables:** por acordar entre Maria Fernanda Ruiz Velasquez y Karen
Angelica Sandoval Martinez. No se asignan tareas hasta que ellas confirmen el
reparto.

## Tareas pendientes y en curso

| ID | Tarea | Resultado comprobable | Depende de | Estado | Responsable |
|---|---|---|---|---|---|
| T01 | Conseguir la especificación OpenAPI y el script oficial de conformidad. | Archivos oficiales guardados en el proyecto y fuente registrada. | Solicitar al curso o localizar los materiales. | Pendiente (P02) | Por acordar |
| T02 | Comparar el contrato oficial con la federación implementada. | Lista de diferencias; canvas actualizado antes de cualquier cambio de comportamiento. | T01 | Pendiente | Por acordar |
| T03 | Construir y levantar el proyecto con Docker. | `docker compose up --build` funciona y el chat responde en `localhost:8000`. | Docker Desktop disponible. | Pendiente | Por acordar |
| T04 | Preparar la URL pública y la configuración del central. | Central puede alcanzar las rutas del servidor; configuración sin secretos en Git. | Instrucciones y URL del curso (P05). | Pendiente | Por acordar |
| T05 | Ejecutar conformidad e interoperabilidad real. | Salida del script oficial y bitácora de mensajes entre grupos, incluyendo recuperación y ausencia de duplicados observados. | T01, T02, T04 y otro grupo disponible | Pendiente | Por acordar |
| T06 | Acordar cómo se hará el experimento y cómo se contará cada resultado. | Emisor, topología, inicio/fin de repetición y reglas de pérdida/duplicado definidos. | Disponibilidad de servidor emisor (P03) y criterio de conteo (P04) | Pendiente | Por acordar |
| T07 | Preparar y ejecutar el script del experimento. | Script, datos brutos y resultados de al menos tres repeticiones, con unidades. | T06; conservar los parámetros aprobados D10–D13 salvo que el equipo los cambie | Pendiente | Por acordar |
| T08 | Crear tabla y gráfica a partir de los datos observados. | Tabla y gráfica reproducibles, sin resultados estimados presentados como reales. | T07 | Pendiente | Por acordar |
| T09 | Completar el póster en la plantilla original. | Póster legible con pregunta, hipótesis, arquitectura, método, resultados, interoperabilidad, límites, conclusiones y referencias. | T05, T08 y confirmar contenido/referencias (P09) | Pendiente | Por acordar |
| T10 | Preparar el guion minuto a minuto y la demostración. | Guion de hasta 10 minutos que indica qué se dice y qué se muestra, con una demo ensayada. | T03, T05, T08 y P09 | Pendiente | Por acordar |
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
| P02 | ¿Dónde están la especificación OpenAPI y el script oficial de conformidad? | La guía dice que la especificación completa prevalece sobre su resumen. | Pendiente |
| P03 | ¿Habrá un servidor de otro grupo para emitir mensajes durante la caída? | El método del experimento de la guía depende de otro servidor. | Pendiente |
| P04 | ¿Qué regla define mensaje perdido, recuperado o duplicado y cuándo termina cada repetición? | Sin una regla acordada, los resultados no son reproducibles. | Pendiente |
| P05 | ¿Qué instrucciones y URL pública oficial se usarán para que el central alcance `g1`? | Docker por sí solo no publica el servidor en Internet. | Pendiente |
| P07 | ¿Qué resultados reales dan las repeticiones? | Se necesitan observaciones para la tabla, gráfica, conclusiones y póster. | Pendiente hasta T07 |
| P09 | ¿Qué contenido final se confirma para el guion y el póster? | No se deben completar con datos o afirmaciones no verificados. | Pendiente |
| P11 | ¿Qué tareas acepta Maria y cuáles acepta Karen? | La estudiante pidió dividir el trabajo, pero los responsables todavía no se han acordado. | Pendiente |

El permiso de colaboradora de Karen (Angélica) ya fue confirmado por la
estudiante; no hace falta volver a solicitarlo.

Las decisiones ya confirmadas del diseño y del experimento están en
[decision-log.md](decision-log.md). Una pregunta pendiente no se transforma en
decisión hasta que Maria y Karen la confirmen.
