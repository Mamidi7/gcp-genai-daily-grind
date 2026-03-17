# CODE-LENS Interview Delivery Standard (AI/ML Backend)

Use this when you want to explain code in interviews without memorizing every line.

## 1) Goal in 1 line
Explain logic, tradeoffs, and debugging evidence clearly and confidently.

## 2) What to Remember (Only 6 Anchors)
1. Purpose: Why this code exists.
2. Input: What comes in.
3. Core Flow: Main steps inside.
4. Failure Handling: What can fail and how it is handled.
5. Tradeoff: Why this design choice was made.
6. Outcome Metric: What improved (latency, reliability, correctness, etc.).

If you remember these six, you do not need line-by-line memory.

## 3) Standard Explain Flow (8-12 min)
1. 30 sec: One-line purpose + where this fits in system.
2. 2 min: Input -> Process -> Output.
3. 2 min: Key design choices (example: timeout + retry + to_thread).
4. 2 min: Failure path and debugging story.
5. 1 min: Improvement/scaling idea.
6. 1-2 min: Q&A.

## 4) Simple Visual Format
```text
Input -> Validate -> Core Logic -> External Call/DB -> Output
            |              |
         fail fast     timeout/retry/error map
```

## 5) Terminology Decoder (for interviews)
- Sync: Do one thing and wait until it finishes.
- Async: When waiting, switch to other work.
- Blocking: Main request loop is stuck and cannot move to other requests.
- Retry: Try again after temporary failure.
- Backoff: Wait a little more between retries.

## 6) Debugging Artifact Rule
For each important issue, capture:
1. Symptom
2. Root cause
3. Fix
4. Prevention
5. Impact

This gives production-style interview signal.

## 7) Mandatory Output per Code Piece
1. `CodeCard`
2. `BugCard`
3. `InterviewPack` (30s, 90s, 3min)
4. `QuestionBank` (5 likely questions)

Templates are in `docs/templates/`.

## 8) Delivery Format I will use with you
1. Goal in 1 line
2. ASCII diagram
3. Concept in 3-6 simple lines
4. Minimal example
5. Common mistake + fix
6. Check question
7. Tiny exercise
8. Interview conversion (30s/90s/3min)

## 9) Mastery Gate (Pass/Fail)
Pass when all are true:
1. You explain all 6 anchors without opening code.
2. You answer 4/5 likely questions.
3. You explain one real failure path with prevention.
4. You give 30s and 3min versions smoothly.
