# Code adapted from:
# https://github.com/junfanz1/Cognito-LangGraph-RAG-Chatbot/blob/main/graph/chains/answer_grader.py
# Author: Junfan Zhang (https://github.com/junfanz1)
# License: Apache License 2.0


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


class GradeAnswer(BaseModel):
    binary_score: bool = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
grader_llm = llm.with_structured_output(GradeAnswer)

system = """You are a grader assessing whether an answer addresses / resolves a question.\n
Give a binary score 'yes' or 'no'. 'yes' means the answer resolves the question."""

answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "User question: \n\n {query} \n\n LLM generation: {generation}"),
    ]
)

answer_grader_chain: RunnableSequence = answer_prompt | grader_llm
