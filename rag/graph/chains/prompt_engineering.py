from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


class SearchQuery(BaseModel):

    modified_query: str = Field(
        None,
        description="Modified user query to get best relevant documents from vector database",
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

search_query_formatter_llm = llm.with_structured_output(SearchQuery)

system_prompt = """You are a helpful assistant that reformulates user questions to improve document retrieval in a RAG (Retrieval-Augmented Generation) system. \
    "Your goal is to rewrite the user's query in to be standalone, clear, and optimized for retrieving relevant \
    "documents—even if the original question is vague, follow-up-based, or context-dependent. Do not answer \
    "the question. Only rewrite it for retrieval. Preserve the user's intent to know about the owner Rishi or rishitosh or richie and include necessary context to make it specific."""


search_router_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt,
        ),
        ("user", "{query}"),
    ]
)

search_query_formatter: RunnableSequence = (
    search_router_prompt | search_query_formatter_llm
)
