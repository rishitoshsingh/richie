import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

from rag.graph.consts import (
    ANSWER_GRADER,
    CONTEXT_CHATBOT,
    GENERAL_CHATBOT,
    OUT_OF_SCOPE_CHATBOT,
    PROMPT_ENGINEERING,
    QUERY_CLASSIFIER,
)
from rag.graph.nodes.answer_grader import answer_grader_node
from rag.graph.nodes.context_generation import context_chatbot_node
from rag.graph.nodes.general_generation import general_chatbot_node
from rag.graph.nodes.out_of_scope import out_of_scope_chatbot_node
from rag.graph.nodes.prompt_engineer import prompt_engineering_node
from rag.graph.nodes.query_classifier import query_classifier_node
from rag.graph.state import RichieGraphState

load_dotenv()

richie_workflow = StateGraph(RichieGraphState)
richie_workflow.add_node(QUERY_CLASSIFIER, query_classifier_node)
richie_workflow.add_node(GENERAL_CHATBOT, general_chatbot_node)
richie_workflow.add_node(OUT_OF_SCOPE_CHATBOT, out_of_scope_chatbot_node)
richie_workflow.add_node(PROMPT_ENGINEERING, prompt_engineering_node)
richie_workflow.add_node(CONTEXT_CHATBOT, context_chatbot_node)
# richie_workflow.add_node(ANSWER_GRADER, answer_grader_node)
richie_workflow.add_edge(START, QUERY_CLASSIFIER)
richie_workflow.add_conditional_edges(
    QUERY_CLASSIFIER,
    lambda state: state["router_next_state"],
    {
        GENERAL_CHATBOT: GENERAL_CHATBOT,
        OUT_OF_SCOPE_CHATBOT: OUT_OF_SCOPE_CHATBOT,
        PROMPT_ENGINEERING: PROMPT_ENGINEERING,
    },
)
richie_workflow.add_edge(PROMPT_ENGINEERING, CONTEXT_CHATBOT)
# richie_workflow.add_edge(CONTEXT_CHATBOT, ANSWER_GRADER)
# richie_workflow.add_edge(ANSWER_GRADER, END)
richie_workflow.add_edge(CONTEXT_CHATBOT, END)
richie_workflow.add_edge(OUT_OF_SCOPE_CHATBOT, END)
richie_workflow.add_edge(GENERAL_CHATBOT, END)


richie_graph = richie_workflow.compile()

if __name__ == "__main__":
    from IPython.display import Image, display

    img_data = richie_graph.get_graph().draw_mermaid_png()
    with open("richie_graph.png", "wb") as f:
        f.write(img_data)
