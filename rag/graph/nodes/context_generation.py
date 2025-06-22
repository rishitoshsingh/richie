import os
from typing import Dict

from dotenv import load_dotenv

load_dotenv()

from rag.graph.chains.context_generation import rag_chain
from rag.graph.state import RichieGraphState
from rag.graph.utils import Database

<<<<<<< HEAD
# print(os.getenv("PINECONE_API"))
# print(os.getenv("PINECONE_INDEX_DEV"))
# print(os.getenv("MONGODB_HOST"))
=======
print(os.getenv("PINECONE_API"))
print(os.getenv("PINECONE_INDEX_DEV"))
print(os.getenv("MONGODB_HOST"))
>>>>>>> 3d2975f2f53bdd564a56526a6efad7429680d740

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
<<<<<<< HEAD
    )
    result = rag_chain.invoke(
        {
            "query": state["modified_query"],
            "context": context,
            "chat_history": state["chat_history"],
        }
=======
>>>>>>> 3d2975f2f53bdd564a56526a6efad7429680d740
    )
    return {"answer": result.content}
