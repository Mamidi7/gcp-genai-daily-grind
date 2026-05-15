# ──────────────────────────────────────────────
# Terraform GCP Infrastructure for AI/ML Serving
# ──────────────────────────────────────────────
# Hands-on exercise for GCP Data Engineering interviews.
# Run: terraform init → terraform plan → review → terraform apply
#
# Free tier safe:
#   - Cloud Run: 2M requests/mo free
#   - BigQuery: 1 TB/mo free
#   - GCS: 5 GB free
#   - Monitoring: free uptime checks
# ──────────────────────────────────────────────

terraform {
  required_version = ">= 1.6"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0, < 7.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Optional: store state in GCS bucket
# Uncomment after first `terraform apply` creates the bucket
# terraform {
#   backend "gcs" {
#     bucket = "terraform-state-ai-demo"
#     prefix = "terraform/state"
#   }
# }
