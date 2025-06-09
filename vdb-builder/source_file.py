import json
import os

import requests
from langchain_core.documents import Document

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
with open(os.path.join(PROJECT_ROOT, "auth", "github-auth.json"), "r") as auth_file:
    auth_data = json.load(auth_file)
    GITHUB_USERNAME = auth_data["username"]
    GITHUB_TOKEN = auth_data["access_token"]


class Repository:

    def __init__(
        self,
        name: str,
        author: str,
        is_fork: bool,
        files: list,
        unique_file_extensions: set,
        modules: set,
        commits_by_user: list,
        important_files: list,
    ):
        self.name = name
        self.author = author
        self.is_fork = is_fork
        self.files = files
        self.unique_file_extensions = unique_file_extensions
        self.modules = modules
        self.commits_by_user = commits_by_user
        self.important_files = important_files
        self.v = self.generate_langchain_documents(important_files, name)

    def __repr__(self):
        return f"Repository(name={self.name}, author={self.author}, is_fork={self.is_fork})"

    @staticmethod
    def generate_langchain_documents(important_files: list, repo_name: str):
        print(
            "Generating LangChain documents for important files in repository:",
            repo_name,
        )
        print(f"Found {len(important_files)} important files.")
        return [File(name=file, repo_name=repo_name) for file in important_files]


class File(Document):
    def __init__(self, name: str, repo_name: str):
        content = self.get_file_content(repo_name, name)
        if name.endswith(".ipynb"):
            content = self._extract_code_cells(content)
        super().__init__(
            page_content=content, metadata={"name": name, "repo_name": repo_name}
        )

    @staticmethod
    def get_file_content(repo, path):
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.raw+json",
        }
        url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo}/contents/{path}"
        return requests.get(url, headers=headers).text

    def _extract_code_cells(self, notebook_content):
        try:
            notebook = json.loads(notebook_content)
            code_cells = []
            for cell in notebook.get("cells", []):
                if cell.get("cell_type") == "code":
                    code_cells.append("".join(cell.get("source", [])))
                elif cell.get("cell_type") == "markdown":
                    commented_lines = [
                        "# " + line if not line.startswith("#") else line
                        for line in cell.get("source", [])
                    ]
                    code_cells.append("".join(commented_lines))
            return "\n\n".join(code_cells)
        except json.JSONDecodeError:
            print("Error decoding JSON from notebook content for file:", self.name)
            return ""

    def __repr__(self):
        return f"File(name={self.metadata["name"]})"


if __name__ == "__main__":
    RAW_URL = "OwnVisEncDec.ipynb"
    RAW_URL = "benchmark-amp.py"

    file = File(RAW_URL, "amp")
