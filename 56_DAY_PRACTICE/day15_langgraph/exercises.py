"""
DAY 15: LangGraph Exercises
Practice building AI agents with LangGraph
"""

# Exercise 1: Create a simple 2-node agent
# TODO: Create analyze -> generate workflow

from langgraph.graph import StateGraph, END
from typing import TypedDict

class SimpleState(TypedDict):
    question: str
    answer: str

def read_question(state: SimpleState) -> SimpleState:
    """Node 1: Read the question"""
    print(f"Reading: {state['question']}")
    return {"answer": "Answer from node 1"}

def generate_answer(state: SimpleState) -> SimpleState:
    """Node 2: Generate answer"""
    print(f"Generating based on: {state['answer']}")
    return {"answer": "Final answer!"}

# Build workflow
workflow = StateGraph(SimpleState)
workflow.add_node("read", read_question)
workflow.add_node("generate", generate_answer)
workflow.set_entry_point("read")
workflow.add_edge("read", "generate")
workflow.add_edge("generate", END)

agent = workflow.compile()

# Test
result = agent.invoke({"question": "What is LangGraph?"})
print(result)


# Exercise 2: Add a third node (improve)
# TODO: Add "improve" node that adds "Answer: " prefix


# Exercise 3: Add a retry loop
# TODO: If answer is too short, go back to generate
