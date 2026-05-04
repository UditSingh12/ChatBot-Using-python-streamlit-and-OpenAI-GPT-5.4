import streamlit as st
import os
import json
from datetime import datetime
from typing import Optional, List, Dict
from pathlib import Path
from dotenv import load_dotenv
import requests

# ==================== CONFIGURATION ====================
load_dotenv()

# Page configuration with enhanced settings
st.set_page_config(
    page_title="IntelliChat - AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "🚀 IntelliChat v2.0 - Professional AI Chatbot built with Streamlit & OpenRouter"
    }
)

# ==================== CONSTANTS ====================
CONVERSATIONS_DIR = Path("conversations")
CONVERSATIONS_DIR.mkdir(exist_ok=True)

# OpenRouter Models - Free and Paid options
AVAILABLE_MODELS = {
    "Claude 3.5 Sonnet (Fast & Smart)": "anthropic/claude-3.5-sonnet",
    "Claude 3 Opus (Most Capable)": "anthropic/claude-3-opus",
    "GPT-4 Turbo": "openai/gpt-4-turbo",
    "GPT-4o Mini (Fast & Cheap)": "openai/gpt-4o-mini",
    "Llama 2 70B (Free)": "meta-llama/llama-2-70b-chat",
    "Mistral 7B (Free)": "mistralai/mistral-7b-instruct",
}

OPENROUTER_API_URL = "https://openrouter.io/api/v1/chat/completions"
MAX_CHAT_HISTORY = 50

# ==================== CUSTOM CSS & STYLING ====================
st.markdown("""
    <style>
    :root {
        --primary: #0066cc;
        --secondary: #1f6feb;
        --background: #0d1117;
        --surface: #161b22;
        --border: #30363d;
        --text-primary: #c9d1d9;
        --text-secondary: #8b949e;
        --success: #1f8934;
        --warning: #d29922;
        --danger: #da3633;
    }
    
    * {
        transition: all 0.2s ease;
    }
    
    .main {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        color: var(--text-primary);
    }
    
    /* Chat Messages */
    .chat-user {
        background: linear-gradient(135deg, #0066cc 0%, #1f6feb 100%);
        color: white;
        padding: 14px 16px;
        border-radius: 12px;
        margin: 8px 0;
        word-wrap: break-word;
        border-left: 3px solid #0066cc;
        box-shadow: 0 2px 8px rgba(0, 102, 204, 0.2);
    }
    
    .chat-assistant {
        background: var(--surface);
        color: var(--text-primary);
        padding: 14px 16px;
        border-radius: 12px;
        margin: 8px 0;
        word-wrap: break-word;
        border-left: 3px solid #30363d;
        box-shadow: 0 2px 8px rgba(48, 54, 61, 0.2);
    }
    
    .message-actions {
        display: flex;
        gap: 8px;
        margin-top: 8px;
        opacity: 0.7;
        font-size: 12px;
    }
    
    .message-actions button {
        background: transparent;
        border: none;
        color: var(--text-secondary);
        cursor: pointer;
        padding: 4px 8px;
    }
    
    .message-actions button:hover {
        color: var(--primary);
        transform: scale(1.1);
    }
    
    /* Sidebar */
    .sidebar-section {
        margin: 16px 0;
        padding: 12px;
        border-radius: 8px;
        background: var(--surface);
        border: 1px solid var(--border);
    }
    
    .stat-box {
        background: linear-gradient(135deg, #0066cc15, #1f6feb15);
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid var(--border);
        margin: 8px 0;
    }
    
    .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: #0066cc;
    }
    
    .stat-label {
        font-size: 12px;
        color: var(--text-secondary);
        margin-top: 4px;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0066cc, #1f6feb);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 16px;
        font-weight: 500;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.5);
        transform: translateY(-2px);
    }
    
    /* Status Badges */
    .status-connected {
        color: var(--success);
        font-weight: bold;
    }
    
    .status-disconnected {
        color: var(--danger);
        font-weight: bold;
    }
    
    /* Title */
    .main h1 {
        background: linear-gradient(135deg, #0066cc, #1f6feb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3em;
        font-weight: 800;
        margin-bottom: 8px;
    }
    
    .subtitle {
        color: var(--text-secondary);
        font-size: 1.1em;
        margin-bottom: 24px;
    }
    
    /* Input */
    .stChatInputContainer {
        border-top: 1px solid var(--border);
        padding-top: 16px;
    }
    
    /* Divider */
    hr {
        border-color: var(--border);
        margin: 16px 0;
    }
    
    /* Info/Warning/Error messages */
    .stSuccess {
        background-color: rgba(31, 137, 52, 0.1);
        border-left: 3px solid var(--success);
    }
    
    .stError {
        background-color: rgba(218, 54, 51, 0.1);
        border-left: 3px solid var(--danger);
    }
    
    .stWarning {
        background-color: rgba(210, 153, 34, 0.1);
        border-left: 3px solid var(--warning);
    }
    
    </style>
""", unsafe_allow_html=True)

