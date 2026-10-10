# Session 21 - Homework Tracker

I adapted the provided TaskBoard starter to track course assignments. The app has a React frontend, FastAPI backend and PostgreSQL database.

## Architecture

```text
GitHub → Actions: test, build, scan → GHCR images tagged with the commit SHA
                                      ↓
                               Kubernetes + Helm
Browser → Ingress → Frontend → Backend → PostgreSQL
                                 ↓
                            Prometheus → Grafana
```

Technologies: React/Vite, Python/FastAPI, PostgreSQL, Alembic, Docker Compose, GitHub Actions, Trivy, Helm, Terraform, K3s, Prometheus and Grafana.

## Running manually

Start PostgreSQL from `session21-python/`:

```bash
docker run -d --name session21-manual-postgres \
  -e POSTGRES_DB=taskboard -e POSTGRES_USER=taskboard \
  -e POSTGRES_PASSWORD=taskboard -p 127.0.0.1:5432:5432 postgres:16-alpine
docker exec session21-manual-postgres pg_isready -U taskboard -d taskboard
```

Start the backend after the database is ready:

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql+psycopg://taskboard:taskboard@localhost:5432/taskboard
alembic upgrade head
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

In another terminal:

```bash
cd frontend
npm ci
npm run dev -- --host 127.0.0.1
```

