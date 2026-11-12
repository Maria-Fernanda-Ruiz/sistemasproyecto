# Documentos SPDD

Este directorio organiza el trabajo por trazabilidad: requisitos → análisis →
canvas REASONS → implementación por operaciones → pruebas y evidencias.
El repositorio de referencia se consultó solo para inspirar esta organización;
el contenido y las decisiones pertenecen a este proyecto.

## Documentos

| Documento | Para qué sirve | Estado |
|---|---|---|
| [Requisitos CHAT-001](requirements/CHAT-001-requisitos.md) | Requisitos del PDF, sus fuentes y decisiones del equipo, separados de las suposiciones. | Borrador para revisión |
| [Análisis CHAT-001](analysis/CHAT-001-analysis.md) | Hechos revisados, materiales, decisiones, riesgos y pendientes. | Aprobado; actualizar cuando aparezca nueva evidencia |
| [Canvas REASONS CHAT-001](prompt/CHAT-001-chat-distribuido.md) | Entidades, enfoque, estructura, operaciones, normas y salvaguardas del chat. | Aprobado; implementación local y federación provisional realizadas |
| [Plantilla REASONS](template/REASONS-canvas.md) | Estructura vacía para canvases futuros. | Referencia |
| [Log de decisiones](decision-log.md) | Decisiones confirmadas, propuestas, preguntas pendientes y cambios de estado. | Vivo |
| [Plan de entrega](plan-entrega.md) | Tareas verificables que faltan, dependencias y decisiones abiertas con opciones y recomendaciones. | En organización con responsabilidad compartida |

## Flujo y control de cambios

1. Reunir materiales y redactar requisitos con sus fuentes.
2. Analizar hechos, decisiones, suposiciones y dependencias; registrar las
   preguntas abiertas como `P01`, `P02`, etc.
3. Preguntar una decisión por vez, en español sencillo: explicar por qué hace
   falta, ofrecer opciones y recomendar una. No tratar una opción como aprobada
   hasta que el equipo la confirme.
4. Después de la respuesta, registrar la decisión como `D01`, `D02`, etc., con
   estado, motivo y fuente; vincularla a la pregunta `P` y marcar esta como
   resuelta. Si falta evidencia, mantenerla pendiente en vez de adivinar.
5. Aprobar el análisis y el canvas antes de cambiar el código de aplicación.
6. Implementar en el orden de **Operations**, vinculando cada etapa con verificaciones.
7. Si cambia un requisito, actualizar primero el canvas y luego el código.
8. Registrar resultados observados; no presentar simulaciones o hipótesis como
   interoperabilidad ni resultados reales.
9. Describir las tareas y aportes como trabajo del equipo. No atribuir ni
   comparar contribuciones personales usando commits o historial.

Docker está verificado en modo local. Siguen pendientes OpenAPI y conformidad,
la prueba con el central real, el experimento con datos, la bitácora, el guion
y el póster. Consulta el [README del proyecto](../README.md) y el análisis para
el estado y las limitaciones.
