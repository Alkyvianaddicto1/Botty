import streamlit as st
import re
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Environment Setup (from your bot.py logic)
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("API Key not found! Please check your .env file.")
    st.stop()

client = OpenAI(api_key=api_key)

# 2. Your Rule-Based Logic (Directly from bot.py)
def get_rule_based_response(user_input):
    user_input = user_input.lower()
    rules = {
        r"hi|hello|hey": "Hello! How can I help you today?",
        r"status|order": "You can check your order status at /account/orders.",
        r"hours|time": "We are open Monday-Friday, 9 AM to 6 PM.",
        r"bye|goodbye": "Goodbye! Have a great day!",

        r"shipping": "Standard shipping takes 3-5 business days.",

        r"location|address|office": "Our main office is located at 123 Tech Lane, NY.",

        r"price|cost|how much": "Our subscription plans start at $10/month.",

        r"human|agent|support": "I'm connecting you to a live agent. Please wait..."
    }
    for pattern, response in rules.items():
        if re.search(pattern, user_input):
            return response
    return None

# 3. Streamlit UI Layout
st.set_page_config(page_title="Hybrid Chatbot", page_icon="🤖")
st.title("🤖 My Hybrid AI Bot")
st.caption("Using Rules + GPT-4o")

# Initialize chat history (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant" }
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Input & Processing
if prompt := st.chat_input("Ask me about orders, hours, or anything else!"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # First: Try your Rule-Based Logic
        rule_response = get_rule_based_response(prompt)
        
        if rule_response:
            full_response = f"📌 [Rule Match]: {rule_response}"
            st.markdown(full_response)
        else:
            # Second: Try AI Fallback
            try:
                # We send the whole history so the AI has "memory"
                stream = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."}
                    ] + [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                full_response = st.write_stream(stream)
            except Exception as e:
                full_response = f"I'm having trouble connecting to my brain. Error: {e}"
                st.error(full_response)

    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})