Open [localhost:5173](http://localhost:5173). Vite forwards `/api` to port 8000. I ran the frontend/backend as host processes and PostgreSQL separately with Podman. Stop these manual processes before Compose to free their ports.

[Manual API/database output](screenshots/manual-test.txt) · [Browser check](screenshots/manual-browser-test.txt)

![Manual application](screenshots/manual-frontend.png)

## Dockerfiles and Compose

[Frontend Dockerfile](frontend/Dockerfile): Node 22 builds with `npm ci`; non-root Nginx runs as UID 101 on port 8080. [Backend Dockerfile](backend/Dockerfile): Python 3.12 Alpine runs as UID 10001 and applies migrations before Uvicorn starts.

[Compose](docker-compose.yml) keeps PostgreSQL data in a named volume and waits for service readiness. The `taskboard` credentials are local demo defaults.

```bash
docker compose down
docker compose up -d --build
docker compose up -d --wait --wait-timeout 120
docker compose ps
```

I used Docker CLI/Compose with the installed Podman engine on macOS. [Runtime versions](screenshots/runtime.txt).

![Build and startup](screenshots/docker-compose-build.png)

[Full build output](screenshots/docker-compose-build.txt) · [Clean shutdown](screenshots/clean-down.txt) · [Readiness](screenshots/services-ready.txt)

![docker compose ps](screenshots/docker-compose-ps.png)

## Application and API tests

Local URLs: [frontend](http://localhost:3000) · [API docs](http://localhost:8000/docs).

The browser check creates an assignment, advances its status and reloads the page. The saved assignment remains in PostgreSQL.

![Local frontend](screenshots/frontend-running.png)

These curl requests test health, creation, reading, updates, statistics and deletion. Use the ID returned by POST for `TASK_ID`.

```bash
curl -fsS -i http://localhost:8000/health
curl -fsS -i http://localhost:8000/ready
curl -fsS -i -X POST http://localhost:8000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Session 21 API verification","description":"Created by curl and checked in PostgreSQL","priority":"HIGH","assignee":"Kartik"}'
curl -fsS -i "http://localhost:8000/api/tasks/$TASK_ID"
curl -fsS -i -X PUT "http://localhost:8000/api/tasks/$TASK_ID" \
  -H 'Content-Type: application/json' -d '{"status":"DONE"}'
curl -fsS -i http://localhost:8000/api/tasks/stats
curl -fsS -i http://localhost:3000/api/tasks
curl -fsS -i -X DELETE "http://localhost:8000/api/tasks/$TASK_ID"
```

[Exact executed commands and responses](screenshots/api-test.txt): POST 201, GET/PUT 200, DELETE 204, then 404 for the deleted task.

![API results](screenshots/api-test.png)

All five API tests pass using a temporary SQLite database:

```bash
cd backend
python -m pytest -v tests
```

![Five passing tests](screenshots/backend-tests.png)

![Non-root application containers](screenshots/non-root-test.png)

## Kubernetes and Helm

The [chart](helm/taskboard/) has two frontend replicas, two backend replicas, PostgreSQL storage, ConfigMap, Secret, Ingress, HPA and probes. The backend waits for PostgreSQL before starting. [Rendered manifests](k8s/application.yaml).

On K3s, use Traefik and an empty hostname to access the VM's public IP:

```bash
helm upgrade --install homework ./helm/taskboard -n session21 --create-namespace \
  --set backend.tag=<commit-sha> --set frontend.tag=<commit-sha> \
  --set ingress.className=traefik --set ingress.host='' --wait
kubectl -n session21 get pods,svc,ingress,hpa,pvc
helm list -n session21
```

![Azure Kubernetes deployment](screenshots/cloud-kubernetes.png)

![Azure frontend](screenshots/cloud-frontend.png)

![PostgreSQL contains the assignment created through the Azure frontend](screenshots/cloud-database.png)

[Helm output](screenshots/cloud-deploy.txt) · [Cloud browser test](screenshots/cloud-browser-test.txt) · [Cloud API output](screenshots/cloud-api.txt)

## Terraform infrastructure

I used one Azure VM with K3s, as requested, instead of the rubric's AWS/EKS setup. The Azure for Students quota could not support the current AKS minimum. This is an Azure/self-managed Kubernetes variant.

[Terraform files](terraform/) create a VNet with two subnets, the VM, NSG, network interface and public IP. `Standard_B2als_v2` in Central India has 2 vCPUs and 4 GB RAM. SSH is restricted to my IP; port 80 is for the frontend.

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Fill in the subscription ID, public SSH key path and your IP.
terraform init
terraform validate
terraform plan
terraform apply
terraform destroy
```

![Terraform plan](screenshots/terraform-plan.png)

![Terraform apply](screenshots/terraform-apply.png)

![Real Azure VM state](screenshots/azure-vm.png)

This is real Azure CLI evidence. The portal screenshot needs a separate browser sign-in and is not included.

![Terraform destroy](screenshots/terraform-destroy.png)

[Destroy output](screenshots/terraform-destroy.txt) · [Cleanup verification](screenshots/azure-cleanup.txt)

The cloud resources were destroyed after the demo. State, private keys and personal variable files are excluded from Git. [Cost estimate and runtime](screenshots/cloud-cost.json).

## CI/CD and security

[Workflow](../.github/workflows/session21.yml) runs on Session 21 code pushes to `main`: tests, frontend build, Docker builds, Trivy scans, GHCR pushes, Helm deployment into an isolated CI Kubernetes cluster and monitoring checks. Images use the commit SHA. Azure deployment uses the same chart and images.

![Successful GitHub Actions run](screenshots/github-actions.png)

![GHCR image package](screenshots/registry-backend.png)

Trivy scans both application images and blocks HIGH/CRITICAL findings. It flagged old Starlette dependencies and a vulnerable `tiff` package. Updating the framework, changing the backend to Alpine and upgrading `tiff` removed those findings; the final scans passed without ignoring them.

[Backend scan](screenshots/backend-scan.txt) · [Frontend scan](screenshots/frontend-scan.txt)

## Monitoring

Prometheus scrapes the backend's `/metrics` endpoint. Grafana shows the live HTTP request counter. I used self-hosted monitoring to keep Azure costs low.

![Prometheus target UP](screenshots/prometheus-targets.png)

![Grafana live request counter](screenshots/grafana-dashboard.png)

[Target status](screenshots/prometheus-targets.json) · [Saved metric query](screenshots/prometheus-query.json) · [Backend metrics](screenshots/cloud-metrics.txt)

## Troubleshooting

| Issue | Cause | Fix |
| --- | --- | --- |
| Wrong manual proxy port | Vite used 8080; backend uses 8000 | Corrected the proxy port |
| Task form stayed open after saving | Event reference was read after awaiting the API | Saved the form reference first |
| Tests reported no tasks table | TestClient did not run startup | Used a context-managed fixture and temporary database |
| Compose could not bind 5432 | Manual PostgreSQL still occupied the port | Stopped the manual app before Compose |
| Helm backend initially restarted | PostgreSQL was not ready | Added a database readiness init container |
| CI could not resolve Trivy | Action tag missed its `v` prefix | Used the published tag |
| Security gate failed | Vulnerable framework/base packages | Updated the affected packages and rebuilt |
| Framework update caused a dependency conflict | Old metrics plugin required Starlette below 1.0 | Updated the plugin with the framework |
| Local monitoring timed out | The shared local VM had too little memory; logs showed OOM kills | Verified it in CI and on the 4 GB Azure VM |
| AKS could not fit the quota | Required system-node capacity exceeded the student quota | Used the requested small VM with K3s |
| Upstream sync had conflicts | Local homework and instructor files differed | Preserved completed homework while merging upstream |

[First failed Compose run](screenshots/build-first-attempt.txt). I documented actual failures and did not introduce artificial incidents.

## Demo and lessons

[Recorded walkthrough](screenshots/session21-demo.webm) shows the application, CI run and updated cloud deployment.

I learned to check database readiness, test the browser form as well as the APIs, scan before pushing images and remove cloud resources after collecting evidence.

## Final checks

Clean Compose start, all services, API CRUD, browser persistence, PostgreSQL data, non-root users, five tests, CI/security, Kubernetes/Helm, monitoring, Terraform cleanup and README image/link checks passed. Upstream is synchronized and the Session 21 files are committed and pushed.

[Final local checks](screenshots/final-verification.txt) · [Cloud checks](screenshots/cloud-final.txt) · [Commit history](screenshots/git-history.png)
