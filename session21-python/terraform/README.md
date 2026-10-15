# Azure homework infrastructure

One Ubuntu VM runs K3s. Terraform creates a VNet with two subnets, the VM, its network interface, a public IP and an NSG. SSH is restricted to `admin_cidr`; port 80 is for the frontend.

The selected VM is `Standard_B2als_v2` in Central India (2 vCPUs, 4 GB RAM). Used Azure/K3s for the cloud part in place of the original AWS/EKS setup.

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

## Connect to K3s for a presentation

This is an optional replay that creates billable resources. Use the same small VM, collect the demo, then destroy it. The 15 October review did not provision another VM.

After `terraform apply`, from this directory set `SSH_KEY` to the private key matching `ssh_public_key_path`:

```bash
VM_IP=$(terraform output -raw public_ip)
SSH_KEY=/absolute/path/to/private-key
ssh -i "$SSH_KEY" student@"$VM_IP" 'sudo cloud-init status --wait && sudo k3s kubectl get nodes'
umask 077
mkdir -p ~/.kube
ssh -i "$SSH_KEY" student@"$VM_IP" 'sudo cat /etc/rancher/k3s/k3s.yaml' \
  | sed 's/127.0.0.1:6443/127.0.0.1:16443/' > ~/.kube/session21-capstone
chmod 600 ~/.kube/session21-capstone
ssh -i "$SSH_KEY" -N -L 16443:127.0.0.1:6443 student@"$VM_IP"
```

Keep that SSH tunnel open. In another terminal, use a session-specific kubeconfig so other coursework contexts stay separate:

```bash
export KUBECONFIG=~/.kube/session21-capstone
kubectl get nodes
cd /path/to/devops-heros/session21-python
helm upgrade --install homework ./helm/taskboard -n session21 --create-namespace \
  --set ingress.className=traefik --set ingress.host='' --wait --timeout 180s
kubectl -n session21 get pods,svc,ingress,hpa,pvc
```

The chart's SHA tags identify the reviewed release. To demonstrate an update, override both image tags with the successful pipeline's SHA. Open `http://<VM_IP>` to check Ingress. Port 6443 stays private; the tunnel uses the allowed SSH connection.

The copied kubeconfig contains cluster-admin credentials. Keep it outside Git. Follow the [K3s cluster-access documentation](https://docs.k3s.io/cluster-access) when refreshing it.

When finished, stop the tunnel, run `terraform destroy` from this directory, and verify `az group exists --name session21-homework` returns `false`.
