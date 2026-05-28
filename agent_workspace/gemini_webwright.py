#!/usr/bin/env python3
"""
gemini_webwright.py
Minimal terminal-native web agent using Gemini + Playwright.
No OpenAI. No LangChain. One file. Workspace is the source of truth.
"""

import os
import sys
import json
import uuid
import traceback
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ── bootstrap ───────────────────────────────────────────────────────────
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

WORKSPACE_ROOT = Path(__file__).parent / "runs"
WORKSPACE_ROOT.mkdir(exist_ok=True)

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_TEXT = "gemini-2.5-flash"
MODEL_VISION = "gemini-2.5-flash"

# ── prompts ─────────────────────────────────────────────────────────────
SYSTEM_GENERATE = """You are a web automation engineer.
Your job is to write a self-contained Python script using Playwright (sync_api) to complete a user task.

RULES:
1. Output ONLY a fenced Python code block. No explanation outside the block.
2. The script must be runnable with `python3 script.py`.
3. Use `playwright.sync_api import sync_playwright`.
4. Launch browser with `headless=True`.
5. Save a screenshot to the path given by the SCREENSHOT_PATH environment variable.
6. Print a single line of JSON to stdout as the VERY LAST output. This JSON must contain any extracted data.
7. If no data was extracted, print `{}`.
8. Do NOT use `if __name__ == "__main__"` guards. Just top-level code.
9. Handle simple errors gracefully (try/except around navigation).
10. Keep scripts short and focused. One page interaction per script.

EXAMPLE OUTPUT FORMAT:
```python
from playwright.sync_api import sync_playwright
import os, json

screenshot_path = os.environ.get("SCREENSHOT_PATH", "/tmp/screenshot.png")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")
    page.wait_for_timeout(1000)
    page.screenshot(path=screenshot_path, full_page=True)
    data = {"title": page.title()}
    print(json.dumps(data))
    browser.close()
```
"""

SYSTEM_REFLECT = """You are a QA engineer reviewing a web automation attempt.
You will see:
- The original task
- The Playwright script that was executed
- A screenshot of the resulting page

Your job: decide if the task is complete and data is correctly extracted.

Return ONLY a JSON object with this exact schema:
{
  "task_complete": bool,
  "extracted_data": object or null,
  "reasoning": "short explanation"
}

Rules:
- task_complete = true ONLY if the screenshot shows the expected outcome AND extracted_data has the right fields.
- If task_complete = false, set extracted_data = null and explain what is missing in reasoning.
- Be strict. Partial extractions are failures.
"""

# ── helpers ─────────────────────────────────────────────────────────────
def new_workspace() -> Path:
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())[:4]
    ws = WORKSPACE_ROOT / run_id
    ws.mkdir(parents=True)
    return ws


def llm_generate_script(task: str, history: list, workspace: Path) -> str:
    """Ask Gemini to write the next Playwright script."""
    parts = [types.Part.from_text(text=SYSTEM_GENERATE)]

    # build conversation context
    for h in history:
        parts.append(types.Part.from_text(text=f"STEP {h['step']}:\nScript:\n{h['script']}\n\nResult: {h['result']}\nReflection: {json.dumps(h['reflection'])}"))

    parts.append(types.Part.from_text(text=f"TASK: {task}\n\nWrite the next Playwright script."))

    response = client.models.generate_content(
        model=MODEL_TEXT,
        contents=[types.Content(role="user", parts=parts)],
    )
    raw = response.text or ""

    # extract code block
    if "```python" in raw:
        raw = raw.split("```python")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    script_path = workspace / f"step_{len(history)}.py"
    script_path.write_text(raw, encoding="utf-8")
    return raw


