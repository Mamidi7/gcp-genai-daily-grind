# 13-Day Revision Strategy (Repo-Based)

> **Generated:** March 30, 2026
> **Target:** Interview-ready by April 11, 2026
> **Source:** Full audit of every file, commit, and code artifact in this repo

---

## Repo Audit: What's Real vs What's Empty

```
AREA                 | DEPTH     | EVIDENCE
─────────────────────┼───────────┼─────────────────────────────────────────
Python Basics (1-7)  | #####__   | Notes+code+exercises+interview Qs
FastAPI (10,12,13)   | #####__   | Real endpoints, 13/13 tests, debug logs
GCP IAM/WIF (8,9)    | ###___    | Notes + console screenshots
Cloud Storage (10)   | ####___   | Upload scripts + storage class notes
Compute (11)         | ###___    | Notes only, decision tree memorized
BigQuery SQL         | ####___   | Window fns, CTEs, JOINs, UNNEST
Hybrid RAG           | #####__   | 120-line script, keyword+vector search
Agentic RAG          | #####__   | 178-line script, tool calling, agent loop
LangGraph (15)       | ##____    | Folder exists but thin content
LLM Wrapper (15)     | ####___   | Parse/retry patterns added
Vertex AI Pipeline   | ##____    | Template exists, not executed
RAG Eval             | ##____    | Template script, no real evals run
Cheat Sheets         | #######   | REVISION_PYTHON, REVISION_GCP, REVISION_AI_LLM
Interview Punch      | #####__   | 15 Qs + debug stories + STAR
Day 16-30 folders    | #____    | SKELETONS -- notes.md empty templates
Projects             | ##____    | gcp_api_monitor exists but basic
```

---

## Knowledge Map: Strong / Medium / Weak

```
STRONG (can explain in interview without prep)
═══════════════════════════════════
+--------------+  +--------------+  +--------------+
| Python       |  | FastAPI      |  | RAG System   |
| basics       |  | + validation |  | (hybrid +    |
| (days 1-7)   |  | + errors     |  |  agentic)    |
+--------------+  +--------------+  +--------------+
+--------------+  +--------------+  +--------------+
| BigQuery     |  | GCP services |  | Interview    |
| SQL          |  | (10 services |  | Punch        |
| patterns     |  |  overview)   |  | Dialogues    |
+--------------+  +--------------+  +--------------+

MEDIUM (know concepts, need to practice code)
══════════════════════════════════
+--------------+  +--------------+  +--------------+
| IAM/WIF      |  | Cloud Run    |  | LLM Wrapper  |
| concepts     |  | deployment   |  | parse/retry  |
+--------------+  +--------------+  +--------------+

WEAK (empty templates, need real work)
══════════════════════════════════
+--------------+  +--------------+  +--------------+
| Vertex AI    |  | RAG Eval     |  | System       |
| Pipelines    |  | Harness      |  | Design       |
| (not run)    |  | (not run)    |  | (no practice)|
+--------------+  +--------------+  +--------------+
+--------------+  +--------------+  +--------------+
| MLOps/Monitor|  | Embeddings   |  | Agent        |
| /Drift       |  | + Chunking   |  | Guardrails   |
| (no code)    |  | (theory only)|  | (no code)    |
+--------------+  +--------------+  +--------------+
```

---

## 13-Day Plan Overview

```
MAR 30 ──────── APR 11  (13 DAYS TO INTERVIEW-READY)

Phase A        Phase B           Phase C        Phase D
PLUG GAPS      CONNECT DOTS      FULL BUILDS    INTERVIEW MODE
(Day 1-4)      (Day 5-8)         (Day 9-11)     (Day 12-13)

+------+      +------+          +------+       +------+
| #    |      | ##   |          | ###  |       | #### |
|Fix   | ---> |Link  | --->     |Build | --->  |Ship  |
|gaps  |      |pieces|          |real  |       |ready |
+------+      +------+          +------+       +------+
```

---

## PHASE A: PLUG THE GAPS (Days 1-4)

### Day 1 (Mar 30): Embeddings + Chunking — REAL CODE

**WHY:** Cheat sheet has theory. Day 16 is an empty template. This is the #1 thing interviewers drill on for RAG roles.

