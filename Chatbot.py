import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ Please set your OPENAI_API_KEY in a .env file (see .env.example)!")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

st.title("🤖 My Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is your question?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Stream response from OpenAI
        stream = client.chat.completions.create(
            model="gpt-4o-mini",  # Fixed model name (GPT-5.4 nano doesn't exist)
            messages=[
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

