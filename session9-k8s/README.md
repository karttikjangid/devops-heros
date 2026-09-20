# Session 9: Kubernetes Fundamentals & Cluster Architecture

> Screenshot evidence is unavailable; command outputs are recorded below.

## Task 1: Minikube & CLI Installation Verification
```bash
mkdir -p session9-k8s/screenshots
minikube version
kubectl version --client
```

Output:
```text
minikube version: v1.39.0
commit: 7a9f6a841470a207de8cf4bafcccee0969d8ba10
Client Version: v1.37.0
Kustomize Version: v5.8.1
```

## Task 2: Starting the Minikube Kubernetes Cluster

```bash
minikube start --driver=podman
```

Output:
```text
minikube v1.39.0 on Darwin 26.6.2 (arm64)
Using the podman (experimental) driver based on existing profile
Starting "minikube" primary control-plane node in "minikube" cluster
Pulling base image v0.0.51 ...
E0918 16:40:03.876465   36817 cache.go:238] Error downloading kic artifacts:  not yet implemented, see issue #8426
Updating the running podman "minikube" container ...
Preparing Kubernetes v1.37.0 on containerd 2.3.4 ...
Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
Enabled addons: storage-provisioner, default-storageclass
Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```
Note: The warning regarding kic artifacts is normal for the podman driver.

## Task 3: Verifying Cluster Status & Node Health

```bash
minikube status
kubectl get nodes -o wide
```

Output:
```text
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

NAME       STATUS   ROLES           AGE   VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE                         KERNEL-VERSION                   CONTAINER-RUNTIME
minikube   Ready    control-plane   9d    v1.37.0   192.168.49.2   <none>        Debian GNU/Linux 12 (bookworm)   7.1.4-200.fc44.aarch64 (arm64)   containerd://2.3.4
```

## Task 4: Stopping the Minikube Cluster

```bash
minikube stop
minikube status
```

Output:
```text
Stopping node "minikube"  ...
Powering off "minikube" via SSH ...
1 node stopped.
minikube
type: Control Plane
host: Stopped
kubelet: Stopped
apiserver: Stopped
kubeconfig: Stopped
```

## Task 5: Kubernetes Cluster Architecture & Component Analysis

Control Plane Components:
* kube-apiserver: The front door of the control plane; the only component that communicates directly with etcd.
* etcd: A highly available key-value store containing the cluster state.
* kube-scheduler: Watches for newly created Pods without an assigned node and schedules them.
* kube-controller-manager: Runs control loops (e.g., node controller, replicaset controller) to drive the current state towards the desired state.

Worker Node Components:
* kubelet: An agent that runs on each node to ensure containers are running in a Pod and reports health to the control plane.
* kube-proxy: Maintains network routing and iptables rules on nodes to allow network communication to Pods.
* Container Runtime: Software like containerd or CRI-O responsible for running the containers.
* Pod: The smallest deployable unit in Kubernetes that encapsulates one or more containers.

```text
+---------------------------------------+
|            Control Plane              |
| [API Server] <------> [etcd]          |
|    |     |                            |
| [Scheduler] [Controller Manager]      |
+---------------------------------------+
                 ^
                 | (API Calls)
                 v
+---------------------------------------+
|             Worker Node               |
| [kubelet] <--------> [Container       |
|    |                 Runtime] -> Pods |
| [kube-proxy] (Network/iptables)       |
+---------------------------------------+
```
