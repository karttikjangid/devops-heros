# VPC - Networking

A VPC is a logically isolated network in an AWS Region. A CIDR such as `10.20.0.0/16` defines its address range. Subnets divide that range; each subnet belongs to one Availability Zone.

| Component | Purpose |
| --- | --- |
| Route table | Chooses the next destination for traffic based on its routes |
| Internet Gateway | Connects a VPC to the internet |
| NAT Gateway | Allows outbound IPv4 internet access for private-subnet resources without accepting unsolicited inbound connections |
| Security Group | Stateful allow rules at the network-interface level |
| Network ACL | Stateless allow/deny rules at the subnet boundary; return traffic needs appropriate rules |

A public subnet has a route to an Internet Gateway. An instance also needs a public address and allowed traffic to be reachable from the internet. A private subnet has no direct route to that gateway; outbound access can use a NAT Gateway.

A common layout puts a web tier in public subnets and databases in private subnets. The homework uses one public subnet; a NAT Gateway is unnecessary for that architecture.

Sources: [VPC overview](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html), [VPC routing](https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html), [Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html), [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html).
