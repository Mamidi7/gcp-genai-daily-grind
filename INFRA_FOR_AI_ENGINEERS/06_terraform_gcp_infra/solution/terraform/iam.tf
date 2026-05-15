# ──────────────────────────────────────────────
# IAM — Service Accounts + Workload Identity
# ──────────────────────────────────────────────

# Service account that Cloud Run runs as
resource "google_service_account" "ai_workload" {
  account_id   = "ai-workload-sa"
  display_name = "AI Workload Service Account"
  description  = "Used by Cloud Run to access BQ, GCS, and Vertex AI"
}

# Grant BQ access
resource "google_project_iam_member" "bq_user" {
  project = var.project_id
  role    = "roles/bigquery.dataViewer"
  member  = "serviceAccount:${google_service_account.ai_workload.email}"
}

resource "google_project_iam_member" "bq_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.ai_workload.email}"
}

# Grant GCS access
resource "google_storage_bucket_iam_member" "gcs_object_viewer" {
  bucket = google_storage_bucket.ai_documents.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.ai_workload.email}"
}

resource "google_storage_bucket_iam_member" "gcs_object_creator" {
  bucket = google_storage_bucket.ai_documents.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.ai_workload.email}"
}
