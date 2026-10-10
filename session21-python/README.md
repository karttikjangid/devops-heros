# Session 21 - Docker Compose Application

## Project Overview

TaskBoard is the starter React/Vite frontend with a FastAPI backend and PostgreSQL database. I verified task creation, updates, listing, statistics and deletion locally.

## Architecture

```text
Browser → Frontend (3000, Nginx) → /api → Backend (8000, FastAPI) → PostgreSQL (5432)
```

## Running Manually

From `session21-python/`, start PostgreSQL separately:

```bash
docker run -d --name session21-manual-postgres \
  -e POSTGRES_DB=taskboard -e POSTGRES_USER=taskboard \
  -e POSTGRES_PASSWORD=taskboard -p 127.0.0.1:5432:5432 postgres:16-alpine
docker exec session21-manual-postgres pg_isready -U taskboard -d taskboard
```

Start the backend after PostgreSQL reports that it accepts connections:

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql+psycopg://taskboard:taskboard@localhost:5432/taskboard
alembic upgrade head
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

In another terminal (Node.js 22.12+):

```bash
cd frontend
npm ci
npm run dev -- --host 127.0.0.1
```

Open [manual frontend](http://localhost:5173). Vite proxies `/api` to port 8000. The backend and frontend ran as host processes; PostgreSQL ran separately in a container. The actual database launch used `podman run` with the same arguments. [Manual API/database output](screenshots/manual-test.txt) and [browser verification](screenshots/manual-browser-test.txt).

![Manual frontend after creating and updating a task](screenshots/manual-frontend.png)

Stop the two host processes with Ctrl+C and remove only the temporary database before Compose:

```bash
docker stop session21-manual-postgres
docker rm session21-manual-postgres
```

## Dockerfiles

- [Frontend Dockerfile](frontend/Dockerfile): Node 22 builds the locked dependencies with `npm ci`; Nginx serves the compiled frontend and proxies `/api` to `backend:8000`.
- [Backend Dockerfile](backend/Dockerfile): Python 3.12 installs the pinned requirements, runs as a non-root user, applies Alembic migrations and starts Uvicorn.

## Docker Compose

[Compose file](docker-compose.yml) starts three services with readiness checks. PostgreSQL keeps data in a named volume; backend waits for PostgreSQL, and frontend waits for the backend. Ports bind to localhost. The `taskboard` credentials are local homework defaults.

```bash
docker compose down
docker compose up -d --build
docker compose up -d --wait --wait-timeout 120
```

Verified with Docker CLI 28.5.1 and Docker Compose 2.39.4 against the installed Podman 6.1.0 Docker-compatible API on macOS. This run did not use Docker Desktop. [Runtime versions](screenshots/runtime.txt).

For the installed Podman machine, point the Docker CLI at its API socket:

```bash
export DOCKER_HOST="unix://$(podman machine inspect --format '{{.ConnectionInfo.PodmanSocket.Path}}')"
export DOCKER_BUILDKIT=0
export COMPOSE_BAKE=false
```

The CLI and Compose plugin used for verification were downloaded into the agent's temporary work directory; a normal Docker installation needs no Podman environment variables.

![Compose build and startup output](screenshots/docker-compose-build.png)

[Full build transcript](screenshots/docker-compose-build.txt), [clean shutdown](screenshots/clean-down.txt) and [readiness verification](screenshots/services-ready.txt). The build screenshot is a clearly labeled excerpt of the final lines; the full transcript is retained.

## Running Containers

```bash
docker compose ps
```

![All three Compose services running and healthy](screenshots/docker-compose-ps.png)

[Exact output](screenshots/docker-compose-ps.txt).

## Application Test

Open [frontend](http://localhost:3000) and [backend API docs](http://localhost:8000/docs). The browser test created a task, advanced its status to IN_PROGRESS and reloaded the page to verify persistence. The task also appears in PostgreSQL. The starter sidebar and recent-activity panel are static demonstration content.

![Running frontend with the task created through the browser](screenshots/frontend-running.png)

[Browser test result](screenshots/frontend-browser-test.txt).

## Backend API Testing

The exact executed curl commands, headers, response bodies and task ID are in the [API transcript](screenshots/api-test.txt). These requests covered health/readiness, create, read, update, statistics, the frontend proxy, delete and a 404 after deletion.

```bash
curl -fsS -i http://localhost:8000/health
curl -fsS -i http://localhost:8000/ready
curl -fsS -i -X POST http://localhost:8000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Session 21 API verification","description":"Created by curl and checked in PostgreSQL","priority":"HIGH","assignee":"Kartik"}'
# TASK_ID is the id returned by POST (see the exact transcript).
curl -fsS -i "http://localhost:8000/api/tasks/$TASK_ID"
curl -fsS -i -X PUT "http://localhost:8000/api/tasks/$TASK_ID" \
  -H 'Content-Type: application/json' -d '{"status":"DONE"}'
curl -fsS -i http://localhost:8000/api/tasks/stats
curl -fsS -i http://localhost:3000/api/tasks
docker compose exec -T postgres psql -U taskboard -d taskboard \
  -c 'SELECT id, title, status FROM tasks ORDER BY id;'
curl -fsS -i -X DELETE "http://localhost:8000/api/tasks/$TASK_ID"
curl -sS -o /private/tmp/session21-deleted.json -w '%{http_code}' \
  "http://localhost:8000/api/tasks/$TASK_ID"
```

![Real successful API output](screenshots/api-test.png)

![PostgreSQL confirms the browser task is stored](screenshots/database-test.png)

[Database output](screenshots/database-test.txt). The API task was deleted after its database check; the browser task remains visible.

The existing backend tests also passed (3 tests):

```bash
cd backend
python -m pytest -p no:cacheprovider tests
```

[Captured test output](screenshots/backend-tests.txt).

## Troubleshooting

Only issues actually encountered:

| Issue | Cause | Fix |
| --- | --- | --- |
| Docker command missing | This Mac had Podman but no Docker CLI/Compose plugin | Used downloaded official Docker CLI/Compose with Podman's existing API socket |
| Manual backend migration refused connection | PostgreSQL had not finished downloading/starting | Waited for `pg_isready`, then reran migration and Uvicorn |
| Manual proxy pointed at the wrong port | Starter Vite configuration used 8080 while Uvicorn uses 8000 | Changed the proxy to 8000 and verified `/api/tasks` through Vite |
| Create-task form stayed open after saving | React event `currentTarget` was accessed after an awaited request | Saved the form reference before awaiting; creation and update passed in the browser |
| Backend test failed with `no such table: tasks` | TestClient was created without entering its startup context | Added a context-managed fixture and temporary SQLite database; all 3 tests passed |
| First Compose startup could not bind 5432 | The temporary manual PostgreSQL container still occupied the port | Stopped/removed only that container and stopped manual host processes, then ran Compose cleanly |
| Main checkout could not support an isolated normal commit | An existing unfinished merge included unrelated staged files/conflicts | Published only this homework from a separate checkout of existing `origin/main`; preserved the original index/merge |

[Original failed Compose attempt](screenshots/build-first-attempt.txt) is retained. No intentional troubleshooting incidents were introduced.

## Lessons Learned

Service startup order needs readiness checks, and frontend proxy ports must match the backend. A successful API response alone does not prove the browser workflow works, so I tested real task creation and updates too.

## Final Verification

Clean Compose shutdown/build/start, healthy services, API CRUD, browser persistence, PostgreSQL rows, screenshot rendering and README relative links were verified. Evidence is captured from this application; terminal images are rendered from saved real command output.

[Final service/API/database/log checks](screenshots/final-verification.txt).
