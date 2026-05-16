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

# Initialize theme state
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Premium theme definitions
THEMES = {
    "dark": {
        "bg": "#0a0908",
        "bg_secondary": "#13111f",
        "panel": "#1a1927",
        "panel_soft": "#23212e",
        "text": "#f8fafc",
        "text_secondary": "#cbd5e1",
        "muted": "#94a3b8",
        "border": "rgba(248, 250, 252, 0.08)",
        "accent_primary": "#06b6d4",
        "accent_secondary": "#8b5cf6",
        "accent_tertiary": "#ec4899",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "shadow_sm": "0 2px 8px rgba(0, 0, 0, 0.16)",
        "shadow_md": "0 8px 24px rgba(0, 0, 0, 0.24)",
        "shadow_lg": "0 16px 48px rgba(0, 0, 0, 0.32)",
    },
    "light": {
        "bg": "#fafbfc",
        "bg_secondary": "#f1f5f9",
        "panel": "#ffffff",
        "panel_soft": "#f8fafc",
        "text": "#0f172a",
        "text_secondary": "#334155",
        "muted": "#94a3b8",
        "border": "rgba(15, 23, 42, 0.08)",
        "accent_primary": "#0891b2",
        "accent_secondary": "#7c3aed",
        "accent_tertiary": "#db2777",
        "success": "#059669",
        "warning": "#d97706",
        "error": "#dc2626",
        "shadow_sm": "0 2px 8px rgba(0, 0, 0, 0.06)",
        "shadow_md": "0 8px 24px rgba(0, 0, 0, 0.08)",
        "shadow_lg": "0 16px 48px rgba(0, 0, 0, 0.10)",
    }
}

