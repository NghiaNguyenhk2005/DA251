# file: clues_data.py

# Dữ liệu game
clues = [
    # ======================================================
    # LUST CASE 
    # ======================================================
    {
        "name": "Lust Victim",
        "description": "Male, approx. 40 years old, died from cyanide poisoning.",
        "unlocked": False
    },
    {
        "name": "Lust Witness",
        "description": "Female, approx. 35 years old",
        "unlocked": False
    },
    {
        "name": "Witness Sighting",
        "description": "A black sedan was parked outside for hours.",
        "unlocked": False
    },
    # ======================================================
    # WRATH CASE 
    # ======================================================
    {
        "name": "Dojo Rivalry",
        "description": "The victim had a fierce rivalry with a neighboring dojo master.",
        "unlocked": False
    },
    # ======================================================
    # ENVY CASE 
    # ======================================================
    {
        "name": "Stolen Role",
        "description": "The suspect believes the victim stole her lead role in the play.",
        "unlocked": False
    }
]

# Hàm này dùng để reset lại từ đầu khi bạn muốn test lại game
def reset_clues():
    for clue in clues:
        clue["unlocked"] = False
    print("🔄 All clues have been locked.")