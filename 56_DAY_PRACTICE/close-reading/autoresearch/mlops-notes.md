# Autoresearch - MLOps Project Ideas (Phase 3)

---

## Phase 3: MLOps Pipeline Projects

Phase 3 (Days 29-42) is all about **production ML pipelines**. Autoresearch concepts map perfectly to:

| Project | GCP Service | Difficulty |
|--------|-------------|------------|
| AutoML Hyperparameter Tuning | Vertex AI Vizier | ⭐⭐ |
| Experiment Tracker | Cloud Logging + BigQuery | ⭐⭐ |
| Overnight Training Pipeline | Cloud Scheduler + Vertex AI | ⭐⭐⭐ |

---

## Project 1: AutoML Hyperparameter Tuner

### Concept
Build a system that automatically tries different hyperparameters and keeps the best.

### Architecture
```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ Cloud       │───▶│ Vertex AI    │───▶│ BigQuery    │
│ Scheduler   │    │ Training     │    │ Results     │
└─────────────┘    └──────────────┘    └─────────────┘
       │                  │                   │
       │ Nightly          │ Runs experiments  │ Stores val_bpb
       ▼                  ▼                   ▼
   Triggers 5pm      Each job = 5 min    Compare runs
```

### Steps
1. **Define search space** in JSON (LR, batch size, model size)
2. **Create training container** with your model code
3. **Set up Vizier** for hyperparameter search
4. **Schedule nightly** runs with Cloud Scheduler
5. **Store results** in BigQuery for analysis

### GCP Services Used
- Vertex AI Training
- Vertex AI Vizier
- BigQuery
- Cloud Scheduler

---

## Project 2: Experiment Tracker

### Concept
Like Weights & Biases (W&B) but on GCP.

### Features to Build
- Log metrics (loss, val_bpb, etc.)
- Log hyperparameters
- Compare runs
- Alert on degradation

### Simple Implementation
```python
import logging
from google.cloud import logging as cloud_logging

# Log to Cloud Logging
logger = cloud_logging.Client().logger("experiment_metrics")

def log_experiment(step, loss, val_bpb, params):
    logger.log_struct({
        "step": step,
        "train_loss": loss,
        "val_bpb": val_bpb,
        "hyperparams": params,
        "timestamp": datetime.now().isoformat()
    })
```

### GCP Services Used
- Cloud Logging
- BigQuery (for analytics)
- Cloud Monitoring (for alerts)

---

## Project 3: Overnight Training Pipeline

### Concept
Full autoresearch-style loop on GCP.

### Architecture
```
                    ┌──────────────────┐
                    │ Cloud Scheduler  │
                    │ (5pm daily)      │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ Cloud Run       │
                    │ (Orchestrator)  │
                    └────────┬─────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼────┐         ┌────▼────┐         ┌────▼────┐
    │ Job 1  │         │ Job 2  │         │ Job 3  │
    │ 5 min  │         │ 5 min  │         │ 5 min  │
    └────┬────┘         └────┬────┘         └────┬────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                    ┌────────▼─────────┐
                    │ BigQuery         │
                    │ (Results + Best) │
                    └──────────────────┘
```

### Key Components

| Component | GCP Service | Purpose |
|-----------|-------------|---------|
| Orchestrator | Cloud Run | Manages experiment loop |
| Training | Vertex AI Training | Runs 5-min experiments |
| Storage | Cloud Storage | Model checkpoints |
| Results | BigQuery | Experiment metrics |
| Notifications | Pub/Sub + Cloud Functions | Alert on completion |

---

## Interview Talking Points

### "How would you build Karpathy's autoresearch on GCP?"

> "I'd use Vertex AI Training for each 5-minute experiment - it's serverless, so I only pay for compute used. Cloud Scheduler triggers the orchestrator at 5pm. BigQuery stores results. Cloud Functions handles notifications. The key is Vertex AI Vizier - it's Google's hyperparameter optimization service that does similar Bayesian optimization automatically."

### "How do you handle experiment tracking?"

> "I use Cloud Logging for real-time metrics, BigQuery for analytics. Each experiment gets a unique run_id. I log: hyperparameters, training loss curve, validation metric, peak memory. Then I can query BigQuery to find the best run or detect regressions."

### "What's your MLOps philosophy?"

> "Automate everything that repeats. If I'm running an experiment more than once, it should be a pipeline. Use serverless where possible - Vertex AI, Cloud Run - to avoid infrastructure overhead. Start simple, iterate."

---

## Quick Start Checklist

- [ ] Set up GCP project
- [ ] Enable Vertex AI API
- [ ] Create first training job
- [ ] Set up BigQuery dataset
- [ ] Create Cloud Scheduler job
- [ ] Add monitoring alerts

---

## Resources

| Resource | URL |
|----------|-----|
| Vertex AI Training | cloud.google.com/vertex-ai/docs/training |
| Vertex AI Vizier | cloud.google.com/ai-platform/optimization/docs |
| Cloud Scheduler | cloud.google.com/scheduler |

---

*Thaggedhe Le — Build it, ship it, iterate!*