**MORNING:**
1. Take `rag_hybrid_template.py`
2. Extract the chunking logic into `chunk_utils.py`
3. Implement 3 strategies:
   - Fixed-size (char-based)
   - Sentence-boundary (nltk.sent_tokenize)
   - Recursive character (LangChain style)
4. Print chunk quality for each strategy

**AFTERNOON:**
1. Use text-embedding-004 (already in your code!)
2. Embed same text with 3 chunking strategies
3. Measure retrieval quality: query each, compare top-3
4. Write findings in `day16/notes.md` (REPLACE empty)

**INTERVIEW PREP:**
> "I tested 3 chunking strategies. Sentence-boundary gave 40% better retrieval than fixed-size because it preserved context."

**TOOL:** I (Claude) run your code through Code Reviewer agent

---

### Day 2 (Mar 31): RAG Eval Harness — Actually Run It

**WHY:** `rag_eval_template.py` exists but was never executed. "I used RAGAS to measure Faithfulness" is empty without data.

**MORNING:**
1. Create 10 test Q&A pairs from your `knowledge_base.txt`
2. Run each through your hybrid RAG system
3. Score: is the answer grounded in retrieved context?
4. Log: question | retrieved_chunks | answer | pass/fail

**AFTERNOON:**
1. Identify the 3 worst answers from eval
2. Fix: better chunking? lower threshold? add citations?
3. Re-run eval on those 3 -- show improvement
4. Write results in `day19-20/` as real eval evidence

**INTERVIEW PREP:**
> "My eval harness caught 3 hallucinations. I lowered the similarity threshold from 0.3 to 0.5 and added citation enforcement -- hallucinations dropped to zero."

---

### Day 3 (Apr 1): Vertex AI Pipeline — Actually Deploy

**WHY:** `vertex_pipeline_template.py` exists but was never run. MLOps is the "senior differentiator" per your own topic map.

**MORNING:**
1. Use your existing GCP project (e2e-etl-project)
2. Build a 3-step Vertex AI Pipeline:
   - Step 1: Ingest data from GCS
   - Step 2: Generate embeddings (text-embedding-004)
   - Step 3: Log results to BigQuery
3. Run it. Capture screenshots.

**AFTERNOON:**
1. Add error handling (what if GCS bucket empty?)
2. Add pipeline parameters (configurable input path)
3. Write the debug story: "Pipeline failed because X, I fixed it by Y"
4. Commit as: `feat(day29): vertex ai pipeline executed`

**INTERVIEW PREP:**
> "I built a Vertex AI Pipeline that ingests -> embeds -> stores. First run failed because the GCS path was wrong -- I added parameterized inputs and validation at pipeline start."

---

### Day 4 (Apr 2): Agent Guardrails + Tool Validation

**WHY:** Your `agentic_rag_template.py` is solid but has NO safety. Real interviews ask: "What if the agent goes rogue?"

**MORNING:**
1. Open `agentic_rag_template.py`
2. Add: max_iterations limit (agent must stop after 5)
3. Add: tool_call_validator (whitelist allowed functions)
4. Add: timeout per tool call (10 seconds max)
5. Add: trace logging (every step logged to dict)

**AFTERNOON:**
1. Test: What happens with a malicious input?
2. Test: What happens with infinite loop trigger?
3. Write debug journal: "Agent tried calling undefined tool, guardrail caught it"
4. Commit: `feat(day22): agent guardrails + trace logging`

**INTERVIEW PREP:**
> "My agent has 3 safety layers: iteration limit, tool whitelist, and per-call timeout. When it tried calling an undefined tool, the validator caught it and returned a safe fallback."

---

## PHASE B: CONNECT THE DOTS (Days 5-8)

### Day 5 (Apr 3): End-to-End RAG Architecture Drawing

**WHY:** You have the pieces (chunking, embeddings, retrieval, agent) but no architecture diagram connecting them. Interviewers want to see you can DESIGN systems.

**MORNING — Draw the full architecture of YOUR system:**
```
User -> FastAPI -> /chat endpoint
          |
    Input Validation (Pydantic)
          |
    Agent Loop (max 5 iterations)
          |
    Tool Router --> Knowledge Base Search (Hybrid RAG)
                 --> Gemini API (with retry + timeout)
                 --> BigQuery (for analytics)
          |
    Citation Check (grounded in context?)
          |
    Response -> User

Log everything -> Cloud Logging -> BigQuery eval table
```

