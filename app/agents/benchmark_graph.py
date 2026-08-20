from langgraph.graph import StateGraph, START, END

from app.agents.benchmark_state import BenchmarkState

from app.agents.benchmark_nodes import (
    select_benchmark_node,
    generate_benchmark_node,
    evaluate_candidate_node,
    candidate_score_node,
    route_benchmark,
)


graph_builder = StateGraph(BenchmarkState)


graph_builder.add_node(
    "select_benchmark",
    select_benchmark_node,
)

graph_builder.add_node(
    "generate_benchmark",
    generate_benchmark_node,
)

graph_builder.add_node(
    "evaluate",
    evaluate_candidate_node,
)

graph_builder.add_node(
    "calculate_score",
    candidate_score_node,
)


graph_builder.add_edge(
    START,
    "select_benchmark",
)


graph_builder.add_conditional_edges(
    "select_benchmark",
    route_benchmark,
    {
        "generate": "generate_benchmark",
        "evaluate": "evaluate",
    },
)


graph_builder.add_edge(
    "generate_benchmark",
    "evaluate",
)

graph_builder.add_edge(
    "evaluate",
    "calculate_score",
)

graph_builder.add_edge(
    "calculate_score",
    END,
)


benchmark_graph = graph_builder.compile()