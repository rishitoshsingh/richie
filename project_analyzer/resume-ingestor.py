import os
from typing import TypedDict, Union

import openai
from dotenv import load_dotenv
from langchain_writer.text_splitter import WriterTextSplitter
from pinecone import Pinecone

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API"))
index = pc.Index(host=os.getenv("PINECONE_INDEX_DEV"))

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RESUME_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "resume.txt")
with open(RESUME_DATA_PATH, "r") as f:
    resume_text = f.read()


def embed(docs: list[str]) -> list[list[float]]:
    res = openai.embeddings.create(input=docs, model="text-embedding-3-small")
    doc_embeds = [r.embedding for r in res.data]
    return doc_embeds


text_splitter = WriterTextSplitter(strategy="llm_split")

chunks = text_splitter.split_text(resume_text)


def ingest_to_index(vec, namespace):
    index.upsert(vectors=vec, namespace=namespace)


vectors = []
for i, chunk in enumerate(chunks):
    vectors.append(
        {
            "id": f"resume#{i+1}",
            "values": embed([chunk])[0],
            "metadata": {
                "text": chunk,
                "source": "resume",
            },
        }
    )
    if len(vectors) >= 50:
        ingest_to_index(vectors, "resume-analysis")
        vectors = []
if len(vectors) > 0:
    ingest_to_index(vectors, "resume-analysis")
