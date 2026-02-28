import streamlit as st
import re
import os
from openai import OpenAI
from google import genai  # Updated import to the new library
from dotenv import load_dotenv

from data_config import BOT_RULES, SYSTEM_PROMPT

# 1. Environment Setup
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")
google_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini with the new Client structure
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

with st.sidebar:
    st.header("Settings")
    model_choice = st.radio(
        "Choose your AI brain: ",
        ("Open AI (GPT-4o)", "Google Gemini (Free Tier)"),
        index=0 if api_key else 1
    )

    if st.button("Clear Chat History"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.toast("Chat history cleared!", icon="🧹")
        st.rerun()

# Initialize chat history (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

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
        with st.spinner("Zfluffy is thinking ..."):
            rule_response = get_rule_based_response(prompt)
        
        if rule_response:
            full_response = f"📌 [Rule Match]: {rule_response}"
            st.markdown(full_response)
        else:
            try:
                # OPTION A: OpenAI Brain
                if model_choice == "Open AI (GPT-4o)":
                    stream = openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=st.session_state.messages,
                        stream=True,
                    )
                    full_response = st.write_stream(stream)
                
                # OPTION B: Gemini Brain (Using the new library methods)
                else:
                    # The new library simplifies chat history management
                    response = gemini_client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=prompt,
                        config={
                            "system_instruction": SYSTEM_PROMPT
                        }
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