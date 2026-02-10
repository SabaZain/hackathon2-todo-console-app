# Input Variables for Phase 5 Infrastructure

# General Configuration
variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  default     = "production"
}

variable "cloud_provider" {
  description = "Cloud provider to use (digitalocean, gcp, azure)"
  type        = string
  validation {
    condition     = contains(["digitalocean", "gcp", "azure"], var.cloud_provider)
    error_message = "Cloud provider must be one of: digitalocean, gcp, azure"
  }
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "phase5"
}

variable "region" {
  description = "Cloud region for resources"
  type        = string
}

# DigitalOcean Variables
variable "do_token" {
  description = "DigitalOcean API token"
  type        = string
  sensitive   = true
  default     = ""
}

variable "do_k8s_version" {
  description = "Kubernetes version for DOKS"
  type        = string
  default     = "1.28"
}

variable "do_node_size" {
  description = "Node size for DOKS"
  type        = string
  default     = "s-2vcpu-4gb"
}

variable "do_node_count" {
  description = "Number of nodes for DOKS"
  type        = number
  default     = 3
}

# Google Cloud Variables
variable "gcp_project_id" {
  description = "GCP project ID"
  type        = string
  default     = ""
}

variable "gcp_region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "gcp_zone" {
  description = "GCP zone"
  type        = string
  default     = "us-central1-a"
}

variable "gcp_machine_type" {
  description = "Machine type for GKE nodes"
  type        = string
  default     = "e2-standard-2"
}

variable "gcp_node_count" {
  description = "Number of nodes for GKE"
  type        = number
  default     = 3
}

# Azure Variables
variable "azure_subscription_id" {
  description = "Azure subscription ID"
  type        = string
  default     = ""
}

variable "azure_location" {
  description = "Azure location"
  type        = string
  default     = "East US"
}

variable "azure_vm_size" {
  description = "VM size for AKS nodes"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "azure_node_count" {
  description = "Number of nodes for AKS"
  type        = number
  default     = 3
}

# Database Variables
variable "db_instance_size" {
  description = "Database instance size"
  type        = string
  default     = "db-s-2vcpu-4gb" # DigitalOcean default
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "phase5_todo"
}

variable "db_user" {
  description = "Database username"
  type        = string
  default     = "phase5_user"
}

# Redis Variables
variable "redis_instance_size" {
  description = "Redis instance size"
  type        = string
  default     = "db-s-1vcpu-1gb" # DigitalOcean default
}

# Kafka Variables
variable "kafka_enabled" {
  description = "Enable managed Kafka (if available)"
  type        = bool
  default     = false
}

# Networking Variables
variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

# Tags
variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default = {
    Project     = "Phase5"
    ManagedBy   = "Terraform"
    Environment = "production"
  }
}

# Domain Configuration
variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = "phase5.example.com"
}

variable "enable_ssl" {
  description = "Enable SSL/TLS certificates"
  type        = bool
  default     = true
}

# Monitoring
variable "enable_monitoring" {
  description = "Enable monitoring stack (Prometheus, Grafana)"
  type        = bool
  default     = true
}
