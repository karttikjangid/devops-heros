variable "subscription_id" { type = string }
variable "ssh_public_key_path" { type = string }
variable "admin_cidr" {
  type = string
  validation {
    condition     = can(cidrhost(var.admin_cidr, 0)) && endswith(var.admin_cidr, "/32")
    error_message = "Use your public IPv4 address with /32 to restrict SSH."
  }
}
variable "location" {
  default = "centralindia"
}
variable "vm_size" {
  default = "Standard_B2als_v2"
}
variable "name" {
  default = "session21-homework"
}
