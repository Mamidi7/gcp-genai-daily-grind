# 📅 DAY 13: VERTEX AI + AGENTS

## 🎯 Today's Mission

**Main Topic:** Build your first agent on GCP Vertex AI
**Why:** Production agents need cloud deployment. GCP has Vertex AI Agent Builder.

---

## 🛠️ Agent Options on GCP

### Option 1: Vertex AI Agent Builder (NEW!)
- **What:** No-code agent builder
- **Use for:** Quick prototypes, retrieval agents
- **Docs:** cloud.google.com/vertex-ai/agent-builder

### Option 2: LangChain + Cloud Run
- **What:** Your own agent code deployed
- **Use for:** Custom agents, full control
- **Deploy:** Same as Day 11 project

### Option 3: Gemini API + Function Calling
- **What:** Gemini natively supports tools
- **Use for:** Simple tool-use agents

---

## 🧪 Hands-On: Build Agent with Function Calling

**Task:** Use Gemini's native function calling

```python
from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project="your-project", location="us-central1")

# Define a function
def get_weather(city: str) -> str:
    """Get weather for a city"""
    return f"Weather in {city}: 22°C, sunny"

# Configure function
tools = [{
    "function_declarations": [{
        "name": "get_weather",
        "description": "Get weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }]
}]

# Generate with function
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="What's the weather in San Francisco?",
    config=types.GenerateContentConfig(
        tools=tools,
    )
)

# Check if function was called
print(response.function_calls)
```

---

## 📝 Deploy Agent to Cloud Run

**Same process as Day 11-12:**
1. Write `app.py` with agent logic
2. `gcloud run deploy agent-service --source .`
3. Test endpoint

---

## ✅ Checkpoint

- [ ] Tried Gemini function calling
- [ ] OR built LangChain agent
- [ ] Deployed to Cloud Run (if time)
- [ ] Can explain: "I built an agent that uses tools"
