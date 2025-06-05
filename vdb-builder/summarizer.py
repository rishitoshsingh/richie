import os
import json

os.environ["LANGSMITH_TRACING"] = "true"
auth_path = os.path.expanduser("auth/langsmith_auth.json")
with open(auth_path, "r") as f:
    auth_data = json.load(f)
os.environ["LANGSMITH_API_KEY"] = auth_data.get("LANGSMITH_API_KEY", "")

from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
])

print(prompt_template.invoke({"topic": "cats"}))