**AFTERNOON:**
1. Practice explaining this diagram aloud (3 min)
2. For each arrow, know: "Why this choice?"
3. For each box, know: "What fails? How do I detect?"
4. Record yourself explaining it -- play back, improve

**TOOL:** Use Excalidraw MCP to draw this, or draw on paper

---

### Day 6 (Apr 4): Connect GCP Services — Real Integration

**WHY:** You know individual GCP services (Day 10 cheat sheet) but haven't connected them into a working pipeline.

**MORNING:**
1. GCS: Upload a document -> trigger Cloud Function
2. Cloud Function: Read file -> chunk -> embed -> store
3. BigQuery: Log each ingestion (timestamp, chunks, size)
4. This is your "data ingestion pipeline" hero story

**AFTERNOON:**
1. What if GCS upload fails? -> Add retry logic
2. What if embedding API times out? -> Add fallback
3. What if BigQuery insert fails? -> Queue in Pub/Sub
4. Write the "production thinking" story for each

**INTERVIEW PREP:**
> "My pipeline: GCS upload triggers Cloud Function -> chunks text -> generates embeddings via Vertex AI -> logs to BigQuery. If embedding fails, it retries 3x with backoff. If BQ fails, it queues to Pub/Sub for guaranteed delivery."

---

### Day 7 (Apr 5): Monitoring + Drift + Structured Logging

**WHY:** Your topic map says "Production Engineering" is needed. Zero code exists for this. Shows senior thinking.

**MORNING:**
1. Add structured logging to your agentic_rag:
   - `{timestamp, query, tool_called, latency, tokens, retrieval_score, answer_length}`
2. Write logs to a local JSONL file (simulate Cloud Log)
3. After 10 queries, load into pandas and analyze:
   - Average latency
   - Which tool is called most?
   - Any query with retrieval_score < 0.5?

**AFTERNOON:**
1. Simulate "drift": change your knowledge_base.txt
   -> re-embed -> compare old vs new retrieval results
2. Create a simple "alert": if avg_retrieval_score drops below 0.4, print WARNING
3. Write monitoring dashboard notes
4. This is your "I think about production" proof

**INTERVIEW PREP:**
> "I log every query with structured JSON -- latency, tool used, retrieval score, token count. I have drift detection: if average retrieval quality drops below threshold, it alerts."

---

### Day 8 (Apr 6): Deploy Everything to Cloud Run

**WHY:** Day 10 has Cloud Run deployment notes, but your RAG+Agent has never been deployed. Interview-proof your "full stack".

**MORNING:**
1. Take `agentic_rag_template.py` + guardrails
2. Wrap in FastAPI (you already know how -- Day 12/13)
3. Endpoints:
   - `POST /ask` -> agent handles query
   - `GET /healthz` -> alive check
   - `GET /readyz` -> model + GCS + BQ connectivity
4. Dockerize -> push to Artifact Registry -> Cloud Run

**AFTERNOON:**
1. Test the deployed API: curl the /ask endpoint
2. Check Cloud Run logs for your structured logging
3. Screenshot: working URL + logs + response
4. Update README with the live architecture
5. Commit: `feat: deploy agentic RAG to Cloud Run`

**INTERVIEW PREP:**
> "I containerized my Agentic RAG system with FastAPI, deployed to Cloud Run with /healthz and /readyz endpoints. It uses WIF for authentication -- zero API keys stored anywhere."

---

## PHASE C: FULL BUILDS — INTERVIEW-GRADE (Days 9-11)

### Day 9 (Apr 7): System Design Practice (3 Scenarios)

**WHY:** Your Bhagavad Geetha plan says "System Design War Room" in Week 7-8. But you've practiced ZERO system design problems.

**SCENARIO 1 (Morning):**
"Design an AI system to classify 10,000 customer support tickets daily into categories on GCP."

Draw:
```
Cloud Storage -> Dataflow -> Vertex AI (classifier)
              -> BigQuery (analytics)
              -> Pub/Sub -> Slack notification
```
Explain tradeoffs: batch vs real-time, cost, accuracy

