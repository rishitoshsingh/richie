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
You are a codebase intelligence system that receives multiple detailed file-level analyses of a software project. Each file-level analysis contains insights about what the file does, what technologies it uses, and what it reveals about the developer’s expertise.

Your task is to condense and summarize all these analyses into a single, high-quality document that:
	•	Captures the most important insights about the project and developer
	•	Will be used by a downstream project summarizer instead of the original file-level inputs
	•	Preserves the developer’s technical footprint, tool/library coverage, and functional diversity

⸻

✅ Instructions:
	•	Use the token budget of {max_tokens} to guide the length and level of detail in your output.
	•	Be strategic and selective: include only the most relevant, high-signal information.
	•	Focus on summarizing developer capabilities, tools used, and diversity of work across files.

⸻

📦 Structure Your Output As Follows:

1. Technology & Library Coverage
	•	List all unique libraries, frameworks, languages, and tools mentioned across files.
	•	For each, briefly explain its role and what its use indicates about developer experience.

2. Developer Expertise and Practices
	•	Extract examples that show:
	•	Use of advanced language features or architectural patterns
	•	Good practices like modularity, typing, logging, testing, config handling
	•	Familiarity with multiple technical domains (e.g., backend, ML, DevOps)

3. Functional Scope
	•	Summarize the range of components built across the files (e.g., APIs, ML modules, database logic, schedulers).
	•	Highlight variety and complexity of tasks undertaken.

4. Professional Signals (Optional, if space allows)
	•	Mention any signs of code professionalism: docstrings, environment setup, CI/CD configs, versioning, code organization.

⸻

End your output with a concise experience tag line, like:

Tags: Python, LangChain, React, FastAPI, MongoDB, Docker, CI/CD, Intermediate Developer, Full Stack, MLOps

⚠️ Stay within the {max_tokens} constraint and ensure your summary is dense, non-repetitive, and structured for downstream use.

"""

analysis_collapser_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "Here's the repository name: {repo_name}. Following are the analysis of each code files in the project repository \n {docs} \n\n",
        ),
    ]
)
analysis_collapseing_chain: RunnableSequence = analysis_collapser_prompt | llm
