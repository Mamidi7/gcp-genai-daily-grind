# ──────────────────────────────────────────────
# Variables — EDIT terraform.tfvars (gitignored)
# ──────────────────────────────────────────────

variable "project_id" {
  description = "Your GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Cloud Run service name"
  type        = string
  default     = "ai-model-serving"
}

variable "container_image" {
  description = "Container image URL (Artifact Registry or Docker Hub)"
  type        = string
  default     = "us-central1-docker.pkg.dev/cloudrun/container/hello"
}

variable "bq_dataset_id" {
  description = "BigQuery dataset ID for vector search"
  type        = string
  default     = "vector_store"
}

variable "bq_table_name" {
  description = "BigQuery table name for embeddings"
  type        = string
  default     = "embeddings"
}

variable "gcs_bucket_name" {
  description = "GCS bucket for raw documents"
  type        = string
  default     = "ai-documents-storage"
}

variable "alert_email" {
  description = "Email for monitoring alerts"
  type        = string
  default     = "alert@example.com"
}
