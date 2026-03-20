# Day 10 Manual-First Execution Packet

Date: March 15, 2026

Goal in 1 line:
Understand why `Cloud Storage + FastAPI + Gemini + BigQuery thinking` belong together in a real applied AI system, then do the work manually before touching CLI-heavy flow.

## Start Here: Action List

Complete these in order.

1. Read the big picture section below.
2. Draw the system by hand using the ASCII diagram.
3. Do the manual GCP Console tasks.
4. Open `notebook.ipynb` and work through the notebook topic blocks.
5. Practice the SQL/BigQuery tasks in `DAY10_BIGQUERY_WINDOW_FUNCTIONS.sql`.
6. Run one FastAPI debug scenario manually.
7. Write one debug entry in `DAY10_DEBUG_LOG_TEMPLATE.md`.
8. Write one 30-second and one 90-second answer from the interview section.
9. Push at least one artifact today to keep the green streak.

## Big Picture First

Simple English:
- `Cloud Storage` stores files and artifacts.
- `FastAPI` gives your AI system an API surface.
- `Gemini` generates or summarizes content.
- `BigQuery` is where you later analyze feedback, logs, and eval-style results.
- Together, they form a small production-style AI backend.

Why this day exists:
- yesterday-level learning is "I uploaded a file"
- interview-level learning is "I understand where storage sits in an AI product architecture"

## Visualization

```text
User uploads document
        |
        v
   GCS bucket stores file
        |
        v
 FastAPI app receives question
        |
        +--> fetch file metadata or reference
        |
        +--> send prompt/context to Gemini
        |
        v
 structured response returned
        |
        v
feedback + request logs later analyzed in BigQuery
```

## One Consistent Example

Use this example for everything today:

`Customer Support Knowledge Assistant`

Why this example is correct for today:
- support PDFs, FAQs, and policy docs can live in GCS
- FastAPI can expose `/chat`, `/healthz`, `/readyz`
- Gemini can summarize or answer using document context
- BigQuery can store feedback and request analytics

## Block-wise Understanding

### Block 1: Cloud Storage

Why it is here:
- AI apps need somewhere to keep files outside the app container
- examples: PDFs, CSVs, embeddings source files, evaluation datasets, logs exported as files

What goes in:
- documents
- model artifacts
- screenshots
- exported test data

What happens inside:
- files become objects inside buckets
- access is controlled by IAM or signed URLs

What comes out:
- durable storage
- retrievable artifacts
- sharable links when needed

### Block 2: FastAPI

Why it is here:
- interviewers want to see that you can expose reliable APIs, not just notebooks

What goes in:
- HTTP request with prompt and settings

What happens inside:
- validation
- logging
- model call
- error mapping

What comes out:
- JSON response with answer and trace info

### Block 3: Gemini

Why it is here:
- the model is the reasoning/generation engine
- but it must sit inside a controlled backend flow

What goes in:
- cleaned prompt
- optional context

What happens inside:
- generation
- potential upstream failures

What comes out:
- text response or model-side failure

### Block 4: BigQuery thinking

Why it is here today even if you do not build full integration yet:
- serious AI teams measure request behavior, feedback, and failures
- BigQuery is your bridge from app events to analysis

What goes in:
- request logs
- latency
- retries
- thumbs up/down feedback

What comes out:
- analytics
- debugging patterns
- later eval datasets

## Manual GCP Console Tasks

Do these manually first.

### Task A: Bucket understanding in Console

1. Open Cloud Storage in GCP Console.
2. Inspect one existing bucket or create a practice bucket.
3. Check:
   - name
   - region
   - storage class
   - public access prevention
   - uniform bucket-level access

What to observe:
- bucket name must be globally unique
- region and storage class are cost/performance decisions
- uniform access is simpler and more modern

### Task B: Upload one file manually

1. Upload one small text or PDF file.
2. Open the object details page.
3. Note:
   - object name
   - size
   - generation
   - metadata

Question to answer:
- what is bucket-level info vs object-level info?

### Task C: Signed URL concept

Manual understanding first:
- do not generate it yet if not needed
- first explain in your own words what problem a signed URL solves

Correct explanation:
- it gives temporary controlled access without making the whole bucket public

### Task D: Link to AI system

Look at the uploaded object and answer:
- if this were a support policy PDF, how would FastAPI know which file to summarize?

Expected answer:
- by object path, metadata, or a database record pointing to the GCS object

## Rich Notebook Topics

Open `notebook.ipynb` and make sure your notebook work follows these blocks.

### Notebook Block 1: High-level architecture

Write:
- one 5-line summary
- one ASCII diagram
- one note: why storage is outside the API app

### Notebook Block 2: GCS concepts

Write:
- bucket vs object
- standard vs nearline vs coldline vs archive
- uniform access vs fine-grained access

Minimal example:
- "FAQ PDF stored in a bucket, later referenced by API"

Common mistake:
- choosing a storage class before knowing access frequency

Fix:
- decide based on how often the file is read

