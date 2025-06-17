import json
import os

from langchain_core.documents import Document
from tqdm import tqdm

from project_analyzer.graph.graph import richie_graph
from project_analyzer.graph.state import AnalyzerState
from project_analyzer.source_file import Repository

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

REPO_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "user_repo_data.json")
with open(REPO_DATA_PATH, "r") as f:
    repo_data = json.load(f)


def summarize_repository(repo: Repository) -> AnalyzerState:
    state: AnalyzerState = {
        "context_max_token": 1000000,
        "n_files": len(repo.important_files),
        "repo_name": repo.name,
        "filenames": repo.important_files,
        "file_contents": [file.page_content for file in repo.v],
        "analyzed_files": -1,
        "collapsed_files": 0,
        "file_analysis": [],
        "collapsed_analysis": [],
        "project_analysis": None,
    }
    return richie_graph.invoke(
        state, {"recursion_limit": len(repo.important_files) * 4}
    )


def save_summary(summary: dict) -> None:
    summary_path = os.path.join(PROJECT_ROOT, "data", "user_repo_summaries_new.json")
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


# repo_state = summarize_repository(Repository(**repo_data[0]))


with tqdm(repo_data[19:], desc="Summarizing repositories") as pbar:
    # with tqdm(repo_data[15:], desc="Summarizing repositories") as pbar:
    for _rp in pbar:
        repo = Repository(**_rp)
        if len(repo.important_files) == 0:
            pbar.write(f"Skipping repository {repo.name} as it has no important files.")
            continue
        repo_state = summarize_repository(repo)
        summary = {
            "repo_name": repo.name,
            "file_analysis": {
                f: s
                for f, s in zip(repo_state["filenames"], repo_state["file_analysis"])
            },
            "project_analysis": repo_state["project_analysis"],
        }
        save_summary(summary)
