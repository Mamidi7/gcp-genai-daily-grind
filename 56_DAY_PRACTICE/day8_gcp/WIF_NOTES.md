# 🔐 Workload Identity Federation (WIF) - Real World Debugging

**Date:** Day 8 of 56 Day Practice
**Topic:** Connecting GitHub to Google Cloud securely (without service account keys).

## The Scenario
We tried to reuse an existing WIF Pool (`github-pools`) for our new repository (`gcp-genai-daily-grind`). 
When we checked the WIF Provider configuration, we found this:

```yaml
attributeCondition: assertion.repository == "Mamidi7/legal-ai-agent"
```

## The Problem (The 403 Forbidden Trap)
This is the **Gatekeeper**. It looks at the incoming GitHub token and says: 
*"I will ONLY allow the `legal-ai-agent` repository to enter GCP. If any other repo tries to deploy, I will immediately block them with a 403 Permission Denied error."*

If we had blindly run our GitHub Action pipeline in our new repo, it would have failed completely.

## The Fix
We must update the `attributeCondition` in the WIF Provider to allow multiple repositories, or change it to allow the specific one we are working on.

```text
assertion.repository == "Mamidi7/legal-ai-agent" || assertion.repository == "Mamidi7/gcp-genai-daily-grind"
```

## 🎤 The Interview Punchline (Memorize This)
> "When setting up CI/CD pipelines, I never download Service Account JSON keys. I use Workload Identity Federation (WIF). To ensure strict security, I configure the **attributeCondition** on the OIDC provider to strictly match the exact GitHub repository name. This prevents unauthorized repositories in the same GitHub organization from deploying into production."
## The Enterprise CI/CD Flow (For Future Reference)
When we are ready for MLOps (Phase 5), this is the exact architecture we will use to automate deployments without storing JSON keys in GitHub.

1. **The Code:** We create `.github/workflows/deploy.yml`
2. **The Authentication:** We use `google-github-actions/auth` passing the WIF Provider name.
3. **The Deployment:** We use `google-github-actions/deploy-cloudrun` to ship the code.

### Required IAM Roles for the Service Account:
For WIF to successfully deploy to Cloud Run, the Service Account must have:
- `roles/run.admin` (Cloud Run Admin)
- `roles/iam.serviceAccountUser` (Service Account User)
- `roles/artifactregistry.writer` (Artifact Registry Writer)
- `roles/storage.admin` (If using Cloud Build behind the scenes)

We will revisit this when we do Agentic MLOps!
