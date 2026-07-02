import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY not found in .env file")
    st.stop()

# Gemini client
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="Gemini AI Chatbot", page_icon="🤖")
st.title("🤖 Gemini AI Chatbot")

# ================= Welcome =================
st.success("""
👋 Welcome to Gemini AI Chatbot!

I'm your AI assistant 🚀
Ask me anything below
""")

# ================= Session State =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= Sidebar Settings =================
st.sidebar.title("⚙️ Settings")

language = st.sidebar.selectbox(
    "🌍 Language",
    ["English", "Urdu", "Roman Urdu", "Pashto"]
)

model_name = st.sidebar.selectbox(
    "🤖 AI Model",
    ["gemini-2.5-flash", "gemini-2.5-pro"]
)

theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])

ai_tone = st.sidebar.selectbox(
    "😊 AI Tone",
    ["Friendly", "Professional", "Teacher"]
)

response_length = st.sidebar.selectbox(
    "📏 Response Length",
    ["Short", "Medium", "Long"]
)

# ================= Dark Theme =================
if theme == "Dark":
    st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# ================= Download Chat =================
chat = ""
for role, msg in st.session_state.messages:
    chat += f"{role}: {msg}\n\n"

st.sidebar.download_button(
    "📥 Download Chat",
    chat,
    file_name="chat.txt"
)

# ================= Show Chat =================
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)

# ================= Input =================
prompt = st.chat_input("Type your message...")

if prompt:

    # Save user message
    st.session_state.messages.append(("user", prompt))

    # Show user message immediately
    with st.chat_message("user"):
        st.write(prompt)

    try:
        system_prompt = f"""
You are a helpful AI assistant.

Language: {language}
Tone: {ai_tone}
Length: {response_length}

User:
{prompt}
"""

        response = client.models.generate_content(
            model=model_name,
            contents=system_prompt
        )

        answer = response.text

        # Save AI response
        st.session_state.messages.append(("assistant", answer))

        # Show AI response
        with st.chat_message("assistant"):
            st.write(answer)

    except Exception as e:
        st.error(f"Error: {e}")