import os
from typing import Dict

from project_analyzer.graph.chains.file_analyzing import file_analyzing_chain
from project_analyzer.graph.state import AnalyzerState
from project_analyzer.graph.utils import Database

richi_db = Database(
    pinecone_api=os.getenv("PINECONE_API"),
    vec_db_host=os.getenv("PINECONE_INDEX"),
    mongo_collection="project-summaries",
    mongo_host=os.getenv("MONGODB_HOST"),
)


def file_analyzer_node(state: AnalyzerState) -> Dict[str, str]:
    # print("~" * 5, " file_analyzer_node ", "~" * 5)
    response = file_analyzing_chain.invoke(
        {
            "filename": state["filenames"][state["analyzed_files"] + 1],
            "repo_name": state["repo_name"],
            "file_content": state["file_contents"][state["analyzed_files"] + 1],
        }
    )
    return {
        "file_analysis": [response.content],
        "analyzed_files": state["analyzed_files"] + 1,
    }
