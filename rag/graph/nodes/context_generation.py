import os
from typing import Dict

from rag.graph.chains.context_generation import rag_chain
from rag.graph.state import RichieGraphState
from rag.graph.utils import Database

richi_db = Database(
    pinecone_api=os.getenv("PINECONE_API"),
    vec_db_host=os.getenv("PINECONE_INDEX"),
    mongo_collection="project-summaries",
    mongo_host=os.getenv("MONGODB_HOST"),
)


def context_chatbot_node(state: RichieGraphState) -> Dict[str, str]:
    print("~" * 5, " context_chatbot_node ", "~" * 5)
    query = state["modified_query"]
    context = richi_db.search(
        query=query, namespace=state["retrieve_namespace"], top_k=100
    )
    result = rag_chain.invoke(
        {
            "query": state["modified_query"],
            "context": context,
            "chat_history": state["messages"],
        }
    )
    return {"answer": result.content}
