# Session 11: Kubernetes Services

> Screenshot evidence is unavailable; command outputs are recorded below.

## Task 1: Kubernetes Port Architecture & Clarification Drill

```bash
kubectl explain pod.spec.containers.ports.containerPort
kubectl explain service.spec.ports
```

Output:
```text
KIND:       Pod
VERSION:    v1

FIELD: containerPort <integer>

DESCRIPTION:
    Number of port to expose on the pod's IP address. This must be a valid port
    number, 0 < x < 65536.

---
KIND:       Service
VERSION:    v1

FIELD: ports <[]ServicePort>

DESCRIPTION:
    The list of ports that are exposed by this service.
...
```

Client Browser -> nodePort (host IP) -> port (Service VIP) -> targetPort (pod network) -> containerPort (container process)

## Task 2: Type 1 Service — ClusterIP

```bash
cd 01-clusterip/
kubectl apply -f app-deployment.yaml
kubectl apply -f service.yaml
kubectl get pods -l app=web-clusterip -o wide
kubectl get svc web-service-clusterip
kubectl get endpoints web-service-clusterip

kubectl apply -f client-pod.yaml
kubectl wait --for=condition=ready pod/curl-client --timeout=60s

kubectl exec -it curl-client -- curl -s http://web-service-clusterip:8080 | grep -i "<title>"
kubectl exec -it curl-client -- curl -s http://web-service-clusterip.default.svc.cluster.local:8080 | grep -i "<title>"
cd ..
```

Output:
```text
deployment.apps/web-app-clusterip created
service/web-service-clusterip created
NAME                                 READY   STATUS              RESTARTS   AGE   IP       NODE       NOMINATED NODE   READINESS GATES
web-app-clusterip-66865d4855-9s7tr   0/1     ContainerCreating   0          0s    <none>   minikube   <none>           <none>
web-app-clusterip-66865d4855-lxbzh   0/1     ContainerCreating   0          0s    <none>   minikube   <none>           <none>
web-app-clusterip-66865d4855-mx2kn   0/1     ContainerCreating   0          0s    <none>   minikube   <none>           <none>
NAME                    TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
web-service-clusterip   ClusterIP   10.104.2.103   <none>        8080/TCP   0s
NAME                    ENDPOINTS                                   AGE
web-service-clusterip   10.244.0.3:80,10.244.0.4:80,10.244.0.5:80   23s
pod/curl-client created
pod/curl-client condition met
<title>Welcome to nginx!</title>
<title>Welcome to nginx!</title>
```

## Task 3: Type 2 Service — NodePort

```bash
cd 02-nodeport/
kubectl apply -f app-deployment.yaml
kubectl apply -f service.yaml
kubectl get svc web-service-nodeport

MINIKUBE_IP=$(minikube ip)
curl -I http://${MINIKUBE_IP}:30080 || echo "direct node-ip access failed — see Task 12 for why"
minikube service web-service-nodeport --url
cd ..
```

Output:
```text
deployment.apps/web-app-nodeport created
service/web-service-nodeport created
NAME                   TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
web-service-nodeport   NodePort   10.100.190.113   <none>        80:30080/TCP   0s
Testing direct connection to 192.168.49.2:30080...
direct node-ip access failed — see Task 12 for why

$ minikube service web-service-nodeport --url
http://127.0.0.1:58731
Because you are using a Docker driver on darwin, the terminal needs to be open to run it.

$ curl -I http://127.0.0.1:58731
HTTP/1.1 200 OK
Server: nginx/1.25.5
Date: Fri, 18 Sep 2026 11:25:15 GMT
Content-Type: text/html
Content-Length: 615
Last-Modified: Tue, 16 Apr 2024 15:47:06 GMT
Connection: keep-alive
ETag: "661e9d7a-267"
Accept-Ranges: bytes
```
Note: Due to macOS networking with podman, `minikube service --url` created a tunnel mapping to `127.0.0.1:58731` which succeeded.

## Task 4: Type 3 Service — LoadBalancer

