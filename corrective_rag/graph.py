from langgraph.graph import StateGraph

from corrective_rag.state import (
    GraphState
)

from corrective_rag.nodes import (
    process_query,
    retrieve_documents,
    evaluate_retrieval,
    rewrite_bad_query,
    search_web,
    generate,
    validate_answer
)


# -----------------------------------
# CONDITIONAL ROUTING
# -----------------------------------

def route_after_grading(state):

    if state["use_web_search"]:

        return "rewrite_query"

    return "generate"


# -----------------------------------
# BUILD GRAPH
# -----------------------------------

graph_builder = StateGraph(
    GraphState
)


graph_builder.add_node(
    "process_query",
    process_query
)

graph_builder.add_node(
    "retrieve_documents",
    retrieve_documents
)

graph_builder.add_node(
    "evaluate_retrieval",
    evaluate_retrieval
)

graph_builder.add_node(
    "rewrite_query",
    rewrite_bad_query
)

graph_builder.add_node(
    "web_search",
    search_web
)

graph_builder.add_node(
    "generate",
    generate
)

graph_builder.add_node(
    "validate_answer",
    validate_answer
)


# -----------------------------------
# EDGES
# -----------------------------------

graph_builder.set_entry_point(
    "process_query"
)

graph_builder.add_edge(
    "process_query",
    "retrieve_documents"
)

graph_builder.add_edge(
    "retrieve_documents",
    "evaluate_retrieval"
)

graph_builder.add_conditional_edges(
    "evaluate_retrieval",
    route_after_grading,
    {
        "rewrite_query": "rewrite_query",
        "generate": "generate"
    }
)

graph_builder.add_edge(
    "rewrite_query",
    "web_search"
)

graph_builder.add_edge(
    "web_search",
    "generate"
)

graph_builder.add_edge(
    "generate",
    "validate_answer"
)

graph_builder.set_finish_point(
    "validate_answer"
)


graph = graph_builder.compile()