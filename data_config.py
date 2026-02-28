# data_config.py

# Your Rule-Based Logic patterns
BOT_RULES = {
    r"hi|hello|hey": "Hello! How can I help you today?",
    r"status|order": "You can check your order status at /account/orders.",
    r"hours|time": "We are open Monday-Friday, 9 AM to 6 PM.",
    r"bye|goodbye": "Goodbye! Have a great day!",
    r"shipping": "Standard shipping takes 3-5 business days.",
    r"location|address|office": "Our main office is located at 123 Tech Lane, NY.",
    r"price|cost|how much": "Our subscription plans start at $10/month.",
    r"human|agent|support": "I'm connecting you to a live agent. Please wait...",
    r"planet|venus": "Venus is the second planet from the Sun and the hottest planet due to its thick atmosphere.",
    r"planet|earth": "Earth is the third planet from the Sun and the only known world that supports life.",
    r"planet|mars": "Mars is the fourth planet from the Sun and is known as the Red Planet.",
    r"planet|jupiter": "Jupiter is the largest planet and a gas giant with a massive storm called the Great Red Spot.",
    r"planet|saturn": "Saturn is a gas giant famous for its bright ring system.",
    r"planet|uranus": "Uranus is an ice giant that rotates on its side.",
    r"planet|neptune": "Neptune is the farthest planet from the Sun and has very strong winds.",
    r"mercury|hot": "Mercury is hot because it is very close to the Sun and has almost no atmosphere.",
    r"mercury|cold": "Mercury also gets very cold because it lacks an atmosphere to trap heat.",
    r"venus|moons": "No, Venus does not have any moons.",
    r"mercury|moons": "No, Mercury has no moons."
}

# The personality/instruction for the AI
SYSTEM_PROMPT = "You are a helpful assistant. If you don't know an answer, suggest the user contacts support."