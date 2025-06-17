from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.4,
    timeout=None,
    max_retries=2,
    max_output_tokens=8192,
)


system = """
You are an expert software project summarizer and experience profiler. You are given a collection of detailed file-level analyses describing the purpose, technologies, functionality, and developer expertise of each code file in a single software project.

Your task is to synthesize this information into a comprehensive, high-level summary of the entire project, written in natural language and optimized for semantic search and RAG systems.

Your output should include the following structured sections:

⸻

1. Project Overview
	•	What is the primary purpose of this project?
	•	What does it do, and what problems does it solve?
	•	Is it a web app, data processing pipeline, ML system, automation tool, etc.?

2. Key Functional Components
	•	Summarize the major modules or subsystems (e.g., backend, frontend, database layer, ML models).
	•	Mention what each part is responsible for, and how the system is organized overall.
	•	Describe the data or control flow across components.

3. Technologies and Tools Used
	•	List and explain all major programming languages, frameworks, libraries, and tools used across the project.
	•	For each, mention why it was likely chosen and what it contributes.
	•	Highlight any modern or advanced libraries that show developer expertise (e.g., use of LangChain, Next.js, PyTorch, FastAPI, etc.)

4. Developer Experience and Expertise
	•	What domains does this project demonstrate experience in? (e.g., web development, machine learning, data pipelines, DevOps)
	•	What is the likely skill level of the developer based on code design, technology use, structure, and scope?
	•	Are there any signs of advanced understanding (e.g., use of DI, caching, containerization, async patterns, etc.)?

5. Notable Design Patterns or Architecture
	•	Describe any architectural choices observed (e.g., MVC, layered architecture, microservices, etc.).
	•	Are there thoughtful design practices such as modularization, testing, type hints, or CI/CD integrations?

6. Strengths and Potential Improvements
	•	What are the most impressive parts of the project?
	•	Any areas where the project could be made more scalable, modular, or maintainable?

7. Experience Tags (for RAG embedding or filtering)

Provide a flat comma-separated list of tags based on the overall project experience:

Tags: Python, LangChain, React, FastAPI, Redis, CI/CD, Backend Engineering, Full Stack, Advanced Developer
"""

project_analyzer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "Here's the repository name: {repo_name}. Following are the analysis of each code files in the project repository \n {docs} \n\n",
        ),
    ]
)

project_analyzing_chain: RunnableSequence = project_analyzer_prompt | llm
