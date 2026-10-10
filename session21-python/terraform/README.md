# Azure homework infrastructure

One Ubuntu VM runs K3s. Terraform creates a VNet with two subnets, the VM, its network interface, a public IP and an NSG. SSH is restricted to `admin_cidr`; port 80 is for the frontend.

The selected VM is `Standard_B2als_v2` in Central India (2 vCPUs, 4 GB RAM). This is the requested Azure/K3s alternative to the original AWS/EKS rubric.

Copy `terraform.tfvars.example` to `terraform.tfvars` and fill in your subscription, public SSH key path and public IP. Sign in with `az login`, then run:

```bash
terraform init
terraform validate
terraform plan
terraform apply
```

After the demo:

```bash
terraform destroy
```

State files, keys and personal variable files stay out of Git.
