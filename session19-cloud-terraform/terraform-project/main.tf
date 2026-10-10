resource "azurerm_resource_group" "homework" {
  name     = "session19-homework"
  location = var.location
  tags     = { session = "19", managed_by = "Terraform" }
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

resource "azurerm_virtual_network" "homework" {
  name                = "session19-vnet"
  location            = var.location
  resource_group_name = azurerm_resource_group.homework.name
  address_space       = ["10.19.0.0/16"]
}
resource "azurerm_subnet" "nodes" {
  name                 = "nodes"
  resource_group_name  = azurerm_resource_group.homework.name
  virtual_network_name = azurerm_virtual_network.homework.name
  address_prefixes     = ["10.19.1.0/24"]
}
resource "azurerm_network_security_group" "homework" {
  name                = "homework-nsg"
  location            = var.location
  resource_group_name = azurerm_resource_group.homework.name
  security_rule {
    name                       = "SSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = var.admin_cidr
    destination_address_prefix = "*"
  }
  security_rule {
    name                       = "Frontend"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}
resource "azurerm_public_ip" "homework" {
  name                = "homework-ip"
  location            = var.location
  resource_group_name = azurerm_resource_group.homework.name
  allocation_method   = "Static"
  sku                 = "Standard"
}
resource "azurerm_network_interface" "homework" {
  name                = "homework-nic"
  location            = var.location
  resource_group_name = azurerm_resource_group.homework.name
  ip_configuration {
    name                          = "primary"
    subnet_id                     = azurerm_subnet.nodes.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.homework.id
  }
}
resource "azurerm_network_interface_security_group_association" "homework" {
  network_interface_id      = azurerm_network_interface.homework.id
  network_security_group_id = azurerm_network_security_group.homework.id
}
resource "azurerm_linux_virtual_machine" "homework" {
  name                  = "session19-web"
  location              = var.location
  resource_group_name   = azurerm_resource_group.homework.name
  size                  = var.vm_size
  admin_username        = "student"
  network_interface_ids = [azurerm_network_interface.homework.id]
  admin_ssh_key {
    username   = "student"
    public_key = file(var.ssh_public_key_path)
  }
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
    disk_size_gb         = 32
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }
  custom_data = base64encode(file("${path.module}/cloud-init.yaml"))
  depends_on  = [azurerm_network_interface_security_group_association.homework]
}
