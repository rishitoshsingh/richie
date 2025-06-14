from dotenv import load_dotenv

load_dotenv()

from rag.graph.chains.general_generation import chatbot
from rag.graph.chains.prompt_engineering import SearchQuery, search_query_formatter
from rag.graph.chains.router import QueryClassifier, query_router


def test_query_router_general():
    """Test the query router for general queries."""
    query = "Hi, How are you?"
    result = query_router.invoke({"query": query})
    assert result.q_type == "general", "Query type should be 'general'"


def test_query_router_project():
    """Test the query router for project queries."""
    query = "What is Rishitosh Singh's latest project?"
    result = query_router.invoke({"query": query})
    assert result.q_type == "project", "Query type should be 'project'"


def test_query_router_resume():
    """Test the query router for resume queries."""
    query = "From where rishi have done his masters?"
    result = query_router.invoke({"query": query})
    assert result.q_type == "resume", "Query type should be 'resume'"


def test_query_router_out_of_scope():
    """Test the query router for out-of-scope queries."""
    query = "What is the capital of France?"
    result = query_router.invoke({"query": query})
    assert result.q_type == "out_of_scope", "Query type should be 'out_of_scope'"


def test_search_query_formatter():
    """Test the search query formatter."""
    query = "Tell me about Rishitosh Singh's work."
    result = search_query_formatter.invoke({"query": query})
    print(result.modified_query)
    assert isinstance(result, SearchQuery), "Result should be of type SearchQuery"


def test_chatbot():
    """Test the chatbot generation."""
    user_question = "What is Richie?"
    result = chatbot.invoke({"query": user_question})
    print(result)
    assert isinstance(result.content, str), "Result should be a string"
