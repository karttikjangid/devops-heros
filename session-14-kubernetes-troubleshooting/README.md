# Session 14 - Completed Kubernetes Troubleshooting Homework

I used an isolated `session14-lab` namespace in local Minikube. The faults below were intentionally introduced, investigated and repaired. No cloud infrastructure was created.

## Commands

`kubectl get`, `describe`, `logs`, `exec`, `events`, `explain`, `top` and `get -o wide` were executed. Metrics Server was enabled so `top` could collect real CPU and memory samples.

![Command practice and real resource metrics](screenshots/commands.png)

[All command output](screenshots/commands.txt)

## Faults and repairs

- [CrashLoopBackOff: investigation, cause, fix and verification](homework/reports/crashloop.md)
- [ErrImagePull / ImagePullBackOff: investigation, cause, fix and verification](homework/reports/imagepull.md)
- [Pending: investigation, cause, fix and verification](homework/reports/pending.md)
- [ContainerCreating: investigation, cause, fix and verification](homework/reports/containercreating.md)
- [Configuration error: investigation, cause, fix and verification](homework/reports/configuration.md)
- [DNS failure: investigation, cause, fix and verification](homework/reports/dns.md)
- [Pod connectivity: investigation, cause, fix and verification](homework/reports/pod-networking.md)
- [Service connectivity / mini project: investigation, cause, fix and verification](homework/reports/service-mini-project.md)

[Reproducible manifests](homework/) include both broken configurations and their fixes. Run these only in the demo namespace.

## Mini project

The Nginx application was healthy, but its Service could not reach it. I repaired the selector first, then found and fixed the incorrect target port. The final request succeeded through the Service. [Full before/after report](homework/reports/service-mini-project.md).

## Lessons from the exercises

A Running container can still be starting its HTTP listener. I verified HTTP readiness before declaring the volume repair complete. Pod DNS fields are immutable, so the DNS fix required deleting the old Pod and waiting for deletion before recreating it.

## Cleanup

```bash
kubectl delete namespace session14-lab
```

[Final verification](screenshots/final-verification.txt) · [Cleanup output](screenshots/cleanup.txt)

The original lesson notes follow.

---

# Kubernetes Troubleshooting

The goal is to learn how to answer:

> "My Kubernetes application is not working. How do I find out why?"

---

## Topics

We will cover:

* `kubectl get`
* `kubectl describe`
* `kubectl logs`
* `kubectl exec`
* `Events`
* `CrashLoopBackOff`
* `ImagePullBackOff`
* `Pending Pods`
* `Service Troubleshooting`
* `DNS Troubleshooting`

---

## Folder Structure

```text
01-kubectl-get
02-kubectl-describe
03-kubectl-logs
04-kubectl-exec
05-events
06-crashloopbackoff
07-imagepullbackoff
08-pending-pods
09-service-dns-troubleshooting
mini-project
```

Each folder contains a small practical example.

---

## Troubleshooting Mindset

When an application is not working, don't randomly run commands.

Follow a process:

```text
1. Observe
      │
      ▼
2. Identify the resource
      │
      ▼
3. Check status
      │
      ▼
4. Check details
      │
      ▼
5. Check events
      │
      ▼
6. Check logs
      │
      ▼
7. Enter container if possible
      │
      ▼
8. Test connectivity
      │
      ▼
9. Find root cause
      │
      ▼
10. Fix
      │
      ▼
11. Verify
```

---

## The Five Commands

### 1. `kubectl get`

Use it for a quick view.

```bash
kubectl get pods
```

**Question:**
> "What is happening?"

---

### 2. `kubectl describe`

Use it for detailed information.

```bash
kubectl describe pod <pod-name>
```

**Question:**
> "What details can explain the problem?"

---

### 3. `kubectl logs`

Use it to see application output.

```bash
kubectl logs <pod-name>
```

**Question:**
> "What is the application saying?"

---

### 4. `kubectl exec`

Use it to run commands inside a running container.

```bash
kubectl exec -it <pod-name> -- sh
```

**Question:**
> "What can I see from inside the container?"

---

### 5. `Events`

Use Events to understand what Kubernetes tried to do.

```bash
kubectl get events
```

or:

```bash
kubectl describe pod <pod-name>
```

**Question:**
> "What did Kubernetes try, and what happened?"

---

## Common Kubernetes Problems

### CrashLoopBackOff

```text
Container starts
      │
      ▼
Application crashes
      │
      ▼
Container restarts
      │
      ▼
Crash again
      │
      ▼
CrashLoopBackOff
```

**Check:**

```bash
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
kubectl describe pod <pod-name>
```

---

### ImagePullBackOff

```text
Kubernetes
    │
    ▼
Needs image
    │
    ▼
Pull fails
    │
    ▼
Retries
    │
    ▼
ImagePullBackOff
```

**Check:**

```bash
kubectl describe pod <pod-name>
```

Look at Events.

---

### Pending Pod

```text
Pod created
    │
    ▼
Scheduler tries to find a node
    │
    ▼
Cannot schedule
    │
    ▼
Pending
```

**Check:**

```bash
kubectl describe pod <pod-name>
```

Look at Events.

---

### Service Problem

**Check:**

```bash
kubectl get pods
kubectl get service
kubectl describe service <service-name>
kubectl get endpoints <service-name>
```

Most importantly:

```text
Pod labels
    │
    ▼
Service selector
    │
    ▼
Endpoints
```

They need to match correctly.

---

### DNS Problem

Test from inside a Pod:

```bash
nslookup <service-name>
```

Check CoreDNS:

```bash
kubectl get pods -n kube-system
```

Check CoreDNS logs:

```bash
kubectl logs -n kube-system -l k8s-app=kube-dns
```

---

## Golden Troubleshooting Flow

Students should remember this:

```text
              PROBLEM
                 │
                 ▼
            kubectl get
                 │
                 ▼
           What is the status?
                 │
                 ▼
         kubectl describe
                 │
                 ▼
              Events
                 │
                 ▼
           kubectl logs
                 │
                 ▼
           kubectl exec
                 │
                 ▼
           Test connectivity
                 │
                 ▼
            Find root cause
                 │
                 ▼
                FIX
                 │
                 ▼
              VERIFY
```

---

## Learning

* Check Kubernetes resource status
* Inspect detailed resource information
* Read application logs
* Execute commands inside containers
* Understand Kubernetes Events
* Troubleshoot `CrashLoopBackOff`
* Troubleshoot `ImagePullBackOff`
* Troubleshoot `Pending` Pods
* Troubleshoot Services
* Test Kubernetes DNS
* Identify root causes instead of guessing