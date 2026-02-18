import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from vertexai.generative_models import GenerativeModel
import numpy as np

# Initialize Vertex AI
vertexai.init(project="e2e-etl-project", location="us-central1")

# Load Models
embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
gen_model = GenerativeModel("gemini-2.5-flash")

def get_embedding(text, task_type="RETRIEVAL_DOCUMENT"):
    inputs = [TextEmbeddingInput(text, task_type)]
    embeddings = embedding_model.get_embeddings(inputs)
    return embeddings[0].values

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def build_stores(file_path="/Users/krishnavardhan/projects/GCP_GENAI/vertex-ai-genai/knowledge_base.txt"):
    print("⏳ Building Hybrid Index...")
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # 1. Vector Store (for Semantic Search)
    vector_store = []
    
    # Batch processing to respect API limits
    batch_size = 5
    print(f"🧠 Generating embeddings for {len(lines)} documents in batches of {batch_size}...")
    
    for i in range(0, len(lines), batch_size):
        batch = lines[i:i+batch_size]
        try:
            # Prepare inputs for batch embedding
            inputs = [TextEmbeddingInput(text, "RETRIEVAL_DOCUMENT") for text in batch]
            embeddings = embedding_model.get_embeddings(inputs)
            
            # Map embeddings back to text
            for j, text in enumerate(batch):
                vector_store.append({"text": text, "vector": embeddings[j].values})
            
            # Rate limit handling (simple sleep)
            import time
            time.sleep(0.5) 
            
        except Exception as e:
            print(f"⚠️ Error embedding batch {i}: {e}")
            # Skip this batch to prevent crash
            continue

    # 2. Keyword Store (just the list of lines for now)
    keyword_store = lines
    
    print(f"✅ Indexed {len(vector_store)} documents.")
    return vector_store, keyword_store

def keyword_search(query, keyword_store):
    """Simple keyword matching."""
    results = []
    query_words = query.lower().split()
    for line in keyword_store:
        if any(word in line.lower() for word in query_words if len(word) > 3):
            results.append(line)
    return results

def vector_search(query, vector_store, top_k=2):
    """Semantic search."""
    query_vector = get_embedding(query, "RETRIEVAL_QUERY")
    scored_docs = []
    for doc in vector_store:
        score = cosine_similarity(query_vector, doc["vector"])
        scored_docs.append((score, doc["text"]))
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return [d[1] for d in scored_docs[:top_k]]

def hybrid_retrieve(query, vector_store, keyword_store):
    # 1. Get Keyword Results
    kw_results = keyword_search(query, keyword_store)
    
    # 2. Get Vector Results
    vec_results = vector_search(query, vector_store)
    
    # 3. Combine (Deduplicate)
    combined = list(set(kw_results + vec_results))
    
    # print(f"[Debug] Keyword found: {len(kw_results)}, Vector found: {len(vec_results)}")
    return combined

def rag_chat():
    vector_store, keyword_store = build_stores()
    
    print("\n🤖 Ask me about Kadapa Smart City! (Hybrid Powered)")
    while True:
        query = input("You: ")
        if query.lower() in ["quit", "exit"]:
            break
            
        # HYBRID RETRIEVAL
        results = hybrid_retrieve(query, vector_store, keyword_store)
        context_str = "\n".join(results)
        
        if not context_str:
            print("Gemini: I don't have information about that.\n")
            continue

        prompt = f"""
        Answer the question based ONLY on the following context:
        
        Context:
        {context_str}
        
        Question: {query}
        """
        response = gen_model.generate_content(prompt)
        print(f"Gemini (Hybrid RAG): {response.text}\n")

if __name__ == "__main__":
    rag_chat()