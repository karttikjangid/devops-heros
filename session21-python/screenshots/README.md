# Evidence index

## Review on 15 October 2026

- [API and migration tests](review-tests.txt)
- [Assignment creation, status update and reload](review-frontend.png)
- [Rejected save with form data retained](review-frontend-error.png)
- [Mobile layout](review-frontend-mobile.png)
- [Pipeline run](https://github.com/karttikjangid/devops-heros/actions/runs/38735507512): source SHA and job logs are available on the run page. Test, security, browser, monitoring, troubleshooting and GitOps artifacts are uploaded there.

The browser error check deliberately returns HTTP 503 for one POST request to verify error handling; it is not an unexplained production outage.

## Earlier run on 10 October 2026

The other files record the earlier local and Azure deployment. Dates and commands remain in the `.txt` files. Terminal images are formatted views of those linked transcripts, not captures of a terminal window. Browser images are direct browser captures. Refer to the text and workflow logs for exact commands and results.

- [Manual API/database checks](manual-test.txt)
- [Compose build/start](docker-compose-build.txt) and [service list](docker-compose-ps.txt)
- [API CRUD](api-test.txt) and [database checks](database-test.txt)
- [Terraform plan](terraform-plan.txt), [apply](terraform-apply.txt), [destroy](terraform-destroy.txt), [Azure cleanup](azure-cleanup.txt)
- [Cloud deployment](cloud-deploy.txt), [Kubernetes](cloud-kubernetes.txt), [cloud API](cloud-api.txt), [rollout](cloud-rollout.txt)
- [Cloud browser](cloud-frontend.png), [Prometheus](prometheus-targets.png), [Grafana](grafana-dashboard.png)
- [Earlier walkthrough](session21-demo.webm)

The cloud resources were destroyed after that run. No new Azure deployment was created during the review. The earlier recording and images do not demonstrate the new session/due-date fields or replace the final presentation.
