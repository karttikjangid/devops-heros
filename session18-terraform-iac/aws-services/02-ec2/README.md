# EC2 - Compute

EC2 provides virtual servers called instances. I choose an instance's operating system, capacity, storage and network access.

| Concept | Meaning |
| --- | --- |
| AMI | A machine image used to launch an instance; it must match the CPU architecture |
| Instance type | The CPU, memory and networking capacity, such as an Arm-based T4g instance |
| Key pair | A public/private key pair commonly used for SSH authentication; protect the private key |
| Security Group | Stateful inbound and outbound traffic rules attached to network interfaces |
| EBS | Block storage volumes used for root disks and persistent application data |
| Private IP | Address used inside the VPC and connected private networks |
| Public IP | Internet-routable address; connectivity also requires suitable routes and firewall rules |

Lifecycle: pending → running → stopping → stopped, or shutting-down → terminated. Stopping an EBS-backed instance preserves its volumes; termination deletes volumes configured for deletion on termination. Storage costs can continue while an instance is stopped.

Common uses: hosting websites, running application servers, development environments and batch jobs.

Sources: [EC2 concepts](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html), [IP addressing](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-instance-addressing.html), [Instance lifecycle](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html).
