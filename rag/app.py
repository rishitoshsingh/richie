import json
import os

from pinecone import Pinecone
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

api_path = os.path.join(PROJECT_ROOT, "auth", "api.json")
with open(api_path, "r") as f:
    apis = json.load(f)

os.environ["GOOGLE_API_KEY"] = apis.get("GCP")
pc = Pinecone(api_key=apis.get("PINECONE"))
index = pc.Index(host="https://richie-brain-384-roilyxl.svc.aped-4627-b74a.pinecone.io")


from langchain import hub
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict

rag_prompt_template = """
You are Richie, a virtual persona of Rishitosh Singh. Respond to users as if you are Rishi himself, speaking casually and confidently in the first person.

Use the retrieved context below to answer questions truthfully, accurately, and in Rishi's tone and style.

If the context doesn’t contain enough information to answer, say something like:
- “I don't think my owner have given me this information”
- “Hmm, I guess Rishi haven't given me that information, want to contact him directly?”

Always sound like a real, intelligent human — helpful, warm, honest, and thoughtful. Be as respectful as you can be as mostly a recruiter will be talking to you. Be as detailed as possible

---

Context:
{context}

---

Now answer the following user question as Rishi:
{question}
"""
from langchain_core.prompts import PromptTemplate

rag_prompt = PromptTemplate(
    template=rag_prompt_template,
    input_variables=["question", "context"],
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
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    results = index.search(
        namespace="project-summaries",
        query={"inputs": {"text": state["question"]}, "top_k": 25},
        fields=["text"],
    )
    return {
        "context": [
            Document(page_content=doc["fields"]["text"])
            for doc in results["result"]["hits"]
        ]
    }


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = rag_prompt.invoke(
        {"question": state["question"], "context": docs_content}
    )
    response = llm.invoke(messages)
    return {"answer": response.content}


# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()


def retrieve_test(question: str):
    results = index.search(
        namespace="repo-summaries",
        query={"inputs": {"text": question}, "top_k": 25},
        fields=["text"],
    )
    print(results)


response = graph.invoke({"question": "Do you have experience with pytorch?"})
print(response["answer"])
# retrieve_test("Does the candidate have experience with pytorch?")
