# Session 21 - Homework Tracker

## Project Overview

Homework Tracker keeps course assignments and their progress. I adapted the TaskBoard starter for my coursework using React/Vite, FastAPI and PostgreSQL.

## Architecture

```text
Browser → Frontend (3000, Nginx) → /api → Backend (8000, FastAPI) → PostgreSQL (5432)
```

## Running Manually

From `session21-python/`, start PostgreSQL:

```bash
docker run -d --name session21-manual-postgres \
  -e POSTGRES_DB=taskboard -e POSTGRES_USER=taskboard \
  -e POSTGRES_PASSWORD=taskboard -p 127.0.0.1:5432:5432 postgres:16-alpine
docker exec session21-manual-postgres pg_isready -U taskboard -d taskboard
```

Once PostgreSQL accepts connections, start the backend:

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

Open [manual frontend](http://localhost:5173). Vite sends `/api` requests to port 8000. I ran the frontend and backend directly on my Mac, with PostgreSQL in a separate container using `podman run`. [Manual API/database output](screenshots/manual-test.txt) and [browser verification](screenshots/manual-browser-test.txt).

![Manual frontend after creating and updating a task](screenshots/manual-frontend.png)

Before Compose, stop both host processes with Ctrl+C and remove the temporary database:

```bash
docker stop session21-manual-postgres
docker rm session21-manual-postgres
```

## Dockerfiles

- [Frontend Dockerfile](frontend/Dockerfile): Node 22 builds with `npm ci`. Non-root Nginx (UID 101) serves the frontend on port 8080 and forwards `/api` to `backend:8000`.
- [Backend Dockerfile](backend/Dockerfile): Python 3.12 runs as a non-root user. It applies Alembic migrations before starting Uvicorn.

## Docker Compose

The [Compose file](docker-compose.yml) starts all three services. The backend waits for PostgreSQL to be ready, then the frontend starts. PostgreSQL stores data in a named volume. Ports are local only; `taskboard` is the local homework password.

```bash
docker compose down
docker compose up -d --build
docker compose up -d --wait --wait-timeout 120
```

I used Docker CLI 28.5.1 and Compose 2.39.4 with Podman 6.1.0 on macOS. [Runtime versions](screenshots/runtime.txt).

For Podman, connect the Docker CLI to its API socket:

```bash
export DOCKER_HOST="unix://$(podman machine inspect --format '{{.ConnectionInfo.PodmanSocket.Path}}')"
export DOCKER_BUILDKIT=0
export COMPOSE_BAKE=false
```

I downloaded the Docker CLI and Compose plugin into a temporary folder. With Docker installed normally, skip the Podman variables above.

![Compose build and startup output](screenshots/docker-compose-build.png)

[Full build output](screenshots/docker-compose-build.txt), [clean shutdown](screenshots/clean-down.txt) and [readiness check](screenshots/services-ready.txt). The screenshot shows the final build lines.

## Running Containers

```bash
docker compose ps
```

![All three Compose services running and healthy](screenshots/docker-compose-ps.png)

[Exact output](screenshots/docker-compose-ps.txt).

## Application Test

Open [frontend](http://localhost:3000) and [backend API docs](http://localhost:8000/docs). I created a task in the browser, changed it to IN_PROGRESS and refreshed. It stayed saved in PostgreSQL. The starter sidebar and recent-activity panel are static.

![Running frontend with the task created through the browser](screenshots/frontend-running.png)

[Browser test result](screenshots/frontend-browser-test.txt).

## Backend API Testing

The [API transcript](screenshots/api-test.txt) has the exact commands and responses. Creation returned 201, reads and updates returned 200, deletion returned 204, and reading the deleted task returned 404.

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

[Database output](screenshots/database-test.txt). I deleted the API test task and kept the browser task.

All 5 backend tests passed:

```bash
cd backend
python -m pytest -p no:cacheprovider tests
```

[Captured test output](screenshots/backend-tests.txt).

![Five passing API tests](screenshots/backend-tests.png)

![Both application containers run as non-root](screenshots/non-root-test.png)

## Troubleshooting

| Issue | Cause | Fix |
| --- | --- | --- |
| Docker command missing | Only Podman was installed | Downloaded Docker CLI/Compose and connected to Podman |
| Backend migration refused connection | PostgreSQL was still starting | Waited for `pg_isready`, then restarted the backend |
| Wrong manual proxy port | Vite used 8080; Uvicorn uses 8000 | Changed the proxy to 8000 and checked `/api/tasks` |
| Task form stayed open after saving | `currentTarget` was read after the API request | Saved the form reference before awaiting |
| Tests failed with `no such table: tasks` | TestClient did not run startup | Used a context-managed fixture and temporary SQLite database |
| Compose could not bind 5432 | Manual PostgreSQL still occupied the port | Stopped the manual app and database, then reran Compose |
| Existing Git merge was unfinished | Earlier sessions had staged changes and conflicts | Committed this homework from a separate checkout of `origin/main` |

[Failed first Compose attempt](screenshots/build-first-attempt.txt).

## Lessons Learned

I learned to wait for database readiness and check the frontend proxy port. Testing the form in the browser caught a bug that curl tests missed.

## Final Verification

I checked a clean Compose start, all services, API CRUD, frontend updates and PostgreSQL data. The screenshots load in the README. Terminal screenshots use the saved command output.

[Final service/API/database/log checks](screenshots/final-verification.txt).

## Capstone progress

Application, tests and Docker are verified locally. The full rubric also requires a green CI pipeline, registry images, Kubernetes/Helm, monitoring, real cloud infrastructure and a demo. Those checks are in progress; this is not yet a full-rubric PASS.

The provided rubric specifies AWS VPC/EKS. An Azure VNet/AKS deployment needs instructor approval.