# ==================== UTILITY FUNCTIONS ====================

def validate_api_key() -> bool:
    """Validate OpenRouter API key"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key or api_key == "Your api key":
        return False
    
    return True

def get_api_key() -> Optional[str]:
    """Get API key from environment"""
    return os.getenv("OPENROUTER_API_KEY")

def call_openrouter_api(
    messages: List[Dict],
    model: str,
    temperature: float = 0.7
) -> Optional[str]:
    """
    Call OpenRouter API with streaming support
    
    Args:
        messages: List of message dictionaries
        model: Model name from AVAILABLE_MODELS
        temperature: Response temperature (0-2)
    
    Returns:
        Full response text or None if error
    """
    api_key = get_api_key()
    
    if not api_key:
        raise Exception("API key not found. Please check your .env file.")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/UditSingh12/ChatBot-Using-python-streamlit-and-OpenAI",
        "X-Title": "IntelliChat"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 2048,
        "stream": True
    }
    
    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )
        
        if response.status_code == 401:
            raise Exception("Authentication failed: Invalid API key")
        elif response.status_code == 429:
            raise Exception("Rate limited: Too many requests. Please wait a moment.")
        elif response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text[:100]}")
        
        # Process streaming response
        full_response = ""
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]
                    if data == '[DONE]':
                        break
                    try:
                        json_data = json.loads(data)
                        if 'choices' in json_data:
                            delta = json_data['choices'][0].get('delta', {})
                            if 'content' in delta:
                                full_response += delta['content']
                                yield full_response
                    except json.JSONDecodeError:
                        continue
        
        return full_response
        
    except requests.exceptions.Timeout:
        raise Exception("Request timeout: API took too long to respond")
    except requests.exceptions.ConnectionError:
        raise Exception("Connection error: Unable to reach OpenRouter API")
    except Exception as e:
        raise e

def save_conversation(name: str, messages: List[Dict]) -> Path:
    """Save conversation to JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.json"
    filepath = CONVERSATIONS_DIR / filename
    
    with open(filepath, 'w') as f:
        json.dump({
            "name": name,
            "timestamp": timestamp,
            "messages": messages
        }, f, indent=2)
    return filepath

def load_conversations() -> List[Dict]:
    """Load all saved conversations"""
    conversations = []
    for file in sorted(CONVERSATIONS_DIR.glob("*.json"), reverse=True):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                conversations.append({
                    "file": file.name,
                    "name": data.get("name", "Untitled"),
                    "timestamp": data.get("timestamp", "Unknown"),
                    "message_count": len(data.get("messages", []))
                })
        except json.JSONDecodeError:
            continue
    return conversations

def load_conversation_by_file(filename: str) -> Optional[List[Dict]]:
    """Load specific conversation by filename"""
    filepath = CONVERSATIONS_DIR / filename
    if filepath.exists():
        try:
            with open(filepath, 'r') as f:
                return json.load(f).get("messages", [])
        except json.JSONDecodeError:
            st.error("❌ Failed to load conversation")
    return None

def export_chat_as_markdown(messages: List[Dict]) -> str:
    """Export chat history as markdown"""
    md = "# Chat History\n\n"
    md += f"*Exported on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    
    for msg in messages:
        role = "🧑" if msg["role"] == "user" else "🤖"
        md += f"### {role} {msg['role'].title()}\n\n"
        md += f"{msg['content']}\n\n"
        md += "---\n\n"
    
    return md

# ==================== SESSION STATE INITIALIZATION ====================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "anthropic/claude-3.5-sonnet"

if "conversation_name" not in st.session_state:
    st.session_state.conversation_name = f"Chat_{datetime.now().strftime('%H%M%S')}"

# ==================== SIDEBAR ====================

