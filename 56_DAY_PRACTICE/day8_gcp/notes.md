# Day 8 Notes - GCP + First Cloud Deployment

## What I Learned Today

### GCP Basics
- **Project**: Container for all GCP resources
- **Region**: Geographic location (e.g., us-central1, asia-south1)
- **Zone**: Specific data center within a region
- **Cloud Run**: Serverless container platform

### Cloud Run Key Points
- Auto-scales from 0 to 1000+ instances
- Pay only for what you use
- No infrastructure management
- Supports any containerized app

### Deployment Steps
1. Install gcloud CLI: `brew install google-cloud-sdk`
2. Authenticate: `gcloud auth login`
3. Set project: `gcloud config set project YOUR_PROJECT`
4. Enable API: `gcloud services enable run.googleapis.com`
5. Deploy: `gcloud run deploy --source . --region us-central1`

## Interview Answers

**Q: What is Cloud Run?**
> Cloud Run is a fully managed serverless platform that runs containers. It automatically scales from zero to handle traffic, and you only pay for the resources you use.

**Q: Why use containers?**
> Containers package your app with all dependencies, ensuring consistent behavior across dev, test, and production environments.

## Questions to Review
- [ ] Difference between Region and Zone
- [ ] How Cloud Run auto-scaling works
- [ ] Cloud Run pricing model

## Next Steps
- Day 9: GCS (Google Cloud Storage)
- Keep practicing deployments!
