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

# Initialize chat history (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

with st.sidebar:
    st.header("⚙️ Settings")

    personality = st.selectbox(
        "Bot Personality: ",
        ("Professional", "Witty & Spicy", "Sarcastic", "Friendly"),
        index = 1
    )
    model_choice = st.radio(
        "Choose your AI brain: ",
        ("Open AI (GPT-4o)", "Google Gemini (Free Tier)"),
        index=0 if api_key else 1
    )

    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.toast("Chat history cleared!", icon="🧹")
        st.rerun()

    # --- NEW: REGENERATE BUTTON ---
    if len(st.session_state.messages) > 1:
        if st.button("🔄 Regenerate Last Response", use_container_width=True):
            # Remove the last assistant response
            if st.session_state.messages[-1]["role"] == "assistant":
                st.session_state.messages.pop()
                st.rerun()

    st.divider()
    
    st.subheader("📊 Session Stats")
    msg_count = len([m for m in st.session_state.messages if m["role"] != "system"])
    st.write(f"Messages this session: **{msg_count}**")
    
    st.subheader("📥 Export Data")
    chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" 
                          for m in st.session_state.messages if m['role'] != 'system'])
    
    st.download_button(
        label="Download Conversation (.txt)",
        data=chat_text,
        file_name="zfluffy_chat_history.txt",
        mime="text/plain",
        use_container_width=True
    )

# Display chat history
for i, message in enumerate(st.session_state.messages):
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # --- NEW: EDIT LAST USER MESSAGE ---
            # If it's the most recent user message, allow editing
            if message["role"] == "user" and i == len(st.session_state.messages) - 2:
                if st.button("✏️ Edit", key=f"edit_{i}"):
                    # Remove this user message and the following assistant message
                    st.session_state.messages = st.session_state.messages[:i]
                    st.rerun()

# 4. Chat Input & Processing
if prompt := st.chat_input("Ask me about orders, hours, or anything else!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Zfluffy is thinking..."):
            rule_response = get_rule_based_response(prompt)
        
            if rule_response:
                full_response = f"📌 [Rule Match]: {rule_response}"
                st.markdown(full_response)
            else:
                try:
                    # --- NEW: CONTEXT WINDOW MANAGEMENT ---
                    # We always include the System Prompt (index 0) 
                    # plus the last 10 messages to save tokens.
                    system_msg = [st.session_state.messages[0]]
                    recent_history = st.session_state.messages[-10:]
                    
                    # Merge them so the AI always knows its instructions
                    context_messages = system_msg + [m for m in recent_history if m["role"] != "system"]

                    if model_choice == "Open AI (GPT-4o)":
                        stream = openai_client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=context_messages, # Using the limited context
                            stream=True,
                        )
                        full_response = st.write_stream(stream)
                    else:
                        # For Gemini, we pass the limited context history
                        gemini_history = []
                        for m in context_messages[:-1]: # Exclude the current prompt
                            if m["role"] != "system":
                                role = "user" if m["role"] == "user" else "model"
                                gemini_history.append({"role": role, "parts": [m["content"]]})
                        
                        # Start chat with the sliding window history
                        chat = gemini_client.chats.create(
                            model="gemini-1.5-flash",
                            history=gemini_history,
                            config={"system_instruction": SYSTEM_PROMPT}
                        )
                        response = chat.send_message(prompt)
                        full_response = response.text
                        st.markdown(full_response)

                except Exception as e:
                    # ... (Exception handling remains the same)
                    if "insufficient_quota" in str(e).lower():
                        full_response = "🚫 **System Note:** OpenAI credits are empty. Switch to Gemini!"
                    else:
                        full_response = f"Error: {e}"
                    st.error(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()