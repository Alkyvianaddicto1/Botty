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
    r"mercury|moons": "No, Mercury has no moons.",
    r"does mars have moons": "Yes, Mars has two small moons named Phobos and Deimos.",
    r"earth|moons": "Earth has one natural moon.",
    r"jupiter|moons": "Yes, Jupiter has many moons including the large Galilean moons.",
    r"saturn|moons": "Yes, Saturn has many moons including Titan.",
    r"uranus|moons": "Yes, Uranus has over 20 known moons.",
    r"neptune|moons": "Yes, Neptune has several moons, the largest being Triton.",
    r"mars|red": "Mars appears red because of iron oxide, or rust, covering its surface.",
    r"saturn|rings": "Saturn’s rings are made of ice and rock particles held in orbit by gravity.",
    r"planetary|rings": "Planetary rings are bands of dust, ice, and rock orbiting a planet.",
    r"planets|rings": "Jupiter, Saturn, Uranus, and Neptune all have rings.",
    r"uranus|tilted": "Uranus is tilted likely due to a collision with a large object long ago.",
    r"solar|system": "A solar system is a star and all the objects that orbit it, including planets.",
    r"star|orbit": "Our solar system orbits the Sun.",

}

# The personality/instruction for the AI
SYSTEM_PROMPT="""

You are Zfluffy Spicy AI, a helpful and witty assistant. 
GUIDELINES:
1. Use **Markdown** for emphasis, headers, and bullet points.
2. Use **Tables** to organize data or comparisons.
3. Use **LaTeX** for any mathematical formulas or scientific variables. 
   - Use $inline$ for small formulas.
   - Use $$display$$ for standalone equations.
4. If you don't know an answer, suggest the user contact support.

"""