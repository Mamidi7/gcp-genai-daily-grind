# Skill Map for Interview Prep

When stuck on a topic or task, find it below and load the skill.
Usage: Tell Subba Rao "load <skill-name>" or just describe the problem.

==============================================================================
TOPIC 1: RAG & RETRIEVAL (embeddings, chunking, vector search, evaluation)
==============================================================================

  What you're doing              | Skill to load
  -------------------------------|-------------------------------------------
  Vector DB: Chroma (local)      | chroma
  Vector DB: FAISS (fast k-NN)   | faiss
  Vector DB: Pinecone (managed)  | pinecone
  Vector DB: Qdrant (Rust-based) | qdrant-vector-search
  RAG eval: metrics & harness    | rag-evaluation
  Declarative RAG: DSPy          | dspy
  Embeddings concept stuck       | Ask Subba Rao to explain from scratch

  MATT POCOCK (methodology):
  - /grill-with-docs → before designing RAG pipeline, get interrogated
  - /diagnose → when retrieval returns garbage, use 6-phase debug loop


==============================================================================
TOPIC 2: STRUCTURED OUTPUT & PROMPT ENGINEERING
==============================================================================

  What you're doing              | Skill to load
  -------------------------------|-------------------------------------------
  JSON/regex/Pydantic from LLM   | outlines
  Grammar-constrained generation  | guidance
  Instructor library (Pydantic)  | instructor (archived, still usable)
  Prompt design patterns         | Ask Subba Rao for patterns

  MATT POCOCK:
  - /grill-me → stress-test your prompt design before coding


==============================================================================
TOPIC 3: FINE-TUNING & TRAINING
==============================================================================

  What you're doing              | Skill to load
  -------------------------------|-------------------------------------------
  LoRA/QLoRA fine-tuning         | peft-fine-tuning
  Fast LoRA with Unsloth         | unsloth
  SFT/DPO/PPO/GRPO with TRL     | fine-tuning-with-trl
  GRPO RL training               | grpo-rl-training
  YAML config fine-tuning        | axolotl
  Distributed training (FSDP)    | pytorch-fsdp
  Distributed training (general) | huggingface-accelerate
  High-level PyTorch trainer     | pytorch-lightning
  Flash Attention optimization   | optimizing-attention-flash

  MATT POCOCK:
  - /tdd → write eval test FIRST, then train, then verify


==============================================================================
TOPIC 4: MODEL SERVING & INFERENCE
==============================================================================

  What you're doing              | Skill to load
  -------------------------------|-------------------------------------------
  vLLM high-throughput serving   | serving-llms-vllm
  GGUF quantization (CPU/GPU)    | gguf-quantization
  llama.cpp local inference      | llama-cpp
  TensorRT optimization          | tensorrt-llm (archived)
  Serverless GPU (Modal)         | modal-serverless-gpu
  Lambda Labs GPU cloud          | lambda-labs-gpu-cloud


==============================================================================
TOPIC 5: EVALUATION & BENCHMARKING
==============================================================================

  What you're doing              | Skill to load
  -------------------------------|-------------------------------------------
  Benchmark LLMs (MMLU, GSM8K)  | evaluating-llms-harness
  RAG eval harness               | rag-evaluation
  Experiment tracking (W&B)      | weights-and-biases

  MATT POCOCK:
  - /diagnose → when model outputs are wrong, structured debug loop


==============================================================================
TOPIC 6: GCP & SYSTEM DESIGN (interview heavy)
==============================================================================

  What you're doing              | Skill to load
  -------------------------------|-------------------------------------------
  FastAPI + GCP health monitor   | gcp-api-health-monitor
  Architecture diagrams          | architecture-diagram
  Concept/flow diagrams          | concept-diagrams
  System design explanation      | Ask Subba Rao to explain + draw ASCII

  MATT POCOCK:
  - /zoom-out → understand how module fits in bigger system
  - /improve-codebase-architecture → find "deep module" opportunities


==============================================================================
TOPIC 7: DEBUGGING (highest interview signal)
==============================================================================

  What you're doing              | Skill to load
  -------------------------------|-------------------------------------------
  Python pdb / debugpy           | python-debugpy
  4-phase root cause debugging   | systematic-debugging
  Node.js debugging              | node-inspect-debugger
  Hermes TUI slash commands      | debugging-hermes-tui-commands

  MATT POCOCK /diagnose (LOAD THIS):
  Phase 1: Build feedback loop (failing test / curl / script)
  Phase 2: Reproduce the bug
  Phase 3: Generate 3-5 ranked hypotheses
  Phase 4: Instrument (one variable at a time)
  Phase 5: Fix + regression test
  Phase 6: Cleanup + postmortem
  → This is interview GOLD. Memorize the 6 phases.