current_theme = THEMES[st.session_state.theme]

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

    :root {{
        --bg: {current_theme['bg']};
        --bg-secondary: {current_theme['bg_secondary']};
        --panel: {current_theme['panel']};
        --panel-soft: {current_theme['panel_soft']};
        --text: {current_theme['text']};
        --text-secondary: {current_theme['text_secondary']};
        --muted: {current_theme['muted']};
        --border: {current_theme['border']};
        --accent-primary: {current_theme['accent_primary']};
        --accent-secondary: {current_theme['accent_secondary']};
        --accent-tertiary: {current_theme['accent_tertiary']};
        --success: {current_theme['success']};
        --warning: {current_theme['warning']};
        --error: {current_theme['error']};
        --shadow-sm: {current_theme['shadow_sm']};
        --shadow-md: {current_theme['shadow_md']};
        --shadow-lg: {current_theme['shadow_lg']};
    }}

    * {{
        transition: background-color 280ms cubic-bezier(0.4, 0, 0.2, 1),
                    color 280ms cubic-bezier(0.4, 0, 0.2, 1),
                    border-color 280ms cubic-bezier(0.4, 0, 0.2, 1);
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}

    .stApp {{
        background: linear-gradient(135deg, var(--bg) 0%, var(--bg-secondary) 100%);
        color: var(--text);
        overflow-x: hidden;
    }}

    [data-testid="stAppViewContainer"]::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(6, 182, 212, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.06) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
        border-bottom: 1px solid var(--border);
        backdrop-filter: blur(12px);
    }}

    .block-container {{
        max-width: 900px;
        padding: 2rem 1.2rem 8rem !important;
        position: relative;
        z-index: 1;
    }}

    section[data-testid="stSidebar"] {{
        background: var(--panel);
        border-right: 1px solid var(--border);
        backdrop-filter: blur(8px);
        animation: slideInLeft 480ms cubic-bezier(0.34, 1.56, 0.64, 1);
    }}

    @keyframes slideInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}

    section[data-testid="stSidebar"] h1 {{
        color: var(--text);
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        letter-spacing: -0.02em;
    }}

    section[data-testid="stSidebar"] .stSelectbox label {{
        color: var(--text-secondary);
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }}

    .stSelectbox [data-baseweb="select"] > div {{
        background: var(--panel-soft);
        border: 1.5px solid var(--border);
        border-radius: 10px;
        color: var(--text);
        min-height: 44px;
        transition: all 240ms cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 500;
    }}

    .stSelectbox [data-baseweb="select"] > div:hover {{
        border-color: var(--accent-primary);
        background: var(--panel);
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1);
    }}

    .stSelectbox [data-baseweb="select"] > div:focus-within {{
        border-color: var(--accent-primary);
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.15);
    }}

    .stButton button {{
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
        border: none;
        border-radius: 10px;
        color: white;
        min-height: 44px;
        font-weight: 600;
        letter-spacing: 0.02em;
        transition: all 240ms cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: var(--shadow-md);
        position: relative;
        overflow: hidden;
    }}

    .stButton button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.2);
        transition: left 300ms ease;
    }}

    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(6, 182, 212, 0.4);
        background: linear-gradient(135deg, var(--accent-secondary) 0%, var(--accent-primary) 100%);
    }}

    .stButton button:hover::before {{
        left: 100%;
    }}

    .stAlert {{
        border-radius: 10px;
        border: 1.5px solid var(--border);
        background: var(--panel);
        backdrop-filter: blur(8px);
        animation: slideUp 360ms cubic-bezier(0.34, 1.56, 0.64, 1);
    }}

    @keyframes slideUp {{
        from {{
            opacity: 0;
            transform: translateY(12px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .hero-wrap {{
        border: 1.5px solid var(--border);
        border-radius: 16px;
        background: linear-gradient(135deg, var(--panel) 0%, var(--panel-soft) 100%);
        backdrop-filter: blur(10px);
        box-shadow: var(--shadow-lg);
        margin-bottom: 2rem;
        padding: 3rem 2rem 2.5rem;
        animation: fadeInScale 600ms cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
    }}

    .hero-wrap::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
        pointer-events: none;
    }}

    @keyframes rotate {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}

    @keyframes fadeInScale {{
        from {{
            opacity: 0;
            transform: scale(0.95);
        }}
        to {{
            opacity: 1;
            transform: scale(1);
        }}
    }}

    .status-pill {{
        width: fit-content;
        margin: 0 auto 1.2rem;
        padding: 0.5rem 1.2rem;
        border: 1.5px solid var(--accent-primary);
        border-radius: 999px;
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.12) 0%, rgba(139, 92, 246, 0.08) 100%);
        color: var(--accent-primary);
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.12);
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }}

    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
    }}

    .app-title {{
        text-align: center;
        color: var(--text);
        font-size: clamp(2.5rem, 8vw, 4.5rem);
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -0.03em;
        margin: 0 0 0.6rem;
        background: linear-gradient(135deg, var(--text) 0%, var(--accent-primary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    .app-subtitle {{
        color: var(--text-secondary);
        text-align: center;
        font-size: 1.1rem;
        font-weight: 400;
        line-height: 1.6;
        margin: 0 auto;
        max-width: 600px;
        letter-spacing: -0.01em;
    }}

    [data-testid="stChatMessage"] {{
        background: var(--panel-soft);
        border: 1.5px solid var(--border);
        border-radius: 14px;
        box-shadow: var(--shadow-sm);
        padding: 1.2rem 1.4rem;
        margin: 0.8rem 0;
        animation: fadeInUp 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
        backdrop-filter: blur(8px);
    }}

    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(12px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    [data-testid="stChatMessage"]:hover {{
        border-color: var(--accent-primary);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }}

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {{
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(139, 92, 246, 0.08) 100%);
        border-color: var(--accent-primary);
    }}

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {{
        background: linear-gradient(135deg, var(--panel-soft) 0%, rgba(139, 92, 246, 0.05) 100%);
    }}

    [data-testid="stChatMessage"] p {{
        color: var(--text);
        line-height: 1.7;
        letter-spacing: -0.005em;
    }}

    [data-testid="chatAvatarIcon-user"] {{
        color: var(--accent-primary);
        font-size: 1.35rem;
    }}

    [data-testid="chatAvatarIcon-assistant"] {{
        color: var(--accent-secondary);
        font-size: 1.35rem;
    }}

    [data-testid="stChatInput"] {{
        gap: 0.75rem;
    }}

    [data-testid="stChatInput"] textarea {{
        background: var(--panel-soft);
        border: 1.5px solid var(--border);
        border-radius: 12px;
        color: var(--text);
        min-height: 52px;
        font-size: 0.95rem;
        font-weight: 400;
        padding: 0.75rem 1rem;
        resize: vertical;
        transition: all 240ms cubic-bezier(0.4, 0, 0.2, 1);
    }}

    [data-testid="stChatInput"] textarea::placeholder {{
        color: var(--muted);
    }}

    [data-testid="stChatInput"] textarea:focus {{
        border-color: var(--accent-primary);
        background: var(--panel);
        box-shadow: 0 0 0 4px rgba(6, 182, 212, 0.1);
        outline: none;
    }}

    [data-testid="stChatInput"] button {{
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        min-height: 52px;
    }}

    hr {{
        border: none;
        height: 1px;
        background: var(--border);
        margin: 1.5rem 0;
    }}

    .stCaption {{
        color: var(--muted);
        font-size: 0.8rem !important;
        line-height: 1.5;
        margin-top: 1rem;
    }}

    /* Premium scrollbar styling */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: var(--panel);
    }}

    ::-webkit-scrollbar-thumb {{
        background: var(--accent-primary);
        border-radius: 4px;
        transition: background 240ms ease;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: var(--accent-secondary);
    }}

    @media (max-width: 640px) {{
        .block-container {{
            padding-left: 0.75rem;
            padding-right: 0.75rem;
            padding-top: 1.5rem;
        }}

        .hero-wrap {{
            padding: 2rem 1.2rem;
            margin-bottom: 1.5rem;
        }}

        .app-title {{
            font-size: 2.25rem;
            margin-bottom: 0.5rem;
        }}

        .app-subtitle {{
            font-size: 0.95rem;
        }}

        [data-testid="stChatMessage"] {{
            padding: 1rem 1.1rem;
            margin: 0.6rem 0;
        }}

        [data-testid="stChatInput"] textarea {{
            min-height: 48px;
            font-size: 0.9rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

client = create_client()

# Sidebar with premium styling
with st.sidebar:
    st.title("⚙️ Settings")

    # Theme toggle
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌙 Dark", use_container_width=True, key="dark_theme"):
            st.session_state.theme = "dark"
            st.rerun()
    with col2:
        if st.button("☀️ Light", use_container_width=True, key="light_theme"):
            st.session_state.theme = "light"
            st.rerun()

    st.divider()

    # API Status
    if client:
        st.success("✓ OpenRouter Connected", icon="🟢")
    else:
        st.warning("✗ No API Key Configured", icon="🔴")

    st.divider()

    # Model selection
    st.markdown("**AI Model**")
    free_models = get_free_model_options()
    configured_model = read_setting("OPENROUTER_MODEL", DEFAULT_MODEL)
    default_index = (
        free_models.index(configured_model)
        if configured_model in free_models
        else free_models.index(DEFAULT_MODEL)
    )
    model = st.selectbox("Select model", options=free_models, index=default_index, label_visibility="collapsed")

    st.divider()

    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption(
        "📝 **Setup Guide**\n\n"
        "Set `OPENROUTER_API_KEY` in Streamlit secrets or `.env` file. "
        "This app features free AI models only."
    )

# Main content with premium hero section
st.markdown(
    f"""
    <div class="hero-wrap">
        <div class="status-pill">✨ Powered by OpenRouter Free Models</div>
        <h1 class="app-title">{APP_TITLE}</h1>
        <p class="app-subtitle">Experience premium AI conversations with instant, intelligent responses. No signup required.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize chat messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Welcome to IntelliChat! I'm ready to assist you. What would you like to explore today?",
        }
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧠" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Type your message here...", placeholder="Ask me anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🧠"):
        placeholder = st.empty()

        if client is None:
            response = (
                "⚠️ **Configuration Required**\n\n"
                "The chatbot is running, but no OpenRouter API key is configured yet. "
                "Please add `OPENROUTER_API_KEY` to:\n"
                "- Streamlit secrets (in production)\n"
                "- A local `.env` file (in development)\n\n"
                "Visit [OpenRouter](https://openrouter.ai) to get a free API key."
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
                    placeholder.markdown(response + " ▌")

                placeholder.markdown(response)
            except Exception as exc:
                response = (
                    "❌ **Connection Error**\n\n"
                    "I couldn't reach the AI service. Please verify:\n"
                    "- Your OpenRouter API key is valid\n"
                    "- The selected model is available\n"
                    "- Your Streamlit secrets are configured\n\n"
                    f"**Error Details:** `{str(exc)[:100]}...`"
                )
                placeholder.error(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
