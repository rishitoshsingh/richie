import time

import streamlit as st

from rag.graph.consts import CONTEXT_CHATBOT, GENERAL_CHATBOT, OUT_OF_SCOPE_CHATBOT
from rag.graph.graph import richie_graph

st.title("Richie")
st.caption("🚀 A persona of Rishi")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message(
            "assistant",
            avatar="https://0.gravatar.com/avatar/d391fa37f93e8cf1193cba1c40e15fee950e021f4005e52c531f80ba774cf6e8?size=256&d=initials",
        ):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What you want to know about me?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


#  Streamed response emulator
def response_generator(query):

    for chunk, metadata in richie_graph.stream(
        {"query": query}, stream_mode="messages"
    ):
        if chunk.content and (
            metadata["langgraph_node"] == CONTEXT_CHATBOT
            or metadata["langgraph_node"] == GENERAL_CHATBOT
            or metadata["langgraph_node"] == OUT_OF_SCOPE_CHATBOT
        ):
            yield chunk.content


if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message(
        "assistant",
        avatar="https://0.gravatar.com/avatar/d391fa37f93e8cf1193cba1c40e15fee950e021f4005e52c531f80ba774cf6e8?size=256&d=initials",
    ):
        response = st.write_stream(
            response_generator(st.session_state.messages[-1]["content"])
        )
        st.session_state.messages.append({"role": "assistant", "content": response})
