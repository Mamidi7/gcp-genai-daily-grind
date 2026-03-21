 #Write these 3 functions (not found yet in repo):

  # - clean_question(text)
  # - make_payload(question, user_id)
  # - format_answer(answer, sources)


# -------------------------------------------------------------------

def clean_question(text:str)->str:
    text=text.strip()
    if not text:
        raise ValueError("question cannot be empty")
    return text

# -------------------------------------------------------------------
  
def make_payload(question: str, user_id: str) -> dict:
    question = clean_question(question)
    return {"user_id": user_id, "question": question}


# -------------------------------------------------------------------


def format_answer(answer: str, sources: list[str]) -> dict:
    return {"answer": answer.strip(), "sources": sources}

def build_request_log(question: str, status: str) -> dict:
    question = clean_question(question)
    return {
        "question": question,
        "status": status,
        "question_length": len(question),
      }


from day10_applied_ai import clean_question, build_request_log
print(clean_question("  hello  "))
print(build_request_log("  hi  ", "ok"))
for bad in ["", "   "]:
    try:
        clean_question(bad)
    except Exception as e:
        print(type(e).__name__, str(e))