# Managed Redis Configuration

# DigitalOcean Managed Redis
resource "digitalocean_database_cluster" "redis" {
  count      = var.cloud_provider == "digitalocean" ? 1 : 0
  name       = "${var.project_name}-redis-${var.environment}"
  engine     = "redis"
  version    = "7"
  size       = var.redis_instance_size
  region     = var.region
  node_count = 1

  tags = [var.environment, "phase5", "redis"]
}

# Google Cloud Memorystore Redis
resource "google_redis_instance" "redis" {
  count          = var.cloud_provider == "gcp" ? 1 : 0
  name           = "${var.project_name}-redis-${var.environment}"
  tier           = "BASIC"
  memory_size_gb = 1
  region         = var.gcp_region

  authorized_network = google_compute_network.vpc[0].id

  redis_version = "REDIS_7_0"

  display_name = "Phase 5 Redis"
}

# Azure Cache for Redis
resource "azurerm_redis_cache" "redis" {
  count               = var.cloud_provider == "azure" ? 1 : 0
  name                = "${var.project_name}-redis-${var.environment}"
  location            = azurerm_resource_group.phase5[0].location
  resource_group_name = azurerm_resource_group.phase5[0].name
  capacity            = 0
  family              = "C"
  sku_name            = "Basic"
  enable_non_ssl_port = false
  minimum_tls_version = "1.2"

  redis_configuration {
  }

  tags = var.tags
}
