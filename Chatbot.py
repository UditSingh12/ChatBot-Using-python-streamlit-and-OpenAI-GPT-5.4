import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="My ChatBot",
    page_icon="🤖",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .user-msg {
        background-color: #1f6feb;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .bot-msg {
        background-color: #262730;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- LOAD ENV ----------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("⚙️ Settings")
    
    if api_key:
        st.success("API Connected ✅")
    else:
        st.error("Demo Mode (No API) ⚠️")

    st.markdown("---")
    
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []

    st.markdown("---")
    st.write("Built by Udit Singh 🚀")

# ---------------- TITLE ----------------
st.markdown("<h1 style='text-align: center;'>🤖 AI Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ask anything and get instant responses</p>", unsafe_allow_html=True)

# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY CHAT ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(f"<div class='user-msg'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'>{message['content']}</div>", unsafe_allow_html=True)

# ---------------- INPUT ----------------
if prompt := st.chat_input("Type your message..."):

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(f"<div class='user-msg'>{prompt}</div>", unsafe_allow_html=True)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # If no API → fallback
            if not client:
                raise Exception("No API")

            with st.spinner("Thinking..."):
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )

                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(
                            f"<div class='bot-msg'>{full_response}▌</div>",
                            unsafe_allow_html=True
                        )

        except:
            # 🔥 Fallback response
            full_response = f"""
⚠️ AI service unavailable  

👉 You asked: **{prompt}**

💡 This is a demo response. Enable API key for full AI functionality.
"""

        message_placeholder.markdown(
            f"<div class='bot-msg'>{full_response}</div>",
            unsafe_allow_html=True
        )

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