with st.sidebar:
    # Header
    st.markdown("### 🎛️ Control Panel")
    st.divider()
    
    # API Status
    api_valid = validate_api_key()
    if api_valid:
        st.markdown('<span class="status-connected">✅ OpenRouter Connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-disconnected">❌ API Key Missing</span>', unsafe_allow_html=True)
        st.error("⚠️ Add your OpenRouter API key to .env file")
    
    st.divider()
    
    # Chat Settings
    st.markdown("### ⚙️ Chat Settings")
    
    model_display = st.selectbox(
        "AI Model",
        list(AVAILABLE_MODELS.keys()),
        index=0,
        help="Choose the AI model for responses"
    )
    st.session_state.selected_model = AVAILABLE_MODELS[model_display]
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher = more creative, Lower = more focused"
    )
    
    st.divider()
    
    # Chat Management
    st.markdown("### 💾 Manage Conversations")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.success("Chat cleared!")
            st.rerun()
    
    with col2:
        if st.button("💾 Save Chat", use_container_width=True):
            if st.session_state.messages:
                save_conversation(st.session_state.conversation_name, st.session_state.messages)
                st.success("✅ Conversation saved!")
            else:
                st.warning("No messages to save")
    
    st.divider()
    
    # Load Previous Conversations
    st.markdown("### 📂 Previous Chats")
    conversations = load_conversations()
    
    if conversations:
        for conv in conversations[:5]:
            with st.expander(f"📌 {conv['name'][:20]}... ({conv['message_count']} msgs)"):
                st.caption(f"Saved: {conv['timestamp']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"📂 Load", key=f"load_{conv['file']}"):
                        loaded = load_conversation_by_file(conv['file'])
                        if loaded:
                            st.session_state.messages = loaded
                            st.success("Conversation loaded!")
                            st.rerun()
                
                with col2:
                    if st.button(f"📥 Export", key=f"export_{conv['file']}"):
                        loaded = load_conversation_by_file(conv['file'])
                        if loaded:
                            markdown_content = export_chat_as_markdown(loaded)
                            st.download_button(
                                label="Download MD",
                                data=markdown_content,
                                file_name=f"{conv['name']}.md",
                                mime="text/markdown"
                            )
    else:
        st.caption("No saved conversations yet")
    
    st.divider()
    
    # Statistics
    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{len(st.session_state.messages)}</div>
            <div class="stat-label">Messages</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        user_messages = sum(1 for m in st.session_state.messages if m["role"] == "user")
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{user_messages}</div>
            <div class="stat-label">Your Queries</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Footer
    st.markdown("""
    ---
    <div style="text-align: center; color: #8b949e; font-size: 12px;">
        <p>🚀 IntelliChat v2.0</p>
        <p>Powered by OpenRouter</p>
        <p>By: Udit Singh</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN CONTENT ====================

# Title
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.markdown("# 🤖 IntelliChat")
    st.markdown('<p class="subtitle">Your intelligent AI assistant powered by OpenRouter</p>', unsafe_allow_html=True)

# Display chat history
if st.session_state.messages:
    st.markdown("---")
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(f'<div class="chat-user">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-assistant">{message["content"]}</div>', unsafe_allow_html=True)
            
            # Message Actions
            col1, col2, col3 = st.columns([0.2, 0.2, 0.6])
            with col1:
                if st.button("📋 Copy", key=f"copy_{idx}", help="Copy to clipboard"):
                    st.write(f"`{message['content']}`")
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{idx}", help="Delete this message"):
                    st.session_state.messages.pop(idx)
                    st.rerun()

st.divider()

# Chat Input
if prompt := st.chat_input("Type your message here... 💬"):
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(f'<div class="chat-user">{prompt}</div>', unsafe_allow_html=True)
    
    # Get AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            if not validate_api_key():
                raise Exception("API key not configured. Please add OPENROUTER_API_KEY to .env")
            
            # Prepare messages for API
            api_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            
            # Limit context window
            if len(api_messages) > MAX_CHAT_HISTORY:
                api_messages = api_messages[-MAX_CHAT_HISTORY:]
            
            with st.spinner("🤔 Thinking..."):
                # Stream response
                for response_chunk in call_openrouter_api(
                    api_messages,
                    st.session_state.selected_model,
                    temperature
                ):
                    full_response = response_chunk
                    message_placeholder.markdown(
                        f'<div class="chat-assistant">{full_response}▌</div>',
                        unsafe_allow_html=True
                    )
        
        except Exception as e:
            error_msg = str(e)
            full_response = f"""
❌ **Error Occurred**

```
{error_msg}
```

💡 **Solutions:**
- Check your internet connection
- Verify API key in .env file is correct
- Make sure it starts with: `sk-or-`
- Visit: https://openrouter.io/keys to check your key
            """
            st.error(full_response)
        
        finally:
            # Display final response
            message_placeholder.markdown(
                f'<div class="chat-assistant">{full_response}</div>',
                unsafe_allow_html=True
            )
        
        # Save assistant response
        if full_response:
            st.session_state.messages.append({"role": "assistant", "content": full_response})
