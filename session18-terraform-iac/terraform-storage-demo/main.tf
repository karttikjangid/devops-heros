resource "azurerm_resource_group" "homework" {
  name     = "session18-homework"
  location = var.location
  tags     = { session = "18", managed_by = "Terraform" }
}

resource "azurerm_storage_account" "homework" {
  name                            = var.storage_account_name
  resource_group_name             = azurerm_resource_group.homework.name
  location                        = azurerm_resource_group.homework.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  account_kind                    = "StorageV2"
  access_tier                     = "Hot"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
}

resource "azurerm_storage_container" "homework" {
  name                  = "homework"
  storage_account_id    = azurerm_storage_account.homework.id
  container_access_type = "private"
}
