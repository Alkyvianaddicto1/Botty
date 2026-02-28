import streamlit as st
import re
import os
import fitz
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

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in doc])
        return text
    elif uploaded_file.type == "text/plain":
        return str(uploaded_file.read(), "utf-8")
    return ""

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

    st.header("📄 Document Analysis")
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])
    
    doc_context = ""
    if uploaded_file:
        with st.spinner("Reading document..."):
            doc_context = extract_text_from_file(uploaded_file)
            st.success(f"Loaded: {uploaded_file.name}")

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

if "feedback" not in st.session_state:
    st.session_state.feedback = {}

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

            if message ["role"] == "assistant":
                col1, col2, col3 = st.columns([0.1, 0.1, 0.8])

                with col1:
                    if st.button("👍", key=f"up_{i}"):
                        st.session_state.feedback[i] = "Positive"
                        st.toast("Thanks for the feedback!", icon="💖")
                
                with col2:
                    if st.button("👎", key=f"down_{i}"):
                        st.session_state.feedback[i] = "Negative"
                        st.toast("Thanks for letting me know. I'll try to improve!", icon="🔧")
                
                # Show saved feedback status if it exists
                if i in st.session_state.feedback:
                    status = st.session_state.feedback[i]
                    st.caption(f"Rated: {status}")

# These pills give users quick access to your rule-based logic
if "chat_summary" not in st.session_state:
    st.session_state.chat_summary = ""

def compress_memory(history, model_choice):
    """Generates a 2-sentence summary of the conversation if it gets too long."""
    # Only compress if history is long (e.g., more than 15 messages)
    if len(history) < 15:
        return st.session_state.chat_summary
    
    summary_instruction = f"Summarize the key points of this conversation so far in 2 sentences. Previous summary: {st.session_state.chat_summary}"
    
    try:
        if model_choice == "Open AI (GPT-4o)":
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=history + [{"role": "system", "content": summary_instruction}],
                max_tokens=100
            )
            return response.choices[0].message.content
        else:
            response = gemini_client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"History: {history}. {summary_instruction}"
            )
            return response.text
    except:
        return st.session_state.chat_summary

# --- 1. FUNCTION TO GENERATE DYNAMIC SUGGESTIONS ---
def get_dynamic_suggestions(history, model_choice):
    """Generates 3 short follow-up buttons based on context."""
    if len(history) <= 1:
        return ["Shipping Info", "Office Location", "Support"]
    
    suggestion_instruction = "Provide 3 very short (1-3 words) follow-up questions. Format: Item 1, Item 2, Item 3"
    
    try:
        if model_choice == "Open AI (GPT-4o)":
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=history + [{"role": "system", "content": suggestion_instruction}],
                max_tokens=50
            )
            raw = response.choices[0].message.content
        else:
            response = gemini_client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"History: {history}. {suggestion_instruction}"
            )
            raw = response.text
        return [s.strip() for s in raw.split(",")]
    except:
        return ["Shipping Info", "Office Location", "Support"]

# --- 2. DISPLAY DYNAMIC SUGGESTIONS ---
st.write("✨ **Suggested next steps:**")
current_suggestions = get_dynamic_suggestions(st.session_state.messages, model_choice)

cols = st.columns(len(current_suggestions))
suggestion_prompt = None

for i, suggestion in enumerate(current_suggestions):
    with cols[i]:
        if st.button(suggestion, key=f"suggest_{i}_{len(st.session_state.messages)}", use_container_width=True):
            suggestion_prompt = suggestion

# --- 3. UPDATED CHAT INPUT LOGIC ---
if prompt := (st.chat_input("Ask me anything...") or suggestion_prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Zfluffy is thinking..."):
            rule_response = get_rule_based_response(prompt)

            # 1. Handle Memory Compression
            if len(st.session_state.messages) > 15:
                st.session_state.chat_summary = compress_memory(st.session_state.messages, model_choice)

            # 2. Build ONE Consolidated System Prompt (The "Master Instruction")
            doc_info = f"\n\n[DOCUMENT CONTEXT]:\n{doc_context[:5000]}" if doc_context else ""
            summary_info = f"\n\n[CONVERSATION SUMMARY]: {st.session_state.chat_summary}" if st.session_state.chat_summary else ""
            
            master_system_prompt = (
                f"{SYSTEM_PROMPT} "
                f"Your current tone is: {personality}. "
                f"{summary_info}"
                f"{doc_info}"
            )
        
            if rule_response:
                full_response = f"📌 [Rule Match]: {rule_response}"
                st.markdown(full_response)
            else:
                try:
                    # Context Window Management
                    # We create a temporary message list just for this API call
                    recent_history = st.session_state.messages[-10:]
                    # Replace the old system prompt with our new Master Prompt
                    context_messages = [{"role": "system", "content": master_system_prompt}] + \
                                       [m for m in recent_history if m["role"] != "system"]

                    if model_choice == "Open AI (GPT-4o)":
                        stream = openai_client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=context_messages, # Now contains Summary + PDF + Personality
                            stream=True,
                        )
                        full_response = st.write_stream(stream)
                    
                    else:
                        # Gemini Streaming
                        gemini_history = []
                        for m in context_messages[:-1]:
                            if m["role"] != "system":
                                role = "user" if m["role"] == "user" else "model"
                                gemini_history.append({"role": role, "parts": [m["content"]]})
                        
                        response = gemini_client.models.generate_content(
                            model="gemini-1.5-flash",
                            contents=prompt,
                            config={"system_instruction": master_system_prompt}, # Fixed
                            stream=True
                        )
                        full_response = st.write_stream(chunk.text for chunk in response)

                except Exception as e:
                    # ... (keep your existing error handling)
                    if "insufficient_quota" in str(e).lower():
                        full_response = "🚫 **System Note:** OpenAI credits are empty. Switch to Gemini!"
                    else:
                        full_response = f"Error: {e}"
                    st.error(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()