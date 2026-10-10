# Azure Virtual Machines - Compute

An Azure VM is a virtual server with a chosen operating-system image, size, disks and network interface.

| Concept | Meaning |
| --- | --- |
| Image | The operating-system template; this demo uses Ubuntu 22.04 |
| VM size | CPU and memory capacity; the demo uses a permitted small B-series size |
| SSH keys | Public/private key pair for Linux login; the private key stays local |
| NSG | Stateful inbound and outbound network rules |
| Managed disk | Persistent OS or data storage; this demo uses Standard LRS |
| Private IP | Address inside the virtual network |
| Public IP | Internet-routable address, subject to NSG rules |

A VM can be created, started, stopped, deallocated and deleted. Stopping inside the guest can leave it allocated and billed. Deallocation releases compute capacity, but retained disks and networking can still incur charges. Delete the complete demo infrastructure after testing.

Common uses: web servers, development machines and applications needing control over the operating system.

Sources: [VM states and billing](https://learn.microsoft.com/en-us/azure/virtual-machines/states-billing), [Linux VM overview](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/overview).
