# 🎯 INTERVIEW PUNCH DIALOGUES - GCP AI Engineer

> "Thaggedhe Le — Relentless Execution"
> Day 3 completed - Feb 27, 2026

---

## ✅ DAYS COMPLETED

| Day | Topic | Status |
|-----|-------|--------|
| Day 1 | Variables, Data Types, f-strings, print | ✅ Done |
| Day 2 | Lists, Dicts, Loops, if/else | ✅ Done |
| Day 3 | Functions, *args, **kwargs | ✅ Done |
| Day 4 | Data Structures | 📋 Ready |

---

## 🐍 DAY 1-3: PYTHON BASICS

### Day 1: Variables & Data Types

**Q: "What are Python's primitive data types?"**

> "Four basics: int (integers), float (decimals), str (text), bool (True/False). Everything else builds from these — lists, dicts, all are objects."

**Q: "How do f-strings work?"**

> "f-strings let you embed variables directly in strings with f'Hello {name}'. Much cleaner than 'Hello ' + name or .format(). Fast too — Python optimizes them."

---

### Day 2: Lists, Dicts, Loops

**Q: "What's the difference between list and dictionary?"**

> "List is ordered collection accessed by index [0], [1]. Dictionary is key-value pairs accessed by key ['name']. Lists are O(1) by index, dicts are O(1) by key lookup."

**Q: "How do you iterate with enumerate?"**

> "enumerate(list) gives you index and value: for i, name in enumerate(names). Avoids manual counter like i = 0; i += 1."

**Q: "When do you use list comprehension?"**

> "For transforming or filtering: [x*2 for x in nums if x > 5]. More Pythonic and faster than appending in loops."

---

### Day 3: Functions

### 1. Functions & *args, **kwargs

**Q: "Explain *args and **kwargs in Python?"**

> "***args** accepts unlimited positional arguments as a tuple — useful when you don't know how many inputs you'll get, like logging multiple values. **kwargs** accepts unlimited keyword arguments as a dictionary — perfect for configuration options where you want named parameters like model='gemini', temperature=0.7."

---

### 2. Chunking for RAG

**Q: "How do you chunk documents for a RAG system?"**

> "I never use naive character splitting — it breaks words and destroys context. I use boundary-based chunking: either by sentences, paragraphs, or code functions/classes. For code, I use language-specific splitters that respect AST boundaries. This ensures the LLM gets complete, meaningful chunks."

**Q: "What's wrong with fixed-size chunking?"**

> "Fixed-size chunking ignores semantic boundaries. You might cut a sentence halfway — the LLM gets partial context like 'Machine' without 'Learning'. Result: garbage in, garbage out."

---

## 🗄️ SQL / BIGQUERY

### 3. UNNEST & SPLIT (Day 5 Preview)

**Q: "How do you analyze comma-separated or pipe-separated strings in BigQuery?"**

> "I use SPLIT to convert the string into an Array, then UNNEST to flatten that array into individual rows. Once unnested, I can easily GROUP BY and count — this is how you analyze tags like 'python|javascript|react' to find the most popular technologies."

```sql
SELECT tag, COUNT(*) as cnt
FROM table, UNNEST(SPLIT(tags, '|')) as tag
GROUP BY tag
ORDER BY cnt DESC
```

---

### 4. CTEs (Common Table Expressions)

**Q: "Why use CTEs instead of subqueries?"**

> "CTEs are readable and reusable within the same query. They're like creating temporary views on the fly. I chain multiple CTEs for complex transformations — each CTE does one thing, making debugging easy. It's like writing pseudocode that actually runs."

**Q: "When would you use a CTE over a temp table?"**

> "For ad-hoc analysis in BigQuery, CTEs are perfect — no extra storage cost, and the query reads like a story. For production pipelines with repeated use, temp tables make more sense."

---

### 5. Window Functions

**Q: "What's the difference between RANK() and ROW_NUMBER()?"**

> "ROW_NUMBER assigns a unique rank to each row — 1, 2, 3, 4. RANK assigns the same rank to ties — so you might get 1, 1, 3. DENSE_RANK also handles ties but without gaps — 1, 1, 2. Use ROW_NUMBER when you need exact ordering, RANK when you want to identify tied groups."

---

### 6. ARRAY_AGG & STRUCT

**Q: "How do you aggregate multiple columns in BigQuery?"**

