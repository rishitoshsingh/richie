import json
import os

import openai
from dotenv import load_dotenv
from pinecone import Pinecone
from pymongo import MongoClient
from tqdm import tqdm

load_dotenv()

pc = Pinecone(api_key=os.environ.get("PINECONE_API"))
index = pc.Index(host=os.environ.get("PINECONE_INDEX_DEV"))

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

SUMMARY_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "user_repo_summaries_new.json")
with open(SUMMARY_DATA_PATH, "r") as f:
    summary_data = json.load(f)


def embed(docs: list[str]) -> list[list[float]]:
    res = openai.embeddings.create(input=docs, model="text-embedding-3-small")
    doc_embeds = [r.embedding for r in res.data]
    return doc_embeds


def ingest_to_index(vec, namespace):
    index.upsert(vectors=vec, namespace=namespace)


for summary in tqdm(summary_data, desc="Ingesting summaries"):
    vectors = []
    doc_embeds = embed(summary["file_analysis"].values())
    for i, (file, emb) in enumerate(zip(summary["file_analysis"].keys(), doc_embeds)):
        vectors.append(
            {
                "id": f"{summary['repo_name']}#{file}#{i+1}",
                "values": emb,
                "metadata": {
                    "text": summary["file_analysis"][file],
                    "repo_name": summary["repo_name"],
                    "file_name": file,
                },
            }
        )
        if len(vectors) >= 50:
            ingest_to_index(vectors, "project-analysis")
            vectors = []
    if len(vectors) > 0:
        ingest_to_index(vectors, "project-analysis")

summary_docs = [summary["project_analysis"] for summary in summary_data]
repo_embeds = embed(summary_docs)
vectors = []
for summary, emb in zip(summary_data, repo_embeds):
    vectors.append(
        {
            "id": f"{summary['repo_name']}",
            "values": emb,
            "metadata": {
                "text": summary["project_analysis"],
                "repo_name": summary["repo_name"],
            },
        }
    )
# Load MongoDB Atlas credentials from api.json
client = MongoClient(os.environ.get("MONGODB_HOST"))
db = client["richie-dev"]
collection = db["project-analysis"]

# Example usage: insert all summaries into MongoDB
for summary in tqdm(summary_data, desc="Inserting into MongoDB"):
    records = []
    collection.insert_one(
        {
            "repo_name": summary["repo_name"],
            "repo_summary": summary["project_analysis"],
        }
    )