```bash
cd 03-loadbalancer/
kubectl apply -f app-deployment.yaml
kubectl apply -f service.yaml
kubectl get svc web-service-loadbalancer
# minikube tunnel would be run here, but it prompts for sudo password
```

Output:
```text
deployment.apps/web-app-loadbalancer created
service/web-service-loadbalancer created
NAME                       TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
web-service-loadbalancer   LoadBalancer   10.101.115.206   <pending>     80:32613/TCP   0s
```
Note: Attempted to run `minikube tunnel`, but because it binds to a privileged port (80), it prompted interactively for a `sudo` password. The user will need to run `minikube tunnel` in a separate terminal to populate the EXTERNAL-IP and curl it successfully.

## Task 5: Type 4 Service — ExternalName

```bash
cd 04-externalname/
kubectl apply -f service.yaml
kubectl apply -f client-pod.yaml
kubectl wait --for=condition=ready pod/dns-test-client --timeout=60s

kubectl get svc external-database-service
kubectl exec -it dns-test-client -- nslookup external-database-service
kubectl exec -it dns-test-client -- curl -s -k https://external-database-service
cd ..
```

Output:
```text
service/external-database-service created
pod/dns-test-client created
pod/dns-test-client condition met
NAME                        TYPE           CLUSTER-IP   EXTERNAL-IP        PORT(S)   AGE
external-database-service   ExternalName   <none>       nencyravaliya.me   <none>    1s

$ kubectl exec dns-test-client -- nslookup external-database-service
Server:		10.96.0.10
Address:	10.96.0.10:53

** server can't find external-database-service.svc.cluster.local: NXDOMAIN

external-database-service.default.svc.cluster.local	canonical name = nencyravaliya.me
```

## Task 6: Type 5 Service — Headless Service

```bash
cd 05-headless/
kubectl apply -f service.yaml
kubectl apply -f app-statefulset.yaml
kubectl apply -f client-pod.yaml
kubectl rollout status statefulset/web-stateful --timeout=120s
kubectl get pods -l app=web-headless -o wide

kubectl get svc web-service-headless
kubectl exec -it headless-dns-client -- nslookup web-service-headless
kubectl exec -it headless-dns-client -- nslookup web-stateful-0.web-service-headless.default.svc.cluster.local
kubectl exec -it headless-dns-client -- curl -s http://web-stateful-0.web-service-headless:80 | grep -i "<title>"
cd ..
```

Output:
```text
service/web-service-headless created
statefulset.apps/web-stateful created
pod/headless-dns-client created
Waiting for 3 pods to be ready...
Waiting for 2 pods to be ready...
Waiting for 2 pods to be ready...
Waiting for 1 pods to be ready...
Waiting for 1 pods to be ready...
partitioned roll out complete: 3 new pods have been updated...
NAME             READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
web-stateful-0   1/1     Running   0          2s    10.244.0.13   minikube   <none>           <none>
web-stateful-1   1/1     Running   0          1s    10.244.0.15   minikube   <none>           <none>
web-stateful-2   1/1     Running   0          1s    10.244.0.16   minikube   <none>           <none>
NAME                   TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
web-service-headless   ClusterIP   None         <none>        80/TCP    2s

$ kubectl exec headless-dns-client -- nslookup web-service-headless
Server:		10.96.0.10
Address:	10.96.0.10:53

Name:	web-service-headless.default.svc.cluster.local
Address: 10.244.0.13
Name:	web-service-headless.default.svc.cluster.local
Address: 10.244.0.15
Name:	web-service-headless.default.svc.cluster.local
Address: 10.244.0.16

$ kubectl exec headless-dns-client -- nslookup web-stateful-0.web-service-headless.default.svc.cluster.local
Server:		10.96.0.10
Address:	10.96.0.10:53

Name:	web-stateful-0.web-service-headless.default.svc.cluster.local
Address: 10.244.0.13

$ kubectl exec headless-dns-client -- curl -s http://web-stateful-0.web-service-headless:80 | grep -i "<title>"
<title>Welcome to nginx!</title>
```

