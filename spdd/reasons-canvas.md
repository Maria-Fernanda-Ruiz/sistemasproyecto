# Canvas REASONS

**Estado:** aprobado por la estudiante el 7 de noviembre de 2026.  
Este canvas enlaza decisiones y requisitos. Lo marcado como “pendiente” no autoriza a inventar detalles ni a implementar comportamiento no confirmado.

## R — Requirements

### Objetivo

Construir el servidor de chat de `g1` y un cliente web para que sus usuarios envíen y lean mensajes en la sala global `#general`, compartida con los demás grupos mediante el servidor central del curso.

### Necesidades del curso

- Cumplir persistencia, registro, comunicación HTTP/JSON, reintentos, deduplicación, Lamport, detección de fallos, recuperación y logs: `R04`–`R14` en `requisitos.md`.
- Entregar código, Docker Compose, README, diagrama, script/datos del experimento, evidencias de conformidad e interoperabilidad, historial de commits, póster y sustentación: `R15`–`R19`.
- La interfaz de usuario es una página web sencilla permitida por `R03`; el tablero extendido es una decisión del equipo.

### Experimento

- Pregunta de la guía: «¿Cuántos mensajes se pierden o se duplican cuando el servidor del grupo se cae durante unos segundos?» (`R15`, guía, pág. 5).
- Hipótesis: el equipo espera que después de la caída temporal `g1` recupere los mensajes enviados durante la interrupción y que cada mensaje aparezca una sola vez.
- Diseño propuesto y elegido por el equipo: detener `g1` por 5 segundos mientras se envía 1 mensaje por segundo; al menos 3 repeticiones; presentar tabla y gráfica.
- La tasa, duración y visualización son decisiones del equipo, no obligaciones numéricas de la guía.

## E — Entities

Entidades del dominio identificadas a partir de la guía:

- **Servidor central del curso:** registra servidores, almacena historial global y reenvía mensajes.
- **Servidor de grupo:** este proyecto implementa uno identificado como `g1`, cuya disponibilidad fue confirmada por el equipo.
- **Usuario local:** autor de mensajes; se identifica como `usuario@g1` en el intercambio distribuido.
- **Mensaje:** incluye al menos `id`, `from`, `origin`, `lamport`, `sent_at` y `body` en el ejemplo del PDF (pág. 5). Los campos definitivos dependen de la especificación completa.
- **Sala:** `#general`, única sala compartida según el PDF (pág. 2).
- **Historial:** mensajes persistidos y ordenados por `(lamport, origin)`.
- **Evento de log:** acción de envío, recepción, reintento o descarte, con ID y marca Lamport según la recomendación de la guía (pág. 10).
- **Ejecución experimental:** repetición con mensajes enviados, caída, recuperación y conteo de pérdidas/duplicados.

Las estructuras de datos, relaciones y restricciones exactas quedan pendientes del protocolo completo y del diseño técnico aprobado.

## A — Approach

- Implementar el backend en Python con FastAPI. La guía lo recomienda, pero permite otros lenguajes (`R20`); el equipo eligió FastAPI.
- Servir un cliente web sencillo en HTML/CSS/JavaScript para enviar y leer mensajes de `#general`, con estilo colorido de lobby de juego elegido por el equipo. No se añaden pantallas de tablero que la guía no exige.
- Mantener una sola sala `#general`.
- Usar SQLite y un volumen Docker para persistir usuarios e historial.
- Permitir nombres de usuario sin contraseña para la demostración.
- Actualizar el chat con consultas `GET` del frontend al servidor del grupo cada 2 segundos.
- Usar el resumen de rutas del PDF como referencia provisional para el protocolo central; validar sus detalles antes de declarar interoperabilidad.
- Ejecutar la medición seleccionada con script repetible; guardar datos brutos y resultados por repetición.
- Incluir el libro compartido por la estudiante en las referencias del póster: Vitillo, R. (2022). *Understanding Distributed Systems: What Every Developer Should Know About Large Distributed Applications* (2.ª ed., versión 2.0.0). Ajustar el formato si el curso indica uno.

## S — Structure

### Vista lógica propuesta

```text
Navegador (HTML/CSS/JavaScript)
  └─ Chat de #general; consulta el servidor local cada 2 segundos
          │ API local definida por el proyecto
          ▼
Servidor del grupo (Python + FastAPI, g1)
  ├─ Usuarios y mensajes de #general
  ├─ SQLite en volumen persistente
  ├─ Adaptador de comunicación con el servidor central
  ├─ Reintentos, deduplicación y reloj Lamport
  └─ Recuperación de historial y registro de eventos
          │ HTTP/JSON según protocolo del curso
          ▼
Servidor central del curso
  └─ Reenvía mensajes a los servidores registrados
```

