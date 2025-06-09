import json
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import get_file_analyzer_prompt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)


os.environ["LANGSMITH_TRACING"] = "true"
auth_path = os.path.expanduser("auth/langsmith_auth.json")
with open(auth_path, "r") as f:
    auth_data = json.load(f)
os.environ["LANGSMITH_API_KEY"] = auth_data.get("LANGSMITH_API_KEY", "")

REPO_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "user_repo_data.json")

with open(REPO_DATA_PATH, "r") as f:
    repo_data = json.load(f)


from source_file import Repository

# repos = [Repository(**repo) for repo in repo_data]
first_repo = Repository(**repo_data[0])


gemini_auth_path = os.path.expanduser("auth/gemini.json")
with open(gemini_auth_path, "r") as f:
    gemini_auth_data = json.load(f)
os.environ["GOOGLE_API_KEY"] = gemini_auth_data.get("api-key")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)


prompt = get_file_analyzer_prompt()


chain = prompt | llm
i = 0

# f_name = first_repo.important_files[i].split("/")[-1]

# with open(f_name, "w") as f:
#     f.write(first_repo.lang_documents[i].page_content)

res = chain.invoke(
    {
        "filename": first_repo.important_files[i],
        "repo_name": first_repo.name,
        "file_content": first_repo.lang_documents[i].page_content,
    }
)
print(res.content)
