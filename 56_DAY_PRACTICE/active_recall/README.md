# Active Recall System — Days 1-14

Research-backed revision: retrieval practice + spaced repetition + interleaving.
No re-reading. No highlighting. Only self-testing.

---

## Files

| File | Purpose |
|---|---|
| `RETRIEVAL_DECK.json` | 66 questions covering Days 1-14. Levels 1-3. |
| `revision_quiz.py` | Interactive quiz with SM-2 scheduling. Run this daily. |
| `INTERLEAVED_SESSIONS.md` | 7 pre-mixed session plans for manual study. |
| `user_progress.json` | Auto-generated. Your spaced-repetition state. |

---

## Quick Start

```bash
cd ~/projects/gcp-genai-daily-grind/56_DAY_PRACTICE/active_recall
python revision_quiz.py
```

First run: all 66 questions (full baseline). ~45 minutes.
After that: only due questions appear. ~10-20 minutes/day.

---

## Rules for Maximum Retention

1. **No peeking**: Read the question, cover the screen, answer OUT LOUD or write on paper.
2. **Be honest**: If you guessed, rate it Hard (2), not Good (3).
3. **Interleaving is the point**: Jumping from Day 3 to Day 10 to Day 1 is INTENTIONAL. Your brain must discriminate which tool fits which problem.
4. **Error-driven feedback**: "Again" questions re-appear at session end. This is where learning happens.
5. **Sleep matters**: Do NOT cram. 20 min quiz + sleep > 2 hours of re-reading.

---

## Rating Guide

| Rating | Meaning | Next Review |
|---|---|---|
| 1 Again | Forgot or wrong | 1 day (re-ask now) |
| 2 Hard | Slow or shaky | ~1-2 days |
| 3 Good | Correct with effort | ~3-7 days |
| 4 Easy | Instant recall | ~7-14+ days |

---

## Question Types

- **recall**: Definition, fact, syntax (Level 1)
- **application**: Write code, design schema (Level 2)
- **debug**: Find bug, diagnose error (Level 2)
- **comparison**: Tradeoffs, when to use X vs Y (Level 3)

---

## Interview Conversion

Every time you rate a question 4 (Easy), try this:

1. **30-second version**: Say the answer out loud as if an interviewer asked.
2. **STAR version**: "In my project, I faced X, tried Y, fixed with Z, outcome was W."
3. **Tradeoff version**: "I chose A over B because C, but D would be better if E."

This turns recall into interview muscle.

---

## Adding New Questions

Edit `RETRIEVAL_DECK.json`. Each entry needs:

```json
{
  "id": "d15_q01",
  "day": 15,
  "topic": "Embeddings",
  "level": 2,
  "type": "application",
  "question": "...",
  "answer": "..."
}
```

Delete `user_progress.json` if you want a full reset.
