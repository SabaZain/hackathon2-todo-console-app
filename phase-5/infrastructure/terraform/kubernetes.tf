# Kubernetes Cluster Configuration

# DigitalOcean Kubernetes Cluster
resource "digitalocean_kubernetes_cluster" "phase5" {
  count   = var.cloud_provider == "digitalocean" ? 1 : 0
  name    = "${var.project_name}-${var.environment}"
  region  = var.region
  version = var.do_k8s_version

  node_pool {
    name       = "${var.project_name}-worker-pool"
    size       = var.do_node_size
    node_count = var.do_node_count
    auto_scale = true
    min_nodes  = 2
    max_nodes  = 10
    tags       = [var.environment, "phase5"]
  }

  tags = [var.environment, "phase5", "kubernetes"]
}

# Google Kubernetes Engine Cluster
resource "google_container_cluster" "phase5" {
  count    = var.cloud_provider == "gcp" ? 1 : 0
  name     = "${var.project_name}-${var.environment}"
  location = var.gcp_zone

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.vpc[0].name
  subnetwork = google_compute_subnetwork.subnet[0].name

  workload_identity_config {
    workload_pool = "${var.gcp_project_id}.svc.id.goog"
  }

  addons_config {
    http_load_balancing {
      disabled = false
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
  }
}

resource "google_container_node_pool" "phase5_nodes" {
  count      = var.cloud_provider == "gcp" ? 1 : 0
  name       = "${var.project_name}-node-pool"
  location   = var.gcp_zone
  cluster    = google_container_cluster.phase5[0].name
  node_count = var.gcp_node_count

  autoscaling {
    min_node_count = 2
    max_node_count = 10
  }

  node_config {
    machine_type = var.gcp_machine_type
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      environment = var.environment
      project     = var.project_name
    }

    tags = ["phase5", var.environment]
  }
}

# Azure Kubernetes Service Cluster
resource "azurerm_kubernetes_cluster" "phase5" {
  count               = var.cloud_provider == "azure" ? 1 : 0
  name                = "${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.phase5[0].location
  resource_group_name = azurerm_resource_group.phase5[0].name
  dns_prefix          = "${var.project_name}-${var.environment}"

  default_node_pool {
    name                = "default"
    node_count          = var.azure_node_count
    vm_size             = var.azure_vm_size
    enable_auto_scaling = true
    min_count           = 2
    max_count           = 10
    vnet_subnet_id      = azurerm_subnet.phase5[0].id
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
  }

  tags = var.tags
}

# Azure Resource Group
resource "azurerm_resource_group" "phase5" {
  count    = var.cloud_provider == "azure" ? 1 : 0
  name     = "${var.project_name}-${var.environment}-rg"
  location = var.azure_location
  tags     = var.tags
}
