import json
import os
import time
from typing import TypedDict, Union

from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from tqdm import tqdm

api_path = os.path.expanduser("auth/api.json")
with open(api_path, "r") as f:
    apis = json.load(f)

pc = Pinecone(api_key=apis.get("PINECONE"))
index = pc.Index(host="https://richie-brain-384-roilyxl.svc.aped-4627-b74a.pinecone.io")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

SUMMARY_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "user_repo_summaries.json")
with open(SUMMARY_DATA_PATH, "r") as f:
    summary_data = json.load(f)


text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " "],
    chunk_size=512,
    chunk_overlap=64,
    length_function=lambda x: len(x),
    is_separator_regex=False,
)

summary = summary_data[0]
summaries = []
for file, content in summary["file_analysis"].items():
    summaries.append(content)


class Record(TypedDict):
    id: str
    text: str
    repo_name: str
    file_name: Union[str, None]
    record_type: str


def ingest_to_index(records, namesoace):
    index.upsert_records(
        namespace=namesoace,
        records=records,
    )


for summary in tqdm(summary_data, desc="Ingesting summaries"):
    records = []
    for file, file_analysis in summary["file_analysis"].items():
        doc_list = text_splitter.create_documents([file_analysis])
        for i, doc in enumerate(doc_list):
            records.append(
                Record(
                    id=f"{summary['repo_name']}#{file}#{i+1}",
                    text=doc.page_content,
                    repo_name=summary["repo_name"],
                    file_name=file,
                    record_type="file-summary",
                )
            )
            if len(records) >= 50:
                ingest_to_index(records, "project-summaries")
                records = []
    if len(records) > 0:
        ingest_to_index(records, "project-summaries")
    repo_sumary_list = text_splitter.create_documents([summary["repo_summary"]])
    records = []
    for i, doc in enumerate(repo_sumary_list):
        records.append(
            Record(
                id=f"{summary['repo_name']}#repo_summary#{i+1}",
                text=doc.page_content,
                repo_name=summary["repo_name"],
                file_name=None,
                record_type="repo-summary",
            )
        )
    time.sleep(60)
