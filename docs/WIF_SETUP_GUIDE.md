# GCP Workload Identity Federation (WIF) Setup - The "Visitor Pass" 🎟️

**Analogy time, Boss!** 🎬
Old way (JSON Keys): Giving your house key to a friend. If they lose it, anyone can enter. ❌
New way (WIF): Giving the security guard a list. "If someone comes from GitHub with a valid ID card, let them in for 1 hour." ✅

## Phase 1: Enable the "Gatekeeper" API 🚪
1.  Go to **APIs & Services > Library**.
2.  Search for **"IAM Service Account Credentials API"**.
3.  Click **Enable**. (This lets the temporary tokens be created).

## Phase 2: Create the "Visitor Pool" 🏊‍♂️
1.  Go to **IAM & Admin > Workload Identity Federation**.
2.  Click **+ CREATE POOL**.
3.  **Name:** `github-pool`.
4.  **Description:** "Pool for GitHub Actions".
5.  **Step 1 (Pool):** Click **CONTINUE**.

## Phase 3: Add the "Provider" (The ID Checker) 🆔
1.  **Select a provider:** `OpenID Connect (OIDC)`.
2.  **Provider Name:** `github-provider`.
3.  **Issuer (URL):** `https://token.actions.githubusercontent.com` (Copy exact!).
4.  **Audiences:** Default is fine (leave as is, or use `https://github.com/YourUsername/YourRepo`).
5.  **Attribute Mapping:** (Crucial Step! ⚠️)
    -   `google.subject` -> `assertion.sub`
    -   `attribute.actor` -> `assertion.actor`
    -   `attribute.repository` -> `assertion.repository`
6.  Click **SAVE**.

## Phase 4: Grant Access to the Service Account 🤝
1.  Go back to the Pool you just created.
2.  Click **GRANT ACCESS**.
3.  **Select Service Account:** Choose the one you want GitHub to use (e.g., `github-deployer` or create a new one).
4.  **Select Principals:**
    -   "PrincipalSet"
    -   Value: `principalSet://iam.googleapis.com/projects/YOUR_PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/YourUsername/YourRepo`
    -   (Or simply select "All repositories in this pool" for testing).
5.  Click **SAVE**.
6.  **Download the Config:** A file `github-actions-setup.yaml` or similar will be generated. Keep this safe! We need the values for GitHub Secrets.

---
**Ready to execute, Boss?** Open the console and tell me when you're done with Phase 1! 🚀
