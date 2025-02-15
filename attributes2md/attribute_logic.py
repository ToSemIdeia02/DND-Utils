def calculate_modifier(value):
    """Calculate the D&D 5e modifier based on the attribute value."""
    return (value - 10) // 2

def update_attribute_table(attribute_values, proficiencies, proficiency_bonus=2):
    """Generate the updated Attributes table with proficiency bonuses."""
    updated_table = []
    updated_table.append("| Attribute    | Value | Modifier |\n")
    updated_table.append("| ------------ | ----- | -------- |\n")
    
    for attr, value in attribute_values.items():
        modifier = calculate_modifier(value)
        modifier_str = f"{modifier:+d}"  # Format as signed integer
        
        # Check if the attribute has proficiency
        if proficiencies.get(attr, False):  # If proficiency is True
            final_modifier = modifier + proficiency_bonus
            modifier_str += f" + PB ({final_modifier:+d})"
        
        updated_table.append(f"| {attr:<12} | {value:^5} | {modifier_str:<8} |\n")
    
    return ''.join(updated_table)

def update_skills_table(attribute_values, proficiencies, proficiency_bonus=2, skill_checkboxes=None):
    """Generate the updated Skills table with proficiency and expertise bonuses."""
    # Map skills to their corresponding attributes
    skill_mapping = {
        "Acrobatics": "DEX", "Animal Handling": "WIS", "Arcana": "INT",
        "Athletics": "STR", "Deception": "CHA", "History": "INT",
        "Insight": "WIS", "Intimidation": "CHA", "Investigation": "INT",
        "Medicine": "WIS", "Nature": "INT", "Perception": "WIS",
        "Performance": "CHA", "Persuasion": "CHA", "Religion": "INT",
        "Sleight of Hand": "DEX", "Stealth": "DEX", "Survival": "WIS"
    }
    
    # Calculate modifiers for each attribute
    attribute_modifiers = {attr[:3].upper(): calculate_modifier(value) for attr, value in attribute_values.items()}
    
    updated_table = []
    updated_table.append("| Skill            | Value | Modifier |\n")
    updated_table.append("| ---------------- | ----- | -------- |\n")
    
    for skill, mod_attr in skill_mapping.items():
        base_modifier = attribute_modifiers.get(mod_attr, 0)
        final_modifier = base_modifier
        
        # Check if the skill has proficiency or expertise
        if skill_checkboxes:
            if skill_checkboxes.get(f"-PROF-{skill}-", False):  # Proficiency
                final_modifier += proficiency_bonus
            elif skill_checkboxes.get(f"-EXPERT-{skill}-", False):  # Expertise
                final_modifier += 2 * proficiency_bonus
        
        updated_table.append(f"| {skill:<16} | {final_modifier:+d} | {mod_attr:^8} |\n")
    
    return ''.join(updated_table)

def calculate_spell_stats(attribute_values, casting_stat, proficiency_bonus):
    """
    Calculate spell-related stats (Spell Save DC, Spell Attack Modifier, Spells Known).
    <button class="citation-flag" data-index="3">
    """
    # Calculate the casting stat modifier
    casting_mod = (attribute_values[casting_stat] - 10) // 2  # Casting stat modifier
    
    # Calculate Spell Save DC and Spell Attack Modifier
    spell_save_dc = 8 + proficiency_bonus + casting_mod
    spell_attack_mod = proficiency_bonus + casting_mod
    spells_known = 3 + proficiency_bonus  # Example logic for spells known
    
    # Return the formatted spell stats
    spell_stats = f"""> [!infobox]+ Collapsible Infobox
> # Spell mods
> ###### Stats
> | Type              | Stat |
> | ------------------| ---- |
> | Spell Save DC     | {spell_save_dc} |
> | Spell Attack Mod  | {spell_attack_mod} |
> | Spell Amount      | {spells_known} |
"""
    return spell_stats

def calculate_proficiency_bonus(level):
    """Calculate proficiency bonus based on character level."""
    if level < 1:
        raise ValueError("Character level must be at least 1.")
    return (level - 1) // 4 + 2

def calculate_armor_class(class_name, attribute_values):
    """
    Calculate the Armor Class (AC) based on the character's class and attributes.
    :param class_name: The character's class (str).
    :param attribute_values: A dictionary of attribute values (e.g., Strength, Dexterity, etc.).
    :return: Calculated Armor Class (int).
    """
    dexterity_modifier = (attribute_values["Dexterity"] - 10) // 2

    # Special cases for Barbarian and Monk
    if class_name == "Barbarian":
        constitution_modifier = (attribute_values["Constitution"] - 10) // 2
        return 10 + dexterity_modifier + constitution_modifier  # Barbarian AC formula <button class="citation-flag" data-index="3">
    elif class_name == "Monk":
        wisdom_modifier = (attribute_values["Wisdom"] - 10) // 2
        return 10 + dexterity_modifier + wisdom_modifier  # Monk AC formula
    else:
        return 10 + dexterity_modifier  # Default AC formula <button class="citation-flag" data-index="2">

def calculate_hit_dice(class_name, level):
    """
    Calculate the type and number of hit dice based on class and level.
    """
    hit_die_types = {
        "Barbarian": 12,
        "Fighter": 10,
        "Paladin": 10,
        "Ranger": 10,
        "Sorcerer": 6,
        "Wizard": 6,
        "Bard": 8,
        "Cleric": 8,
        "Druid": 8,
        "Monk": 8,
        "Rogue": 8,
        "Warlock": 8,
        "Artificer": 8,  # Added Artificer class with d8 hit die
    }
    hit_die = hit_die_types.get(class_name, 8)  # Default to d8 if class is unknown
    return f"d{hit_die} {level}/{level}"

