from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


class QueryClassifier(BaseModel):

    q_type: Literal["general", "project", "resume", "out_of_scope"] = Field(
        None,
        description="Given a user query, decide whether it is a general query, a project-related query, or a resume-related query.",
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
query_decider_llm = llm.with_structured_output(QueryClassifier)

system_prompt = """You are a helpful assistant that classifies user queries into four types: general, project, resume, or out_of_scope. \Add commentMore actions
    General queries are simple greetings or questions like 'Hi' or 'Hello'. Project-related queries are about the user's projects, \
    such as 'What projects have you worked on?'. Resume-related queries are about the user's work experience, education, or other \
    resume-related topics like education, courses taken in college or university, contact details, anything that can tell about the user\
    Out-of-scope queries are those that do not fit into any of these categories. \
    Your task is to classify the user query into one of these four categories."
    """

query_router_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt,
        ),
        ("user", "{query}"),
    ]
)

query_router: RunnableSequence = query_router_prompt | query_decider_llm
