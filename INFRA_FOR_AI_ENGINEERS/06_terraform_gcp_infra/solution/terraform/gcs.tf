# ──────────────────────────────────────────────
# GCS Bucket — Raw Document Storage
# ──────────────────────────────────────────────
# Stores uploaded documents, training data, etc.

resource "google_storage_bucket" "ai_documents" {
  name          = "${var.project_id}-${var.gcs_bucket_name}"
  location      = var.region
  storage_class = "STANDARD"
  force_destroy = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  labels = {
    env     = "dev"
    service = "ai-serving"
  }
}
