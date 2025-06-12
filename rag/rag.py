import json
import os

from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, StateGraph
from prompts import rag_prompt
from typing_extensions import List, TypedDict
from utils import Database

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
api_path = os.path.join(PROJECT_ROOT, "auth", "api.json")
with open(api_path, "r") as f:
    apis = json.load(f)
os.environ["GOOGLE_API_KEY"] = apis.get("GCP2")

richi_db = Database(
    pinecone_api=apis.get("PINECONE"),
    vec_db_host=apis.get("PINECONE_INDEX"),
    mongo_collection="project-summaries",
    mongo_host=apis.get("MONGODB").get("HOST"),
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.6,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


# Define state for application
class State(TypedDict):
    question: str
    context: str
    answer: str


# Define application steps
def retrieve(state: State):
    results = richi_db.search(query=state["question"])
    return {"context": results}


def generate(state: State):
    messages = rag_prompt.invoke(
        {"question": state["question"], "context": state["context"]}
    )
    response = llm.invoke(messages)
    return {"answer": response.content}


# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()
