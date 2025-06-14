from typing import Dict

from rag.graph.chains.answer_grading import GradeAnswer, answer_grader_chain
from rag.graph.state import RichieGraphState


def answer_grader_node(state: RichieGraphState) -> None:
    print("~" * 5, " prompt_engineering_node ", "~" * 5)
    result: GradeAnswer = answer_grader_chain.invoke({"query": state["query"]})
    print("~" * 5, " result ", "~" * 5, result)
    return
