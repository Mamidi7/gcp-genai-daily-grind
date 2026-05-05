# Plan: Context-Gen Skill for Krishna's Interview Prep

## Goal

Create a reusable Hermes skill that generates a rich, personalized context preamble Krishna can paste into ANY model (GLM, MiniMax, Claude, Gemini, GPT) to get tailored, high-quality responses instead of generic textbook answers.

Also works as a "go-to context pack" for Hermes sessions — Krishna runs the skill, gets a fresh context block, then asks better questions.

---

## Why This Matters

```
WITHOUT context:                    WITH context:
                                    
"Teach me RAG"                      [PASTED CONTEXT BLOCK]:
     |                              "I'm Krishna, preparing for Applied AI
     v                              roles at Anthropic/OpenAI/GCP. I've built
GLM searches its training           FastAPI+Gemini on Cloud Run, working on
data for most common "RAG"          RAG evals and agents. My stack: Vertex AI,
example → gives same generic         BigQuery, Cloud Run, Gemini 2.0..."
answer everyone gets.               
                                    "Teach me RAG" →
                                     |
                                     v
                                    Model now knows WHO you are, WHERE you
                                    are, WHAT you've built → gives examples
                                    grounded in YOUR stack, YOUR level.
```

---

## What The Skill Does

### Skill Name: `context-gen`
### Category: `productivity`

### Behavior

When Krishna invokes this skill, it:

1. **Reads his real state files** to build current snapshot:
   - `~/projects/GCP_GENAI/_INTERVIEW_PREP/applied ai/APPLIED_AI_SHOCK_VALUE_PLAN_V3.md`
   - `~/projects/GCP_GENAI/_INTERVIEW_PREP/applied ai/OPTIMIZED_47_DAY_SPRINT_PLAN.md`
   - `~/projects/gcp-genai-daily-grind/56_DAY_PRACTICE/DAILY_PREP_MAIN.md`
   - `~/projects/gcp-genai-daily-grind/56_DAY_PRACTICE/SESSION_STATE.md`
   - Latest day folder content (to detect current topic)

2. **Generates a compact context block** (~300-500 words) containing:
   - WHO: Krishna's target roles (Applied AI at Anthropic/OpenAI/GCP)
   - WHERE: Current progress (which day, what's deployed, what's proven)
   - WHAT: Tech stack (FastAPI, Gemini, Cloud Run, BigQuery, Vertex AI)
   - GAPS: What's still missing (evals, agents, RAG pipeline)
   - STYLE: Prefers simple explanations, ASCII diagrams, debugging rigor
   - CURRENT TOPIC: Whatever he's working on today

3. **Offers 4 context templates** based on what Krishna needs:
   - `concept` — learning a new topic
   - `coding` — building/debugging something
   - `interview` — preparing interview answers
   - `system-design` — designing a system

4. **Outputs a copy-paste ready block** that Krishna can paste into:
   - Any model's chat window (GLM, MiniMax, ChatGPT, Gemini, Claude)
   - Hermes as a preamble
   - A system prompt field if available

### Output Format (what the skill produces)

```
╔══════════════════════════════════════════════════════╗
║  CONTEXT PACK — Generated [DATE]                    ║
║  Mode: [concept/coding/interview/system-design]     ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  [Rich personalized context block, ~300-500 words]   ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

>>> Copy everything between the lines above and paste it
    BEFORE your question in any AI chat window.
```

---

## Skill Structure

```
~/.hermes/skills/productivity/context-gen/
├── SKILL.md                    # Main skill definition
├── templates/
│   ├── concept.md              # Template for learning new topics
│   ├── coding.md               # Template for building/debugging
│   ├── interview.md            # Template for interview prep
│   └── system-design.md        # Template for system design
└── scripts/
    └── generate_context.py     # Auto-reads state files and builds context
```

### SKILL.md Contents

**Frontmatter:**
- name: context-gen
- description: Generate rich personalized context blocks to paste before any AI question
- triggers: "context", "give me context", "prep context", "generate preamble"

