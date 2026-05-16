import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


APP_TITLE = "IntelliChat"
DEFAULT_MODEL = "openrouter/free"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
FREE_MODELS = [
    "openrouter/free",
    "baidu/cobuddy:free",
    "openrouter/owl-alpha",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "poolside/laguna-xs.2:free",
    "poolside/laguna-m.1:free",
    "deepseek/deepseek-v4-flash:free",
    "google/gemma-4-26b-a4b-it:free",
    "google/gemma-4-31b-it:free",
    "arcee-ai/trinity-large-thinking:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "minimax/minimax-m2.5:free",
    "liquid/lfm-2.5-1.2b-thinking:free",
    "liquid/lfm-2.5-1.2b-instruct:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "nvidia/nemotron-nano-12b-v2-vl:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
    "nvidia/nemotron-nano-9b-v2:free",
]


def read_setting(name: str, default: str | None = None) -> str | None:
    """Read a value from Streamlit secrets first, then from environment variables."""
    try:
        value = st.secrets.get(name)
    except Exception:
        value = None

    if value:
        return str(value)

    return os.getenv(name, default)


def read_api_key() -> str | None:
    api_key = read_setting("OPENROUTER_API_KEY") or read_setting("OPENAI_API_KEY")
    if not api_key:
        return None

    api_key = api_key.strip()
    lower_key = api_key.lower()
    placeholders = ("your-key", "your-actual-key", "your api key", "paste")

    if any(placeholder in lower_key for placeholder in placeholders):
        return None

    return api_key


def create_client() -> OpenAI | None:
    api_key = read_api_key()
    if not api_key:
        return None

    headers = {}
    site_url = read_setting("OPENROUTER_SITE_URL")
    site_name = read_setting("OPENROUTER_SITE_NAME", APP_TITLE)

    if site_url:
        headers["HTTP-Referer"] = site_url
    if site_name:
        headers["X-Title"] = site_name

    return OpenAI(
        api_key=api_key,
        base_url=read_setting("OPENAI_BASE_URL", OPENROUTER_BASE_URL),
        default_headers=headers or None,
    )


def is_free_model(model: str) -> bool:
    return model in FREE_MODELS or model.endswith(":free")


def get_free_model_options() -> list[str]:
    configured_model = read_setting("OPENROUTER_MODEL", DEFAULT_MODEL)
    models = FREE_MODELS.copy()

    if configured_model and is_free_model(configured_model) and configured_model not in models:
        models.insert(1, configured_model)

    return models


load_dotenv()

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="AI",
    layout="centered",
)