**SCENARIO 2 (Afternoon):**
"Design a RAG system for a company's internal docs (50,000 PDFs) with <2 second response time."

Draw:
```
GCS (PDFs) -> Cloud Function (parse) -> Chunker
-> Vertex AI Embeddings -> Vertex AI Vector Search
-> Cloud Run (FastAPI + Agent) -> Cloud Logging
```
Explain: Why Vector Search over pgvector? Scaling. Cost.

**SCENARIO 3 (Evening -- quick):**
"How would you detect and handle hallucinations in a production LLM application?"
Answer using YOUR eval harness + monitoring + citations

**TOOL:** I (Claude) play the interviewer. You explain. I push back.

---

### Day 10 (Apr 8): Polish 3 Hero Stories

**WHY:** Your INTERVIEW_CHEAT_SHEET lists 3 hero stories but they're bullet points. Not polished STAR stories.

**HERO STORY 1: The Validation + Debugging Story (Day 10, 12, 13)**

- **S:** Building FastAPI + Gemini endpoint for a RAG app
- **T:** Make it production-safe -- no crashes on bad input
- **A:** Added Pydantic validation (min/max/regex), custom error handler, retry + timeout wrapper, request IDs
- **R:** 13/13 tests pass. Invalid inputs fail fast with 422. Upstream failures return clean 502, not stack traces.

PRACTICE: Say it in 30 seconds. Then 90 seconds. Record. Listen. Refine. Repeat 3x.

**HERO STORY 2: The Hybrid RAG + Agent System (rag_hybrid + agentic_rag)**

- **S:** Needed accurate Q&A over domain docs with citations
- **T:** Build RAG that reduces hallucinations
- **A:** Built hybrid retrieval (keyword + vector), added agent with tool calling, guardrails, eval harness
- **R:** Eval showed X% improvement. Citations enforce grounding. Agent can safely call multiple tools.

PRACTICE: Say it in 30 seconds. Then 90 seconds. Record. Listen. Refine. Repeat 3x.

**HERO STORY 3: The GCP Production Deployment (Day 8 WIF + Day 10 Cloud Run)**

- **S:** Needed to deploy AI service securely without API keys
- **T:** Zero-trust deployment pipeline on GCP
- **A:** Used WIF for auth, Cloud Run for hosting, GCS for document storage, BigQuery for analytics/logging
- **R:** Zero secrets in code. Auto-scaling. Cost-optimized with context caching. Full observability via logging.

PRACTICE: Say it in 30 seconds. Then 90 seconds. Record. Listen. Refine. Repeat 3x.

---

### Day 11 (Apr 9): BigQuery Deep Dive + ML Theory

**WHY:** Your SQL is decent (window fns, CTEs) but BQ-specific features (partitioning, clustering, cost optimization) are theory-only. Also ML theory is missing from your repo.

**MORNING: BigQuery Advanced**
1. Write 5 queries using YOUR actual GCP project:
   - Partitioned query (by date, only scan recent)
   - Clustered query (by category column)
   - DRY RUN comparison (before vs after partitioning)
   - UNNEST + ARRAY_AGG (your existing knowledge)
   - MERGE statement (upsert pattern)
2. Capture: bytes processed, execution time, cost est.

**AFTERNOON: ML Theory Quick-Fire**
Answer these from memory:
- Bias-variance tradeoff?
- Precision vs Recall? When to optimize each?
- What is overfitting? How do you detect it?
- What is cross-validation? Why k-fold?
- Embedding dimension choice? Trade-offs?
- Cosine similarity vs Euclidean distance?
- Transformer attention mechanism in 3 lines?
- What is temperature in LLM? What happens at 0? at 2?

---

## PHASE D: INTERVIEW MODE (Days 12-13)

### Day 12 (Apr 10): Mock Interview Grilling

**MORNING: Technical Deep-Dive (Claude is the interviewer)**

Round 1: Python + Backend (30 min)
- "Explain your FastAPI error handling design"
- "Write a function that chunks text with overlap"
- "How does Pydantic validation work under the hood?"
- "Explain *args, **kwargs, decorators, generators"

Round 2: GCP + Cloud (30 min)
- "Walk me through your Cloud Run deployment"
- "How does WIF work? Why not service account keys?"
- "Choose Compute Engine vs Cloud Run vs Functions"
- "BigQuery cost optimization strategies?"

