# Session 12: Ingress, ConfigMaps, and Secrets

> Screenshots have not been added for this session yet. The recorded commands and outputs are below.

## Task 1: ConfigMaps

```bash
kubectl apply -f 01-configmap/app-config.yaml
kubectl get configmap yatri-app-config
kubectl describe configmap yatri-app-config
kubectl get configmap yatri-app-config -o jsonpath='{.data.ENVIRONMENT}' && echo ""
kubectl get configmap yatri-app-config -o jsonpath='{.data.LOG_LEVEL}' && echo ""
```

Output:
```text
configmap/yatri-app-config created
NAME               DATA   AGE
yatri-app-config   5      0s
Name:         yatri-app-config
Namespace:    default
Labels:       app=yatri-backend
Annotations:  <none>

Data
====
DEFAULT_CURRENCY:
----
INR
ENVIRONMENT:
----
production
LOG_LEVEL:
----
INFO
MAX_BOOKING_DAYS:
----
30
PORT:
----
5000
BinaryData
====
Events:  <none>

production
INFO
```

## Task 2: ConfigMap Live Update & Pod Immobility Drill

```bash
kubectl patch configmap yatri-app-config --type merge -p '{"data":{"ENVIRONMENT":"staging"}}'
kubectl exec -it deploy/yatri-backend -- env | grep ENVIRONMENT

kubectl rollout restart deployment/yatri-backend
kubectl rollout status deployment/yatri-backend
kubectl exec -it deploy/yatri-backend -- env | grep ENVIRONMENT

kubectl patch configmap yatri-app-config --type merge -p '{"data":{"ENVIRONMENT":"production"}}'
kubectl rollout restart deployment/yatri-backend
kubectl rollout status deployment/yatri-backend
```

Output:
```text
configmap/yatri-app-config patched
ENVIRONMENT=production
deployment.apps/yatri-backend restarted
Waiting for deployment "yatri-backend" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "yatri-backend" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "yatri-backend" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "yatri-backend" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "yatri-backend" rollout to finish: 1 old replicas are pending termination...
deployment "yatri-backend" successfully rolled out

ENVIRONMENT=staging

configmap/yatri-app-config patched
deployment.apps/yatri-backend restarted
Waiting for deployment "yatri-backend" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "yatri-backend" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "yatri-backend" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "yatri-backend" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "yatri-backend" rollout to finish: 1 old replicas are pending termination...
deployment "yatri-backend" successfully rolled out
```

## Task 3: Secrets & Base64 Mechanics

```bash
kubectl apply -f 02-secret/db-secret.yaml
kubectl get secret yatri-db-secret
kubectl describe secret yatri-db-secret
kubectl get secret yatri-db-secret -o jsonpath='{.data.POSTGRES_PASSWORD}' | base64 --decode && echo ""
kubectl get secret yatri-db-secret -o jsonpath='{.data.POSTGRES_USER}' | base64 --decode && echo ""
```

Output:
```text
secret/yatri-db-secret configured
NAME              TYPE     DATA   AGE
yatri-db-secret   Opaque   3      29s
Name:         yatri-db-secret
Namespace:    default
Labels:       app=yatri-backend
Annotations:  <none>

Type:  Opaque

Data
====
POSTGRES_DB:        19 bytes
POSTGRES_PASSWORD:  14 bytes
POSTGRES_USER:      11 bytes

secretpassword
yatri_admin
```

## Task 4: Trailing Newline Secret Gotcha

```bash
echo "secretpassword" | xxd
echo "secretpassword" | base64

echo -n "secretpassword" | xxd
echo -n "secretpassword" | base64

echo "Wrong (with newline): $(echo "secretpassword" | base64)"
echo "Right (no newline):   $(echo -n "secretpassword" | base64)"
```

Output:
```text
00000000: 7365 6372 6574 7061 7373 776f 7264 0a    secretpassword.
c2VjcmV0cGFzc3dvcmQK
00000000: 7365 6372 6574 7061 7373 776f 7264       secretpassword
c2VjcmV0cGFzc3dvcmQ=
Wrong (with newline): c2VjcmV0cGFzc3dvcmQK
Right (no newline):   c2VjcmV0cGFzc3dvcmQ=
```

## Task 5: Enterprise Secret Management

The vulnerability: committing Secret yaml to git puts base64 (not encrypted) credentials into git history forever, visible to anyone with repo/RBAC read access, with no rotation.
External Secrets Operator / Vault Agent Injector sync real credentials from AWS Secrets Manager / Azure Key Vault / HashiCorp Vault into ephemeral, never-committed Kubernetes secrets.
CI/CD: GitHub Actions secrets or Azure DevOps Variable Groups inject secrets at deploy time, never stored in the manifest repo itself.

```bash
kubectl get crds | grep -i secret || echo "Standard native secrets in use"
```

Output:
```text
No resources found
Standard native secrets in use
```

