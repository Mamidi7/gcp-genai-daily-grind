# Exercise 6: Terraform GCP Infrastructure for AI

## Goal (one line)
Define your entire GCP AI infrastructure as code: Cloud Run, Vertex AI, BigQuery, GCS, IAM.

## Why This Matters
Interview question: "How do you manage your cloud infrastructure?"
Bad: "I click through the GCP console."
Good: "Everything is in Terraform — VPC, IAM roles, Cloud Run services, Vertex AI endpoints,
BigQuery datasets. We review infra changes in PRs just like code."

## What You Build

### 1. Terraform modules (one file per resource)
```
terraform/
├── main.tf          # provider + project config
├── variables.tf     # project_id, region, model_name
├── outputs.tf       # service_url, endpoint_id
├── cloud_run.tf     # model serving service
├── bigquery.tf      # vector search dataset + table
├── gcs.tf           # document storage bucket
├── vertex_ai.tf     # model endpoint + index
├── iam.tf           # service accounts + roles
└── monitoring.tf    # uptime checks + alert policies
```

### 2. Key GCP Resources for AI
```
google_cloud_run_service        → model serving
google_bigquery_dataset         → vector search storage
google_bigquery_table           → embeddings table
google_storage_bucket           → raw documents
google_vertex_ai_endpoint       → model deployment
google_service_account          → workload identity
google_monitoring_alert_policy  → latency/error alerts
```

## Architecture
```
┌─ Terraform Plan ──────────────────────────────┐
│                                               │
│  terraform apply                              │
│       │                                       │
│       ├──→ VPC + Subnet (networking)          │
│       ├──→ GCS Bucket (document store)        │
│       ├──→ BigQuery Dataset (embeddings)      │
│       ├──→ Cloud Run (model serving)          │
│       ├──→ Vertex AI Endpoint (model deploy)  │
│       ├──→ Service Account (WIF auth)         │
│       └──→ Monitoring Alerts (p99 > 2s)       │
│                                               │
│  terraform output → service_url, endpoint_id  │
└───────────────────────────────────────────────┘
```

## Free Tier Constraints
- Cloud Run: 2 million requests/month free
- BigQuery: 1 TB query/month free
- GCS: 5 GB free
- Vertex AI: predict costs money (use sparingly)
- Terraform: free (it's just API calls)

## Common Mistake
Hardcoding project IDs and regions.
Fix: Use variables + terraform.tfvars (gitignored).

## Check Question
Why is `terraform plan` important before `terraform apply`?
(Answer: plan shows you exactly what will change — create, modify, destroy.
You can catch mistakes BEFORE they hit your infrastructure.)

## Tiny Exercise
1. Install terraform: `brew install terraform`
2. `cd solution/terraform && terraform init`
3. `terraform plan` — review what it would create
4. DO NOT apply yet (costs money). Just review the plan output.
5. Write the plan output in your debug journal.
