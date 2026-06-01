# Snowflake: Time Travel & Zero-Copy Cloning

---

## Telugu Analogy

**Time Travel:** Nuvvu oka Word document lo pani chestunnav. Accidental ga undo chestav anuko. Cmd+Z back chestav — Snowflake Time Travel kuda alage, but 90 days back varaku.

Nuvvu delete chesina table, drop chesina row — anni 90 days undo history lo padipoyi untayi. Query tho "nenu 2 hours back unde state ni choodali" anna, direct ga aa point ki travel chesi data choodachu.

**Zero-Copy Cloning:** WhatsApp lo "Forward" button untadi — photo forward chesina, photo duplicate storage avadu, just reference copy. Adе Snowflake clone — table ni clone chestene, data duplicate avadu. Nuvvu changes chesinappudu danni separate ga store chestadi.

Bhayya oka 10GB table ni clone chestunnav anuko. 0 bytes extra storage. Neku aa clone lo oka column modify chesav ante, appudu aa column ki neeku storage vestundi. Migata 9.9GB shared.

---

## 1. What Problem Does It Solve?

**Problem:** Production data kaburlu — deploy ayyaka bug kanipistadi, yesterday's state kavali. Leka developer ki data kavali but production paina direct query kottalemu.

**Solution:** Time Travel = go back in time without restoring from backup. Cloning = instant copy without duplicating storage.

---

## 2. Time Travel — 90-Day Window

### How It Works

Snowflake maintains previous data states for:
- **Time Travel**: 0 to 90 days (based on edition) — queryable, clonable
- **Fail-safe**: Additional 7 days — Snowflake manages, NOT queryable by user (ask Snowflake support to recover)

| Edition | Time Travel Days |
|---------|-----------------|
| Standard | 1 |
| Enterprise | 90 |
| Business Critical | 90 |
| Virtual Private | 90 |

### Key Syntax

```sql
-- 1. Query data as of 2 hours ago
SELECT * FROM my_table
  AT (TIMESTAMP => '2026-06-01 10:00:00');

-- 2. Query using OFFSET (negative seconds from now)
SELECT * FROM my_table
  AT (OFFSET => -3600);  -- 1 hour ago

-- 3. Query using Statement ID (query ID)
SELECT * FROM my_table
  AT (STATEMENT => '0190a5a5-0000-4a5a-0000-000000000001');

-- 4. Query using BEFORE (does NOT include the statement's changes)
SELECT * FROM my_table
  BEFORE (STATEMENT => '0190a5a5-0000-4a5a-0000-000000000001');
```

### Common Operations

```sql
-- Recover a dropped table
UNDROP TABLE my_table;

-- Create a table as it was 1 day ago
CREATE TABLE my_table_restored AS
  SELECT * FROM my_table
  AT (OFFSET => -86400);

-- Restore specific rows
DELETE FROM my_table
  WHERE id IN (SELECT id FROM my_table AT (OFFSET => -3600) WHERE status = 'active');
```

### Common Mistake + Fix

```sql
-- ❌ WRONG: Table dropped long ago, trying direct clone
CREATE TABLE restored CLONE my_table;
-- Error: SQL compilation error: Object 'my_table' does not exist.

-- ✅ RIGHT: Use AT with timestamp from BEFORE drop
CREATE TABLE restored CLONE my_table
  AT (TIMESTAMP => '2026-05-15 14:30:00'::TIMESTAMP);

-- Or better: use UNDROP first
UNDROP TABLE my_table;
```

### What Can Fail

