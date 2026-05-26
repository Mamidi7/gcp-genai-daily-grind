# Webwright Deep Dive — Microsoft Research (May 2026)

> Inspected: 2026-05-26 | Source: https://github.com/microsoft/Webwright | ~3.8K LoC total, ~1.5K core harness

---

## 30-Second Pitch

Webwright gives an LLM a terminal, a local workspace, and Playwright. Instead of predicting the next click in a locked browser session, the model writes Python scripts that spawn disposable browsers, take screenshots, and save artifacts. The durable output is code, not browser state. SOTA on long-horizon web tasks: 60.8% Odysseys, 86.7% Online-Mind2Web.

---

## Core Idea in 3 Lines

1. **Separate agent from browser.** Traditional agents are chained to one browser tab. Webwright treats the browser as disposable — spawn, inspect, discard.
2. **Code composes actions.** Multi-step interactions (date selection, filtering, form filling) become loops and functions in a Python script, not long chains of primitive actions.
3. **Workspace is state.** Code, logs, screenshots, and `final_script.py` persist. The browser does not.

---

## Architecture — 3 Modules, ~1K Lines

```
webwright/
├── src/webwright/
│   ├── agents/default.py      (~450 LoC) — Runner: send context → get bash → loop
│   ├── environments/          (~570 LoC) — Terminal + Playwright browser workspace
│   │   ├── local_workspace.py   — bash execution, file I/O, workspace mgmt
│   │   └── local_browser.py     — local Playwright/CDP browser helpers
│   ├── models/                (~150-200 LoC each) — OpenAI, Anthropic, OpenRouter
│   │   ├── base.py              — format_message, observation formatting, serialize
│   │   ├── openai_model.py
│   │   ├── anthropic_model.py
│   │   └── openrouter_model.py
│   ├── tools/                 — image_qa, self_reflection (visual verification)
│   ├── run/cli.py             (~150 LoC) — Typer CLI entrypoint
│   └── config/
│       ├── base.yaml            — Main system + instance prompt templates
│       ├── model_openai.yaml
│       ├── model_claude.yaml
│       └── model_openrouter.yaml
```

### The Agent Loop (`agents/default.py`)

```python
def run(self, task: str = "", **kwargs):
    # 1. Build messages: system prompt + instance prompt
    self.messages = [system_msg, user_msg]
    while True:
        self.step()   # query model → execute actions → observe → append
        if done: break
        if step_limit_reached: break
        if every_n_steps: compact_history()  # LLM summarization to save tokens
```

```python
def step(self):
    return self.execute_actions(self.query())

def query(self):
    message = self.model.query(self.messages)  # LLM call
    self.n_calls += 1
    self.add_messages(message)
    return message

def execute_actions(self, message):
    extra = message.get("extra", {})
    if extra.get("done"):
        # Gate: require self_reflection success before declaring done
        gate_error = self._self_reflection_gate_error()
        if gate_error: return gate_error_message
        return exit_message
    outputs = [self.env.execute(action) for action in extra.get("actions", [])]
    observation_messages = self.model.format_observation_messages(message, outputs, vars)
    return self.add_messages(*observation_messages)
```

Key design: `done=true` is GATED. The agent cannot declare completion until:
1. `plan.md` exists with critical points
2. `self_reflect_config.json` exists with 4 prompts
3. `final_script.py` ran successfully in `final_runs/run_<id>/`
4. `self_reflection` tool exited 0 with `predicted_label: 1`

This forces the model to produce verifiable artifacts, not just claim success.

---

## Environment — Two Modes

| Mode | How | Credentials Needed |
|------|-----|-------------------|
| `local` | `playwright.chromium.launch(headless=True)` | None |
| `browserbase` | Browserbase cloud session via CDP | `BROWSERBASE_API_KEY`, `BROWSERBASE_PROJECT_ID` |

The environment executes bash commands from the model. If the command writes a Python script with Playwright, the environment runs it. stdout, stderr, screenshots, and files become the next observation.

---

## Prompt Engineering — System Template

The `base.yaml` system template is massive (~23K chars) and explicitly instructs the model to:

