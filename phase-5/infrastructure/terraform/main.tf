# Phase 5 - Terraform Infrastructure Configuration
# Multi-cloud support for DOKS, GKE, and AKS

terraform {
  required_version = ">= 1.0"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
  }

  backend "s3" {
    # Configure your backend here
    # bucket = "phase5-terraform-state"
    # key    = "phase5/terraform.tfstate"
    # region = "us-east-1"
  }
}

# DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
  count = var.cloud_provider == "digitalocean" ? 1 : 0
}

# Google Cloud Provider
provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
  count   = var.cloud_provider == "gcp" ? 1 : 0
}

# Azure Provider
provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
  count           = var.cloud_provider == "azure" ? 1 : 0
}

# Kubernetes Provider (configured after cluster creation)
provider "kubernetes" {
  host                   = local.kubernetes_host
  token                  = local.kubernetes_token
  cluster_ca_certificate = base64decode(local.kubernetes_ca_cert)
}

# Helm Provider
provider "helm" {
  kubernetes {
    host                   = local.kubernetes_host
    token                  = local.kubernetes_token
    cluster_ca_certificate = base64decode(local.kubernetes_ca_cert)
  }
}

# Local variables for provider configuration
locals {
  kubernetes_host = (
    var.cloud_provider == "digitalocean" ? try(digitalocean_kubernetes_cluster.phase5[0].endpoint, "") :
    var.cloud_provider == "gcp" ? try("https://${google_container_cluster.phase5[0].endpoint}", "") :
    var.cloud_provider == "azure" ? try(azurerm_kubernetes_cluster.phase5[0].kube_config[0].host, "") :
    ""
  )

  kubernetes_token = (
    var.cloud_provider == "digitalocean" ? try(digitalocean_kubernetes_cluster.phase5[0].kube_config[0].token, "") :
    var.cloud_provider == "gcp" ? try(data.google_client_config.default[0].access_token, "") :
    var.cloud_provider == "azure" ? try(azurerm_kubernetes_cluster.phase5[0].kube_config[0].password, "") :
    ""
  )

  kubernetes_ca_cert = (
    var.cloud_provider == "digitalocean" ? try(digitalocean_kubernetes_cluster.phase5[0].kube_config[0].cluster_ca_certificate, "") :
    var.cloud_provider == "gcp" ? try(google_container_cluster.phase5[0].master_auth[0].cluster_ca_certificate, "") :
    var.cloud_provider == "azure" ? try(azurerm_kubernetes_cluster.phase5[0].kube_config[0].cluster_ca_certificate, "") :
    ""
  )
}

# Data source for GCP
data "google_client_config" "default" {
  count = var.cloud_provider == "gcp" ? 1 : 0
}
