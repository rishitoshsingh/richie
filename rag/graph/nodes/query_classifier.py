from typing import Dict

from rag.graph.chains.router import QueryClassifier, query_router
from rag.graph.consts import (
    GENERAL_CHATBOT,
    OUT_OF_SCOPE_CHATBOT,
    PROJECT_RETREIVE_NAMESPACE,
    PROMPT_ENGINEERING,
    RESUME_RETREIVE_NAMESPACE,
)
from rag.graph.state import RichieGraphState


def query_classifier_node(state: RichieGraphState) -> Dict[str, str]:
    print("~" * 5, " routing query ", "~" * 5)
    query = state["query"]
    result: QueryClassifier = query_router.invoke({"query": query})
    if result.q_type == "general":
        print("~" * 5, " route query to general_node", "~" * 5)
        return {"router_next_state": GENERAL_CHATBOT}
    elif result.q_type == "resume":
        print("~" * 5, " route query to RAG", "~" * 5)
        return {
            "router_next_state": PROMPT_ENGINEERING,
            "retrieve_namespace": RESUME_RETREIVE_NAMESPACE,
        }
    elif result.q_type == "project":
        print("~" * 5, " route query to RAG", "~" * 5)
        return {
            "router_next_state": PROMPT_ENGINEERING,
            "retrieve_namespace": PROJECT_RETREIVE_NAMESPACE,
        }
    elif result.q_type == "out_of_scope":
        print("~" * 5, " route query to out_of_scope", "~" * 5)
        return {"router_next_state": OUT_OF_SCOPE_CHATBOT}