- Emit ONE strict JSON object per turn with `thought`, `bash_command`, `done`, `final_response`
- Use heredocs for inline Python: `python - <<'PY' ... PY`
- Never use `full_page=True` screenshots (viewport 1280x1800 only)
- Save screenshots to `final_runs/run_<id>/screenshots/`
- Write action logs to `final_runs/run_<id>/final_script_log.txt`
- Use `image_qa` tool for visual verification during exploration
- Author `self_reflect_config.json` once, reuse it
- Run `self_reflection` before declaring done
- If self_reflection fails, fix `final_script.py`, rerun in NEW `run_<id+1>/`, re-run reflection

This is not an agent framework — it is a **constraint document**. The entire intelligence is in the prompt. The harness just enforces the loop and gates.

---

## Self-Reflection Tool

Two-stage visual judge:

1. **Stage 1 (per-image):** Each screenshot scored 1-5 against critical points from `plan.md`.
2. **Stage 2 (aggregate):** All per-image reasonings + action log → final verdict `Status: success|failure`.

Requires OpenAI API key (uses GPT-4o for vision). This is the only hard dependency on OpenAI regardless of which backend drives the main loop.

---

## Performance Benchmarks

| Benchmark | Score | Notes |
|-----------|-------|-------|
| Online-Mind2Web (300 tasks, 136 sites) | **86.7%** | GPT-5.4, 100-step budget. Highest open-source harness in AutoEval. |
| Odysseys (200 long-horizon tasks) | **60.8%** | +35.1% relative over prior SOTA. Avg 76.1 steps. |
| Small model + tools | **66.2%** | Qwen3.5-9B with 5+ reusable CLI tools on hard split. |

Key insight: **Code-as-action beats coordinate prediction.** Writing Playwright scripts is more robust than predicting x,y clicks from screenshots, especially on long horizons where error accumulation kills pure action chains.

---

## Plugin Ecosystem

| Platform | How | Notes |
|----------|-----|-------|
| Claude Code | `.claude-plugin/plugin.json` + `skills/webwright/` | Slash commands: `/webwright:run`, `/webwright:craft` |
| OpenAI Codex | `.codex-plugin/plugin.json` | Same marketplace format as Claude |
| OpenClaw | `openclaw plugins install /path/to/Webwright` | Skill loads automatically |
| **Hermes Agent** | `ln -sfn /path/to/Webwright/skills/webwright ~/.hermes/skills/webwright` | **No manifest needed. SKILL.md only.** |

Hermes integration is simplest: just symlink the skill folder. The `SKILL.md` tells Hermes to use its native `Bash`/`Read`/`Write`/`Edit` tools exactly like the Webwright harness uses bash commands. No extra API keys needed because Hermes reads screenshots natively.

---

## How It Differs From Tools I Know

| | Webwright | browser-use | Stagehand (Browserbase) |
|--|-----------|-------------|------------------------|
| **Paradigm** | Coding agent + terminal | Autonomous LLM over DOM/AX | Hybrid code + NL primitives |
| **Action space** | Free-form Python scripts | Indexed click/type | Playwright or NL→LLM |
| **State** | Workspace (code, logs) | Browser session | Browser session |
| **Browser** | Disposable, spawnable | Persistent | Persistent |
| **Orchestration** | None — flat loop | None — flat loop | Imperative `agent()` |
| **Output** | Reusable `final_script.py` | Action trace | Extracted data |
| **Lines of code** | ~1.5K harness | ~3K+ | Heavy framework |

---

## Local Setup (Verified)

```bash
# 1. Clone
git clone https://github.com/microsoft/Webwright.git
cd Webwright

# 2. Install (verified on macOS 26.5, Python 3.13)
pip install -e .
playwright install chromium

# 3. Verify CLI
python3 -m webwright.run.cli --help

# 4. Run (requires API key)
export OPENAI_API_KEY=...
python3 -m webwright.run.cli \
    -c base.yaml -c model_openai.yaml \
    -t "Search for flights from SEA to JFK on 2026-08-15" \
    --start-url https://www.google.com/flights \
    --task-id demo \
    -o outputs/default
```

