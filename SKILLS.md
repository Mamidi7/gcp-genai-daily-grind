# Recommended Skills for GCP GenAI Daily Grind

> Auto-generated on 2026-05-01  
> This file tracks the AI skills most useful for this project's interview prep workflow.

---

## Quick Start

Run these commands to load the right skills for your current activity:

```bash
# Learning / Study Mode
hermes -s karpathy-gcp-ml-coding,duckduckgo-search,arxiv,concept-diagrams

# Coding / Building Mode
hermes -s python-patterns,python-testing,api-design,fastapi-python,karpathy-gcp-ml-coding

# Research / Deep Dive Mode
hermes -s firecrawl-search,firecrawl,duckduckgo-search

# ML / RAG / Fine-tuning Mode
hermes -s peft-fine-tuning,huggingface-accelerate,chroma,pinecone,rag-evaluation

# Diagram / System Design Mode
hermes -s concept-diagrams,excalidraw

# Code Review / Debug Mode
hermes -s karpathy-gcp-ml-coding,systematic-debugging,github-code-review
```

Or use the launcher script:
```bash
~/.hermes/scripts/gcp-prep-mode.sh learn
~/.hermes/scripts/gcp-prep-mode.sh code
~/.hermes/scripts/gcp-prep-mode.sh research
```

---

## Hermes Skills (Installed)

### Core Coding & Quality
| Skill | Use Case |
|-------|----------|
| `karpathy-gcp-ml-coding` | Surgical changes, debugging rigor, simplicity first |
| `python-patterns` | PEP 8, type hints, pythonic idioms |
| `python-testing` | pytest, TDD, fixtures, mocking |
| `api-design` | REST API design, status codes, versioning |
| `fastapi-python` | FastAPI development patterns |
| `systematic-debugging` | Debug methodology, root cause analysis |

### AI / ML / LLM
| Skill | Use Case |
|-------|----------|
| `peft-fine-tuning` | LoRA, QLoRA for Project 2 fine-tuning |
| `huggingface-accelerate` | Distributed training setup |
| `huggingface-hub` | Model download, upload, versioning |
| `huggingface-tokenizers` | Fast tokenization for RAG |
| `chroma` | Local vector DB for RAG experiments |
| `pinecone` | Managed vector DB for production RAG |
| `qdrant-vector-search` | Alternative local vector DB |
| `rag-evaluation` | RAGAs metrics, retrieval quality |
| `clip` | Vision-language, multimodal basics |
| `llava` | Visual instruction tuning |

### Search / Research / Scraping
| Skill | Use Case |
|-------|----------|
| `firecrawl-search` | AI-powered web search + extraction |
| `firecrawl` | Web scraping, crawling |
| `firecrawl-setup` | Firecrawl MCP server setup |
| `duckduckgo-search` | Free web search (no API key) |
| `arxiv` | Academic paper search |
| `domain-intel` | Passive domain reconnaissance |

### Visualization / Diagrams
| Skill | Use Case |
|-------|----------|
| `concept-diagrams` | SVG architecture diagrams, flowcharts |
| `excalidraw` | Hand-drawn style diagrams for interviews |

---

## OpenCode / Claude Skills (Auto-Loaded)

These live in `~/.agents/skills/` and activate automatically when relevant:

| Skill | Use Case |
|-------|----------|
| `gcp-daily-prep` | 45-day GCP AI/ML interview prep workflow |
| `python-patterns` | Python best practices |
| `python-testing` | pytest, TDD strategies |
| `docker-patterns` | Docker, Compose, orchestration |
| `deployment-patterns` | CI/CD, health checks, rollbacks |
| `backend-patterns` | API design, database optimization |
| `postgres-patterns` | PostgreSQL schema, indexing, queries |
| `api-design` | REST API production patterns |
| `firecrawl-*` | Full firecrawl suite (8 skills) |
| `coding-standards` | TS/JS/React/Node best practices |

---

## Missing Skills (Retry Later)

These failed to install due to registry issues. Retry with:

```bash
hermes skills install vertex-ai-api-dev --force -y
hermes skills install gemini-api-dev --force -y
hermes skills install tavily-search --force -y
```

---

## Health Check

Run this to verify all critical skills are ready:

```bash
bash ~/.hermes/scripts/skill-health-check.sh
```

---

## Skill Arsenal Document

Full details at: `~/.hermes/CURATED_SKILLS.md`

