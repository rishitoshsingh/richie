from typing import Dict

from rag.graph.chains.prompt_engineering import SearchQuery, search_query_formatter
from rag.graph.state import RichieGraphState


def prompt_engineering_node(state: RichieGraphState) -> Dict[str, str]:
    print("~" * 5, " prompt_engineering_node ", "~" * 5)
    result: SearchQuery = search_query_formatter.invoke(
        {"query": state["query"], "chat_history": state["chat_history"]}
    )
    print("~" * 5, " modified query: ", result.modified_query)
    return {"modified_query": result.modified_query}