st.markdown(
    """
    <style>
    :root {
        --bg: #11100e;
        --panel: #191816;
        --panel-soft: #201f1c;
        --text: #f8fafc;
        --muted: #a8b0bd;
        --line: rgba(255, 255, 255, 0.12);
        --accent: #14b8a6;
        --accent-2: #f59e0b;
    }

    .stApp {
        background:
            linear-gradient(135deg, rgba(20, 184, 166, 0.12), transparent 34%),
            linear-gradient(225deg, rgba(245, 158, 11, 0.10), transparent 30%),
            var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 920px;
        padding: 2rem 1.2rem 6rem;
    }

    section[data-testid="stSidebar"] {
        background: #151412;
        border-right: 1px solid var(--line);
    }

    section[data-testid="stSidebar"] h1 {
        color: var(--text);
        font-size: 1.4rem;
        font-weight: 700;
    }

    .stSelectbox [data-baseweb="select"] > div {
        background: var(--panel-soft);
        border: 1px solid var(--line);
        border-radius: 8px;
        color: var(--text);
        min-height: 44px;
    }

    .stButton button {
        background: var(--panel-soft);
        border: 1px solid var(--line);
        border-radius: 8px;
        color: var(--text);
        min-height: 44px;
        transition: border-color 180ms ease, background 180ms ease, transform 180ms ease;
    }

    .stButton button:hover {
        background: #25231f;
        border-color: rgba(20, 184, 166, 0.65);
        color: var(--text);
        transform: translateY(-1px);
    }

    .stAlert {
        border-radius: 8px;
        border: 1px solid var(--line);
    }

    .hero-wrap {
        border: 1px solid var(--line);
        border-radius: 10px;
        background: rgba(25, 24, 22, 0.78);
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.28);
        margin-bottom: 1.35rem;
        padding: 1.5rem 1.4rem 1.35rem;
    }

    .status-pill {
        width: fit-content;
        margin: 0 auto 0.75rem;
        padding: 0.35rem 0.7rem;
        border: 1px solid rgba(20, 184, 166, 0.38);
        border-radius: 999px;
        background: rgba(20, 184, 166, 0.10);
        color: #99f6e4;
        font-size: 0.82rem;
        font-weight: 650;
    }

    .app-title {
        text-align: center;
        color: var(--text);
        font-size: clamp(2.3rem, 7vw, 4.3rem);
        font-weight: 800;
        line-height: 1.02;
        letter-spacing: 0;
        margin: 0 0 0.45rem;
    }

    .app-subtitle {
        color: var(--muted);
        text-align: center;
        font-size: 1.02rem;
        margin: 0 auto;
        max-width: 580px;
    }

    [data-testid="stChatMessage"] {
        background: rgba(25, 24, 22, 0.72);
        border: 1px solid var(--line);
        border-radius: 10px;
        box-shadow: 0 16px 44px rgba(0, 0, 0, 0.16);
        padding: 1rem 1rem 0.8rem;
        margin: 0.72rem 0;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: rgba(20, 184, 166, 0.12);
        border-color: rgba(20, 184, 166, 0.30);
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: rgba(255, 255, 255, 0.055);
    }

    [data-testid="stChatMessage"] p {
        color: #f1f5f9;
        line-height: 1.65;
    }

    [data-testid="chatAvatarIcon-user"] {
        color: var(--accent);
    }

    [data-testid="chatAvatarIcon-assistant"] {
        color: var(--accent-2);
    }

    [data-testid="stChatInput"] textarea {
        background: #1b1a17;
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 10px;
        color: var(--text);
        min-height: 48px;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: rgba(20, 184, 166, 0.72);
        box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.12);
    }

    [data-testid="stChatInput"] button {
        border-radius: 8px;
    }

    hr {
        border-color: var(--line);
    }

    @media (max-width: 640px) {
        .block-container {
            padding-left: 0.85rem;
            padding-right: 0.85rem;
        }

        .hero-wrap {
            padding: 1.2rem 1rem;
        }

        .app-title {
            font-size: 2.25rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

client = create_client()

with st.sidebar:
    st.title("Settings")

    if client:
        st.success("OpenRouter connected")
    else:
        st.warning("No API key configured")

    free_models = get_free_model_options()
    configured_model = read_setting("OPENROUTER_MODEL", DEFAULT_MODEL)
    default_index = (
        free_models.index(configured_model)
        if configured_model in free_models
        else free_models.index(DEFAULT_MODEL)
    )
    model = st.selectbox("Free model", options=free_models, index=default_index)

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Set OPENROUTER_API_KEY in Streamlit secrets. This app only lists free models.")

st.markdown(
    f"""
    <div class="hero-wrap">
        <div class="status-pill">OpenRouter Free Models</div>
        <h1 class="app-title">{APP_TITLE}</h1>
        <p class="app-subtitle">Ask anything and get an instant AI response.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi, I am ready. What would you like to ask?",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()

        if client is None:
            response = (
                "The chatbot is running, but no OpenRouter API key is configured yet. "
                "Add OPENROUTER_API_KEY in Streamlit secrets or in a local .env file."
            )
            placeholder.markdown(response)
        else:
            response = ""
            try:
                stream = client.chat.completions.create(
                    model=model.strip() or DEFAULT_MODEL,
                    messages=[
                        {"role": item["role"], "content": item["content"]}
                        for item in st.session_state.messages
                    ],
                    stream=True,
                )

                for chunk in stream:
                    token = chunk.choices[0].delta.content or ""
                    response += token
                    placeholder.markdown(response + "...")

                placeholder.markdown(response)
            except Exception as exc:
                response = (
                    "I could not reach the AI service. Please check your OpenRouter "
                    f"key, selected model, and Streamlit secrets. Error: {exc}"
                )
                placeholder.error(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
