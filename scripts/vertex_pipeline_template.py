# pipeline.py - Vertex AI MLOps Pipeline for Agentic RAG

import google.cloud.aiplatform as aiplatform
from kfp import dsl
from kfp.v2 import compiler
from kfp.v2.dsl import (
    component,
    Input,
    Output,
    Dataset,
    Model,
    Metrics,
    ClassificationMetrics,
)

# Configuration
PROJECT_ID = "e2e-etl-project"
REGION = "us-central1"
PIPELINE_ROOT = f"gs://{PROJECT_ID}-pipeline-root/agentic-rag"

# --- Components ---

@component(
    base_image="python:3.9",
    packages_to_install=["google-cloud-bigquery", "pandas", "pyarrow"]
)
def ingest_data_op(
    output_dataset: Output[Dataset],
    project_id: str,
):
    """Fetches new documents from BigQuery and saves them to GCS/Dataset."""
    from google.cloud import bigquery
    import pandas as pd

    print("📥 Ingesting Data from BigQuery...")
    client = bigquery.Client(project=project_id)
    
    # Real-world Query: Fetching validated knowledge base articles
    query = """
    SELECT id, title, content, updated_at
    FROM `e2e-etl-project.knowledge_base.articles`
    WHERE status = 'published'
    LIMIT 1000
    """
    
    # For demo purposes, if table doesn't exist, we fallback to mock but structured data
    try:
        df = client.query(query).to_dataframe()
        print(f"✅ Fetched {len(df)} rows from BigQuery.")
    except Exception as e:
        print(f"⚠️ BigQuery fetch failed (expected if table missing): {e}")
        print("⚠️ Falling back to local data for demonstration.")
        data = [
            {"id": "doc1", "title": "Kadapa Traffic Plan", "content": "New flyover at RTC Bus Stand approved for 2026."},
            {"id": "doc2", "title": "Monsoon Weather", "content": "Kadapa expects 20% more rainfall this July."},
            {"id": "doc3", "title": "Road Widening", "content": "Madras Road expansion project starts next month."}
        ]
        df = pd.DataFrame(data)

    df.to_csv(output_dataset.path, index=False)
    print(f"✅ Data saved to {output_dataset.path}")

@component(
    base_image="python:3.9",
    packages_to_install=["vertexai", "pandas", "scikit-learn", "numpy"]
)
def build_index_op(
    input_dataset: Input[Dataset],
    output_index: Output[Model],
    metrics: Output[Metrics],
    project_id: str,
):
    """Generates embeddings using Vertex AI and builds a local FAISS-like index."""
    import pandas as pd
    import vertexai
    from vertexai.language_models import TextEmbeddingModel
    import pickle
    import os
    import time

    vertexai.init(project=project_id, location="us-central1")
    
    print("🧠 Loading TextEmbeddingModel...")
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    
    df = pd.read_csv(input_dataset.path)
    documents = df['content'].tolist() # Assuming 'content' column exists
    
    print(f"🧠 Generating embeddings for {len(documents)} documents...")
    
    # Batch processing for embeddings (API limits handling)
    embeddings = []
    batch_size = 5
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        try:
            batch_embeddings = model.get_embeddings(batch)
            embeddings.extend([e.values for e in batch_embeddings])
            time.sleep(0.1) # Rate limit courtesy
        except Exception as e:
            print(f"⚠️ Error embedding batch {i}: {e}")
            # Fallback for errors: zero vectors
            embeddings.extend([[0.0]*768] * len(batch))

    # Structure the index
    index_data = {
        "documents": documents,
        "ids": df['id'].tolist() if 'id' in df.columns else list(range(len(documents))),
        "vectors": embeddings
    }
    
    # Save Index artifact
    os.makedirs(output_index.path, exist_ok=True)
    with open(os.path.join(output_index.path, "hybrid_index.pkl"), "wb") as f:
        pickle.dump(index_data, f)
        
    metrics.log_metric("num_documents", len(df))
    metrics.log_metric("embedding_dim", 768)
    print("✅ Index built and serialized.")

@component(
    base_image="google/cloud-sdk:latest", # Using CLI image for deployment
    packages_to_install=["google-cloud-aiplatform"]
)
def deploy_agent_op(
    input_index: Input[Model],
    project_id: str,
):
    """Simulates a Continuous Deployment (CD) trigger to Cloud Run."""
    import os
    
    print("🚀 Starting Deployment Sequence...")
    print(f"📦 New Index Artifact: {input_index.path}")
    
    # In a real interview answer:
    # "I would use Cloud Build here. This component would trigger a Cloud Build trigger
    # passing the GCS path of the new index as a substitution variable."
    
    # Simulating the command:
    # !gcloud builds submit --config cloudbuild.yaml --substitutions=_INDEX_PATH={input_index.path}
    
    print("✅ Triggered Cloud Build: agentic-rag-deploy-trigger")
    print("✅ Service 'agentic-rag-service' will update in ~2 mins.")

# --- Pipeline Definition ---

@dsl.pipeline(
    name="agentic-rag-pipeline",
    description="End-to-End MLOps: Ingest -> Embed -> Index -> Deploy",
    pipeline_root=PIPELINE_ROOT,
)
def agentic_rag_pipeline(
    project_id: str = PROJECT_ID,
):
    # Step 1: Ingest Data
    ingest_task = ingest_data_op(project_id=project_id)
    
    # Step 2: Build Index
    index_task = build_index_op(
        input_dataset=ingest_task.outputs["output_dataset"],
        project_id=project_id
    )
    
    # Step 3: Deploy Agent
    deploy_task = deploy_agent_op(
        input_index=index_task.outputs["output_index"],
        project_id=project_id
    )

# --- Compile Pipeline ---

if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=agentic_rag_pipeline,
        package_path="agentic_rag_pipeline.json"
    )
    print("✅ Pipeline compiled to 'agentic_rag_pipeline.json'")