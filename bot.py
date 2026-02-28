import streamlit as st
import re
import os
from openai import OpenAI
from google import genai 
from dotenv import load_dotenv

from data_config import BOT_RULES, SYSTEM_PROMPT

# 1. Environment Setup
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")
google_key = os.getenv("GOOGLE_API_KEY")

if google_key:
    gemini_client = genai.Client(api_key=google_key)

if not api_key:
    st.error("API Key not found! Please check your .env file.")
    st.stop()

openai_client = OpenAI(api_key=api_key)

# 2. Rule-Based Logic
def get_rule_based_response(user_input):
    user_input = user_input.lower()
    for pattern, response in BOT_RULES.items():
        if re.search(pattern, user_input):
            return response
    return None

# 3. Streamlit UI Layout
st.set_page_config(page_title="Hybrid Chatbot", page_icon="🤖")
st.title("🤖 Zfluffy Spicy AI")

# Initialize chat history (Memory) early so sidebar can access it
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# --- UPDATED SIDEBAR FEATURES ---
with st.sidebar:
    st.header("⚙️ Settings")
    model_choice = st.radio(
        "Choose your AI brain: ",
        ("Open AI (GPT-4o)", "Google Gemini (Free Tier)"),
        index=0 if api_key else 1
    )

    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.toast("Chat history cleared!", icon="🧹") # Clear Chat Toast
        st.rerun()

    st.divider()
    
    # Feature: Sidebar Chat Statistics
    st.subheader("📊 Session Stats")
    # Count messages excluding the system prompt
    msg_count = len([m for m in st.session_state.messages if m["role"] != "system"])
    st.write(f"Messages this session: **{msg_count}**")
    
    # Feature: Advanced Data Export
    st.subheader("📥 Export Data")
    # Prepare chat history for download
    chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" 
                          for m in st.session_state.messages if m['role'] != 'system'])
    
    st.download_button(
        label="Download Conversation (.txt)",
        data=chat_text,
        file_name="zfluffy_chat_history.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.divider()
    st.subheader("💡 About")
    st.caption("Zfluffy uses a hybrid system: local rules for speed and AI for complex logic.")

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. Chat Input & Processing
if prompt := st.chat_input("Ask me about orders, hours, or anything else!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Feature: Spinner for "Thinking" state
        with st.spinner("Zfluffy is thinking..."):
            rule_response = get_rule_based_response(prompt)
        
            if rule_response:
                full_response = f"📌 [Rule Match]: {rule_response}"
                st.markdown(full_response)
            else:
                try:
                    if model_choice == "Open AI (GPT-4o)":
                        stream = openai_client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=st.session_state.messages,
                            stream=True,
                        )
                        full_response = st.write_stream(stream)
                    else:
                        response = gemini_client.models.generate_content(
                            model="gemini-1.5-flash",
                            contents=prompt,
                            config={"system_instruction": SYSTEM_PROMPT}
                        )
                        full_response = response.text
                        st.markdown(full_response)

                except Exception as e:
                    if "insufficient_quota" in str(e).lower():
                        full_response = "🚫 **System Note:** OpenAI credits are empty. Switch to Gemini in the sidebar!"
                    else:
                        full_response = f"Error connecting to brain: {e}"
                    st.error(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

    st.rerun()