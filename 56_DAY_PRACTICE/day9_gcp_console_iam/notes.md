# Day 9: Notes - GCP Console + IAM Basics

## Key Takeaways

### GCP Console
- Web-based interface at console.cloud.google.com
- Can access all GCP services from left sidebar
- Search bar at top is super useful (press `/` to focus)

### Projects
- Every resource in GCP belongs to a project
- Project has: ID (unique globally), Name (friendly), Number (internal)
- Resources can't be shared across projects without explicit config

### IAM Roles (CRITICAL FOR INTERVIEWS)

| Role | View | Edit | Delete | Manage IAM |
|------|------|------|--------|------------|
| Viewer | ✓ | ✗ | ✗ | ✗ |
| Editor | ✓ | ✓ | ✓ | ✗ |
| Owner | ✓ | ✓ | ✓ | ✓ |

**Important:** Editor CANNOT add/remove users - only Owner can!

### Predefined Roles (Better for Production)
- More granular than primitive roles
- Examples:
  - `roles/bigquery.dataViewer` - Read BigQuery data only
  - `roles/storage.objectAdmin` - Full control of objects
  - `roles/aiplatform.user` - Use Vertex AI resources

### Custom Roles
- Created at organization or project level
- Combine specific permissions needed for a role
- Use when predefined roles don't fit exactly

---

## SQL Track: ARRAY_AGG & STRUCT

### ARRAY_AGG
- Aggregates multiple rows into a single array
- Great for "get all items per category" type queries

```sql
SELECT department, ARRAY_AGG(name) as employees
FROM employees
GROUP BY department
```

### STRUCT
- Creates a nested/structured data type (like a Python dict or JSON object)
- Useful for grouping related fields together

```sql
SELECT STRUCT(name, department, salary) as emp_info
FROM employees
```

### Combined Power
```sql
SELECT
    department,
    ARRAY_AGG(STRUCT(name, salary)) as team_members
FROM employees
GROUP BY department
```

---

## Interview Punch Dialogue

**Q:** "What's the difference between Viewer, Editor, and Owner in GCP?"

**A:** "Viewer gives read-only access - you can see everything but can't change anything. Editor lets you create, modify, and delete resources but cannot manage IAM permissions. Owner has full control including the ability to add or remove team members and manage billing. For production environments, I prefer using predefined roles like BigQuery Data Viewer for fine-grained access control."

---

## Common Mistakes to Avoid

1. **Giving Editor instead of Owner for billing** - Only Owner can access billing
2. **Using primitive roles in production** - Predefined roles follow principle of least privilege
3. **Forgetting project number** - Sometimes APIs need project number, not just ID

---

## Next Up: Day 10
Cloud Storage (GCS) - buckets, objects, access control

---

## Time Spent
- GCP Console exploration: 20 min
- IAM concepts: 25 min
- SQL Track (ARRAY_AGG/STRUCT): 30 min
- Total: ~75 min
