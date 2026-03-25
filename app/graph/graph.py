from langgraph.graph import StateGraph, START, END

from app.graph.state import RepoState


from app.graph.nodes.inspector_node import inspector_node
from app.graph.nodes.scorer_node import scorer_node
from app.graph.nodes.collector_node import collector_node
from app.graph.nodes.deep_dive_node import deep_dive_node
from app.graph.nodes.context_builder_node import context_builder_node
from app.graph.nodes.summarize_node import summarize_node





def routing_decision(state: RepoState):
    score = state.get("score", 0)

    if score >= 80:
        return "enough_context"

    return "need_more_context"




builder = StateGraph(RepoState)

builder.add_node("inspector", inspector_node)
builder.add_node("scorer", scorer_node)
builder.add_node("collector", collector_node)
builder.add_node("deep_dive", deep_dive_node)
builder.add_node("context_builder", context_builder_node)
builder.add_node("summarize", summarize_node)


builder.add_edge(START, "inspector")


builder.add_edge("inspector", "scorer")


builder.add_conditional_edges(
    "scorer",
    routing_decision,
    {
        "enough_context": "collector",
        "need_more_context": "deep_dive",
    },
)


builder.add_edge("collector", "context_builder")
builder.add_edge("deep_dive", "context_builder")

builder.add_edge("context_builder", "summarize")
builder.add_edge("summarize", END)




repo_graph = builder.compile()