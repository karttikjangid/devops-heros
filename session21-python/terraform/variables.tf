variable "subscription_id" { type = string }
variable "ssh_public_key_path" { type = string }
variable "admin_cidr" { type = string }
variable "location" {
  default = "centralindia"
}
variable "vm_size" {
  default = "Standard_B2als_v2"
}
variable "name" {
  default = "session21-homework"
}
