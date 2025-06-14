from typing import TypedDict


class RichieGraphState(TypedDict):
    query: str
    modified_query: str
    context: str
    answer: str
    retrieve_namespace: str
    router_next_state: str
    answer_correct: str
