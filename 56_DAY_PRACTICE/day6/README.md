# 🎬 Day 6: pip, venv, and Your First Package Install

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
```

---

## Required Packages for RAG

| Package | Purpose |
|---------|---------|
| `google-generativeai` | Gemini API SDK |
| `requests` | REST API calls |
| `python-dotenv` | Load .env files |
| `faiss-cpu` | Vector database |
| `langchain` | RAG framework |

---

## Interview Punch

> "I use venv to isolate each project's dependencies. Before any deployment, I run pip freeze to lock versions in requirements.txt — this ensures reproducibility."

---

## Resources
- pip docs: pip.pypa.io
- venv: docs.python.org/3/library/venv

---

*Mantra: Thaggedhe Le* 🔥
