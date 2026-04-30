# Exercise 7: Autoscaling Model Serving

## Goal (one line)
Configure your model API to automatically scale up under load and scale down when idle.

## Why This Matters
Interview question: "Your model API gets 10x traffic during business hours. How do you handle it?"
Bad: "I buy a bigger server."
Good: "I configure horizontal pod autoscaling based on CPU and request queue depth.
Min replicas: 1 (cost savings at night). Max replicas: 10 (handle peak).
Scale-up trigger: CPU > 70% or queue depth > 100.
Scale-down: stabilize for 5 minutes before shrinking."

## Concept
1. Autoscaling = automatically add/remove instances based on load
2. Cloud Run does this natively (min/max instances setting)
3. Kubernetes uses HPA (Horizontal Pod Autoscaler)
4. For AI: you also scale by GPU utilization and request queue depth
5. Cold start problem: first request to a new instance is slow (model loading)
6. Solution: keep min_instances=1 to avoid cold starts

## Two Paths

### Path A: Cloud Run (simpler, GCP-native)
```yaml
# Already built into Cloud Run:
min_instances: 1        # always warm
max_instances: 10       # cap cost
concurrency: 100        # requests per instance
cpu_utilization: 70%    # scale-up trigger
```

### Path B: Kubernetes HPA (more control)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Pods
      pods:
        metric:
          name: http_requests_queue_depth
        target:
          type: AverageValue
          averageValue: "100"
```

## What You Build

### 1. Load test script
```python
# load_test.py — sends N concurrent requests
# Shows how the system behaves under load
# Usage: python load_test.py --concurrency 50 --requests 500
```

### 2. Cloud Run config (main.tf addition)
```hcl
resource "google_cloud_run_service" "model_api" {
  template {
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "1"
        "autoscaling.knative.dev/maxScale" = "10"
      }
    }
  }
}
```

### 3. Observe scaling
- Run load test → watch instances scale up in GCP console
- Stop load → watch instances scale down after 5 min

## Common Mistake
Setting min_instances=0 to save money, then getting cold start complaints.
Fix: min_instances=1 for user-facing APIs. 0 is fine for batch jobs.

## Check Question
Why is cold start a bigger problem for model serving than for regular APIs?
(Answer: Model serving often needs to load large model weights into memory.
This can take 10-30 seconds vs milliseconds for a regular web app.)

## Tiny Exercise
1. Run load_test.py against your local model API
2. Watch the latency increase as concurrency grows
3. In Cloud Run, changing min/max instances shows the scaling behavior
4. Write down: at what concurrency does latency spike past 1 second?
