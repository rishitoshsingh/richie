import json
import os

from pinecone import Pinecone

api_path = os.path.expanduser("auth/api.json")
with open(api_path, "r") as f:
    apis = json.load(f)

pc = Pinecone(api_key=apis.get("PINECONE"))
index = pc.Index(host="https://richie-brain-384-roilyxl.svc.aped-4627-b74a.pinecone.io")

index.delete(delete_all=True, namespace="project-summaries")
