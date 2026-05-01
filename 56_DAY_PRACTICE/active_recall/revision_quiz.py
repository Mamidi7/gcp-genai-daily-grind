#!/usr/bin/env python3
"""
Active Recall Quiz for GCP GenAI Days 1-14
Simplified SM-2 spaced repetition + interleaving.

Usage:
    cd ~/projects/gcp-genai-daily-grind/56_DAY_PRACTICE/active_recall
    python revision_quiz.py

How it works:
    - Loads questions from RETRIEVAL_DECK.json
    - Tracks your progress in user_progress.json
    - Asks only questions that are "due" today
    - Interleaves topics automatically (random shuffle)
    - Self-rate: 1=Again  2=Hard  3=Good  4=Easy
    - Schedules next review using SM-2 intervals

Study advice:
    - Run this for 20-25 minutes daily.
    - Do NOT look at answers until you try from memory.
    - If you forgot, type "1" and re-ask at end of session.
    - Interleaving means you will jump between Days 1-14 — this is intentional.
"""
import json
import os
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

DECK_PATH = Path(__file__).with_name("RETRIEVAL_DECK.json")
PROGRESS_PATH = Path(__file__).with_name("user_progress.json")


def load_deck():
    with open(DECK_PATH) as f:
        return json.load(f)


def load_progress():
    if not PROGRESS_PATH.exists():
        return {}
    with open(PROGRESS_PATH) as f:
        return json.load(f)


def save_progress(progress):
    with open(PROGRESS_PATH, "w") as f:
        json.dump(progress, f, indent=2)


def sm2_interval(rating, item):
    """Simplified SM-2 algorithm."""
    ef = item.get("ef", 2.5)
    reps = item.get("repetitions", 0)
    interval = item.get("interval", 0)

    if rating == 1:  # Again
        interval = 1
        reps = 0
        ef = max(1.3, ef - 0.8)
    elif rating == 2:  # Hard
        interval = max(1, int(interval * 1.2)) if reps > 0 else 1
        reps += 1
        ef = max(1.3, ef - 0.15)
    elif rating == 3:  # Good
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 3
        else:
            interval = int(interval * ef)
        reps += 1
    elif rating == 4:  # Easy
        if reps == 0:
            interval = 3
        elif reps == 1:
            interval = 7
        else:
            interval = int(interval * ef * 1.3)
        reps += 1
        ef = ef + 0.15

    item["interval"] = interval
    item["repetitions"] = reps
    item["ef"] = round(ef, 2)
    item["last_reviewed"] = datetime.now().isoformat()
    item["next_review"] = (datetime.now() + timedelta(days=interval)).isoformat()
    return item


def get_due_questions(deck, progress):
    now = datetime.now()
    due = []
    for q in deck:
        qid = q["id"]
        if qid not in progress:
            due.append(q)
        else:
            next_review = datetime.fromisoformat(progress[qid]["next_review"])
            if next_review <= now:
                due.append(q)
    return due


def ask_question(q):
    print(f"\n{'='*65}")
    print(f"[{q['day']:02d}] {q['topic']:<18} | Level {q['level']} | {q['type']:<10}")
    print(f"{'='*65}")
    print(f"\nQUESTION:\n{q['question']}\n")
    input("Press Enter when ready to see answer...")
    print(f"\n{'-'*65}")
    print(f"ANSWER:\n{q['answer']}\n")
    print("Rate yourself:")
    print("  1 = Again (completely forgot)")
    print("  2 = Hard (recalled partially or slowly)")
    print("  3 = Good (correct with normal effort)")
    print("  4 = Easy (instant recall)")
    while True:
        try:
            rating = int(input("Rating (1-4): ").strip())
            if rating in (1, 2, 3, 4):
                return rating
        except ValueError:
            pass
        print("Enter 1, 2, 3, or 4.")


def main():
    if not DECK_PATH.exists():
        print(f"Deck not found: {DECK_PATH}")
        sys.exit(1)

    deck = load_deck()
    progress = load_progress()

    # Initialize progress for all questions
    for q in deck:
        if q["id"] not in progress:
            progress[q["id"]] = {
                "interval": 0,
                "repetitions": 0,
                "ef": 2.5,
                "last_reviewed": None,
                "next_review": datetime.min.isoformat(),
            }

    due = get_due_questions(deck, progress)

    if not due:
        print("\nNo questions due today. Great work!")
        future = sorted(
            [(qid, datetime.fromisoformat(p["next_review"])) for qid, p in progress.items()],
            key=lambda x: x[1],
        )[:5]
        print("\nNext upcoming reviews:")
        for qid, dt in future:
            q = next(x for x in deck if x["id"] == qid)
            print(f"  {dt.strftime('%Y-%m-%d')}: [{q['day']:02d}] {q['topic']}")
        return

    print(f"\nQuestions due today: {len(due)}")
    print("Tip: Cover the answer. Force yourself to recall BEFORE pressing Enter.\n")

    # INTERLEAVING: shuffle so days/topics are mixed
    random.shuffle(due)

    again_queue = []
    for q in due:
        rating = ask_question(q)
        progress[q["id"]] = sm2_interval(rating, progress[q["id"]])
        save_progress(progress)
        if rating == 1:
            again_queue.append(q)

    # Re-ask "Again" questions at end for error-driven feedback
    for q in again_queue:
        print(f"\n[RE-ASK] You marked this 'Again' earlier. Try once more.")
        rating = ask_question(q)
        progress[q["id"]] = sm2_interval(rating, progress[q["id"]])
        save_progress(progress)

    print(f"\nSession complete. Progress saved to {PROGRESS_PATH}")
    print(f"Next run: same command tomorrow (or whenever you want).")


if __name__ == "__main__":
    main()
