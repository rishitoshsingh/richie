from typing import Dict

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import Command, Send

from project_analyzer.graph.chains.project_analyzing import llm, project_analyzer_prompt
from project_analyzer.graph.consts import COLLAPSER, FILE_ANALYZER, PROJECT_ANALYZER
from project_analyzer.graph.state import AnalyzerState


def orchestrator_node(state: AnalyzerState) -> Command:
    # print("~" * 5, " orchestrator_node ", "~" * 5)
    project_analyzer_prompt.invoke(
        {
            "repo_name": state["repo_name"],
            "docs": state["file_analysis"][
                state["collapsed_files"] : state["analyzed_files"] + 1
            ],
        }
    )
    if state["analyzed_files"] + 1 < state["n_files"]:
        if state["collapsed_files"] is not None:
            _slice = slice(state["collapsed_files"], state["analyzed_files"] + 1)
        else:
            _slice = slice(0, state["collapsed_files"] + 1)
        query = project_analyzer_prompt.invoke(
            {
                "repo_name": state["repo_name"],
                "docs": state["file_analysis"][_slice],
            }
        )
        n_content_tokens = llm.get_num_tokens(
            " ".join(st.content for st in query.messages)
        )
        if n_content_tokens > state["context_max_token"]:
            return Command(goto=COLLAPSER)
            # return Send(COLLAPSER, state)
        else:
            return Command(goto=FILE_ANALYZER)
            # return Send(FILE_ANALYZER, state)
    else:
        return Command(goto=PROJECT_ANALYZER)
        # return Send(PROJECT_ANALYZER, state)
