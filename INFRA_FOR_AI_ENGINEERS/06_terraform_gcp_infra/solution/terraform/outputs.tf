# ──────────────────────────────────────────────
# Outputs — printed after `terraform apply`
# ──────────────────────────────────────────────

output "cloud_run_url" {
  description = "URL of the deployed Cloud Run service"
  value       = google_cloud_run_service.ai_service.status[0].url
}

output "gcs_bucket" {
  description = "GCS bucket for document storage"
  value       = google_storage_bucket.ai_documents.name
}

output "bq_dataset" {
  description = "BigQuery dataset ID"
  value       = google_bigquery_dataset.vector_store.dataset_id
}

output "bq_table" {
  description = "BigQuery table for embeddings"
  value       = google_bigquery_table.embeddings.table_id
}

output "service_account" {
  description = "Service account email for workload identity"
  value       = google_service_account.ai_workload.email
}
