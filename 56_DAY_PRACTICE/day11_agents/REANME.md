# 📅 DAY 11: AI AGENTS + ASYNC PYTHON

## 🎯 Today's Mission

**Main Topic:** AI Agents + Async Python
**Why:** Anthropic is hiring for RL + agents NOW. This is infant stage — learn now, own later.

---

## 📚 STUDY MATERIAL

### Part 1: Async Python (30 min)
- **Resource:** Python docs: asyncio (docs.python.org/3/library/asyncio.html)
- **Why:** Job requirement from Anthropic: "Proficiency in Python and async/concurrent programming"

**Task:** Write an async function that calls 3 APIs concurrently

```python
import asyncio
import aiohttp

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [await r.json() for r in responses]
```

### Part 2: AI Agents Introduction (60 min)
- **Resource:** LangChain Agents docs: python.langchain.com/docs/modules/agents
- **Watch:** Andrej Karpathy "Let's build GPT" (first 30 min) — understand: input → model → output

**Core Concept:**
```
Agent = LLM (brain) + Tools (hands) + Memory (context) + Loop (think → act → observe)
```

### Part 3: Your First Agent (90 min)
- **Build:** Simple ReAct agent with LangChain
- **Tools:** Calculator, search (serpapi or mock)
- **Concept:** Agent decides WHEN to use tools

---

## 🛠️ Hands-On Task

**Build a simple agent that:**
1. Takes a user question
2. Decides: "Do I need a calculator?" or "Can I answer directly?"
3. Uses tool if needed
4. Returns answer

**File:** `day11_simple_agent.py`

```python
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

# Simple calculator tool
def calculator(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"

tools = [
    Tool(name="Calculator", func=calculator, description="数学计算")
]

# Initialize agent
llm = ChatOpenAI(model="gpt-4o")
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

# Test
result = agent.run("If I have 15 apples and give away 7, then multiply by 3, how many do I have?")
print(result)
```

---

## 📝 SQL Track (30 min)

Continue your SQL progress. Today's focus: Window Functions

**Task:** Write a query using LAG() to compare consecutive days

```sql
SELECT
    date,
    revenue,
    LAG(revenue) OVER (ORDER BY date) as prev_day_revenue,
    revenue - LAG(revenue) OVER (ORDER BY date) as change
FROM daily_sales
```

---

## ✅ Checkpoint

- [ ] Async Python: Can write concurrent API calls
- [ ] Agent: Understand agent = LLM + tools + loop
- [ ] Built: Simple ReAct agent
- [ ] SQL: Window functions working

---

## 🔥 Interview Talking Point

> "I'm building with LangChain Agents — the shift from chatbots to agents that can use tools and make decisions. Anthropic is hiring 65+ RL engineers right now — this agentic wave is the next big thing."

