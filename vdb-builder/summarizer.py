import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

import json

os.environ["LANGSMITH_TRACING"] = "true"
auth_path = os.path.expanduser("auth/langsmith_auth.json")
with open(auth_path, "r") as f:
    auth_data = json.load(f)
os.environ["LANGSMITH_API_KEY"] = auth_data.get("LANGSMITH_API_KEY", "")

REPO_DATA_PATH = os.path.join(PROJECT_ROOT, "analyzer", "user_repo_data.json")
