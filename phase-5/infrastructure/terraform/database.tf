# Managed Database Configuration

# Random password for databases
resource "random_password" "db_password" {
  count   = var.cloud_provider != "digitalocean" ? 1 : 0
  length  = 32
  special = true
}

# DigitalOcean Managed PostgreSQL
resource "digitalocean_database_cluster" "postgres" {
  count      = var.cloud_provider == "digitalocean" ? 1 : 0
  name       = "${var.project_name}-postgres-${var.environment}"
  engine     = "pg"
  version    = "15"
  size       = var.db_instance_size
  region     = var.region
  node_count = 1

  tags = [var.environment, "phase5", "database"]
}

resource "digitalocean_database_db" "phase5" {
  count      = var.cloud_provider == "digitalocean" ? 1 : 0
  cluster_id = digitalocean_database_cluster.postgres[0].id
  name       = var.db_name
}

resource "digitalocean_database_user" "phase5" {
  count      = var.cloud_provider == "digitalocean" ? 1 : 0
  cluster_id = digitalocean_database_cluster.postgres[0].id
  name       = var.db_user
}

# Google Cloud SQL PostgreSQL
resource "google_sql_database_instance" "postgres" {
  count            = var.cloud_provider == "gcp" ? 1 : 0
  name             = "${var.project_name}-postgres-${var.environment}"
  database_version = "POSTGRES_15"
  region           = var.gcp_region

  settings {
    tier = "db-f1-micro" # Adjust as needed

    backup_configuration {
      enabled = true
    }

    ip_configuration {
      ipv4_enabled    = true
      private_network = google_compute_network.vpc[0].id
    }
  }

  deletion_protection = false
}

resource "google_sql_database" "phase5" {
  count    = var.cloud_provider == "gcp" ? 1 : 0
  name     = var.db_name
  instance = google_sql_database_instance.postgres[0].name
}

resource "google_sql_user" "phase5" {
  count    = var.cloud_provider == "gcp" ? 1 : 0
  name     = var.db_user
  instance = google_sql_database_instance.postgres[0].name
  password = random_password.db_password[0].result
}

# Azure PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "postgres" {
  count               = var.cloud_provider == "azure" ? 1 : 0
  name                = "${var.project_name}-postgres-${var.environment}"
  resource_group_name = azurerm_resource_group.phase5[0].name
  location            = azurerm_resource_group.phase5[0].location
  version             = "15"
  administrator_login = var.db_user
  administrator_password = random_password.db_password[0].result

  storage_mb = 32768
  sku_name   = "B_Standard_B1ms"

  backup_retention_days = 7

  tags = var.tags
}

resource "azurerm_postgresql_flexible_server_database" "phase5" {
  count     = var.cloud_provider == "azure" ? 1 : 0
  name      = var.db_name
  server_id = azurerm_postgresql_flexible_server.postgres[0].id
  collation = "en_US.utf8"
  charset   = "utf8"
}
