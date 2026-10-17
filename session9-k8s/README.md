# Session 9 - Kubernetes Fundamentals

Screenshot refresh (17 October 2026): terminal images now use live Mac zsh views of the recorded results. Original logs and dates are retained; test re-runs are marked separately. [Capture details](screenshots/mac/README.md).

Used the existing Minikube cluster for the six Kubernetes Basics exercises. Checked the versions and cluster status first, then deployed, exposed, scaled and updated Nginx. Used images that work on my Arm-based Mac.

| Module | What I did | Output |
| --- | --- | --- |
| Create/check cluster | Verified Minikube, node health and control-plane components | [Output](screenshots/cluster.txt) |
| Deploy app | Created a Deployment and inspected its ReplicaSet/Pods | [Output](screenshots/deploy-explore.txt) |
| Explore app | Used describe and logs | [Output](screenshots/deploy-explore.txt) |
| Expose app | Created/tested a Service, then a NodePort accessed from the Mac through Minikube | [Internal](screenshots/expose.txt), [public](screenshots/public-access.txt) |
| Scale app | Scaled from one to three ready replicas | [Output](screenshots/scale.txt) |
| Update app | Updated Nginx 1.24-alpine to 1.25-alpine and verified the page | [Output](screenshots/update-verified.txt) |

## Screenshots

![Recorded output in Mac zsh: Minikube and cluster verification](screenshots/mac/cluster.png)

![Recorded output in Mac zsh: Application deployment and inspection](screenshots/mac/deploy-explore.png)

![Recorded output in Mac zsh: Service connectivity](screenshots/mac/expose.png)

![Recorded output in Mac zsh: Public NodePort access from the Mac](screenshots/mac/public-access.png)

![Recorded output in Mac zsh: Scaling to three replicas](screenshots/mac/scale.png)

![Recorded output in Mac zsh: Updated application verified](screenshots/mac/update-verified.png)

A request immediately after the update timed out. A later check returned the page successfully; [the first attempt](screenshots/update.txt) is retained alongside the successful verification.

## Architecture notes

The API server accepts Kubernetes requests; etcd stores cluster state. The scheduler assigns Pods to nodes, and controllers reconcile desired state. The kubelet runs containers through the container runtime. kube-proxy programs Service traffic rules; CoreDNS provides name discovery.

A Deployment manages application releases through ReplicaSets. A ReplicaSet maintains Pod count. Pods run containers, and Services supply stable endpoints for reaching them.

```text
kubectl → API server → controllers/scheduler → node kubelet → containers
             ↕                                  ↑
            etcd                         Service network / CoreDNS
```

The existing shared cluster was reused and kept running. Only the homework namespaces were removed after testing. [Cleanup output](screenshots/cleanup.txt).

Reference: [Kubernetes Basics tutorial](https://kubernetes.io/docs/tutorials/kubernetes-basics/).
