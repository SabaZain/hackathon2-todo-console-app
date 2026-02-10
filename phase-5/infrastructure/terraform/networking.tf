# Networking Configuration

# DigitalOcean VPC
resource "digitalocean_vpc" "phase5" {
  count       = var.cloud_provider == "digitalocean" ? 1 : 0
  name        = "${var.project_name}-vpc-${var.environment}"
  region      = var.region
  ip_range    = var.vpc_cidr
  description = "VPC for Phase 5 ${var.environment} environment"
}

# Google Cloud VPC
resource "google_compute_network" "vpc" {
  count                   = var.cloud_provider == "gcp" ? 1 : 0
  name                    = "${var.project_name}-vpc-${var.environment}"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  count         = var.cloud_provider == "gcp" ? 1 : 0
  name          = "${var.project_name}-subnet-${var.environment}"
  ip_cidr_range = var.vpc_cidr
  region        = var.gcp_region
  network       = google_compute_network.vpc[0].id

  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.1.0.0/16"
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.2.0.0/16"
  }
}

# Google Cloud Firewall Rules
resource "google_compute_firewall" "allow_internal" {
  count   = var.cloud_provider == "gcp" ? 1 : 0
  name    = "${var.project_name}-allow-internal"
  network = google_compute_network.vpc[0].name

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "icmp"
  }

  source_ranges = [var.vpc_cidr]
}

# Azure Virtual Network
resource "azurerm_virtual_network" "phase5" {
  count               = var.cloud_provider == "azure" ? 1 : 0
  name                = "${var.project_name}-vnet-${var.environment}"
  location            = azurerm_resource_group.phase5[0].location
  resource_group_name = azurerm_resource_group.phase5[0].name
  address_space       = [var.vpc_cidr]

  tags = var.tags
}

resource "azurerm_subnet" "phase5" {
  count                = var.cloud_provider == "azure" ? 1 : 0
  name                 = "${var.project_name}-subnet-${var.environment}"
  resource_group_name  = azurerm_resource_group.phase5[0].name
  virtual_network_name = azurerm_virtual_network.phase5[0].name
  address_prefixes     = [var.vpc_cidr]
}

# Azure Network Security Group
resource "azurerm_network_security_group" "phase5" {
  count               = var.cloud_provider == "azure" ? 1 : 0
  name                = "${var.project_name}-nsg-${var.environment}"
  location            = azurerm_resource_group.phase5[0].location
  resource_group_name = azurerm_resource_group.phase5[0].name

  security_rule {
    name                       = "AllowHTTPS"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "AllowHTTP"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = var.tags
}

resource "azurerm_subnet_network_security_group_association" "phase5" {
  count                     = var.cloud_provider == "azure" ? 1 : 0
  subnet_id                 = azurerm_subnet.phase5[0].id
  network_security_group_id = azurerm_network_security_group.phase5[0].id
}
