from typing import Dict

from rag.graph.chains.general_generation import chatbot
from rag.graph.state import RichieGraphState


def general_chatbot_node(state: RichieGraphState) -> Dict[str, str]:
    print("~" * 5, " general_chatbot_node ", "~" * 5)
    result = chatbot.invoke(
        {"query": state["query"], "chat_history": state["chat_history"]}
    )

    # Return the generated response
    return {"answer": result.content}
