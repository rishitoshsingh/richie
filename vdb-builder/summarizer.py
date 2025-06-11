import json
import os
import time
from typing import Annotated, Sequence, TypedDict, Union

from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from model import get_model
from prompts import get_file_analyzer_prompt, get_repository_analyzer_prompt
from source_file import Repository
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

api_path = os.path.expanduser("auth/api.json")
with open(api_path, "r") as f:
    apis = json.load(f)
os.environ["GOOGLE_API_KEY"] = apis.get("GCP")
# os.environ["LANGSMITH_TRACING"] = "true"
# os.environ["LANGSMITH"] = auth_data.get("LANGSMITH_API_KEY", "")

REPO_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "user_repo_data.json")
with open(REPO_DATA_PATH, "r") as f:
    repo_data = json.load(f)
# first_repo = Repository(**repo_data[0])


# llm = get_model("huggingface", "mistralai/Mistral-7B-Instruct-v0.3")
llm = get_model("google")

file_analyzer_prompt = get_file_analyzer_prompt()
repo_analyzer_prompt = get_repository_analyzer_prompt()


class RepoState(TypedDict):
    n_files: int
    repo_name: str
    filenames: Sequence[str]
    file_contents: Sequence[str]
    completed_files: int
    file_analysis: Annotated[Sequence[str], add_messages]
    repo_summaary: Union[str, None]


def analyze_file(state: RepoState) -> RepoState:
    response = llm.invoke(
        file_analyzer_prompt.invoke(
            {
                "filename": state["filenames"][state["completed_files"] + 1],
                "repo_name": state["repo_name"],
                "file_content": state["file_contents"][state["completed_files"] + 1],
            }
        )
    )
    state["file_analysis"] = [
        response.content,
    ]
    state["completed_files"] += 1
    return state


def analyze_repository(state: RepoState) -> RepoState:
    # repo_analyzer_prompt.extend(state["file_analysis"])
    response = llm.invoke(
        repo_analyzer_prompt.invoke(
            {"repo_name": state["repo_name"], "docs": state["file_analysis"]}
        )
    )
    state["repo_summaary"] = response.content
    return state


def all_file_summarized(state: RepoState) -> str:
    if state["completed_files"] + 1 != state["n_files"]:
        return False
    else:
        return True


graph = StateGraph(RepoState)
graph.add_node("analyze_file", analyze_file)
graph.add_node("analyze_repository", analyze_repository)
graph.add_edge(START, "analyze_file")
graph.add_conditional_edges(
    "analyze_file",
    all_file_summarized,
    {True: "analyze_repository", False: "analyze_file"},
)
graph.add_edge("analyze_repository", END)

app = graph.compile()
# graph_image = app.get_graph().draw_mermaid_png()
# with open("graph.png", "wb") as f:
#     f.write(graph_image)


def summarize_repository(repo: Repository) -> RepoState:
    state: RepoState = {
        "n_files": len(repo.important_files),
        "repo_name": repo.name,
        "filenames": repo.important_files,
        "file_contents": [file.page_content for file in repo.v],
        "completed_files": -1,
        "file_analysis": [],
        "repo_summaary": None,
    }
    return app.invoke(state, {"recursion_limit": len(repo.important_files) + 10})


def save_summary(summary: dict) -> None:
    summary_path = os.path.join(PROJECT_ROOT, "data", "user_repo_summaries.json")
    if os.path.exists(summary_path):
        with open(summary_path, "r") as f:
            summaries = json.load(f)
    else:
        summaries = []
    if any(s.get("repo_name") == summary.get("repo_name") for s in summaries):
        # Update the existing summary for this repo_name
        for i, s in enumerate(summaries):
            if s.get("repo_name") == summary.get("repo_name"):
                summaries[i].update(summary)
    else:
        summaries.append(summary)
    with open(summary_path, "w") as f:
        json.dump(summaries, f, indent=4)


with tqdm(repo_data[2:3], desc="Summarizing repositories") as pbar:
    for _rp in pbar:
        repo = Repository(**_rp)
        if len(repo.important_files) == 0:
            pbar.write(f"Skipping repository {repo.name} as it has no important files.")
            continue
        repo_state = summarize_repository(repo)
        summary = {
            "repo_name": repo.name,
            "file_analysis": {
                f: s.text()
                for f, s in zip(repo_state["filenames"], repo_state["file_analysis"])
            },
            "repo_summary": repo_state["repo_summaary"],
        }
        save_summary(summary)
        pbar.write("Sleeping for 60 seconds...")
        time.sleep(60)
