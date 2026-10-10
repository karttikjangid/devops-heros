# Kubernetes FQDN

An FQDN is a fully qualified domain name identifying a DNS name without relying on a local search suffix.

A normal Kubernetes Service name follows:

```text
<service>.<namespace>.svc.<cluster-domain>
web-clusterip.session11-lab.svc.cluster.local
```

Inside the same namespace, a Pod can use `web-clusterip`. Across namespaces, use `web-clusterip.session11-lab` or its full FQDN. The Pod's `/etc/resolv.conf` provides namespace search domains and the cluster DNS server.

For a StatefulSet behind a headless Service:

```text
<pod>.<headless-service>.<namespace>.svc.<cluster-domain>
web-stateful-0.web-service-headless.session11-lab.svc.cluster.local
```

The normal Service resolves to its ClusterIP. The headless Service resolves to endpoint Pod IPs. ExternalName returns a CNAME alias.

```bash
kubectl -n session11-lab exec client -- cat /etc/resolv.conf
kubectl -n session11-lab exec client -- nslookup web-clusterip.session11-lab.svc.cluster.local
kubectl -n session11-lab exec client -- nslookup web-service-headless.session11-lab.svc.cluster.local
```

[Real lookup and HTTP output](../screenshots/headless.txt) · [CoreDNS lookup output](../screenshots/coredns.txt)