def calculate_hit_points(class_name, level, constitution_modifier, use_average=True):
    """
    Calculate hit points based on class, level, and constitution modifier.
    """
    hit_die_types = {
        "Barbarian": 12,
        "Fighter": 10,
        "Paladin": 10,
        "Ranger": 10,
        "Sorcerer": 6,
        "Wizard": 6,
        "Bard": 8,
        "Cleric": 8,
        "Druid": 8,
        "Monk": 8,
        "Rogue": 8,
        "Warlock": 8,
        "Artificer": 8,  # Added Artificer class with d8 hit die
    }
    hit_die = hit_die_types.get(class_name, 8)  # Default to d8 if class is unknown
    if use_average:
        average_hp_per_level = (hit_die // 2) + 1
        total_hp = average_hp_per_level * level + (constitution_modifier * level)
    else:
        # Simulate rolling hit dice (not implemented here for simplicity)
        total_hp = hit_die * level + (constitution_modifier * level)
    return total_hp

def generate_character_info(character_name, race, class_name, level, speed, inspiration, current_xp, attribute_values, use_average_hp=True):
    """
    Generate the character info output following the specified template.
    """
    proficiency_bonus = calculate_proficiency_bonus(level)
    hit_dice = calculate_hit_dice(class_name, level)
    hit_points = calculate_hit_points(class_name, level, (attribute_values["Constitution"] - 10) // 2, use_average_hp)
    armor_class = calculate_armor_class(class_name, attribute_values)  # Use the updated AC calculation
    xp_to_next_level = get_xp_for_next_level(level)

    character_info = f"""
> [!infobox]
> # {character_name}
> ![[image.png|cover hsbig]]
> ###### Stats
| Stat                   | Value     |
| ---------------------- | --------- |
| Race                   | {race}    |
| Class                  | {class_name}       |
| Hit Die                | {hit_dice}   |
| Hit Points             | {hit_points} / {hit_points}   |
| Armor Class (AC)       | {armor_class}         |
| Speed                  | {speed}ft       |
| Proficiency Bonus (PB) | {proficiency_bonus:+d}         |
| XP                     | {current_xp} / {xp_to_next_level}|
| Inspiration            | {inspiration}         |
"""
    return character_info



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

def get_xp_for_next_level(current_level):
    """
    Retrieve the XP required to reach the next level based on the official D&D 5e progression.
    :param current_level: The current level of the character (int).
    :return: XP required to reach the next level (int or str if max level).
    """
    if current_level < 1 or current_level > 20:
        raise ValueError("Level must be between 1 and 20.")
    if current_level == 20:
        return "Max Level"
    return XP_PROGRESSION.get(current_level + 1, 0)

def generate_character_info(character_name, race, class_name, level, speed, inspiration, current_xp, attribute_values, use_average_hp=True):
    """
    Generate the character info output following the specified template.
    """
    # Validate attribute_values
    if not all(isinstance(value, int) for value in attribute_values.values()):
        raise ValueError("attribute_values must contain only integers.")

    # Calculate proficiency bonus
    proficiency_bonus = calculate_proficiency_bonus(level)

    # Calculate hit dice and hit points
    hit_dice = calculate_hit_dice(class_name, level)
    constitution_modifier = (attribute_values["Constitution"] - 10) // 2
    hit_points = calculate_hit_points(class_name, level, constitution_modifier, use_average_hp)

    # Calculate armor class
    armor_class = calculate_armor_class(class_name, attribute_values)

    # Calculate XP to next level
    xp_to_next_level = get_xp_for_next_level(level)

    # Generate the character info string in Obsidian-compatible format
    character_info = f"""
> [!character|center]
> ![[image.png|300]] 
> ### {character_name}
> ###### Stats
| Stat                   | Value     |
| ---------------------- | --------- |
| Race                   | {race}    |
| Class                  | {class_name}       |
| Hit Die                | {hit_dice}   |
| Hit Points             | {hit_points} / {hit_points}   |
| Armor Class (AC)       | {armor_class}         |
| Speed                  | {speed}ft       |
| Proficiency Bonus (PB) | {proficiency_bonus:+d}         |
| XP                     | {current_xp} / {xp_to_next_level}|
| Inspiration            | {inspiration}         |
"""
    return character_info


def generate_full_output(character_info, attributes_table, skills_table, spell_stats):
    """
    Generate the full output in the specified template.
    :param character_info: The character info string (str).
    :param attributes_table: The attributes table string (str).
    :param skills_table: The skills table string (str).
    :param spell_stats: The spell stats string (str).
    :return: Full formatted output (str).
    """
    # Template for the full output
    full_output = f"""
---

# Stats
{character_info}


---
# Attributes
{attributes_table}


---
# Skills
{skills_table}


---

# Inventory
| Currency | Amount |
| -------- | ------ |
| Platinum | 0      |
| Gold     | 0      |
| Silver   | 0      |
| Copper   | 0      |
| Item                | Effect | Weight |
| ------------------- | ------ | ------ |


---

# Abilities

## Attacks
| method      | damage                          | type        | Attack Roll         |
| ----------- | ------------------------------- | ----------- | ------------------- |

## Spells
{spell_stats}

---

"""
    return full_output.strip()