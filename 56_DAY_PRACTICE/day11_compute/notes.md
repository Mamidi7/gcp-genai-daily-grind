# Day 11: Notes - Compute Services

## Key Takeaways

### Compute Options (MUST KNOW)

| Service | Control | Scaling | Best For |
|---------|---------|---------|----------|
| Compute Engine | Full OS | Manual/Auto | Custom software, GPUs |
| Cloud Run | Container | Auto (0→many) | Web apps, APIs |
| Cloud Functions | Function | Auto (0→many) | Simple event tasks |
| GKE | Kubernetes | Auto | Microservices |

### Interview Decision Tree
1. Need full OS? → Compute Engine
2. Container app? → Cloud Run
3. Simple function? → Cloud Functions
4. Complex microservices? → GKE

### ML Workloads
- **Training**: Compute Engine (GPU/TPU)
- **Serving**: Cloud Run or Vertex AI
- **Batch**: Cloud Run or Dataflow

---

## SQL Track: CTEs vs Subqueries

### CTE (Common Table Expression)
- Better readability
- Can reference multiple times
- Use WITH keyword

### Subquery
- Nested in WHERE or FROM
- Good for simple filters
- Correlated subqueries: references outer table

---

## Interview Punch Dialogue

**Q:** "When would you choose Cloud Run over Compute Engine?"

**A:** "If I have a containerized application, I'd use Cloud Run for automatic scaling from zero to handle traffic spikes without managing servers. Compute Engine makes sense when I need full OS control, GPU access, or custom software that can't run in containers. For my Flask API example, Cloud Run is perfect - just push the container and it scales automatically."

---

## Common Mistakes

1. **Using Cloud Functions for long tasks** - Max 60 seconds (9 min with 2nd gen)
2. **Not using Cloud Run for containers** - It's cheaper than Compute Engine!
3. **Overengineering with GKE** - Use Cloud Run unless you need Kubernetes

---

## Next Up
Day 12: Networking basics (VPC, Load Balancing)

---

## Time Spent
- Compute services: 25 min
- Decision flow: 15 min
- SQL CTEs/Subqueries: 30 min
- Total: ~70 min
