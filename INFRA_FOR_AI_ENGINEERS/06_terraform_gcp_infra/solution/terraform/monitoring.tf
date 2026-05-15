# ──────────────────────────────────────────────
# Monitoring — Uptime Checks + Alert Policies
# ──────────────────────────────────────────────

# Uptime check for Cloud Run endpoint
resource "google_monitoring_uptime_check_config" "cloud_run_health" {
  display_name = "AI Service Health Check"
  timeout      = "10s"
  period       = "60s"

  http_check {
    path         = "/healthz"
    port         = 443
    use_ssl      = true
    validate_ssl = true
  }

  monitored_resource {
    type = "uptime_url"
    labels = {
      host = google_cloud_run_service.ai_service.status[0].url
    }
  }

  depends_on = [google_cloud_run_service.ai_service]
}

# Alert if health check fails for 2 minutes
resource "google_monitoring_alert_policy" "service_down" {
  display_name = "AI Service Down Alert"
  combiner     = "OR"

  conditions {
    display_name = "Health check failure rate > 0"
    condition_threshold {
      filter     = "metric.type=\"monitoring.googleapis.com/uptime_check/check_passed\" AND resource.type=\"uptime_url\""
      duration   = "120s"
      comparison = "COMPARISON_GT"
      threshold_value = 0

      aggregations {
        alignment_period     = "60s"
        per_series_aligner   = "ALIGN_NEXT_OLDER"
        cross_series_reducer = "REDUCE_COUNT_FALSE"
      }

      trigger {
        count = 1
      }
    }
  }

  alert_strategy {
    auto_close = "3600s"
  }

  notification_channels = [google_monitoring_notification_channel.email.id]

  depends_on = [google_monitoring_uptime_check_config.cloud_run_health]
}

# Email notification channel
resource "google_monitoring_notification_channel" "email" {
  display_name = "Alert Email"
  type         = "email"
  labels = {
    email_address = var.alert_email
  }
}
