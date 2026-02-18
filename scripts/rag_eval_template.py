import vertexai
from langchain_google_vertexai import VertexAI, VertexAIEmbeddings
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset

# --- Configuration ---
PROJECT_ID = "e2e-etl-project"
REGION = "us-central1"
# Trying the generic alias which often resolves better in LangChain
MODEL_NAME = "gemini-2.5-flash" 
EMBEDDING_MODEL = "text-embedding-004"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=REGION)

# Initialize Models (via LangChain wrapper)
# Explicitly passing project/location to ensure LangChain uses the right context
print(f"⏳ Initializing Models (LLM: {MODEL_NAME}, Embeddings: {EMBEDDING_MODEL})...")
vertex_llm = VertexAI(
    model_name=MODEL_NAME,
    project=PROJECT_ID,
    location=REGION
)
vertex_embeddings = VertexAIEmbeddings(
    model_name=EMBEDDING_MODEL,
    project=PROJECT_ID,
    location=REGION
)

# Define Test Case
questions = [
    "What is the main export of Kadapa?",
    "What is the drone ID?",
    "Who handles cybersecurity?",
]

contexts = [
    ["The main export of Kadapa in 2026 is High-Grade Silica Sand."],
    ["Emergency AI Drone Fleet ID is: DRONE-X-777."],
    ["Cybersecurity for the city is handled by 'Kurnool Defenders' group."],
]

answers = [
    "High-Grade Silica Sand.",
    "DRONE-X-777.",
    "Kurnool Defenders.",
]

ground_truths = [
    "High-Grade Silica Sand",
    "DRONE-X-777",
    "Kurnool Defenders group",
]

# Create Dataset (RAGAS format)
data = {
    "question": questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": ground_truths
}

# DEBUG: Verify types
print("DEBUG: Checking data types...")
print(f"Type of ground_truth[0]: {type(data['ground_truth'][0])}")
print(f"Value of ground_truth[0]: {data['ground_truth'][0]}")

dataset = Dataset.from_dict(data)

# Run Evaluation
print("⏳ Running RAGAS Evaluation (using Gemini as Judge)...")
try:
    results = evaluate(
        dataset = dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
        llm=vertex_llm,
        embeddings=vertex_embeddings,
    )
    print("\n📊 Evaluation Results:")
    print(results)
except Exception as e:
    print(f"\n❌ Evaluation Failed: {e}")