Check question:
- why is Archive bad for frequently accessed files?

Tiny exercise:
- write one sentence for when to use `Standard` and one for when to use `Coldline`

### Notebook Block 3: FastAPI request flow

Write:
- request enters app
- Pydantic validates
- request_id added
- Gemini call happens
- JSON response returns

Minimal example:
- a POST request to `/chat`

Common mistake:
- thinking the model call should happen before input validation

Fix:
- validate first, fail fast

Check question:
- why should empty prompts fail before Gemini is called?

Tiny exercise:
- write one example invalid payload and expected status code

### Notebook Block 4: Reliability features

Write:
- timeout
- retry
- request_id
- health checks

Why they exist:
- they reduce chaos during failures

Minimal example:
- upstream Gemini times out, app retries, then returns safe error

Common mistake:
- treating retries as a fix for all failures

Fix:
- retries help only with temporary failures

Check question:
- when should you not retry?

Tiny exercise:
- describe one failure that should return `502`

### Notebook Block 5: Applied AI system thinking

Write:
- where GCS sits
- where FastAPI sits
- where Gemini sits
- where BigQuery can sit later

Minimal example:
- support-doc assistant

Common mistake:
- learning each tool separately with no system picture

Fix:
- always place the tool in a flow diagram

Check question:
- why is BigQuery useful even if Gemini already answers?

Tiny exercise:
- name 3 events you would store for later analysis

## SQL / BigQuery Topics for Today

Today’s SQL track should be relevant to the same AI backend.

Topic list:
- `ROW_NUMBER()`
- `RANK()`
- `DENSE_RANK()`
- `LAG()`
- `LEAD()`
- `PARTITION BY`

Why these matter:
- rank most frequent failures
- find latest request per user
- compare yesterday vs today latency
- analyze retries and error trends

Use the file:
- `DAY10_BIGQUERY_WINDOW_FUNCTIONS.sql`

## Debugging Artifact for Today

If anything breaks during manual work, record it.

Use this format:
- symptom
- trigger
- root cause
- fix
- prevention
- impact
- interview framing

Use the file:
- `DAY10_DEBUG_LOG_TEMPLATE.md`

## High-Probability Errors You May Hit Today

### Error 1: bucket name already exists

Why:
- GCS bucket names are globally unique

Fix:
- add project/date suffix

Interview value:
- shows real cloud naming constraints

### Error 2: permission denied on bucket/object

Why:
- missing IAM role or access policy mismatch

Fix:
- inspect IAM or uniform bucket-level access setting

Interview value:
- good story about access control and least privilege

### Error 3: FastAPI request fails validation

Why:
- blank prompt or out-of-range fields

Fix:
- correct payload and keep schema strict

Interview value:
- defensive API design

### Error 4: upstream Gemini call fails

Why:
- invalid config, rate limit, network, or model issue

Fix:
- log request id, inspect config, retry only when appropriate

Interview value:
- graceful degradation and observability

## Interview Questions for This Topic

### Q1. Why does Cloud Storage belong in an AI system?

Answer shape:
- AI systems need durable file storage
- buckets hold documents/artifacts outside the app container
- this helps with source docs, model files, exports, and reproducibility

### Q2. Why not keep files inside the FastAPI container?

Answer shape:
- containers are ephemeral
- scaling creates multiple instances
- shared durable storage should live outside the app instance

### Q3. What is the difference between `healthz` and `readyz`?

Answer shape:
- `healthz` says the process is alive
- `readyz` says the app is ready to serve traffic and dependencies are okay enough

### Q4. Why validate input before calling Gemini?

Answer shape:
- prevents wasted cost
- makes failures predictable
- improves safety and observability

### Q5. How would BigQuery help this system later?

Answer shape:
- store request analytics
- track retries and failure rates
- analyze user feedback
- build eval-like datasets from production traces

### Q6. Give one real debugging story from today.

Use:
- symptom
- root cause
- fix
- prevention
- impact

## If You Get Stuck

Do not break the streak.

Fallback completion plan:

1. Write the architecture diagram.
2. Finish the notebook theory blocks.
3. Solve 2 SQL queries from the SQL file.
4. Record one hypothetical debug artifact from a likely failure.
5. Commit the notes and SQL progress.

This still creates visible proof.

## End-of-Day Deliverables

Minimum:
- notebook updated with all 5 blocks
- 2 SQL queries solved
- 1 debug entry written
- 1 short interview answer written

Strong day:
- manual bucket exercise done
- FastAPI route behavior understood
- 5 SQL queries solved
- debug story converted to STAR

## 30-Second Interview Version

I studied how a small applied AI backend is structured using Cloud Storage, FastAPI, Gemini, and BigQuery-style analytics. I first learned the architecture manually, then mapped each component to its job: storage for documents, FastAPI for validated API flow, Gemini for generation, and BigQuery for later analysis. I also documented real failure paths like validation and access errors so I can explain production-style debugging, not just demos.
