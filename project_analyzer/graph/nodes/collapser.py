from typing import Dict

from project_analyzer.graph.chains.analysis_collapsing import analysis_collapseing_chain
from project_analyzer.graph.state import AnalyzerState


def collapser_node(state: AnalyzerState) -> Dict[str, str]:
    # print("~" * 5, " collapser_node ", "~" * 5)
    response = analysis_collapseing_chain.invoke(
        {
            "max_tokens": state["context_max_token"],
            "repo_name": state["repo_name"],
            "docs": state["file_analysis"][
                state["collapsed_files"] : state["analyzed_files"] + 1
            ],
        }
    )
    return {
        "collapsed_analysis": [response.content],
        "collapsed_files": state["analyzed_files"],
    }
