import os
from typing import TypedDict, Union

from dotenv import load_dotenv
from langchain_writer.text_splitter import WriterTextSplitter
from pinecone import Pinecone

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API"))
index = pc.Index(host=os.getenv("PINECONE_INDEX"))

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RESUME_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "resume.txt")
with open(RESUME_DATA_PATH, "r") as f:
    resume_text = f.read()


text_splitter = WriterTextSplitter(strategy="llm_split")

chunks = text_splitter.split_text(resume_text)


class ResumeRecord(TypedDict):
    id: str
    text: str
    record_type: str


def ingest_to_index(records, namesoace):
    index.upsert_records(
        namespace=namesoace,
        records=records,
    )


records = []
for i, chunk in enumerate(chunks):
    records.append(
        ResumeRecord(
            id=f"chunk#{i+1}",
            text=chunk,
            record_type="resume-summary",
        )
    )
    if len(records) >= 50:
        ingest_to_index(records, "resume-summaries")
        records = []
if len(records) > 0:
    ingest_to_index(records, "resume-summaries")
