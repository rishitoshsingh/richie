import os
from typing import Dict

from dotenv import load_dotenv

load_dotenv()

from rag.graph.chains.context_generation import rag_chain
from rag.graph.state import RichieGraphState
from rag.graph.utils import Database

print(os.getenv("PINECONE_API"))
print(os.getenv("PINECONE_INDEX_DEV"))
print(os.getenv("MONGODB_HOST"))

richi_db = Database(
    pinecone_api=os.getenv("PINECONE_API"),
    vec_db_host=os.getenv("PINECONE_INDEX_DEV"),
    mongo_collection="project-analysis",
    mongo_database="richie-dev",
    mongo_host=os.getenv("MONGODB_HOST"),
)


def context_chatbot_node(state: RichieGraphState) -> Dict[str, str]:
    print("~" * 5, " context_chatbot_node ", "~" * 5)
    query = state["modified_query"]
    context = richi_db.search(
        query=query, namespace=state["retrieve_namespace"], top_k=15
    )
    result = rag_chain.invoke(
        {
            "query": state["modified_query"],
            "context": context,
            "chat_history": state["messages"],
        }
    )
    return {"answer": result.content}
