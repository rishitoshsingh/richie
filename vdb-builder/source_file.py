import json
from langchain_core.documents import Document
from prompts import get_file_analyzer_prompt

class Repository:

    def __init__(self, name: str, author: str, is_fork: bool, files: list, unique_file_extensions: set, modules: set, commits_by_user: list, important_files:list):
        self.name = name
        self.author = author
        self.is_fork = is_fork
        self.files = files
        self.unique_file_extensions = unique_file_extensions
        self.modules = modules
        self.commits_by_user = commits_by_user
        self.important_files = important_files
    
    def get_prompt(self):
        prompt = "You are an expert in analyzing repositories. "
        prompt += "I will give you a repository name, author, whether it is a fork, list of files, unique file extensions, modules used, commits by user and important files. "
        prompt += "You will analyze this repository and provide insights about it.\n\n"
        prompt += "You should strictly follow the following format to answer these questions, just replace <str> with your response. Don't use any other new_line character:\n"
        prompt += "repository_name:\n<str>\nauthor:\n<str>\nis_fork:\n<str>\nfiles:\n<list>\nunique_file_extensions:\n<set>\nmodules:\n<set>\ncommits_by_user:\n<list>\nimportant_files:\n<list>\n\n"
        return prompt

class File(Document):
    def __init__(self, name: str, repo_name:str, content: str):
        if name.endswith('.ipynb'):
            content = self._extract_code_cells(content)
        super().__init__(page_content=content, metadata={"name": name, "repo_name": repo_name})

    def _extract_code_cells(self, notebook_content):
        try:
            notebook = json.loads(notebook_content)
            code_cells = []
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'code':
                    code_cells.append(''.join(cell.get('source', [])))
                elif cell.get('cell_type') == 'markdown':
                    commented_lines = ['# ' + line if not line.startswith('#') else line for line in cell.get('source', [])]
                    code_cells.append(''.join(commented_lines))
            return "\n\n".join(code_cells)
        except json.JSONDecodeError:
            print("Error decoding JSON from notebook content for file:", self.name)
            return ""

    def __repr__(self):
        return f"File(name={self.metadata["name"]})"

if __name__ == "__main__":
    RAW_URL = "https://github.com/rishitoshsingh/i2c/raw/7f5a5bf5385e2e691748e48f0b723e11be394784/OwnVisEncDec.ipynb"
    import requests
    with open('auth/github-auth.json') as auth_file:
        auth_data = json.load(auth_file)
        GITHUB_USERNAME = auth_data['username']
        GITHUB_TOKEN = auth_data['access_token']

    def get_files(repo_name):
        url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents'
        response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
        response.raise_for_status()
        return response.json()
    

    file = File(RAW_URL, requests.get(RAW_URL).text)
    print(file.get_prompt())