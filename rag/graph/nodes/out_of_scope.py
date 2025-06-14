import random
import time
from typing import Dict

from langchain_core.messages import AIMessage

from rag.graph.state import RichieGraphState


def out_of_scope_chatbot_node(state: RichieGraphState) -> Dict[str, str]:
    print("~" * 5, " out_of_scope_chatbot_node ", "~" * 5)
    messages = [
        "I'm sorry, but I cannot assist with that.",
        "Unfortunately, that question is beyond my capabilities.",
        "That topic is outside the scope of my knowledge.",
        "I'm not equipped to handle that request.",
        "I regret to inform you that I cannot provide an answer to that.",
        "That question is not within my area of expertise.",
        "I'm unable to assist with that topic.",
    ]

    return {"answer": [AIMessage(content=random.choice(messages))]}
