variable "subscription_id" { type = string }
variable "storage_account_name" { type = string }
variable "location" { default = "centralindia" }
variable "ssh_public_key_path" { type = string }
variable "admin_cidr" { type = string }
variable "vm_size" { default = "Standard_B2als_v2" }
