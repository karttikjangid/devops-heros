# Azure Virtual Network - Networking

A VNet is an isolated network in an Azure Region. A CIDR such as `10.19.0.0/16` defines its address space; a subnet such as `10.19.1.0/24` divides it.

| Component | Purpose |
| --- | --- |
| System routes | Default routing between subnets and other supported destinations |
| Route table | User-defined routes that override routing for selected destinations |
| Public IP | Provides a VM with internet-facing addressing |
| NAT Gateway | Provides explicit outbound connectivity for attached subnets |
| NSG | Stateful allow/deny rules applied to a subnet or network interface |

Azure does not use AWS's separate Internet Gateway resource or the same public/private-subnet classification. Reachability depends on public addressing, routing and network rules. Explicit outbound connectivity is preferable to relying on default outbound access.

For this demo, the VM has a Standard public IP. Its NSG allows HTTP and restricts SSH to the administrator's IP. Private services can use private endpoints and restricted networking. Azure NSGs are not a direct equivalent of AWS's stateless network ACLs.

Common uses: isolating application tiers, connecting VMs and linking Azure with on-premises networks.

Sources: [VNet overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview), [NSGs](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview).
