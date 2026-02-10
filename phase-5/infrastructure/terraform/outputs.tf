# Output Values

# Kubernetes Cluster Outputs
output "kubernetes_cluster_name" {
  description = "Kubernetes cluster name"
  value = (
    var.cloud_provider == "digitalocean" ? try(digitalocean_kubernetes_cluster.phase5[0].name, "") :
    var.cloud_provider == "gcp" ? try(google_container_cluster.phase5[0].name, "") :
    var.cloud_provider == "azure" ? try(azurerm_kubernetes_cluster.phase5[0].name, "") :
    ""
  )
}

output "kubernetes_cluster_endpoint" {
  description = "Kubernetes cluster endpoint"
  value = (
    var.cloud_provider == "digitalocean" ? try(digitalocean_kubernetes_cluster.phase5[0].endpoint, "") :
    var.cloud_provider == "gcp" ? try(google_container_cluster.phase5[0].endpoint, "") :
    var.cloud_provider == "azure" ? try(azurerm_kubernetes_cluster.phase5[0].kube_config[0].host, "") :
    ""
  )
  sensitive = true
}

output "kubernetes_cluster_id" {
  description = "Kubernetes cluster ID"
  value = (
    var.cloud_provider == "digitalocean" ? try(digitalocean_kubernetes_cluster.phase5[0].id, "") :
    var.cloud_provider == "gcp" ? try(google_container_cluster.phase5[0].id, "") :
    var.cloud_provider == "azure" ? try(azurerm_kubernetes_cluster.phase5[0].id, "") :
    ""
  )
}

# Database Outputs
output "database_host" {
  description = "Database host"
  value = (
    var.cloud_provider == "digitalocean" ? try(digitalocean_database_cluster.postgres[0].host, "") :
    var.cloud_provider == "gcp" ? try(google_sql_database_instance.postgres[0].connection_name, "") :
    var.cloud_provider == "azure" ? try(azurerm_postgresql_flexible_server.postgres[0].fqdn, "") :
    ""
  )
  sensitive = true
}

output "database_port" {
  description = "Database port"
  value = (
    var.cloud_provider == "digitalocean" ? try(digitalocean_database_cluster.postgres[0].port, 5432) :
    5432
  )
}

output "database_name" {
  description = "Database name"
  value = var.db_name
}

output "database_user" {
  description = "Database username"
  value     = var.db_user
  sensitive = true
}

output "database_password" {
  description = "Database password"
  value = (
    var.cloud_provider == "digitalocean" ? try(digitalocean_database_cluster.postgres[0].password, "") :
    var.cloud_provider == "gcp" ? try(random_password.db_password[0].result, "") :
    var.cloud_provider == "azure" ? try(random_password.db_password[0].result, "") :
    ""
  )
  sensitive = true
}

output "database_connection_string" {
  description = "Database connection string"
  value = (
    var.cloud_provider == "digitalocean" ? try(digitalocean_database_cluster.postgres[0].uri, "") :
    var.cloud_provider == "gcp" ? "postgresql://${var.db_user}:${random_password.db_password[0].result}@${google_sql_database_instance.postgres[0].connection_name}/${var.db_name}" :
    var.cloud_provider == "azure" ? "postgresql://${var.db_user}:${random_password.db_password[0].result}@${azurerm_postgresql_flexible_server.postgres[0].fqdn}:5432/${var.db_name}" :
    ""
  )
  sensitive = true
}

# Redis Outputs
output "redis_host" {
  description = "Redis host"
  value = (
    var.cloud_provider == "digitalocean" ? try(digitalocean_database_cluster.redis[0].host, "") :
    var.cloud_provider == "gcp" ? try(google_redis_instance.redis[0].host, "") :
    var.cloud_provider == "azure" ? try(azurerm_redis_cache.redis[0].hostname, "") :
    ""
  )
  sensitive = true
}

output "redis_port" {
  description = "Redis port"
  value = (
    var.cloud_provider == "digitalocean" ? try(digitalocean_database_cluster.redis[0].port, 6379) :
    var.cloud_provider == "gcp" ? try(google_redis_instance.redis[0].port, 6379) :
    var.cloud_provider == "azure" ? try(azurerm_redis_cache.redis[0].ssl_port, 6380) :
    6379
  )
}

# Networking Outputs
output "vpc_id" {
  description = "VPC ID"
  value = (
    var.cloud_provider == "digitalocean" ? try(digitalocean_vpc.phase5[0].id, "") :
    var.cloud_provider == "gcp" ? try(google_compute_network.vpc[0].id, "") :
    var.cloud_provider == "azure" ? try(azurerm_virtual_network.phase5[0].id, "") :
    ""
  )
}

# Application URLs
output "frontend_url" {
  description = "Frontend application URL"
  value       = "https://app.${var.domain_name}"
}

output "backend_url" {
  description = "Backend API URL"
  value       = "https://api.${var.domain_name}"
}

# Kubectl Configuration Command
output "kubectl_config_command" {
  description = "Command to configure kubectl"
  value = (
    var.cloud_provider == "digitalocean" ? "doctl kubernetes cluster kubeconfig save ${digitalocean_kubernetes_cluster.phase5[0].name}" :
    var.cloud_provider == "gcp" ? "gcloud container clusters get-credentials ${google_container_cluster.phase5[0].name} --zone ${var.gcp_zone} --project ${var.gcp_project_id}" :
    var.cloud_provider == "azure" ? "az aks get-credentials --resource-group ${azurerm_resource_group.phase5[0].name} --name ${azurerm_kubernetes_cluster.phase5[0].name}" :
    ""
  )
}

# Helm Installation Commands
output "helm_install_commands" {
  description = "Commands to install Helm charts"
  value = <<-EOT
    # Install backend
    helm install phase5-backend ./infrastructure/helm/backend \
      --set database.url="${self.database_connection_string}" \
      --set redis.host="${self.redis_host}" \
      --set redis.port="${self.redis_port}"

    # Install frontend
    helm install phase5-frontend ./infrastructure/helm/frontend \
      --set config.nextPublicApiUrl="https://api.${var.domain_name}" \
      --set config.nextPublicWsUrl="wss://api.${var.domain_name}"

    # Install agents
    helm install phase5-agents ./infrastructure/helm/agents \
      --set database.url="${self.database_connection_string}"
  EOT
}
