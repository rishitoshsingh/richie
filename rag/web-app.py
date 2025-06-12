import time

import streamlit as st

from rag import graph

st.title("Richie")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


#  Streamed response emulator
def response_generator(query):
    for chunk, metadata in graph.stream({"question": query}, stream_mode="messages"):
        if chunk.content and metadata["langgraph_node"] == "generate":
            yield chunk.content


if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        response = st.write_stream(
            response_generator(st.session_state.messages[-1]["content"])
        )
        st.session_state.messages.append({"role": "assistant", "content": response})
