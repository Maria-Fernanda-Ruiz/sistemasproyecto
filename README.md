# Proyecto de sistemas distribuidos

Chat distribuido del grupo `g1`, con un cliente web sencillo, un servidor
FastAPI y almacenamiento SQLite persistente.

## Requisitos para ejecutar

- Docker Desktop instalado y en ejecución, con Docker Compose disponible.
- Una URL pública para este servidor y la URL del servidor central para activar
  la federación. Sin `CENTRAL_URL`, el servidor funciona en modo local.

## Inicio rápido con Docker Compose

1. Abre esta carpeta en Visual Studio Code.
2. Copia `.env.example` como `.env`.
3. Para el modo local, deja `CENTRAL_URL` y `PUBLIC_URL` vacías.
4. Abre **Terminal → Nuevo terminal** y ejecuta:

   ```sh
   docker compose up --build
   ```

5. Cuando aparezca que Uvicorn está escuchando en el puerto `8000`, abre
   <http://localhost:8000>.
6. Detén el servidor con `Ctrl+C`. Los datos quedan en el volumen Docker
   `chat-data` y se conservan al reiniciar el contenedor.

El comando `docker compose down` detiene y elimina el contenedor, pero conserva
el volumen de datos. No uses `docker compose down -v` si quieres conservar el
historial.

## Activar la conexión con el servidor central

Antes de habilitar la federación, configura `.env` con los datos proporcionados
por el curso:

```dotenv
GROUP_ID=g1
CENTRAL_URL=
PUBLIC_URL=
```

- `GROUP_ID`: identificador asignado al grupo.
- `CENTRAL_URL`: URL base del servidor central.
- `PUBLIC_URL`: URL pública desde la que el central puede alcanzar este servidor.
- `HEALTH_INTERVAL_SECONDS`: intervalo entre consultas de salud (5 s por defecto).
- `HEALTH_FAILURE_THRESHOLD`: fallos consecutivos para marcar el central como
  caído (3 por defecto).
- `REGISTRATION_INTERVAL_SECONDS`: intervalo para renovar el registro (30 s).
- `RETRY_INITIAL_SECONDS` y `RETRY_MAX_SECONDS`: espera exponencial inicial y
  límite para reintentar mensajes (1 s y 30 s).

Guarda `.env` y ejecuta de nuevo `docker compose up --build`. La URL pública
debe apuntar al servicio de este proyecto en el puerto `8000` y permitir que el
servidor central alcance sus rutas `/fed/health` y `/fed/messages`. La guía
menciona Cloudflare, pero no se incluyeron aquí instrucciones ni credenciales
para configurar un túnel.

### Contrato provisional

La integración sigue las rutas y los campos resumidos en el PDF de la actividad.
La guía indica que la especificación OpenAPI completa prevalece; como todavía no
está disponible en los materiales revisados, el formato de respuesta de
`GET /history?since=...` se implementó provisionalmente como una lista JSON
directa. La interoperabilidad con el central no se considera verificada hasta
probar contra esa especificación y el servicio real.

## Ejecución local sin Docker

Con Python 3.12 o posterior, desde la carpeta del proyecto:

```sh
python -m venv .venv
```

Activa el entorno virtual y luego instala dependencias e inicia el servidor:

```sh
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Abre <http://localhost:8000>. Los datos se guardan por defecto en
`data/chat.sqlite3`. Para cambiar esa ruta, configura `CHAT_DB_PATH`.

## Pruebas automatizadas

```sh
python -m unittest discover -s tests -v
```

Las pruebas usan un central simulado para revisar el registro, el envío,
reintentos, recuperación del historial, deduplicación, reloj Lamport y
migración de la base de datos. No sustituyen la prueba de interoperabilidad con
el central del curso.

## Rutas del servidor de grupo

| Método y ruta | Uso |
|---|---|
| `GET /` | Abre el cliente web. |
| `POST /users` | Crea un usuario local. |
| `POST /messages` | Envía un mensaje desde un usuario local. |
| `GET /messages` | Lee el historial para el cliente. |
| `GET /fed/health` | Informa el grupo y el reloj Lamport al central. |
| `POST /fed/messages` | Recibe un mensaje reenviado por el central. |

El flujo entre componentes se muestra en [docs/arquitectura.md](docs/arquitectura.md).
Los requisitos, decisiones y pendientes SPDD están en [spdd/](spdd/).

## Estado de entrega

- Implementados: cliente web, API local, persistencia SQLite, integración
  federada provisional y pruebas automatizadas.
- Validación local: pruebas unitarias y sintaxis de Docker Compose.
- Pendientes: contrastar el protocolo con OpenAPI, ejecutar Docker cuando el
  daemon esté activo, configurar la URL pública, probar con el central y otro
  grupo, y realizar el experimento con datos reales.
- Los resultados del experimento, la bitácora de interoperabilidad, la salida
  de conformidad, el guion y el póster deben completarse con evidencias reales;
  no se incluyen resultados inventados.