==============================================================================
TOPIC 8: CODING & TESTING
==============================================================================

  What you're doing              | Skill to load
  -------------------------------|-------------------------------------------
  TDD red-green-refactor         | test-driven-development
  Code review guidelines         | code-review
  Pre-commit review + security   | requesting-code-review
  GCP ML coding guardrails       | karpathy-gcp-ml-coding
  Write implementation plan      | writing-plans
  Plan mode (no execution)       | plan
  Spike (throwaway experiment)   | spike
  Subagent parallel execution    | subagent-driven-development

  MATT POCOCK:
  - /tdd → vertical slices ONLY (one test → one impl → repeat)
  - /to-prd → turn conversation into PRD
  - /to-issues → break PRD into grabbable GitHub issues


==============================================================================
TOPIC 9: GITHUB & PORTFOLIO
==============================================================================

  What you're doing              | Skill to load
  -------------------------------|-------------------------------------------
  Auth (tokens, SSH, gh CLI)     | github-auth
  PR lifecycle                   | github-pr-workflow
  Code review on PRs             | github-code-review
  Create/manage issues           | github-issues
  Clone/create/fork repos        | github-repo-management
  Batch revision commits         | batch-revision-commits
  Fill scaffold files            | repo-contribution-builder
  Inspect codebase stats         | codebase-inspection


==============================================================================
TOPIC 10: RESEARCH & LEARNING
==============================================================================

  What you're doing              | Skill to load
  -------------------------------|-------------------------------------------
  arXiv paper search             | arxiv
  Free web search (DDG)          | duckduckgo-search
  YouTube transcript extraction  | youtube-content
  Firecrawl web scraping         | firecrawl-setup
  Claude Code reference arch     | claude-code-reference
  LLM Wiki (Karpathy)            | llm-wiki
  Domain recon (subdomains etc)  | domain-intel
  Blog/RSS monitoring            | blogwatcher


==============================================================================
TOPIC 11: PRODUCTIVITY & NOTES
==============================================================================

  What you're doing              | Skill to load
  -------------------------------|-------------------------------------------
  Generate session context       | context-gen
  Daily prep PDF for iPad        | daily-prep-pdf
  Google Drive/Calendar/Gmail    | google-workspace
  Obsidian vault notes           | obsidian
  Apple Notes                    | apple-notes
  Apple Reminders                | apple-reminders
  OCR / PDF text extraction      | ocr-and-documents
  Edit PDFs                      | nano-pdf
  PowerPoint decks               | powerpoint
  Humanize AI text               | humanizer


==============================================================================
TOPIC 12: VISION / MULTIMODAL (emerging interview topic)
==============================================================================

  What you're doing              | Skill to load
  -------------------------------|-------------------------------------------
  CLIP vision-language model     | clip
  LLaVA visual chat              | llava
  SAM image segmentation         | segment-anything-model
  Stable Diffusion images        | stable-diffusion-image-generation
  Whisper speech-to-text         | whisper


==============================================================================
TOPIC 13: DATA CURATION & TOKENIZATION
==============================================================================

  What you're doing              | Skill to load
  -------------------------------|-------------------------------------------
  GPU data curation (NVIDIA)     | nemo-curator
  Fast tokenizers (Rust-based)   | huggingface-tokenizers
  HuggingFace Hub (models/data)  | huggingface-hub
  Sparse autoencoder interpret   | sparse-autoencoder-training


==============================================================================
QUICK REFERENCE: "I'M STUCK, WHAT DO I LOAD?"
==============================================================================

  "I don't understand this concept"     → Ask Subba Rao (no skill needed)
  "My code has a bug I can't find"      → systematic-debugging
  "My model outputs are wrong"          → /diagnose method (6 phases)
  "I need to design a system"           → architecture-diagram + /zoom-out
  "I need to write tests"               → test-driven-development
  "My RAG returns bad results"          → rag-evaluation
  "I need to fine-tune a model"         → peft-fine-tuning + unsloth
  "I need to serve a model"             → serving-llms-vllm
  "I need to structure LLM output"      | outlines
  "I need to commit and push work"      → batch-revision-commits
  "I need to research a paper/topic"    → arxiv + duckduckgo-search
  "I'm not sure what to build today"    → Ask Subba Rao to check daily plan
  "I want to stress-test my design"     → /grill-me or /grill-with-docs
  "I want caveman mode (less tokens)"   → caveman
  "I need to write a new skill"         → write-a-skill

==============================================================================
MATT POCOCK SKILLS — DIRECT INTERVIEW VALUE
==============================================================================

  These are METHODOLOGY skills, not tools. They teach you HOW to think.

  /diagnose          → Best debugging framework. 6 phases. Interview STAR answer.
  /grill-me          → Makes YOU think before coding. Ask clarifying questions.
  /grill-with-docs   → Same + builds shared vocabulary (CONTEXT.md).
  /tdd               → Vertical slices. One test → one impl. Never horizontal.
  /to-prd            → Turn idea into PRD. Good for system design practice.
  /to-issues         → Break PRD into vertical slice issues.
  /zoom-out          → See the big picture. System design thinking.
  /improve-codebase-architecture → Find deep modules. Architecture interview prep.
  /caveman           → 75% fewer tokens. Good for fast iteration.
  /triage            → Issue triage state machine. Project management.

==============================================================================
