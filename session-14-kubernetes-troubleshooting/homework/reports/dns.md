# DNS failure

This was an intentionally introduced classroom fault in `session14-lab`.

- Problem/root cause: The client used an unusable custom resolver with dnsPolicy=None.
- Investigation: Inspected /etc/resolv.conf and ran a failing nslookup.
- Fix: Recreated the Pod with the default ClusterFirst DNS policy.
- Verification: The Kubernetes service name resolved and HTTP to web succeeded.

![Real before-and-after output](../../screenshots/dns.png)

[Complete commands and output](../../screenshots/dns.txt)