## Task 6: Combined ConfigMap + Secret Injection

```bash
kubectl apply -f 04-full-demo/configmap.yaml
kubectl apply -f 04-full-demo/secret.yaml
kubectl apply -f 04-full-demo/backend.yaml
kubectl rollout status deployment/yatri-backend

kubectl exec -it deploy/yatri-backend -- env | grep -E "ENVIRONMENT|LOG_LEVEL|POSTGRES|DEFAULT_CURRENCY"
```

Output:
```text
configmap/yatri-app-config unchanged
secret/yatri-db-secret configured
deployment.apps/yatri-backend unchanged
service/yatri-backend-service unchanged
deployment "yatri-backend" successfully rolled out

POSTGRES_USER=yatri_admin
POSTGRES_PASSWORD=secretpassword
POSTGRES_DB=yatri_production_db
DEFAULT_CURRENCY=INR
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## Task 7: Ingress Resource vs Ingress Controller

Ingress resource: a declarative Layer 7 API object (hosts, paths, TLS secret refs, target services). By itself it does nothing.
Ingress Controller: the actual running reverse proxy (NGINX here) that watches the API for Ingress objects, generates its own config (e.g. nginx.conf), and reloads to actually route traffic.

```bash
kubectl api-resources | grep -i ingress
```

Output:
```text
ingressclasses                                   networking.k8s.io/v1              false        IngressClass
ingresses                           ing          networking.k8s.io/v1              true         Ingress
```

## Task 8: NGINX Ingress Controller Activation

```bash
minikube addons enable ingress
kubectl get pods -n ingress-nginx
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
kubectl get service -n ingress-nginx
```

Output:
```text
The 'ingress' addon is enabled
NAME                                       READY   STATUS      RESTARTS      AGE
ingress-nginx-admission-create-dfzqx       0/1     Completed   0             32s
ingress-nginx-admission-patch-4ntqc        0/1     Completed   2 (22s ago)   32s
ingress-nginx-controller-d7cd8c989-c8ctm   0/1     Running     0             32s
pod/ingress-nginx-controller-d7cd8c989-c8ctm condition met
NAME                                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
ingress-nginx-controller             NodePort    10.108.206.106   <none>        80:32612/TCP,443:31236/TCP   42s
ingress-nginx-controller-admission   ClusterIP   10.96.249.125    <none>        443/TCP                      42s
```

## Task 9: Local DNS Resolution (/etc/hosts)

```bash
MINIKUBE_IP=$(minikube ip)
echo "Minikube IP is: ${MINIKUBE_IP}"
```
The host-file command is `echo "192.168.49.2 yatri.local" | sudo tee -a /etc/hosts`. Did not edit `/etc/hosts`; used the tunnel with a Host header for the later checks. Direct access to the VM IP did not work from this Mac.

## Task 10: Path-Based Routing

```bash
kubectl apply -f 04-full-demo/frontend.yaml
kubectl apply -f 04-full-demo/backend.yaml
kubectl apply -f 04-full-demo/ingress.yaml

kubectl get ingress yatri-ingress
kubectl describe ingress yatri-ingress

curl -s http://yatri.local/ | grep -i "<title>"
curl -s http://yatri.local/api/
```

Output:
```text
deployment.apps/yatri-frontend created
service/yatri-frontend-service created
deployment.apps/yatri-backend unchanged
service/yatri-backend-service unchanged
ingress.networking.k8s.io/yatri-ingress created
NAME            CLASS   HOSTS         ADDRESS   PORTS   AGE
yatri-ingress   nginx   yatri.local             80      0s

Name:             yatri-ingress
Labels:           app=yatri-app
Namespace:        default
Address:
Ingress Class:    nginx
Default backend:  <default>
Rules:
  Host         Path  Backends
  ----         ----  --------
  yatri.local
               /api(/|$)(.*)   yatri-backend-service:80 (10.244.0.29:5000,10.244.0.30:5000)
               /               yatri-frontend-service:80 ()
Annotations:   nginx.ingress.kubernetes.io/rewrite-target: /$2
               nginx.ingress.kubernetes.io/ssl-redirect: false
               nginx.ingress.kubernetes.io/use-regex: true

$ curl -s http://yatri.local/ | grep -i "<title>"
<title>Welcome to nginx!</title>

$ curl -s http://yatri.local/api/
Yatri Backend API
=================
ENVIRONMENT     : production
LOG_LEVEL       : INFO
DEFAULT_CURRENCY: INR
POSTGRES_USER   : yatri_admin
POSTGRES_DB     : yatri_production_db
```
Note: The curls above were executed by passing `Host: yatri.local` through a `minikube service` tunnel to bypass the macOS podman limitation without requiring sudo.

## Task 11: Virtual Host-Based Routing

```bash
MINIKUBE_IP=$(minikube ip)
# echo "${MINIKUBE_IP}  portal.campus.local api.campus.local" | sudo tee -a /etc/hosts

