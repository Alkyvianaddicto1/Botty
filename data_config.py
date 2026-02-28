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
    r"what galaxy are we in": "Our solar system is in the Milky Way galaxy.",
    r"how old are planets": "Most planets in our solar system formed about 4.5 billion years ago.",
    r"why do planets spin": "Planets spin because of the momentum from the rotating cloud of gas and dust they formed from.",
    r"why do planets orbit": "Planets orbit because gravity pulls them toward the Sun while their motion keeps them moving.",
    r"what is planet axis": "A planet’s axis is an imaginary line it spins around.",
    r"what causes seasons": "Seasons are caused by a planet’s tilt as it orbits the Sun.",
    r"does mars have seasons": "Yes, Mars has seasons because it is tilted like Earth.",
    r"does jupiter have solid ground": "No, Jupiter is mostly gas and does not have a solid surface like Earth.",
    r"can you stand on saturn": "No, Saturn is a gas giant and does not have a solid surface.",
    r"can humans live on mars": "Humans cannot currently live on Mars without special equipment, but scientists are researching it.",
    r"can humans live on venus": "Venus is too hot and has toxic clouds, making it extremely difficult for humans to live there.",
    r"what is planet gravity": "Planetary gravity is the force that pulls objects toward a planet’s center.",
    r"which planet has strongest gravity": "Jupiter has the strongest gravity of all the planets.",
    r"which planet has weakest gravity": "Mercury has one of the weakest gravities among the planets.",
    r"what is escape velocity": "Escape velocity is the speed needed to break free from a planet’s gravity.",
    r"why is earth special": "Earth is special because it has liquid water, oxygen, and conditions suitable for life.",
    r"what is atmosphere made of": "An atmosphere can contain gases like nitrogen, oxygen, carbon dioxide, and others.",
    r"which planet has thickest atmosphere": "Venus has the thickest atmosphere among terrestrial planets.",
    r"which planet has strongest winds": "Neptune has the fastest winds in the solar system.",
    r"does it rain on other planets": "Yes, but not always water. Some planets have methane or acid rain.",
    r"does it rain diamonds": "Scientists think it may rain diamonds on Neptune and Uranus due to high pressure.",
    r"what is a day on mars": "A day on Mars is about 24.6 hours.",
    r"what is a day on jupiter": "A day on Jupiter lasts about 10 hours.",
    r"what is a year on mercury": "A year on Mercury is about 88 Earth days.",
    r"what is a year on neptune": "A year on Neptune lasts about 165 Earth years.",
    r"what planet spins backward": "Venus spins backward compared to most planets.",
    r"why does venus spin backward": "Scientists think a collision or gravitational effects may have reversed Venus’s rotation.",
    r"what is planet core": "A planet’s core is its central region, often made of metal or rock.",
    r"what is mantle": "The mantle is the thick layer between a planet’s core and crust.",
    r"what is crust": "The crust is the outermost layer of a rocky planet.",
    r"which planets are rocky": "Mercury, Venus, Earth, and Mars are rocky planets.",
    r"which planets are gas": "Jupiter and Saturn are gas giants.",
    r"which planets are ice": "Uranus and Neptune are ice giants.",
    r"why are gas giants big": "Gas giants grew large because they captured massive amounts of gas during formation.",
    r"can planets collide": "Yes, planets can collide, especially during early solar system formation.",
    r"have planets collided before": "Yes, scientists believe Earth’s Moon formed after a giant collision.",
    r"what is asteroid": "An asteroid is a rocky object orbiting the Sun, smaller than a planet.",
    r"what is comet": "A comet is an icy object that forms a glowing tail when near the Sun.",
    r"what is meteoroid": "A meteoroid is a small rock traveling through space.",
    r"what is meteor": "A meteor is a meteoroid burning up in Earth’s atmosphere.",
    r"what is meteorite": "A meteorite is a meteoroid that reaches the ground.",
    r"what is exoplanet": "An exoplanet is a planet outside our solar system.",
    r"how many exoplanets": "Scientists have discovered thousands of exoplanets beyond our solar system.",
    r"can exoplanets have life": "Some exoplanets may have conditions suitable for life, but none are confirmed yet.",
    r"what is habitable zone": "The habitable zone is the region around a star where liquid water could exist.",
    r"which planet is in habitable zone": "Earth lies in the Sun’s habitable zone.",
    r"does mars have water": "Mars has frozen water and evidence that liquid water existed in the past.",


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