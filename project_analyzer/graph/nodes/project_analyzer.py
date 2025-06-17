import os
from typing import Dict

from project_analyzer.graph.chains.project_analyzing import project_analyzing_chain
from project_analyzer.graph.state import AnalyzerState

# from project_analyzer.graph.utils import Database

# richi_db = Database(
#     pinecone_api=os.getenv("PINECONE_API"),
#     vec_db_host=os.getenv("PINECONE_INDEX"),
#     mongo_collection="project-summaries",
#     mongo_host=os.getenv("MONGODB_HOST"),
# )


def project_analyzer_node(state: AnalyzerState) -> Dict[str, str]:
    # print("~" * 5, " project_analyzer_node ", "~" * 5)

    content = [s for s in state["collapsed_analysis"][0 : state["collapsed_files"] + 1]]
    content.extend(
        [
            s
            for s in state["file_analysis"][
                state["collapsed_files"] : state["analyzed_files"] + 1
            ]
        ]
    )
    response = project_analyzing_chain.invoke(
        {"repo_name": state["repo_name"], "docs": content}
    )
    return {"project_analysis": response.content}