> "ARRAY_AGG bundles values into an array. STRUCT lets you bundle multiple columns into a named structure. Together, you can aggregate entire rows: ARRAY_AGG(STRUCT(col1, col2, col3)) — this is powerful for creating nested outputs for JSON or Vertex AI prompts."

---

## 📄 RAG SYSTEMS

### 7. RAG Architecture

**Q: "Explain your RAG system architecture?"**

> "User query → Embedding model → Vector search (like Pinecone or Vertex AI Vector Search) → Top-K chunks retrieved → Inject into LLM prompt (Context + Question) → LLM generates answer. The key is measuring quality — I use RAGAS scores for faithfulness and answer relevance."

---

### 8. Embeddings

**Q: "What are embeddings and why do we need them?"**

> "Embeddings convert text into dense numerical vectors — so 'cat' and 'kitten' become vectors that are mathematically close in 768-dimensional space. This allows semantic search: finding meaning, not just keywords. Without embeddings, you'd only match exact words."

---

### 9. Vector Databases

**Q: "What's the difference between Pinecone and Vertex AI Vector Search?"**

> "Pinecone is a managed vector DB — easy setup, pay for storage + queries. Vertex AI Vector Search (formerly Matching Engine) is GCP-native, scales to billions of vectors, but needs more setup. For startups, Pinecone is simpler. For enterprise on GCP, Vector Search is natural."

---

## ☁️ GCP / VERTEX AI

### 10. Vertex AI

**Q: "How do you call Gemini from your Python code?"**

> "Two ways: 1) AI Studio Quick API — just an API key, good for prototyping. 2) Vertex AI SDK — production-ready, uses Workload Identity, enterprise features. I always use Vertex AI for production — no API key management, better security."

---

### 11. Cloud Run vs Cloud Functions

**Q: "When do you use Cloud Run vs Cloud Functions?"**

> "Cloud Run is for persistent services — my Flask/FastAPI apps that handle requests. It scales to zero and handles spikes well. Cloud Functions is for event-driven — triggered by HTTP, storage changes, or Pub/Sub. For my RAG API, Cloud Run all the way."

---

### 12. Workload Identity Federation (WIF)

**Q: "How do you secure your GCP credentials in production?"**

> "Never use service account JSON keys — they're a security risk. I use Workload Identity Federation: the deployment pipeline (GitHub Actions, Cloud Build) impersonates a service account directly. Zero secrets stored, automatically rotated, audit-ready."

---

### 13. Cost Optimization

**Q: "How do you optimize BigQuery costs?"**

> "Three ways: 1) Partition tables by date — query only what you need. 2) Use clustering for frequently filtered columns. 3) Always run DRY RUN first to estimate costs before billing. In RAG, cache embeddings — don't regenerate for the same document."

---

## 🔧 PRODUCTION TIPS

### 14. Error Handling

**Q: "How do you handle API failures in production?"**

> "Three layers: 1) Retry with exponential backoff — API calls fail transiently. 2) Circuit breaker — if a provider is down, fail fast rather than timeout. 3) Graceful degradation — return a fallback answer like 'I'm having trouble right now, please try again.'"

---

### 15. Logging & Monitoring

**Q: "What do you log in a production RAG system?"**

> "Everything: input question, retrieved chunks (for debugging), LLM response, latency, token count, and RAGAS scores. Cloud Logging + Cloud Monitoring (Prometheus metrics) on Cloud Run. If something fails, I need to reproduce it — logs are my replay button."

---

## 🎯 ONE-LINERS FOR QUICK ANSWERS

| Question | Punch Dialogue |
|----------|----------------|
| "What's the difference between list and tuple?" | "Lists are mutable — you can change them. Tuples are immutable — safer, slightly faster. Think tuple for constants, list for collections you'll modify." |
| "Why use dictionaries?" | "O(1) lookup by key. For any 'find by ID' scenario, dictionaries beat lists which are O(n)." |
| "What is list comprehension?" | "One-line way to filter/transform lists. [x*2 for x in nums if x > 5] — more Pythonic than loops." |
| "Explain map()" | "Apply a function to every element. But list comprehension is usually more readable in Python." |
| "What does yield do?" | "Makes a function a generator — yields one value at a time instead of returning all at once. Memory efficient for large sequences." |
| "What is __init__.py?" | "Makes a folder a Python package. Empty file tells Python 'this directory is importable.'" |
| "Explain *args again in one line" | "It lets any number of positional arguments funnel into your function as a tuple." |
| "What is pip freeze?" | "Saves all installed packages and versions to requirements.txt — essential for reproducible environments." |
| "Why use virtualenv?" | "Isolate project dependencies — project A might need pandas 1.0, project B needs 2.0. No conflicts." |

