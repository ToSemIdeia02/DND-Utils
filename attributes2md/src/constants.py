# constants.py

# Standard array values for testing
STANDARD_ARRAY = [15, 14, 13, 12, 10, 8]  # Standard array as per D&D 5e  

# Skill mapping for checkboxes
SKILL_MAPPING = {
    "Acrobatics": "DEX", "Animal Handling": "WIS", "Arcana": "INT",
    "Athletics": "STR", "Deception": "CHA", "History": "INT", 
    "Insight": "WIS", "Intimidation": "CHA", "Investigation": "INT",
    "Medicine": "WIS", "Nature": "INT", "Perception": "WIS",
    "Performance": "CHA", "Persuasion": "CHA", "Religion": "INT",
    "Sleight of Hand": "DEX", "Stealth": "DEX", "Survival": "WIS"
}

# Define the list of attribute keys for navigation
ATTRIBUTE_KEYS = ["-STR-", "-DEX-", "-CON-", "-INT-", "-WIS-", "-CHA-"]

# Official XP progression for D&D 5e
XP_PROGRESSION = {
    1: 0,
    2: 300,
    3: 900,
    4: 2700,
    5: 6500,
    6: 14000,
    7: 23000,
    8: 34000,
    9: 48000,
    10: 64000,
    11: 85000,
    12: 100000,
    13: 120000,
    14: 140000,
    15: 165000,
    16: 195000,
    17: 225000,
    18: 265000,
    19: 305000,
    20: 355000,
}