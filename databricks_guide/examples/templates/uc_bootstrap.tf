# Minimal platform example. Authentication uses protected unified-auth values.
# Run in its own Terraform project with a reviewed provider lock and backend.
terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "= 1.137.0"
    }
  }
}
variable "workspace_host" { type = string }
variable "catalog_name" {
  type    = string
  default = "de_lab_dev"
}
variable "managed_storage_root" {
  type        = string
  description = "Approved non-overlapping cloud path under an external location"
}
provider "databricks" { host = var.workspace_host }
resource "databricks_catalog" "lab" {
  name         = var.catalog_name
  storage_root = var.managed_storage_root
  comment      = "Development data engineering lab"
}
resource "databricks_schema" "bronze" {
  catalog_name = databricks_catalog.lab.name
  name         = "bronze"
}
# Add reviewed ops/silver/gold, credentials, locations, bindings and grants through
# the platform design. This example alone is not the full lab bootstrap.