**Body:**
1. Read the 5 source files listed above
2. Ask user which mode (concept / coding / interview / system-design)
3. Fill the selected template with real data from source files
4. Optionally accept a topic arg to add "CURRENTLY WORKING ON: [topic]"
5. Output the copy-paste block

### Templates

Each template is ~20 lines with placeholders like `{{CURRENT_DAY}}`, `{{DEPLOYED_APP}}`, `{{STACK}}`, `{{GAPS}}` that get filled from real file reads.

### generate_context.py Script

A Python script that:
- Reads the source files automatically
- Extracts key facts (current day, deployed URLs, completed topics)
- Fills template placeholders
- Prints the context block to stdout

This allows Krishna to run it standalone in terminal too:
```bash
python ~/.hermes/skills/productivity/context-gen/scripts/generate_context.py --mode concept --topic "RAG evals"
```

---

## Step-by-Step Plan

### Step 1: Create the skill directory structure
- `~/.hermes/skills/productivity/context-gen/SKILL.md`
- `~/.hermes/skills/productivity/context-gen/templates/` (4 files)
- `~/.hermes/skills/productivity/context-gen/scripts/generate_context.py`

### Step 2: Write SKILL.md
- Define the skill with clear triggers and behavior
- Include the source file list for reading state
- Define the 4 modes and when to use each

### Step 3: Write the 4 templates
- Each template is a markdown file with `{{PLACEHOLDER}}` syntax
- Templates are concise (300-500 words when filled)
- Each template has a different focus/emphasis

### Step 4: Write generate_context.py
- Reads the 5 source files
- Extracts: current day, deployed apps, tech stack, completed topics, gaps
- Accepts `--mode` and `--topic` arguments
- Fills template and prints to stdout
- Works standalone (no Hermes needed)

### Step 5: Test the skill
- Load it via `skill_view(name="context-gen")`
- Run it manually with each mode
- Verify output is copy-pasteable and ~300-500 words
- Test with GLM/MiniMax to confirm better responses

### Step 6: Save to memory
- Add a memory entry pointing to this skill
- So future sessions know to suggest it

---

## Files to Create

| File | Purpose |
|------|---------|
| `~/.hermes/skills/productivity/context-gen/SKILL.md` | Main skill definition |
| `~/.hermes/skills/productivity/context-gen/templates/concept.md` | Learning mode template |
| `~/.hermes/skills/productivity/context-gen/templates/coding.md` | Building mode template |
| `~/.hermes/skills/productivity/context-gen/templates/interview.md` | Interview mode template |
| `~/.hermes/skills/productivity/context-gen/templates/system-design.md` | System design template |
| `~/.hermes/skills/productivity/context-gen/scripts/generate_context.py` | Standalone script |

---

## Risks and Tradeoffs

1. **Stale context** — If Krishna doesn't update source files, context becomes outdated.
   - Mitigation: Script reads files fresh each time, so it auto-updates when files change.

2. **Too long context** — If preamble is too big, models might ignore parts of it.
   - Mitigation: Keep it under 500 words. Templates are designed to be compact.

3. **Model-specific behavior** — Some models handle system prompts differently.
   - Mitigation: Output is plain text, works as either system prompt or user message prefix.

4. **Privacy** — Context includes personal details (name, project URLs).
   - Mitigation: Flag this in the skill. Krishna can strip sensitive parts before pasting to public tools.

---

## Open Questions

1. Should we also generate a "system prompt" version (for APIs) alongside the "paste before question" version?
   - Recommendation: Yes, add as optional output format.

2. Should the script also pull from GitHub (commits, latest activity)?
   - Recommendation: V2 feature. Keep V1 simple with local files only.

3. Should we add a `--quiet` mode that just prints the block without any explanation?
   - Recommendation: Yes, useful for piping to clipboard.

---

## Verification

- [ ] Skill loads via `skill_view(name="context-gen")`
- [ ] Running the skill produces a copy-pasteable context block
- [ ] Context block is under 500 words
- [ ] Context block includes real data (not placeholder text)
- [ ] All 4 modes work (concept, coding, interview, system-design)
- [ ] Standalone script works without Hermes
- [ ] Pasting the block into GLM produces visibly better responses vs raw prompt