## Task 7: Services Without Selectors (Manual Endpoints Mapping)

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: external-legacy-db
spec:
  ports:
    - protocol: TCP
      port: 3306
      targetPort: 3306
EOF

kubectl get endpoints external-legacy-db

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Endpoints
metadata:
  name: external-legacy-db
subsets:
  - addresses:
      - ip: 192.168.1.150
    ports:
      - port: 3306
EOF

kubectl get endpoints external-legacy-db
kubectl delete service external-legacy-db
kubectl delete endpoints external-legacy-db
```

Output:
```text
service/external-legacy-db created
Error from server (NotFound): endpoints "external-legacy-db" not found
endpoints/external-legacy-db created
NAME                 ENDPOINTS            AGE
external-legacy-db   192.168.1.150:3306   0s
service "external-legacy-db" deleted from default namespace
Error from server (NotFound): endpoints "external-legacy-db" not found
```
Note: `kubectl delete endpoints` returned NotFound because deleting the Service implicitly deleted the connected Endpoints object as well.

## Task 8: FQDN & CoreDNS Deep Dive

```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns -o wide
kubectl exec -it curl-client -- cat /etc/resolv.conf
kubectl exec -it curl-client -- nslookup web-service-clusterip
kubectl exec -it curl-client -- nslookup api.github.com
```

Output:
```text
NAME                       READY   STATUS    RESTARTS        AGE   IP           NODE       NOMINATED NODE   READINESS GATES
coredns-559f6c778d-zrnvp   1/1     Running   3 (2m12s ago)   9d    10.244.0.2   minikube   <none>           <none>

$ kubectl exec curl-client -- cat /etc/resolv.conf
search default.svc.cluster.local svc.cluster.local cluster.local dns.podman
nameserver 10.96.0.10
options ndots:5

$ kubectl exec curl-client -- nslookup web-service-clusterip
Server:		10.96.0.10
Address:	10.96.0.10:53

Name:	web-service-clusterip.default.svc.cluster.local
Address: 10.104.2.103

$ kubectl exec curl-client -- nslookup api.github.com
Server:		10.96.0.10
Address:	10.96.0.10:53

Non-authoritative answer:
Name:	api.github.com
Address: 20.207.73.85
```

## Task 9: Pod Identity & Lifecycle Invariance — Deployment vs StatefulSet

```bash
kubectl apply -f 01-clusterip/app-deployment.yaml
kubectl apply -f 05-headless/service.yaml
kubectl apply -f 05-headless/app-statefulset.yaml

kubectl get pods -l app=web-clusterip
kubectl get pods -l app=web-headless

DEPLOY_POD=$(kubectl get pods -l app=web-clusterip -o jsonpath='{.items[0].metadata.name}')
echo "Deleting Deployment Pod: ${DEPLOY_POD}"
kubectl delete pod "${DEPLOY_POD}"
kubectl get pods -l app=web-clusterip

