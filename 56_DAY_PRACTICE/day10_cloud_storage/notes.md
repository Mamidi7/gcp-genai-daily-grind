# Day 10: Notes - Cloud Storage (GCS)

## Key Takeaways

### Buckets vs Objects
- **Bucket**: Container (like S3 bucket), global unique name
- **Object**: File inside bucket, identified by name (includes path)
- Objects can be up to 5TB each!

### Storage Classes (MUST MEMORIZE)

| Class | Min Retention | Use Case |
|-------|---------------|----------|
| Standard | None | Frequently accessed |
| Nearline | 30 days | Monthly access |
| Coldline | 90 days | Quarterly access |
| Archive | 365 days | Yearly/compliance |

**Interview trick:** Think "N-30, C-90, A-365" for retention!

### Access Control
- **Uniform (recommended)**: IAM only, simpler
- **Fine-grained**: IAM + ACLs (legacy)
- **Signed URLs**: Temporary access (minutes to hours)
- **Signed Policy**: Control what users can upload

---

## SQL Track: Window Functions

### ROW_NUMBER()
- Assigns unique sequential numbers
- Great for "top N per category"

```sql
SELECT *, ROW_NUMBER() OVER (ORDER BY sales DESC) as rank
FROM products
```

### RANK() vs DENSE_RANK()
- RANK(): Ties get same rank, next rank skips (1, 1, 3)
- DENSE_RANK(): Ties get same rank, next doesn't skip (1, 1, 2)

### LAG/LEAD
- LAG(): Previous row's value
- LEAD(): Next row's value
- Perfect for time series comparison

---

## Interview Punch Dialogue

**Q:** "How would you choose a storage class for ML model files?"

**A:** "For production ML models accessed frequently for inference, I'd use Standard storage for the 99.99% availability. For archived models used during rollback scenarios, Coldline makes sense. The key is matching access frequency to storage class to optimize costs - using Archive for compliance data that might only be accessed yearly can save 90%+ compared to Standard."

---

## Common Mistakes

1. **Using wrong storage class** - Check access frequency first!
2. **Bucket names with uppercase** - Always lowercase
3. **Forgetting signed URLs expire** - They're time-limited

---

## Next Up
Day 11: Compute (Compute Engine, Cloud Run, Cloud Functions)

---

## Time Spent
- GCS concepts: 20 min
- Storage classes: 15 min
- SQL Window Functions: 30 min
- Total: ~65 min