**AFTERNOON: AI/ML + System Design**

Round 3: AI/LLM (30 min)
- "Explain your RAG architecture"
- "How do you evaluate RAG quality?"
- "What are embeddings? Why not keyword search only?"
- "How do you prevent hallucinations?"
- "Explain your agent's tool calling flow"

Round 4: System Design (30 min)
- "Design a production RAG system for 10K documents"
- I push back on every choice. You defend.

**EVENING: Behavioral**
- "Tell me about a time you debugged a hard problem"
- "Why are you transitioning to AI/ML?"
- "How do you handle the career gap?"
- "Tell me about a project you're proud of"

---

### Day 13 (Apr 11): Final Polish + Confidence Build

**MORNING:**
1. Revisit weak areas from Day 12 mock
2. Re-record Hero Stories -- aim for natural, not scripted
3. Quick quiz: 20 random questions from your cheat sheets
4. Review your GitHub repo -- would an interviewer be impressed? Fix README if needed.

**AFTERNOON:**
1. One final mock interview (full 60 min)
2. Focus on areas you struggled with on Day 12
3. Practice: "Tell me about yourself" (2 min version)
4. Practice: "Any questions for us?" (have 3 ready)

**EVENING: REST. You're ready.**

```
+-----------------------------------------------------+
|                                                     |
|           YOU ARE READY.                            |
|                                                     |
|  56-day repo with real code                         |
|  3 hero stories polished                            |
|  Hybrid RAG + Agent deployed                        |
|  Eval harness with real results                     |
|  System design practice                             |
|  GCP services connected end-to-end                  |
|                                                     |
|  Thaggedhe Le. Go get that job.                     |
|                                                     |
+-----------------------------------------------------+
```

---

## Daily Session Flow

```
YOU SAY: "Let's start Day X"
     |
     v
+----------------------------------------------+
| 1. Create TodoWrite with today's tasks       |
| 2. Quick warm-up quiz (5 Qs from existing    |
|    cheat sheets)                              |
| 3. Teach the gap concept (repo-specific)      |
| 4. You write code (Claude reviews via agent)  |
| 5. Debug session (real failures, real fixes)  |
| 6. Interview prep (STAR story + quiz)         |
| 7. Commit to YOUR repo                        |
| 8. Update progress tracker                    |
+----------------------------------------------+

TOOLS PER DAY:
+--------------+----------------------------------+
| Phase        | Tool                             |
+--------------+----------------------------------+
| Research     | Web Search + Web Reader (GCP)    |
| Coding       | Bash + Codex (write + run code)  |
| Review       | Code Reviewer agent              |
| Quiz         | Claude generates + scores 10 Qs  |
| Diagrams     | Excalidraw MCP                   |
| Mock Intv    | Claude plays interviewer         |
| Deploy       | Bash (gcloud commands)           |
+--------------+----------------------------------+
```

---

## Key Difference: Generic vs Your Plan

```
GENERIC PLAN                   YOUR REPO-BASED PLAN
(Last time)                    (This time)

+----------------+          +----------------------+
| Day 1: Python  |          | Day 1: Chunking +    |
| fundamentals   |          | Embeddings (REAL)    |
| (you already   |          | (fills Day 16 gap)   |
|  know this)    |          |                      |
+----------------+          +----------------------+
+----------------+          +----------------------+
| Day 3: GCP     |          | Day 3: Vertex AI     |
| Core services  |          | Pipeline (DEPLOY     |
| (theory again) |          |  for real)           |
+----------------+          +----------------------+
+----------------+          +----------------------+
| Day 6: DL      |          | Day 6: GCP services  |
| Basics         |          | CONNECTED pipeline   |
| (not asked in  |          | (you know pieces,    |
|  interviews)   |          |  connect them)       |
+----------------+          +----------------------+

KEY DIFFERENCE:
  X  Re-learn what you already know
  *  Fill ACTUAL gaps in YOUR repo
  *  Build REAL code where templates are empty
  *  Convert existing code into interview stories
```

---

*Generated from full repo audit: Mar 30, 2026*
*Thaggedhe Le -- Relentless Execution*
