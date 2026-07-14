from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.agents.context_agent import analyze_context
from app.agents.prioritizer_agent import prioritize
from app.agents.writer_agent import write_summary


class ReportState(TypedDict):
    activity: dict
    tone: str
    context_summary: str
    prioritized: str
    final_summary: str


def context_node(state: ReportState) -> ReportState:
    state["context_summary"] = analyze_context(state["activity"])
    return state


def prioritizer_node(state: ReportState) -> ReportState:
    state["prioritized"] = prioritize(state["context_summary"])
    return state


def writer_node(state: ReportState) -> ReportState:
    state["final_summary"] = write_summary(state["prioritized"], state["tone"])
    return state


def build_graph():
    graph = StateGraph(ReportState)
    graph.add_node("context", context_node)
    graph.add_node("prioritizer", prioritizer_node)
    graph.add_node("writer", writer_node)

    graph.set_entry_point("context")
    graph.add_edge("context", "prioritizer")
    graph.add_edge("prioritizer", "writer")
    graph.add_edge("writer", END)

    return graph.compile()


# Usage:
# app_graph = build_graph()
# result = app_graph.invoke({"activity": activity_dict, "tone": "professional"})
# print(result["final_summary"])