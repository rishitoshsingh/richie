import operator
from typing import Annotated, Sequence, TypedDict, Union


class AnalyzerState(TypedDict):
    context_max_token: int
    n_files: int
    repo_name: str
    filenames: Sequence[str]
    file_contents: Sequence[str]
    analyzed_files: int
    collapsed_files: int
    file_analysis: Annotated[Sequence[str], operator.add]
    collapsed_analysis: Annotated[Sequence[str], operator.add]
    project_analysis: Union[str, None]
