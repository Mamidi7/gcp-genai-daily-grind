# gemini-webwright

Minimal terminal-native web agent. Gemini writes Playwright scripts. Playwright executes them. Gemini reflects on screenshots to decide if the task is done.

No OpenAI. No LangChain. One Python file.

## Architecture

```
User Task
    |
    v
+-----------+     +-----------+     +-----------+
|  Gemini   | --> | Playwright| --> | Screenshot|
|  (script) |     | (execute) |     | (disk)    |
+-----------+     +-----------+     +-----------+
    ^                                      |
    |                                      v
+-----------+     +---------------------------+
|  Gemini   | <-- | Reflection: task done?    |
|  (vision) |     | Data correct?             |
+-----------+     +---------------------------+
```

## Workspace = Source of Truth

Every run creates a timestamped folder under `runs/`:

- `step_0.py` — the Playwright script Gemini wrote
- `screenshot_step_0.png` — full-page screenshot after execution
- `result.json` — final extracted data (only if reflection passes)

If the agent crashes, the workspace still has the script and screenshot. Resume or debug from there.

## One-File Design

| Module | Responsibility | Lines |
|--------|---------------|-------|
| `llm_generate_script` | Prompt Gemini to write Playwright Python | ~25 |
| `run_script` | Execute in subprocess, capture stdout + screenshot | ~40 |
| `llm_reflect` | Send screenshot to Gemini vision, gate `done` | ~35 |
| `run_task` | Flat loop: generate -> execute -> reflect -> retry | ~30 |

Total: ~220 lines of harness. The intelligence is in the prompts, not the framework.

## Run

```bash
cd agent_workspace
python3 gemini_webwright.py
```

Requires:
- `GEMINI_API_KEY` in `.env`
- `playwright` installed (`pip install playwright && playwright install chromium`)
- `google-genai` installed (`pip install google-genai`)

## Prompt Engineering

Two prompts do all the work:

1. **System Generate** — constrains Gemini to output ONLY a fenced Python block using `playwright.sync_api`. Rules: headless=True, screenshot via env var, print JSON to stdout as last line.
2. **System Reflect** — sends original task + executed script + screenshot. Returns strict JSON: `{task_complete: bool, extracted_data: object, reasoning: str}`.

No JSON-mode API. No function calling. Just text-in, text-out, parsed with regex.

## Why This Approach

- **Terminal-native**: LLMs understand code better than click coordinates.
- **Disposable browser**: Browser is a throwaway executor. Workspace is permanent state.
- **Self-reflection gate**: `done=true` is blocked until a second vision pass confirms the screenshot.
- **Gemini-only**: Zero OpenAI dependencies. Uses `gemini-2.5-flash` for both text and vision.

## Demo Output

Task: "Go to http://quotes.toscrape.com/, extract the text and author of the first quote."

Result (`result.json`):
```json
{
  "quote_text": "The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.",
  "quote_author": "Albert Einstein"
}
```

First-try success. No retries needed.

## Interview Answers

### 30-Second Pitch
> Most web agents predict clicks inside a locked browser session. Errors cascade. I built a terminal-native agent where Gemini writes Playwright scripts instead. The browser is disposable; the workspace on disk is the real state. A second vision pass gates completion. Result: recoverable, auditable, and OpenAI-free.

### 90-Second STAR
> **Situation**: I needed a web agent for automated data extraction, but existing frameworks were either OpenAI-locked or bloated.
> **Task**: Build a minimal harness that uses Gemini's free tier, writes executable scripts, and verifies results visually.
> **Action**: I read Microsoft Research's Webwright paper, extracted the "workspace as source of truth" pattern, and rebuilt it for Gemini. I wrote a 220-line Python loop: generate Playwright script -> execute in subprocess -> screenshot -> vision-based self-reflection -> gate done. The prompt constrains output to fenced Python blocks; reflection returns strict JSON.
> **Result**: First task (quote extraction) succeeded in one step. Every action is a file on disk. The agent is recoverable if it crashes. No OpenAI dependency.

### 3-Minute Walkthrough
> The harness has four phases. One: the user gives a natural language task. Two: the system prompt tells Gemini it's a web automation engineer. The model returns only a fenced Python script using Playwright sync API. Three: the harness writes that script to disk and runs it in a subprocess with a 60-second timeout. The script prints a JSON line to stdout and saves a screenshot to a path provided via environment variable. Four: the harness reads the screenshot and sends it back to Gemini with a second prompt — the reflection prompt. This prompt asks: is the task complete? Is the extracted data correct? It returns strict JSON with `task_complete`, `extracted_data`, and `reasoning`. If `task_complete` is true, the harness writes `result.json` and exits. If false, the loop retries with history. The workspace folder contains every script, screenshot, and result. This makes debugging trivial — you can inspect the exact script that failed and the screenshot that proved it.

## License

MIT. Steal the architecture.
