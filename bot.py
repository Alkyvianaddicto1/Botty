import re
import os
from openai import OpenAI
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')

load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("PI Key not found! Check your .env file.")

client = OpenAI(api_key=api_key)

def get_rule_based_response(user_input):
    """Checks for specific patterns using Regular Expressions."""
    user_input = user_input.lower()
    
    rules = {
        r"hi|hello|hey": "Hello! How can I help you today?",
        r"status|order": "You can check your order status at /account/orders.",
        r"hours|time": "We are open Monday-Friday, 9 AM to 6 PM.",
        r"bye|goodbye": "Goodbye! Have a great day!"
    }
    
    for pattern, response in rules.items():
        if re.search(pattern, user_input):
            return response
    return None

def get_ai_response(user_input):
    """Fallback to AI API if no rules match."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I'm having trouble connecting to my brain. Error: {e}"

def chatbot():
    print("Bot: Hi! I'm your hybrid assistant. Type 'exit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        # First: Try Rules
        response = get_rule_based_response(user_input)
        
        # Second: Try AI (if no rule matched)
        if not response:
            print("Bot: (Thinking with AI...)")
            response = get_ai_response(user_input)
            
        print(f"Bot: {response}")

if __name__ == "__main__":
    chatbot()