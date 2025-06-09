from langgraph.graph import StateGraph, END
from typing import TypedDict
from agents.extractor_agent import extractor_agent
from agents.summarizer_agent import summarizer_agent
from agents.qa_agent import qa_agent

# === Define the state schema ===
class WorkflowState(TypedDict):
    file_path: str
    extracted_text: str
    summary: str
    query: str
    answer: str

# === Define node functions ===
def run_extractor(state: WorkflowState) -> WorkflowState:
    extracted = extractor_agent(state["file_path"])
    return {**state, "extracted_text": extracted}

def run_summarizer(state: WorkflowState) -> WorkflowState:
    summary = summarizer_agent(state["extracted_text"])
    return {**state, "summary": summary}

def run_qa(state: WorkflowState) -> WorkflowState:
    answer = qa_agent(state["summary"], state["query"])
    return {**state, "answer": answer}

# === Build the graph ===
def build_qa_graph():
    graph = StateGraph(WorkflowState)

    graph.add_node("extractor", run_extractor)
    graph.add_node("summarizer", run_summarizer)
    graph.add_node("qa", run_qa)

    graph.set_entry_point("extractor")
    graph.add_edge("extractor", "summarizer")
    graph.add_edge("summarizer", "qa")
    graph.add_edge("qa", END)

    return graph.compile()
