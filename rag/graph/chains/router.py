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

system_prompt = """You are a helpful assistant tasked with classifying user queries into one of four categories:
	•	general: Greetings or casual questions (e.g., “Hi”, “How are you?”, “What’s up?”).
	•	project: Questions about the user’s personal, academic, or professional projects. For example: “What projects have you done?”, “Describe your machine learning project”, or “Tell me about your robotics work.”
	•	resume: Questions about the user’s resume details — including work experience, education, internships, certifications, courses, skills, or contact details. Example: “What did you study in college?”, “Tell me about your last job”, “What’s your phone number?”, or “List your technical skills.”
	•	out_of_scope: Anything that does not fall into the above categories. This includes questions unrelated to the user’s background or work, such as current events, weather, philosophical questions, etc.

Task:

Given a user’s query, classify it into exactly one of the following categories:
general, project, resume, out_of_scope
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
