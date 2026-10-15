# Session 21 capstone - Homework Tracker

A course-assignment tracker with a React frontend, FastAPI backend and PostgreSQL database. Assignments have a course session, due date, assignee, priority and status. The UI supports creating, filtering, advancing and deleting assignments.

Based on the instructor's [TaskBoard starter](https://github.com/Nency-Ravaliya/devops-heros/tree/main/session21-python). The assignment fields, second migration, validation tests, save-error handling and delivery checks extend that reference. See [submission checks](SUBMISSION.md) and the [evidence index](screenshots/README.md).

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
pip install -r requirements-dev.txt
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

![Assignment tracker after browser creation, status update and reload](screenshots/review-frontend.png)

[Browser test](scripts/test-frontend.cjs) also checks a rejected save without losing form data and deletion. [Mobile view](screenshots/review-frontend-mobile.png).

These curl requests test health, creation, reading, updates, statistics and deletion. Set `TASK_ID` to the ID returned by POST, for example `TASK_ID=1`.

```bash
curl -fsS -i http://localhost:8000/health
curl -fsS -i http://localhost:8000/ready
curl -fsS -i -X POST http://localhost:8000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Session 21 API verification","description":"Created by curl and checked in PostgreSQL","priority":"HIGH","assignee":"Kartik","session_number":21,"due_date":"2026-10-31"}'
curl -fsS -i "http://localhost:8000/api/tasks/$TASK_ID"
curl -fsS -i -X PUT "http://localhost:8000/api/tasks/$TASK_ID" \
  -H 'Content-Type: application/json' -d '{"status":"DONE"}'
curl -fsS -i http://localhost:8000/api/tasks/stats
curl -fsS -i http://localhost:3000/api/tasks
curl -fsS -i -X DELETE "http://localhost:8000/api/tasks/$TASK_ID"
```

[Exact executed commands and responses](screenshots/api-test.txt): POST 201, GET/PUT 200, DELETE 204, then 404 for the deleted task.

![API results](screenshots/api-test.png)

The review has eleven API and migration tests. Each API test starts with clean SQLite tables; the migration test upgrades an existing assignment without losing its data:

```bash
cd backend
python -m pytest -v tests
```

[Review test output](screenshots/review-tests.txt). The older five-test output is retained as historical evidence.

![Non-root application containers](screenshots/non-root-test.png)

## Kubernetes and Helm

The [chart](helm/taskboard/) has two frontend replicas, two backend replicas, PostgreSQL storage, ConfigMap, Secret, Ingress, HPA and probes. The backend waits for PostgreSQL before starting. PostgreSQL advisory locks serialize Alembic migrations when replicas start together; the application does not create tables outside migrations. The chart defaults to a published SHA tag. Pass the successful pipeline SHA to deploy a new release. [Rendered manifests](k8s/application.yaml).

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

## Terraform infrastructure (Azure demo: 10 October 2026)

Used one Azure VM with K3s for the cloud deployment instead of AWS/EKS. This is a deliberate change from the instructor rubric, which specifically names AWS/EKS; equivalence has not been confirmed by the instructor. AKS did not fit the available student quota, so Kubernetes ran on the VM.

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

![Azure VM state](screenshots/azure-vm.png)

The screenshot shows the VM state from Azure CLI. A portal screenshot is not included.

![Terraform destroy](screenshots/terraform-destroy.png)

[Destroy output](screenshots/terraform-destroy.txt) · [Cleanup verification](screenshots/azure-cleanup.txt)

Destroyed the cloud resources after the demo. Kept state, private keys and personal variable files out of Git. [Cost estimate and runtime](screenshots/cloud-cost.json).

## CI/CD and security

[Workflow](../.github/workflows/session21.yml) runs on Session 21 code pushes to `main`: eleven tests, Bandit SAST, pip-audit dependency checks, Trivy secret scanning, frontend build/npm audit, Docker builds, Trivy image scans, GHCR pushes, Helm deployment into an isolated CI Kubernetes cluster, browser checks, failure/recovery exercises, monitoring and Argo CD reconciliation checks. Images use the commit SHA. Azure deployment uses the same chart and images.

[Capstone review pipeline](https://github.com/karttikjangid/devops-heros/actions/runs/38735507512). The historical successful run and registry screenshots below are from 10 October.

![Earlier successful GitHub Actions run](screenshots/github-actions.png)

![GHCR image package](screenshots/registry-backend.png)

Trivy scans both application images and blocks HIGH/CRITICAL findings. It flagged old Starlette dependencies and a vulnerable `tiff` package. Updating the framework, changing the backend to Alpine and upgrading `tiff` removed those findings; the final scans passed without ignoring them.

[Backend scan](screenshots/backend-scan.txt) · [Frontend scan](screenshots/frontend-scan.txt)

## Monitoring

Prometheus scrapes the backend's `/metrics` endpoint. Grafana shows the live HTTP request counter. I used self-hosted monitoring to keep Azure costs low.

![Prometheus target UP](screenshots/prometheus-targets.png)

![Grafana live request counter](screenshots/grafana-dashboard.png)

[Target status](screenshots/prometheus-targets.json) · [Saved metric query](screenshots/prometheus-query.json) · [Backend metrics](screenshots/cloud-metrics.txt)

## GitOps

[Argo CD Application](gitops/application.yaml) reads the Helm chart and [release values](helm/taskboard/values-gitops.yaml) from Git. Automatic sync, pruning and self-healing are enabled. The CI exercise uses a separate namespace to avoid two controllers managing the same release.

To use GitOps on K3s, install Argo CD first, then apply the Application. Use either Argo CD or manual Helm ownership for the application, not both. Promote only images from a successful pipeline by changing the SHA tags in `values-gitops.yaml` and committing the file. Revert that commit to request a rollback.

```bash
kubectl apply -f gitops/application.yaml
kubectl -n argocd get application session21
```

The small reconciliation profile disables HPA. The normal chart enables it; verify CPU metrics before load testing:

```bash
kubectl -n session21 get hpa
kubectl -n session21 top pods
URL=http://<ingress-address>/api/tasks bash scripts/load-test.sh
kubectl -n session21 get hpa,pods
```

The load script fails if requests fail. Configuring an HPA alone does not prove scaling; capture replica changes during the presentation.

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
| AKS could not fit the quota | Required system-node capacity exceeded the student quota | Used a small VM with K3s |
| Upstream sync had conflicts | Local homework and instructor files differed | Merged upstream and kept the homework changes |

[First failed Compose run](screenshots/build-first-attempt.txt). The troubleshooting table covers the problems encountered during setup.

The CI failure exercise runs [these commands](scripts/troubleshoot.sh): it observes a nonexistent image tag, checks Pod events, fixes the image, then diagnoses and fixes a Service selector with no endpoints. It deletes only its two temporary resources afterward.

## Demo and lessons

[Earlier walkthrough](screenshots/session21-demo.webm) shows the 10 October application and deployment. It predates the assignment-field changes and does not replace the required final presentation. Follow the [presentation checklist](SUBMISSION.md).

I learned to check database readiness, test the browser form as well as the APIs, scan before pushing images and remove cloud resources after collecting evidence.

## Earlier checks before cloud cleanup

Started Compose from a clean state and checked the frontend, API CRUD and PostgreSQL data. The then-current five tests, CI scans, Helm deployment and monitoring checks passed on 10 October. Destroyed the cloud resources after the demo and checked the README links and screenshots before pushing.

[Final local checks](screenshots/final-verification.txt) · [Cloud checks](screenshots/cloud-final.txt) · [Commit history](screenshots/git-history.png)