echo "Deleting StatefulSet Pod: web-stateful-0"
kubectl delete pod web-stateful-0
kubectl get pods -l app=web-headless
```

Output:
```text
deployment.apps/web-app-clusterip unchanged
service/web-service-headless unchanged
statefulset.apps/web-stateful unchanged
NAME                                 READY   STATUS    RESTARTS   AGE
web-app-clusterip-66865d4855-9s7tr   1/1     Running   0          118s
web-app-clusterip-66865d4855-lxbzh   1/1     Running   0          118s
web-app-clusterip-66865d4855-mx2kn   1/1     Running   0          118s
NAME             READY   STATUS    RESTARTS   AGE
web-stateful-0   1/1     Running   0          23s
web-stateful-1   1/1     Running   0          22s
web-stateful-2   1/1     Running   0          22s
Deleting Deployment Pod: web-app-clusterip-66865d4855-9s7tr
pod "web-app-clusterip-66865d4855-9s7tr" deleted from default namespace
NAME                                 READY   STATUS    RESTARTS   AGE
web-app-clusterip-66865d4855-lxbzh   1/1     Running   0          2m4s
web-app-clusterip-66865d4855-mx2kn   1/1     Running   0          2m4s
web-app-clusterip-66865d4855-v9v2m   1/1     Running   0          6s
Deleting StatefulSet Pod: web-stateful-0
pod "web-stateful-0" deleted from default namespace
NAME             READY   STATUS    RESTARTS   AGE
web-stateful-0   1/1     Running   0          5s
web-stateful-1   1/1     Running   0          34s
web-stateful-2   1/1     Running   0          34s
```

## Task 10: Master Architectural Matrix — Deployment vs StatefulSet vs DaemonSet

| Metric | Deployment | StatefulSet | DaemonSet |
|---|---|---|---|
| Workload type | Stateless services/APIs | Clustered databases, queues | Node-level agents |
| Pod naming | Random hash | Deterministic ordinal (`-0,-1,-2`) | One per eligible node |
| Identity | Ephemeral | Invariant (identity/IP/hostname stick) | Bound to its node |
| Start/stop order | Parallel, unordered | Strictly sequential | Parallel across nodes |
| Storage | Shared/ephemeral | Per-ordinal PVC via `volumeClaimTemplates` | HostPath / node-local |
| Service type | ClusterIP/NodePort/LB | Headless (`clusterIP: None`) | Usually none |
| Scaling | Arbitrary | Ordinal (adds/removes at the tail) | Follows node count |
| Examples | Nginx, Flask, Node APIs | Kafka, MongoDB, Postgres | Fluentd, node-exporter, Falco |

```bash
kubectl get deploy,sts,ds
```
Output:
```text
NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/web-app-clusterip      3/3     3            3           2m25s
deployment.apps/web-app-loadbalancer   3/3     3            3           90s
deployment.apps/web-app-nodeport       2/2     2            2           117s

NAME                            READY   AGE
statefulset.apps/web-stateful   3/3     50s
```

## Task 11: Production Cost Optimization & Service Selection Decision Tree

```text
ANTI-PATTERN: 1 LoadBalancer per microservice ($25/mo each) -> 50 services = $1,250/mo
BEST PRACTICE: 1 LoadBalancer -> Ingress Controller -> N ClusterIP services = $25/mo total

Need to expose outside the cluster?
├── NO  → need direct pod discovery (Kafka/DB)? → HEADLESS, else ClusterIP
└── YES → external 3rd-party domain? → ExternalName
          else on public cloud + HTTP(S)? → 1 Ingress + LoadBalancer, apps as ClusterIP
          else TCP/UDP direct? → LoadBalancer
          else on-prem/dev? → NodePort
```

## Task 12: Minikube Docker-Driver Port Binding & Tunnel Gotcha Analysis

```bash
kubectl get svc web-service-nodeport
NODE_IP=$(minikube ip)
echo "Testing direct connection to ${NODE_IP}:30080..."
curl --connect-timeout 2 -s http://${NODE_IP}:30080 || echo "Connection failed"

minikube service web-service-nodeport --url
```

Output:
```text
NAME                   TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
web-service-nodeport   NodePort   10.100.190.113   <none>        80:30080/TCP   109s
Testing direct connection to 192.168.49.2:30080...
Connection failed

$ minikube service web-service-nodeport --url
http://127.0.0.1:58731
Because you are using a Docker driver on darwin, the terminal needs to be open to run it.

$ curl -I http://127.0.0.1:58731
HTTP/1.1 200 OK
Server: nginx/1.25.5
Date: Fri, 18 Sep 2026 11:26:45 GMT
Content-Type: text/html
Content-Length: 615
```

Analysis:
Because the environment runs Minikube on macOS using the podman driver, the internal node IP (`192.168.49.2`) is housed inside the podman VM's isolated network namespace and cannot be directly routed from the macOS host, leading to a connection failure. `minikube service --url` addresses this by spinning up a local proxy/tunnel that maps the NodePort securely to a port on the host's `127.0.0.1` interface.
