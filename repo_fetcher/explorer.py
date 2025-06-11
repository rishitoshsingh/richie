import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

import json

import requests
from tqdm import tqdm

SLEEP_TIME = 2
import re

# Replace with your GitHub username and personal access token
with open(os.path.join(PROJECT_ROOT, "auth", "github-auth.json"), "r") as auth_file:
    auth_data = json.load(auth_file)
    GITHUB_USERNAME = auth_data["username"]
    GITHUB_TOKEN = auth_data["access_token"]

with open(os.path.join(SCRIPT_DIR, "extensions.json"), "r") as f:
    ext_data = json.load(f)
    required_extensions = set()
    for typ, exts in ext_data.items():
        required_extensions.update(exts)

with open(os.path.join(SCRIPT_DIR, "modules.json"), "r") as f:
    module_data = json.load(f)
    required_modules = set()
    for typ, mods in module_data.items():
        required_modules.update(mods)

with open(os.path.join(SCRIPT_DIR, "skip_files.json"), "r") as f:
    skip_files = set(json.load(f))

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def get_repositories():
    params = {"visibility": "all", "affiliation": "owner", "per_page": 100}
    response = requests.get(
        "https://api.github.com/user/repos", headers=headers, params=params
    )
    response.raise_for_status()
    return response.json()


def get_commits(repo_name):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/commits"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_commit_details(repo_name, commit_sha):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/commits/{commit_sha}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def extract_modules(file_content, file_type):
    if file_type == "py":
        import_statements = re.findall(
            r"^\s*(?:import|from)\s+([^\s]+)", file_content, re.MULTILINE
        )
        modules = set()
        for statement in import_statements:
            module = statement.split(".")[0]
            modules.add(module)
        return list(modules)
    elif file_type == "ipynb":
        import_statements = re.findall(
            r"^\s*(?:import|from)\s+([^\s]+)", file_content, re.MULTILINE
        )
        modules = set()
        for statement in import_statements:
            module = statement.split(".")[0]
            modules.add(module)
        return list(modules)
    elif file_type == "cpp":
        include_statements = re.findall(
            r"^\s*#include\s*<([^>]+)>", file_content, re.MULTILINE
        )
        return list(set(include_statements))


def is_within_hidden_folder(file_path):
    parts = file_path.split(os.sep)
    for part in parts:
        if part.startswith(".") and part != ".":
            return True
    return False


def main():
    all_repositories_data = []
    repositories = get_repositories()
    for repo in tqdm(repositories, desc="Repositories"):
        repo_name = repo["name"]
        if repo["fork"]:
            continue
        # print(f'Repository: {repo_name}')
        repo_data = {
            "name": repo["name"],
            "author": repo["owner"]["login"],
            "is_fork": repo["fork"],
            "files": [],
            "unique_file_extensions": set(),
            "important_files": set(),
            "modules": set(),
            "commits_by_user": [],
        }
        if repo["owner"]["login"] == GITHUB_USERNAME:
            commits = get_commits(repo["name"])
        else:
            continue
        # for commit in tqdm(commits, desc=f"Commits in {repo_name}", leave=False):
        for commit in commits:
            # time.sleep(SLEEP_TIME)  # Pause for 1 second to avoid rate limit
            commit_sha = commit["sha"]
            if commit["commit"]["author"]["name"] != GITHUB_USERNAME:
                continue
            commit_details = get_commit_details(repo["name"], commit_sha)
            user_commit = {
                "commithash": commit_sha,
                "commit_message": commit_details["commit"]["message"],
            }
            if "files" in commit_details:
                repo_data["commits_by_user"].append(user_commit)
                committed_files = []
                for file in commit_details["files"]:
                    if (
                        is_within_hidden_folder(file["filename"])
                        or file["filename"].split(os.path.sep)[-1] in skip_files
                    ):
                        continue
                    repo_data["files"].append(file["filename"])
                    file_extension = file["filename"].split(".")[-1]
                    if f".{file_extension}" in required_extensions:
                        repo_data["unique_file_extensions"].add(file_extension)
                        committed_files.append(
                            {
                                "filename": file["filename"],
                                "raw_url": file["raw_url"],
                                "patch": file.get("patch", " "),
                            }
                        )
                        repo_data["important_files"].update([file["filename"]])
                        # print(repo_data['important_files'])
                        if file_extension in ["py", "ipynb", "cpp"]:
                            file_content = requests.get(
                                file["raw_url"], auth=(GITHUB_USERNAME, GITHUB_TOKEN)
                            ).text
                            modules = extract_modules(file_content, file_extension)
                            modules = [
                                mod for mod in modules if mod in required_modules
                            ]
                            repo_data["modules"].update(modules)
                user_commit.update({"committed_files": committed_files})
        repo_data["unique_file_extensions"] = list(repo_data["unique_file_extensions"])
        repo_data["important_files"] = list(repo_data["important_files"])
        repo_data["modules"] = list(repo_data["modules"])
        all_repositories_data.append(repo_data)

    with open(
        os.path.join(PROJECT_ROOT, "data", "user_repo_data.json"), "w"
    ) as json_file:
        json.dump(all_repositories_data, json_file, indent=4)


if __name__ == "__main__":
    main()
