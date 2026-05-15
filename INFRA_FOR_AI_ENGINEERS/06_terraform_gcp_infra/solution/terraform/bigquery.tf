# ──────────────────────────────────────────────
# BigQuery — Vector Search Storage
# ──────────────────────────────────────────────
# Stores embeddings for similarity search.
# Dataset + table with partitioning and clustering.

resource "google_bigquery_dataset" "vector_store" {
  dataset_id  = var.bq_dataset_id
  description = "Vector store for AI embeddings and similarity search"
  location    = var.region

  labels = {
    env     = "dev"
    service = "ai-serving"
  }
}

resource "google_bigquery_table" "embeddings" {
  dataset_id = google_bigquery_dataset.vector_store.dataset_id
  table_id   = var.bq_table_name

  schema = jsonencode([
    { name = "id",          type = "STRING",  mode = "REQUIRED" },
    { name = "content",     type = "STRING",  mode = "REQUIRED" },
    { name = "embedding",   type = "FLOAT64", mode = "REPEATED" },
    { name = "metadata",    type = "STRING",  mode = "NULLABLE" },
    { name = "created_at",  type = "TIMESTAMP", mode = "NULLABLE" },
  ])

  clustering = ["id"]

  labels = {
    env     = "dev"
    service = "ai-serving"
  }

  depends_on = [google_bigquery_dataset.vector_store]
}
