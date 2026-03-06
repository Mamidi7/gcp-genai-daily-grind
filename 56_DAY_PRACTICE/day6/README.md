# 🎬 Day 6: pip, venv, and Your First Package Install
## 🔥 HOT TOPIC: Async Python (Mentioned in Anthropic Jobs!)

## Mission
Set up your Python environment professionally — install packages, manage dependencies!

## Today's Topic: pip, venv, requirements.txt

### 🐍 Virtual Environment Analogy
venv = Your project's personal bubble 🎈
- Isolates packages for each project
- Prevents version conflicts
- Keep projects clean and separate!

---

## Key Concepts

| Command | What It Does |
|---------|--------------|
| `python -m venv myenv` | Create virtual environment |
| `source myenv/bin/activate` | Activate (Mac/Linux) |
| `myenv\Scripts\activate` | Activate (Windows) |
| `pip install package` | Install a package |
| `pip freeze > requirements.txt` | Save all packages |
| `pip install -r requirements.txt` | Install from file |

---

## 🔥 BONUS: Why Async Python Matters

**Anthropic Job Requirement:**
> "Proficiency in Python and async/concurrent programming with frameworks like Trio"

**What is async?**
```python
# Sync: Wait for each API call
result1 = requests.get(url1)  # Wait...
result2 = requests.get(url2)  # Wait...
result3 = requests.get(url3)  # Wait...

# Async: Fire all at once
results = await asyncio.gather(
    fetch(url1),
    fetch(url2),
    fetch(url3)
)  # All at once!
```

---

## Hands-On Task

**Set up venv and install required packages:**

```bash
# 1. Create virtual environment
python -m venv gcp-ai-env

# 2. Activate it
source gcp-ai-env/bin/activate  # Mac/Linux
gcp-ai-env\Scripts\activate     # Windows

# 3. Install packages
pip install google-generativeai requests python-dotenv

# 4. Save dependencies
pip freeze > requirements.txt

# 5. Install async packages (for AI agents!)
pip install aiohttp asyncio
```

---

## Required Packages for RAG + Agents

| Package | Purpose |
|---------|---------|
| `google-generativeai` | Gemini API SDK |
| `requests` | REST API calls |
| `python-dotenv` | Load .env files |
| `faiss-cpu` | Vector database |
| `langchain` | RAG framework |
| `aiohttp` | **Async HTTP (HOT!)** |
| `langchain-openai` | OpenAI/Anthropic APIs |

---

## Interview Punch

> "I use venv to isolate each project's dependencies. Before any deployment, I run pip freeze to lock versions in requirements.txt — this ensures reproducibility. I'm also learning async Python because Anthropic lists it as a requirement for RL engineering roles."

---

## Resources
- pip docs: pip.pypa.io
- venv: docs.python.org/3/library/venv
- Async Python: docs.python.org/3/library/asyncio

---

## ⚡ Today's Hot Topic Checkbox

- [ ] Set up venv
- [ ] Install packages
- [ ] Understand async vs sync
- [ ] Know: "async = faster for multiple API calls"

---
*Mantra: Thaggedhe Le* 🔥
