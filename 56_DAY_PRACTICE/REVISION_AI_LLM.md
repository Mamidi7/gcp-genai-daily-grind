# 🤖 AI & LLM Cheat Sheet — 10th Std Level

> Simple ga explain cheyyali! 😎

---

## 1. LLM — Large Language Model

**What is it?**
LLM ante oka huge brain training chesina model. Internet lo undhiEla data ni train chesi, text generate cheyyataniki learn ayyindi.

**Simple:**
```
Internet lo entire books, websites, code...
        ↓
    TRAIN CHEYYI
        ↓
LLM Model (like Gemini, GPT)
        ↓
User: "Hello" → Model: "Hi! How can I help?"
```

**Common LLMs:**
| Model | Company | Use Case |
|-------|---------|----------|
| Gemini | Google | General purpose |
| GPT | OpenAI | General purpose |
| Claude | Anthropic | Coding, analysis |
| Llama | Meta | Open source |

---

## 2. RAG — Retrieval Augmented Generation

**What is it?**
RAG ante - LLM ki extra brain add cheyyataniki. LLM emaina knowladge ledhu kani, emaina documents ni search chesi answer generate cheyyachu.

**Why RAG?**
- LLM outdated info adi (2024 data kani 2026 answer)
- Hallucinations (fake answers)
- Specific company data use cheyyalaniki

**How it works:**
```
User Query: "My company policy?"
        ↓
1. Search (Vector DB) ← Documents
        ↓
2. Get relevant chunks
        ↓
3. Send to LLM: "Here are docs + Question"
        ↓
4. LLM generates answer based on docs
        ↓
Final Answer
```

**Code Simple:**
```python
# Step 1: Split text into chunks
text = "large document..."
chunks = chunk_text(text, size=500)

# Step 2: Convert to embeddings
embeddings = model.encode(chunks)

# Step 3: Store in vector DB
vector_db.add(embeddings, chunks)

# Step 4: Query
query_embedding = model.encode("question")
results = vector_db.search(query_embedding)

# Step 5: Send to LLM
response = llm.generate(f"Context: {results}\nQuestion: {question}")
```

---

## 3. Embeddings — Text to Numbers

**What is it?**
Embeddings ante text ni numbers (vectors) lo convert cheyyataniki. Computer ki text kakunda numbers easiest.

```
"cat" → [0.1, 0.3, -0.2, ...]
"dog" → [0.1, 0.3, -0.1, ...]   ← Similar!
"car" → [0.9, -0.5, 0.2, ...]  ← Different!
```

**Use?**
- Similarity search (Find related content)
- RAG lo documents match cheyyalaniki
- Clustering

---

## 4. Vector Database

**What is it?**
Embeddings ni store cheyyadaniki database. Fast ga search cheyyali ante vector DB use cheyyachu.

**Popular:**
| Database | Type |
|----------|------|
| Pinecone | Cloud |
| Chroma | Local |
| Weaviate | Open source |
| pgvector | PostgreSQL extension |
| Vertex AI Vector Search | GCP |

---

## 5. Prompt Engineering

**What is it?**
Prompt ante LLM ki question/query. Good prompt = Good answer.

**Tips:**
```python
# ❌ Bad
"Summarize"

# ✅ Good
"Summarize this article in 3 bullet points:
- Keep it brief
- Use simple language
- Include main takeaways"
```

**Few-Shot Learning:**
```python
# Give examples first
prompt = """
Task: Sentiment analysis

Example:
"This is great!" → Positive
"This is bad" → Negative

Now analyze: "I love this product"
"""
```

---

## 6. Tool Calling — LLM ni Tool Use Cheyyamantha

**What is it?**
LLM ki tools (functions) call cheyyataniki allow cheyyi. LLM alone text generate cheyyi, kani external API call cheyyali ante tool calling use.

```python
# Define tool
def get_weather(city):
    return {"temp": 25, "city": city}

# LLM decides to call tool
response = model.generate(
    contents="What's weather in Bangalore?",
    tools=[get_weather]  # Give tool to LLM
)
# LLM calls get_weather("Bangalore") automatically
```

---

## 7. Agents — LLM + Tools + Memory

**What is it?**
Agent ante - LLM + Tools + Memory + Loop. LLM oka task complete cheyyali ante, tools use chesi, step by step proceed cheyyi.

**Simple Flow:**
```
Task: "Book flight to Delhi"
        ↓
1. Agent thinks: Need to check flights
2. Calls flight API tool
3. Gets options
4. Agent decides: Book cheapest
5. Calls booking tool
6. Done!
```

**Key Components:**
- LLM (Brain)
- Tools (Actions)
- Memory (History)
- Loop (Repeat until done)

---

## 8. Hallucinations — Fake Answers

**What is it?**
LLM create chesina false information. LLM bayataki correct anipisthundi, kani sometimes fake facts generate cheyyi.

**How to reduce:**
1. RAG use cheyyi (context provide)
2. Prompt lo "Only use provided context"
3. Evaluation (RAGAs) do
4. Fine-tune on correct data

---

## 9. Context Caching — Save Money!

**What is it?**
Same context repeat use cheste, cache lo store chesi money save cheyyi. GCP Feature.

**Example:**
```
Without cache: Every request → Full prompt → Pay full price
With cache: First request → Pay full
           Repeat requests → Pay cheap (cache hit!)
```

**Savings:** Up to 50% cost reduction!

---

## 10. Chunking — Big Text ni Small Pieces

**What is it?**
Large document ni small chunks lo divide cheyyi. LLM ki ekkuva data send cheyyale, so chunking needed.

**Methods:**
```python
# Fixed size
chunks = []
for i in range(0, len(text), 500):  # 500 chars each
    chunks.append(text[i:i+500])

# Sentence based
chunks = text.split('. ')  # By sentences
```

---

## Quick Interview Answers

| Question | Answer |
|----------|--------|
| What is RAG? | LLM gets external info to answer accurately |
| Why RAG? | Reduces hallucinations, uses fresh/specific data |
| What are embeddings? | Text converted to numbers for similarity search |
| How do vectors help? | Similar items have similar numbers |
| What is an Agent? | LLM + Tools + Loop to complete tasks |
| Hallucination? | LLM giving false/fake information |
| Reduce hallucinations? | RAG, better prompts, evaluations |
| Context caching? | Reuse same context to save API costs |

---

*Last Updated: Feb 26, 2026*
