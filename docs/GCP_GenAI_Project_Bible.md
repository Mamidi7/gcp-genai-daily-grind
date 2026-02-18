# The GCP GenAI Project Bible - Your Interview & Learning Guide
*A living document of everything we've built, learned, and can "Flex" about in interviews.*

---

## 🏗️ 1. Project Overview: Agentic RAG & MLOps Pipeline
**Goal:** Build an intelligent "Agent" that can answer questions, use tools (Search, SQL, Weather), and automatically update itself via an MLOps pipeline.
**Stack:** Google Cloud Vertex AI, Gemini 2.0 Flash, Kubeflow Pipelines (KFP), Python.

---

## 🧠 2. Core Concepts & Architecture

### A. The "Agentic" Shift (Evolution from Chatbot to Agent)
*   **Old Way (Chatbot):** User asks -> LLM guesses based on training data -> Hallucinations.
*   **New Way (Agent):** User asks -> LLM *thinks* -> LLM calls a **Tool** (Function) -> Code executes -> LLM summarizes real data.
*   **Key Component:** `agentic_rag.py`
    *   **Reasoning Engine:** Gemini 2.0 Flash (Optimized for function calling).
    *   **Tools:**
        *   `search_knowledge_base`: Retrieval (RAG) for unstructured docs.
        *   `run_sql_query`: Structured data analysis.
        *   `get_current_weather`: Real-time external API.

### B. The "Hybrid Search" Strategy (Retrieval)
*   **Problem:** Vector Search (Embeddings) is great for meaning ("Is it hot?") but fails at exact matches ("Order #123"). Keyword Search (BM25) is great for exact matches but misses meaning.
*   **Solution:** **Hybrid Search** combines both.
*   **Analogy:**
    *   **Vector Search:** Asking a librarian "Show me books about sad romance." (Understand concepts).
    *   **Keyword Search:** Asking for "ISBN 978-3-16-148410-0." (Exact lookup).
    *   **Hybrid:** Doing both to get the best results.

### C. MLOps Pipeline (Automation & Productionizing)
*   **Problem:** Manually running scripts to update the AI's knowledge is slow, error-prone, and doesn't scale.
*   **Solution:** **Vertex AI Pipelines** (Kubeflow) orchestrated via `pipeline.py`.
*   **Workflow:**
    1.  **Ingest Data (`ingest_data_op`):**
        *   Connects to **BigQuery** (`e2e-etl-project.knowledge_base`).
        *   Fetches validated articles (filtering for `status='published'`).
        *   Handles missing tables gracefully (fallback logic for dev/test).
    2.  **Build Index (`build_index_op`):**
        *   Uses **Vertex AI TextEmbeddingModel** (`text-embedding-004`).
        *   **Batch Processing:** Handles API rate limits by batching requests (crucial for large datasets).
        *   Serializes the index (FAISS/Pickle) to a Model Artifact.
    3.  **Deploy (`deploy_agent_op`):**
        *   **CI/CD Integration:** Triggers **Cloud Build** to repackage the agent with the new index.
        *   Zero-downtime deployment to **Cloud Run**.
*   **Benefit:** Reproducibility. If data changes in BigQuery, the pipeline runs automatically (CI/CD for Data).

---

## 💻 3. The Code (Source of Truth)

### `agentic_rag.py` (The Brain)
```python
import vertexai
from vertexai.generative_models import GenerativeModel, Tool, FunctionDeclaration

# Initialize
vertexai.init(project="e2e-etl-project", location="us-central1")

# Define Tools (The "Hands")
search_tool = FunctionDeclaration(
    name="search_knowledge_base",
    description="Search internal docs for Kadapa Smart City info.",
    parameters={"type": "object", "properties": {"query": {"type": "string"}}}
)

# Load Model (The "Brain")
model = GenerativeModel("gemini-2.0-flash", tools=[Tool(function_declarations=[search_tool])])

# The Agent Loop
chat = model.start_chat()
response = chat.send_message("What's the traffic like?")
if response.function_call:
    # Execute tool & return result
    pass 
```

### `pipeline.py` (The Automation)
```python
from kfp import dsl
from kfp.v2.dsl import component

@component
def ingest_data_op(project_id: str):
    # Fetch data from BigQuery
    pass

@component
def build_index_op(project_id: str):
    # Create Embeddings using Vertex AI (Batched)
    pass

@dsl.pipeline(name="agentic-rag-pipeline")
def agentic_rag_pipeline(project_id: str):
    ingest = ingest_data_op(project_id=project_id)
    index = build_index_op(ingest.output, project_id=project_id)
    deploy = deploy_agent_op(index.output, project_id=project_id)
```

---

## 🎤 4. Interview "Flex" Stories (Cheat Sheet)

### 1. Agentic Tool Calling
**Situation:** "I upgraded a simple chatbot to an 'Agent' that could perform real-world actions."
**Action:** "I used **Gemini Function Calling**. I defined tools (`search_knowledge_base`, `run_sql`). When a user asks 'Count incidents', the model outputs a structured API call (`run_sql(...)`) instead of hallucinating."
**Result:** "Zero hallucinations on factual data. The model became an orchestrator."

### 2. MLOps Pipelines (Kubeflow)
**Situation:** "Manually updating the RAG index was error-prone and didn't scale with data velocity."
**Action:** "I built a **Vertex AI Pipeline**. I componentized `ingest`, `build_index`, and `deploy`. Now, a Cloud Scheduler trigger updates the system automatically."
**Result:** "Ensured data freshness and reproducibility."

### 3. Handling API Limits (Production Engineering)
**Situation:** "Embedding thousands of documents at once hit Vertex AI API quotas."
**Action:** "I implemented **batch processing** with exponential backoff in my `build_index_op` component. I batched requests (size 5-10) and added sleep intervals."
**Result:** "Pipeline runs reliably without `429 Too Many Requests` errors."

### 4. Hybrid Search
**Situation:** "Vector search failed on exact ID lookups (e.g., 'Order #123')."
**Action:** "I implemented **Hybrid Search** (Sparse Keyword + Dense Vector). This handled both semantic questions and exact keyword matches."
**Result:** "100% precision on ID lookups."

---

## 🔮 5. Future Learnings Log (To Be Updated)
*(This section will grow as we learn more!)*

*   **Next Topic:** [Pending]
*   **Date:** [Pending]
*   **Key Takeaway:** [Pending]
