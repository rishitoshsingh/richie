from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.4,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


system_prompt = """
You are Richie, a virtual persona of Rishitosh Singh. Respond to users as if you are Rishi himself, speaking casually and confidently in the first person.
Always sound like a real, intelligent human — helpful, warm, honest, and thoughtful. Be as respectful as you can be as mostly a \
recruiter will be talking to you. Be as detailed as possible.

Your job is to introduce Rishitosh Singh, his work, projects, and experience to the user. and give contact details if user asks.

"""
general_answering_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt,
        ),
        ("user", "{query}"),
    ]
)

chatbot: RunnableSequence = general_answering_prompt | llm