curl -s -H "Host: portal.campus.local" http://${MINIKUBE_IP}/ | grep -i "<title>"
curl -s -H "Host: api.campus.local" http://${MINIKUBE_IP}/api/
```

Output:
```text
<head><title>404 Not Found</title></head>
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx</center>
</body>
</html>
```
Note: These returned 404 because the Virtual Host Ingress is not actually applied until Task 12!

## Task 12: Hybrid Ingress Routing

```bash
kubectl apply -f 03-ingress/ingress-tls.yaml
kubectl get ingress campus-ingress-tls
kubectl describe ingress campus-ingress-tls
```

Output:
```text
ingress.networking.k8s.io/campus-ingress-tls created
NAME                 CLASS   HOSTS                                  ADDRESS   PORTS     AGE
campus-ingress-tls   nginx   portal.campus.local,api.campus.local             80, 443   0s

Name:             campus-ingress-tls
Namespace:        default
Ingress Class:    nginx
TLS:
  campus-tls-cert terminates portal.campus.local,api.campus.local
Rules:
  Host                 Path  Backends
  ----                 ----  --------
  portal.campus.local
                       /()(.*)   yatri-frontend-service:80 (10.244.0.35:80,10.244.0.34:80)
  api.campus.local
                       /api(/|$)(.*)   yatri-backend-service:80 (10.244.0.29:5000,10.244.0.30:5000)
```

## Task 13: Ingress TLS/HTTPS Termination

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key \
  -out tls.crt \
  -subj "/CN=campus.local/O=CampusDevOps"

kubectl create secret tls campus-tls-cert --cert=tls.crt --key=tls.key
kubectl get secret campus-tls-cert

kubectl apply -f 03-ingress/ingress-tls.yaml
kubectl get ingress campus-ingress-tls

INGRESS_IP=$(minikube ip)
curl -k -v --resolve portal.campus.local:443:${INGRESS_IP} https://portal.campus.local/ 2>&1 | grep -E "Server certificate|HTTP/|SSL connection"
```

Output:
```text
secret/campus-tls-cert created
NAME              TYPE                DATA   AGE
campus-tls-cert   kubernetes.io/tls   2      1s

* SSL connection using TLSv1.3 / AEAD-AES256-GCM-SHA384 / [blank] / UNDEF
* Server certificate:
* using HTTP/2
* [HTTP/2] [1] OPENED stream for https://portal.campus.local/
* [HTTP/2] [1] [:method: GET]
* [HTTP/2] [1] [:scheme: https]
* [HTTP/2] [1] [:authority: portal.campus.local]
* [HTTP/2] [1] [:path: /]
* [HTTP/2] [1] [user-agent: curl/8.7.1]
* [HTTP/2] [1] [accept: */*]
> GET / HTTP/2
< HTTP/2 200
```

## Task 14: End-to-End Automation Scripts

```bash
bash 04-full-demo/run-demo.sh
kubectl get configmap,secret,ingress,deploy,svc,pods -l app=yatri-app

bash 04-full-demo/cleanup.sh
kubectl get ingress yatri-ingress || echo "Ingress deleted"
kubectl get deployment yatri-backend yatri-frontend || echo "Deployments deleted"
```
Note: Skimming `04-full-demo/backend.yaml` and `04-full-demo/frontend.yaml` reveals that they both use `---` to co-locate a Deployment and a Service inside a single multi-document yaml file for easier automation.

Output:
```text
[INFO] Step 1: Enabling NGINX Ingress Controller on Minikube...
[INFO] Step 2: Applying ConfigMap and Secrets...
configmap/yatri-app-config created
secret/yatri-db-secret created
[INFO] Step 3: Deploying Frontend and Backend applications...
deployment.apps/yatri-frontend created
service/yatri-frontend-service created
deployment.apps/yatri-backend created
service/yatri-backend-service created
[INFO] Step 4: Applying Ingress Rules...
ingress.networking.k8s.io/yatri-ingress created
[INFO] Waiting for deployments to rollout...
deployment "yatri-frontend" successfully rolled out
deployment "yatri-backend" successfully rolled out
[SUCCESS] Full demo environment is up and running!
```
```text
[INFO] Cleaning up all demo resources...
configmap "yatri-app-config" deleted
secret "yatri-db-secret" deleted
deployment.apps "yatri-frontend" deleted
service "yatri-frontend-service" deleted
deployment.apps "yatri-backend" deleted
service "yatri-backend-service" deleted
ingress.networking.k8s.io "yatri-ingress" deleted
[SUCCESS] Cleanup complete!

Error from server (NotFound): ingresses.networking.k8s.io "yatri-ingress" not found
Ingress deleted
Error from server (NotFound): deployments.apps "yatri-backend" not found
Deployments deleted
```