---

## 🔥 QUICK REFERENCE COMMANDS

### BigQuery
```bash
# Run query from CLI
bq query --use_legacy_sql=false 'YOUR_QUERY'

# Save to CSV
bq query --format=csv --max_rows=1000 'QUERY' > output.csv

# Check query cost first
bq query --dry_run 'QUERY'
```

### GCP
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT
gcloud run deploy SERVICE_NAME --source .
gsutil cp file.csv gs://BUCKET/
```

### Python
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python script.py
```

---

## 📅 DAY-BY-DAY TOPICS

| Day | Topic | Key Interview Points | Status |
|-----|-------|---------------------|--------|
| Day 1 | Variables, Data Types | int, float, str, bool, f-strings | ✅ Done |
| Day 2 | Lists, Dicts, Loops | enumerate, comprehensions, if/else | ✅ Done |
| Day 3 | Functions | def, *args, **kwargs, return | ✅ Done |
| Day 4 | Data Structures | List/Dict/Set operations, comprehensions | 📋 Ready |
| Day 5 | Classes + OOP | __init__, to_dict(), inheritance |
| Day 6 | JSON + File I/O | json.load(), json.dump(), os.path |
| Day 7 | REST APIs + Gemini | requests.post(), API keys, JSON response |
| Day 8 | GCP Projects + IAM | Viewer vs Editor vs Owner, roles |
| Day 9 | Cloud Storage | GCS buckets, upload/download, gsutil |
| Day 10 | BigQuery in Python | google-cloud-bigquery client |
| Day 11 | Cloud Run | Deploy Flask, containerize |
| Day 12 | Workload Identity | WIF, keyless auth |
| Day 13 | Vertex AI | Model Garden, Gemini via SDK |

---

## 🔧 ERRORS & DEBUG LEARNINGS

### Error 1: BigQuery Returns 0 Rows for 2024 Data

**Problem:** Query with `WHERE creation_date BETWEEN "2024-01-01" AND "2024-12-31"` returned 0 rows.

**Root Cause:** The StackOverflow public dataset only has data **up to 2022**.

**Fix:** Use 2022 dates instead of 2024.

```sql
-- WRONG (0 rows)
WHERE creation_date BETWEEN "2024-01-01" AND "2024-12-31"

-- CORRECT
WHERE creation_date BETWEEN "2022-01-01" AND "2022-12-31"
```

**Interview Tip:** "Always check data availability before writing production queries. I verified the date range first."

---

### Error 2: Git Push Failed - Remote Has Changes

**Problem:** `git push` failed with "rejected - fetch first" error.

**Fix:**
```bash
git stash              # Save local changes
git pull --rebase     # Get remote changes
git push              # Push your changes
```

**Interview Tip:** "In team environments, always pull before push to avoid conflicts."

---

### Error 3: zsh Command Not Found (Dollar Sign)

**Problem:** `gcloud config set account $ krishna27sep2025@gmail.com` failed.

**Root Cause:** Typed `$` before command. In terminal, `$` is just the prompt indicator, not part of the command.

**Fix:** Just type the command without `$`:
```bash
gcloud config set account krishna27sep2025@gmail.com
```

---

### Error 4: chunk_text() - Last Chunk Missing

**Problem:** If you loop through text with step size but never append the final partial chunk, it gets lost.

**Fix:** Always handle the final chunk after the loop:
```python
for i in range(0, len(text), size):
    chunks.append(text[i:i+size])

# BUT WAIT — what if text is "Hello" and size is 10?
# Loop runs once, appends "Hello", done.

# What if text is "HelloWorld" and size is 5?
# i=0: "Hello" -> appended
# i=5: "World" -> appended
# Loop ends. All good!

# BUT if using word-boundary chunking:
# After loop ends, current_chunk might still have data!
# So ALWAYS add:
if current_chunk:
    chunks.append(current_chunk.strip())
```

**Interview Tip:** "Edge cases matter. Always test empty strings, single words, and exact size boundaries."

---

*Last Updated: Day 3 (Feb 27, 2026)*
*Mantra: Thaggedhe Le — Relentless Execution* 💪🔥