### Alcance del cliente elegido

- Una página sencilla para usar el chat de `#general`.
- No se mostrarán vistas adicionales de tablero ni una lista lateral de participantes.
- Cada mensaje muestra nombre y grupo.

### Estructura física

La estructura inicial del código y los contenedores quedó aprobada junto con la etapa local. Los cambios siguientes se propondrán antes de implementarse. Todo lo nuevo debe vivir bajo la carpeta del proyecto `proyecto-sistemas-distribuidos/`.

## O — Operations

Orden propuesto, todavía pendiente de aprobación:

1. Preparar la configuración de `g1` y aclarar cómo hacer accesible la URL del servidor al central.
2. Revisar la especificación completa del protocolo; si no está disponible, marcar los detalles de interoperabilidad que solo se basen en el resumen.
3. **Completado:** diseñar la estructura local y las rutas `POST /users`, `POST /messages` y `GET /messages`, separadas del protocolo central.
4. **Completado:** implementar usuarios e historial local persistente con SQLite.
5. **Implementado provisionalmente:** registro central, envío/recepción, Lamport, deduplicación, reintentos, heartbeat y recuperación según el resumen del PDF. Las pruebas actuales usan un central simulado; validar el contrato OpenAPI y la interoperabilidad real sigue pendiente.
6. **Completado:** construir el cliente web sencillo de `#general`, mostrando nombre y grupo junto a cada mensaje.
7. Pendiente: crear el script repetible para el experimento; realizar al menos 3 repeticiones y guardar datos reales.
8. **Parcial:** las pruebas automatizadas locales y de federación simulada pasan; ejecutar conformidad e interoperabilidad cuando los materiales/servicio estén disponibles.
9. **Parcial:** README y diagrama de arquitectura creados como borradores. Completar la bitácora, datos del experimento, salida de conformidad, guion y contenido del póster dentro de la plantilla original cuando haya evidencias y aprobación.

No se empieza el código de aplicación hasta que el equipo apruebe explícitamente el análisis y este canvas.

La disponibilidad de un servidor de otro equipo para enviar mensajes durante la caída aún se desconoce. No se debe reemplazar el método indicado por la guía por una simulación sin etiquetarla claramente y revisar primero si cumple el objetivo del curso.

Las etapas local y de federación provisional se implementaron después de aprobar el canvas y el análisis. Las pruebas unitarias pasan con un central simulado y `docker compose config` valida la configuración. La construcción y ejecución del contenedor quedan pendientes porque el daemon de Docker no está activo en el equipo. La integración con el central real no está comprobada.

## N — Norms

- Trabajar en español sencillo en documentos y explicaciones; mantener los nombres de rutas y campos del protocolo como los define el curso.
- Separar funciones del servidor; no concentrar toda la lógica en un único `main`.
- Mantener una separación clara entre API del navegador y protocolo del servidor central.
- Escribir logs legibles con ID y marca Lamport para envío, recepción, reintento y descarte.
- Conservar trazabilidad entre requisitos, decisiones, análisis, canvas, código y pruebas.
- No afirmar que una prueba con otros grupos ocurrió si no se realizó.
- Ambas integrantes deben poder explicar el código y participar en commits que reflejen su trabajo real.
- No copiar código del repositorio de referencia ni compartir código con otros grupos.

## S — Safeguards

- No cambiar la guía ni la plantilla original. Cualquier edición propuesta para el póster debe explicarse y aprobarse antes.
- La estudiante gestiona GitHub desde Visual Studio Code. No se han hecho commits ni push; la carpeta local solo tiene configurado el remoto `origin`.
- No invitar colaboradores ni publicar directamente a `main`.
- No modificar ni copiar el proyecto de ejemplo de `gszhangwei/open-spdd`; fue consultado solo como referencia metodológica.
- No asumir que la especificación OpenAPI está disponible: no se encontró entre los materiales actuales.
- No inventar campos, códigos de estado, autenticación, rutas o semántica del protocolo más allá de lo expresamente resumido por la guía.
- No llamar “en vivo” a una lista de usuarios: no se mostrará lista lateral de participantes.
- Los valores experimentales de 5 segundos o 1 mensaje por segundo son elecciones del equipo, no requisitos indicados por la guía.
- No presentar datos esperados como resultados. Los resultados solo se completan después de ejecutar las repeticiones.
- El análisis y el canvas siguen siendo borradores hasta la aprobación expresa del equipo.
