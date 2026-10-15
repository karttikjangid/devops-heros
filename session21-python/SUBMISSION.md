# Capstone submission checks

Deadline in the course notice: **16 October 2026, 11:59 PM**. Use the course timezone if the instructor specifies one.

Submit once through the [official Google Form](https://forms.gle/XWAP1vAumDJgAPM1A), signed in with the official SST email. Check every link first; the notice says resubmissions are not accepted. This repository has not been submitted through the form.

## Links

- [Project README](https://github.com/karttikjangid/devops-heros/blob/main/session21-python/README.md)
- [Source code](https://github.com/karttikjangid/devops-heros/tree/main/session21-python)
- [Review pipeline](https://github.com/karttikjangid/devops-heros/actions/runs/38735507512)
- [Backend image](https://github.com/users/karttikjangid/packages/container/package/session21-backend)
- [Frontend image](https://github.com/users/karttikjangid/packages/container/package/session21-frontend)
- [Evidence index](screenshots/README.md)
- [Instructor brief](https://github.com/Nency-Ravaliya/devops-heros/tree/main/session21-python)
- [Instructor grading rubric](https://github.com/Nency-Ravaliya/devops-heros/blob/main/session21-python/GRADING.md)

The current upstream directory contains README.md and GRADING.md. The student-guide.md mentioned in the course notice was not found there during the 15 October review. Check with the instructor for any additional submission fields or rules.

## Before submitting

- [ ] Confirm the instructor accepts Azure/K3s in place of the rubric's AWS VPC/EKS. Azure is used here by choice; approval is not recorded.
- [ ] Review the course policy on outside assistance. The project extends the supplied TaskBoard reference and was developed with coding-assistant support; do not claim it was built unaided.
- [ ] Open the GitHub README, pipeline and both image links while signed out, or verify instructor access.
- [ ] Check the review pipeline's final result and scan artifacts.
- [ ] Complete the presentation or record an updated walkthrough of the final application.
- [ ] Submit the verified links using the official SST email through the form, once.

## Presentation

Explain the code and run the steps yourself:

1. Create an assignment with a session and due date. Change its status and reload to show persistence.
2. Show API CRUD, rejected invalid input and the PostgreSQL row.
3. Show the tests, Dockerfiles and three healthy Compose services.
4. Make a small application change, commit and push. Follow the pipeline through tests, security gates and SHA-tagged image publication.
5. Show Terraform code and the saved Azure creation/destruction evidence. Ask before recreating paid resources; remove them after the demo.
6. Deploy the successful SHA with Helm, show two replicas per application, Services, Ingress and PVC.
7. Show HPA CPU metrics and actual replica changes under load. An HPA manifest alone is insufficient.
8. Show Prometheus target UP and a populated Grafana panel.
9. Explain GitOps promotion and demonstrate self-healing.
10. Diagnose and fix the broken image and Service selector using Pod events and EndpointSlices.

The 10 October walkthrough predates the final application changes. Historical cloud output does not imply a cloud deployment is still running.
