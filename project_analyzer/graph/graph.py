import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

from project_analyzer.graph.consts import (
    COLLAPSER,
    FILE_ANALYZER,
    ORCHESTRATOR,
    PROJECT_ANALYZER,
)
from project_analyzer.graph.nodes.collapser import collapser_node
from project_analyzer.graph.nodes.file_analyzer import file_analyzer_node
from project_analyzer.graph.nodes.orchestrator import orchestrator_node
from project_analyzer.graph.nodes.project_analyzer import project_analyzer_node
from project_analyzer.graph.state import AnalyzerState

load_dotenv()

richie_workflow = StateGraph(AnalyzerState)
richie_workflow.add_node(ORCHESTRATOR, orchestrator_node)
richie_workflow.add_node(FILE_ANALYZER, file_analyzer_node)
richie_workflow.add_node(COLLAPSER, collapser_node)
richie_workflow.add_node(PROJECT_ANALYZER, project_analyzer_node)


richie_workflow.add_edge(START, ORCHESTRATOR)
# richie_workflow.add_edge(ORCHESTRATOR, FILE_ANALYZER)
# richie_workflow.add_edge(ORCHESTRATOR, COLLAPSER)
# richie_workflow.add_edge(ORCHESTRATOR, PROJECT_ANALYZER)
richie_workflow.add_edge(FILE_ANALYZER, ORCHESTRATOR)
richie_workflow.add_edge(COLLAPSER, ORCHESTRATOR)
richie_workflow.add_edge(PROJECT_ANALYZER, END)


richie_graph = richie_workflow.compile()

if __name__ == "__main__":
    from IPython.display import Image, display

    img_data = richie_graph.get_graph().draw_mermaid_png()
    with open("richie_analyzer_graph.png", "wb") as f:
        f.write(img_data)