**Current blocker:** No OpenAI/Anthropic/OpenRouter API keys in environment. Cannot run live tasks without one. The `image_qa` and `self_reflection` tools specifically require OpenAI even if main loop uses another backend.

---

## Interview Conversion

### 90-Second STAR Answer

> **Situation:** I was evaluating agent architectures for long-horizon web automation tasks where traditional step-by-step click prediction fails due to error accumulation.
> **Task:** Find a minimal, debuggable approach that produces reusable artifacts.
> **Action:** I inspected Microsoft Research's Webwright — a terminal-native harness where the LLM writes Playwright scripts instead of predicting individual clicks. The agent loop is just 450 lines: send context, get bash command, execute, observe, repeat. The key gate is that `done=true` is blocked until a `self_reflection` tool verifies screenshots against critical points from `plan.md`.
> **Result:** Webwright hits 60.8% on Odysseys (long-horizon) and 86.7% on Online-Mind2Web — with only ~1.5K lines of harness code and no orchestration tower. The insight is that code-as-action beats coordinate prediction because loops and functions generalize across similar tasks.

### 3-Minute Technical Walkthrough

> "Most web agents treat the browser session as state. At each step the model sees the current page and predicts one action — click, type, scroll. This is fragile on long tasks because one wrong action corrupts the session state.
>
> Webwright inverts this: the model gets a terminal and a workspace folder. It writes Python scripts that launch fresh Playwright browsers, navigate, interact, screenshot, and log. The browser is disposable. The persistent state is code and logs in the workspace.
>
> The harness enforces this through a completion gate: the model cannot declare `done=true` until it has (1) written `plan.md` with critical points, (2) authored `self_reflect_config.json`, (3) executed `final_script.py` in a `final_runs/run_<id>/` folder, and (4) passed a two-stage visual self-reflection that scores screenshots against the critical points.
>
> This design is intentionally minimal — 3 modules, ~1K lines — because the authors believe strong models need less harness, not more. The results support this: GPT-5.4 with this simple loop beats complex vision-based agents by 15+ points on long-horizon tasks."

---

## What I Can Do With It Now

1. **Hermes skill:** Symlink `skills/webwright/` into `~/.hermes/skills/` — zero code changes.
2. **Read the core loop:** `agents/default.py` is 434 lines, well-structured. Good reference for building my own minimal agent harness.
3. **Adapt the prompt pattern:** The `base.yaml` system template is a masterclass in constraining model behavior through explicit rules, gates, and workflow enforcement. I can reuse this pattern in my own agent designs.
4. **Task2UI mode:** New feature (May 11) renders task results as HTML web apps — directly relevant to my HTML dashboard workflow.

---

## Open Questions / Gaps

- Can the OpenAI-dependent `image_qa`/`self_reflection` tools be replaced with Gemini vision? This would remove the hard OpenAI dependency.
- How does the local_browser mode handle sites with aggressive bot detection without residential proxies?
- What is the cost per task on GPT-5.4 with 100-step budget? (Not disclosed in repo.)

---

## Related to My Stack

- **FastAPI:** Webwright uses Pydantic v2 for config, same as my stack.
- **Playwright:** I already know this from browser automation tasks.
- **GCP/Vertex AI:** No direct integration yet, but the model backend is pluggable — could write a `gemini_model.py` backend.
- **Hermes Agent:** Direct skill compatibility via symlink.

---

## Files Referenced

- `src/webwright/agents/default.py` — Core loop (434 LoC)
- `src/webwright/environments/local_workspace.py` — Bash + workspace (296 LoC)
- `src/webwright/environments/local_browser.py` — Playwright/CDP helpers (567 LoC)
- `src/webwright/models/base.py` — Message formatting, observation templates (543 LoC)
- `src/webwright/config/base.yaml` — System + instance prompts (~24K chars)
- `skills/webwright/SKILL.md` — Hermes/Claude Code adaptation guide

---

*Artifact type: Research inspection + architecture analysis + interview conversion*
*Next step: Try wiring Hermes skill, or write a Gemini backend adapter to remove OpenAI dependency.*
