# CoreDNS

CoreDNS supplies DNS-based discovery in this Kubernetes cluster. Pods query the kube-dns Service; CoreDNS uses Kubernetes API information to answer Service and endpoint queries. Names outside the cluster are forwarded to upstream resolvers.

## Actual configuration inspected

```bash
kubectl -n kube-system get pods -l k8s-app=kube-dns
kubectl -n kube-system get configmap coredns -o yaml
```

The captured Corefile contains:

- `kubernetes cluster.local`: answers cluster Service/Pod DNS queries.
- `forward . /etc/resolv.conf`: forwards other queries upstream.
- `health` and `ready`: health/readiness endpoints.
- `errors` and `log`: diagnostic output.
- `cache`, `loop`, `reload` and `loadbalance`: caching, loop detection, configuration reload and response ordering.

[Actual Corefile and successful client lookup](../screenshots/coredns.txt)

## Troubleshooting approach

Check the client namespace and FQDN, inspect `/etc/resolv.conf`, then test DNS separately from HTTP connectivity. Inspect CoreDNS Pod readiness and logs, its ConfigMap, and the target Service's EndpointSlices. A successful DNS lookup does not prove the application port is reachable.

```bash
kubectl -n kube-system logs deployment/coredns --tail=30
kubectl -n session11-lab get endpointslices
kubectl -n session11-lab exec client -- nslookup web-clusterip.session11-lab.svc.cluster.local
```

Reference: [Kubernetes DNS debugging](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/).
