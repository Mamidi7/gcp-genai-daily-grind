# 🌐 Day 7: Calling REST APIs + Your First AI Agent!
## 🔥 AGENTS = THE FUTURE

## Mission
Master REST API calls + Meet your first AI Agent!

---

## Today's Topics

### Part 1: REST APIs (30 min)
Call Gemini API directly using `requests` — no SDK. This is foundational.

### Part 2: AI Agents Intro (60 min) 🔥🔥🔥
**This is what's being hired for NOW.**

An agent can:
- Use tools (search, calculator, APIs)
- Make decisions
- Self-correct

---

## 🔥 WHY AGENTS ARE HOT

> "What they're hiring for is what's shipping in 6 months." — @TheGeorgePu

**Anthropic is hiring 65+ RL engineers for agent systems!**

```
Chatbot: User asks → AI responds
Agent: User asks → AI thinks → uses tools → acts → observes → responds
```

---

## Key Concepts

| Concept | What It Does |
|---------|--------------|
| `requests.get()` | Fetch data from server |
| `requests.post()` | Send data to server |
| `requests.headers` | Send authentication tokens |
| `response.json()` | Parse JSON response |
| `response.status_code` | Check if request succeeded |

---

## Hands-On Task 1: Call Gemini API Directly

```python
import requests
import os

API_KEY = os.environ.get("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

headers = {"Content-Type": "application/json"}

data = {
    "contents": [{
        "parts": [{"text": "Explain RAG in one sentence."}]
    }]
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())
```

---

## 🎯 YOUR FIRST AGENT (The Hot Stuff!)

### Install LangChain
```bash
pip install langchain langchain-openai
```

### Build Your First Agent
```python
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

# Define a tool - give the agent "hands"
def calculator(expression):
    """Math calculator"""
    try:
        return str(eval(expression))
    except:
        return "Error"

# Register tools
tools = [
    Tool(name="Calculator", func=calculator, description="Math calculations")
]

# Create agent
llm = ChatOpenAI(model="gpt-4")
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

# Ask agent to use tools
result = agent.run("If I have 25 apples, give 8 to John, 5 to Mary, how many left?")
print(result)
```

**What just happened?**
1. Agent saw a math problem
2. It REASONED: "I need to calculate"
3. It ACTED: Used the calculator tool
4. It RESPONDED with the answer

**That's an AI Agent! 🔥🔥🔥**

---

## Interview Punch

> "I built my first agent using LangChain — it can use tools to solve problems, not just generate text. The shift from chatbots to agents is what's driving Anthropic to hire 65+ RL engineers right now. That's where the industry is going."

---

## 📅 What's Next (This Week)

| Day | Topic | 🔥 Hot? |
|------|-------|----------|
| GCP + First Cloud Day 8 | Deployment | |
| Day 9 | GCS (Storage) | |
| Day 10 | BigQuery | |
| Day 11 | **AI Agents Deep Dive** || Day 12 🔥🔥🔥 |
 | **RL Fundamentals** | 🔥🔥🔥 |
| Day 13 | **GCP + Agents** | 🔥🔥🔥 |

---

## Today's Checkbox

- [ ] Call Gemini API with requests
- [ ] Install langchain
- [ ] Build first LangChain agent
- [ ] Agent uses calculator tool
- [ ] Understand: Agent = LLM + Tools + Loop
- [ ] **Tell someone: "I built an AI agent today!"**

---

*Mantra: Thaggedhe Le — Now you know agents!* 🔥🔥🔥