1. **Time Travel period expired** → `Object does not exist or operation cannot be performed` — query must be within retention window
2. **`AT (BEFORE)` confusion** — BEFORE includes everything THE STATEMENT DID NOT change, AT includes THE POINT IN TIME (they differ by the statement's own changes)
3. **Large tables + Time Travel = cost** — each day of time travel data costs 1x storage per day until you clone/restore

---

## 3. Zero-Copy Cloning — Instant, No-Cost Copies

### How It Works

```sql
-- Clone a table (zero storage initially)
CREATE TABLE prod_backup CLONE prod_table;

-- Clone an entire schema
CREATE SCHEMA dev_schema CLONE prod_schema;

-- Clone a database
CREATE DATABASE dev_db CLONE prod_db;
```

### Storage Behavior

```
Time ────────────────────────────────────────>
┌──────────┐
│ Original  │── data blocks ──→ Shared Storage
└──────────┘
     │
     │ CLONE (0 bytes, instant)
     ▼
┌──────────┐
│  Clone    │── changes ──→ New blocks only for changed data
└──────────┘

Initial state: Clone = 0 bytes
After changing 1 column: Clone storage ≈ size of changed data only
```

### Use Cases

1. **Dev/Test data** — instant clone of production, zero storage cost, query with real data
2. **Point-in-time analysis** — `CREATE TABLE snapshot CLONE my_table AT (TIMESTAMP => ...)`
3. **Backup before risky operations** — `CREATE TABLE pre_deploy CLONE my_table;` then run DDL
4. **Data sharing** — clone a subset and share with different teams

### Clone + Time Travel Together

```sql
-- Most powerful pattern: clone as of specific time
CREATE TABLE yesterday_snapshot CLONE prod_table
  AT (OFFSET => -86400);

-- This is how you do row-level restore
-- 1. Clone as-of before the bad operation
CREATE TABLE clean_data CLONE orders
  AT (TIMESTAMP => '2026-05-31 23:59:59');

-- 2. Swap tables
ALTER TABLE orders SWAP WITH clean_data;
```

### Common Mistake + Fix

```sql
-- ❌ WRONG: Assuming clone is free forever
CREATE DATABASE prod_copy CLONE prod_db;
-- ...runs for 30 days... storage bill spikes
-- Why? Clone stays free only until you write. After writes, 
-- new micro-partitions cost storage.

-- ✅ RIGHT: Clone for short-lived tasks, drop when done
CREATE DATABASE temp_analytics CLONE prod_db;
-- Run analysis...
DROP DATABASE IF EXISTS temp_analytics;
```

### When NOT to Clone

- If you need only a subset of rows → use `CREATE TABLE ... AS SELECT` with WHERE
- If you need to mask PII → clone then apply masking policy
- If schema changes are frequent → clones reference same storage; changes cause divergence cost
- For long-lived copies → budget for storage if you keep making changes

---

## 4. Fail-Safe (The Safety Net)

| Feature | Time Travel | Fail-safe |
|---------|------------|-----------|
| Duration | 0-90 days | 7 days |
| Queryable | Yes (AT/BEFORE) | No |
| Self-service | Yes | No (Snowflake support only) |
| Cost | Storage only | Included |
| Trigger | On completion of Time Travel period | After Time Travel expires |

Fail-safe is automatic — no configuration needed. You don't pay extra, but you can't query it. If you need data from fail-safe, call Snowflake support.

---

## 5. Interview Answers

### 30-Second (Quick Pitch)

"Snowflake Time Travel lets me query or restore any data as it existed up to 90 days ago using AT/BEFORE syntax. Zero-Copy Cloning creates an instant copy of a table, schema, or database without duplicating storage — storage charges only start when the clone's data changes. Together, they're the fastest way to recover from accidents or create dev/test environments with production data."

### 90-Second STAR

**Situation:** Our production orders table had incorrect status updates due to a bug in a scheduled task that ran for 6 hours before detection.

**Task:** Restore the affected 45,000 orders to their correct state without losing valid updates made during the same window.

**Action:** I first created a zero-copy clone of the orders table as-of the timestamp just before the buggy task started:
```sql
CREATE TABLE orders_clean CLONE orders
  AT (TIMESTAMP => '2026-05-20 01:59:59');
```
Then I identified the affected order IDs by comparing current state against the snapshot. I used MERGE to update only the status column for affected rows, preserving all other changes made during the 6-hour window. The whole operation took under 2 minutes.

**Result:** 45,000 orders corrected with zero data loss. No backup restore needed. Documented this as the standard recovery playbook for pipeline failures. Time saved: ~4 hours vs traditional restore-from-backup approach.

### 3-Minute Walkthrough

"Let me explain how Time Travel storage works under the hood..."

Snowflake uses immutable micro-partitions (16MB compressed each). When you UPDATE or DELETE, Snowflake doesn't modify existing files — it creates new micro-partitions and marks old ones as inactive. Those inactive micro-partitions are Time Travel data.

This means:
- `UPDATE` doesn't mutate — it appends new state, keeps old state
- Time Travel window = how long before Snowflake garbage-collects inactive micro-partitions
- Fail-safe = additional grace period for Snowflake's internal recovery

"Zero-Copy Cloning works on the same principle — clone shares the same micro-partitions as the source. Write to clone? Snowflake creates new micro-partitions for changed data only. The unchanged 90%+ still shared."

"A common interview question: 'You accidentally DROP a table. How do you recover it?' Answer: `UNDROP TABLE tablename;` — it's that simple. But if you DROP a DATABASE, you must UNDROP within Time Travel. And if TIME TRAVEL expired, call support for fail-safe recovery."

---

## 6. Quiz

<details>
<summary>Question 1: What does `AT (BEFORE => STATEMENT => 'id')` return?</summary>
A. Data as it existed at the time the statement ran
B. Data as it existed immediately before the statement's changes
C. Data excluding only the specified statement
D. Nothing — syntax error

**Correct: B**
BEFORE returns data prior to the statement's changes. AT includes the statement's point in time.
Common confusion: AT = point in time INCLUDING the statement, BEFORE = immediately prior EXCLUDING it.
</details>

<details>
<summary>Question 2: You clone a 50 GB table. How much storage is billed immediately?</summary>
A. 50 GB
B. 100 GB (original + clone)
C. 0 GB extra
D. 50 GB for the clone + 50 GB for the original

**Correct: C**
Zero-copy clone = 0 bytes initially. Storage billed only when clone's data diverges from source.
</details>

<details>
<summary>Question 3: Your table's Time Travel period ended yesterday. Can you still query data from 5 days ago?</summary>
A. Yes, using AT (OFFSET => -432000)
B. Yes, using Fail-safe
C. No — Time Travel has expired. Fail-safe exists but is not queryable
D. Yes, but only for SELECT, not UNDROP

**Correct: C**
Time Travel window closed. Fail-safe exists for 7 more days but requires Snowflake support to recover. You cannot query fail-safe data directly.
</details>

<details>
<summary>Question 4: Which does NOT consume Time Travel storage?</summary>
A. INSERT
B. UPDATE
C. SELECT
D. DROP TABLE

**Correct: C**
SELECT doesn't modify data, so it doesn't create new micro-partitions or retire old ones.
INSERT/UPDATE/DROP all create inactive micro-partitions that consume Time Travel storage.
</details>

<details>
<summary>Question 5: What's the maximum retention difference between Standard and Enterprise editions?</summary>
A. 1 day vs 7 days
B. 1 day vs 90 days
C. 7 days vs 90 days
D. 90 days vs unlimited

**Correct: B**
Standard = 1 day Time Travel. Enterprise = 90 days. Both have 7 days Fail-safe.
</details>

---

## 7. Interview Framing

### "Tell me about a time you used Snowflake's unique features."

Use the STAR from section 5. Frame as production experience — even if it was a personal project. Say:

"I built a data recovery playbook for my DE project. I used Time Travel and zero-copy cloning to recover from accidental data corruption without waiting for traditional backup restore. This reduced recovery time from hours to minutes."

### "Compare Snowflake Time Travel with BigQuery's time travel."

| Feature | Snowflake | BigQuery |
|---------|-----------|----------|
| Retention | 1-90 days (edition based) | 7 days default |
| Syntax | AT/BEFORE + TIMESTAMP/OFFSET/STATEMENT | FOR SYSTEM_TIME AS OF |
| UNDROP | Yes — tables, schemas, databases | No |
| Zero-copy clone | Yes | No (table snapshots cost storage) |
| Fail-safe | 7 days (support recovery) | N/A |

### "How would you design a CI/CD pipeline for Snowflake?"

Use clones:
1. `CREATE DATABASE dev CLONE prod;` — instant fresh copy
2. Run migrations against dev
3. `CREATE DATABASE staging CLONE prod;` — apply same migrations
4. Validate
5. Deploy to prod using `CREATE OR ALTER` pattern

---

*Prep note prepared for Krishna — Subba Rao anna style. Review and I'll convert to HTML or flashcards if you want.*