def run_script(script_text: str, workspace: Path, step: int) -> dict:
    """Execute the generated script in a subprocess. Returns {stdout, stderr, screenshot, ok}."""
    screenshot_path = workspace / f"screenshot_step_{step}.png"
    script_path = workspace / f"step_{step}.py"

    env = os.environ.copy()
    env["SCREENSHOT_PATH"] = str(screenshot_path)

    result = {
        "stdout": "",
        "stderr": "",
        "screenshot": str(screenshot_path),
        "ok": False,
        "data": {},
    }

    try:
        proc = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=60,
            env=env,
        )
        result["stdout"] = proc.stdout
        result["stderr"] = proc.stderr
        result["returncode"] = proc.returncode

        if proc.returncode == 0:
            result["ok"] = True
            # last non-empty line should be JSON
            lines = [l.strip() for l in proc.stdout.strip().splitlines() if l.strip()]
            if lines:
                try:
                    result["data"] = json.loads(lines[-1])
                except json.JSONDecodeError:
                    result["data"] = {"raw_last_line": lines[-1]}
        else:
            result["ok"] = False

    except subprocess.TimeoutExpired:
        result["stderr"] = "Script timed out after 60s"
    except Exception as e:
        result["stderr"] = traceback.format_exc()

    return result


def llm_reflect(task: str, script: str, exec_result: dict, workspace: Path, step: int) -> dict:
    """Send screenshot + context to Gemini for reflection."""
    screenshot_path = Path(exec_result["screenshot"])
    if not screenshot_path.exists():
        return {
            "task_complete": False,
            "extracted_data": None,
            "reasoning": "Screenshot missing. Browser likely crashed.",
        }

    image_bytes = screenshot_path.read_bytes()
    image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/png")

    prompt_text = f"""Original task: {task}

Script that was executed:
```python
{script}
```

Script stdout:
{exec_result['stdout']}

Script stderr:
{exec_result['stderr']}

Return your JSON assessment now."""

    response = client.models.generate_content(
        model=MODEL_VISION,
        contents=[
            types.Part.from_text(text=SYSTEM_REFLECT),
            types.Part.from_text(text=prompt_text),
            image_part,
        ],
    )

    raw = response.text or "{}"
    # extract JSON if wrapped in fences
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "task_complete": False,
            "extracted_data": None,
            "reasoning": f"Reflection parsing failed. Raw: {raw[:200]}",
        }


# ── core loop ───────────────────────────────────────────────────────────
def run_task(task: str, max_steps: int = 3):
    workspace = new_workspace()
    print(f"Workspace: {workspace}")

    history = []
    for step in range(max_steps):
        print(f"\n=== Step {step} ===")

        # 1. generate script
        print("Generating script...")
        script = llm_generate_script(task, history, workspace)

        # 2. execute
        print("Executing script...")
        exec_result = run_script(script, workspace, step)
        print(f"  stdout: {exec_result['stdout'][:200]}")
        if exec_result["stderr"]:
            print(f"  stderr: {exec_result['stderr'][:200]}")
        print(f"  screenshot: {exec_result['screenshot']}")

        # 3. reflect
        print("Reflecting...")
        reflection = llm_reflect(task, script, exec_result, workspace, step)
        print(f"  complete: {reflection.get('task_complete')}")
        print(f"  reasoning: {reflection.get('reasoning')}")

        history.append({
            "step": step,
            "script": script,
            "result": exec_result,
            "reflection": reflection,
        })

        if reflection.get("task_complete"):
            data = reflection.get("extracted_data") or exec_result.get("data") or {}
            result_path = workspace / "result.json"
            result_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            print(f"\nDONE. Result saved to {result_path}")
            return workspace, data

        print("Task not complete. Retrying...")

    print(f"\nFAILED after {max_steps} steps.")
    return workspace, None


# ── entry ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    TASK = (
        "Go to http://quotes.toscrape.com/, "
        "extract the text and author of the first quote on the page, "
        "and save that information."
    )
    ws, data = run_task(TASK, max_steps=3)
    print("\nFinal data:", json.dumps(data, indent=2) if data else None)
    print("Workspace:", ws)
