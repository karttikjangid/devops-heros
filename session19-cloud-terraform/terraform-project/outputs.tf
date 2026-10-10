output "resource_group" { value = azurerm_resource_group.homework.name }
output "storage_account" { value = azurerm_storage_account.homework.name }
output "container" { value = azurerm_storage_container.homework.name }
output "public_ip" { value = azurerm_public_ip.homework.ip_address }
output "web_url" { value = "http://${azurerm_public_ip.homework.ip_address}" }
output "vnet_id" { value = azurerm_virtual_network.homework.id }
