# ──────────────────────────────────────────────
# Cloud Run — Model Serving Endpoint
# ──────────────────────────────────────────────
# Serverless container for FastAPI model serving.

resource "google_cloud_run_service" "ai_service" {
  name     = var.service_name
  location = var.region

  template {
    spec {
      containers {
        image = var.container_image

        resources {
          limits = {
            cpu    = "1"
            memory = "512Mi"
          }
        }

        env {
          name  = "PROJECT_ID"
          value = var.project_id
        }

        env {
          name  = "LOG_LEVEL"
          value = "INFO"
        }

        startup_probe {
          http_get {
            path = "/healthz"
          }
          initial_delay_seconds = 10
          timeout_seconds       = 3
          period_seconds        = 5
          failure_threshold     = 3
        }

        liveness_probe {
          http_get {
            path = "/readyz"
          }
          initial_delay_seconds = 30
          timeout_seconds       = 3
          period_seconds        = 10
          failure_threshold     = 3
        }
      }

      service_account_name = google_service_account.ai_workload.email
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale"      = "5"
        "autoscaling.knative.dev/minScale"      = "0"
        "run.googleapis.com/cpu-throttling"     = "true"
        "run.googleapis.com/ingress"            = "internal-and-cloud-load-balancing"
      }
    }
  }

  autogenerate_revision_name = true

  depends_on = [google_service_account.ai_workload]
}

# Allow unauthenticated invocations (for internal services)
# Remove this if using IAP/Gateway for auth
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",  # → change to specific SA for production
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.ai_service.location
  project  = google_cloud_run_service.ai_service.project
  service  = google_cloud_run_service.ai_service.name

  policy_data = data.google_iam_policy.noauth.policy_data
}
