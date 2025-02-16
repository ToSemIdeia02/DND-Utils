# events.py
import random
import PySimpleGUI as sg
from .constants import STANDARD_ARRAY, ATTRIBUTE_KEYS  # Relative import
from attribute_logic import (  # Absolute import
    calculate_modifier,
    update_attribute_table,
    update_skills_table,
    calculate_spell_stats,
    calculate_proficiency_bonus,
    generate_character_info,
    generate_full_output,
)

def handle_standard_array(window):
    shuffled_array = STANDARD_ARRAY[:]
    random.shuffle(shuffled_array)
    for i, key in enumerate(ATTRIBUTE_KEYS):
        window[key].update(shuffled_array[i])

def handle_convert_event(values, window):
    try:
        # Extract and validate inputs
        character_name = values["-CHARACTER-NAME-"]
        race = values["-RACE-"]
        class_name = values["-CLASS-"]
        level = int(values["-LEVEL-"]) if values["-LEVEL-"] else 1
        speed = int(values["-SPEED-"]) if values["-SPEED-"] else 30
        inspiration = 1 if values["-INSPIRATION-"] else 0
        current_xp = int(values["-CURRENT-XP-"]) if values["-CURRENT-XP-"] else 0
        use_average_hp = values["-USE-AVERAGE-HP-"]

        # Determine attribute values based on input mode
        if values["-STRING-MODE-"]:
            raw_values = values["-ATTRIBUTES-STRING-"].strip().split(",")
            if len(raw_values) != 6:
                raise ValueError("Please enter exactly 6 values separated by commas.")
            attribute_values = {attr: int(raw_values[i].strip()) for i, attr in enumerate(["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"])}
            proficiencies = {attr: False for attr in attribute_values.keys()}
        else:
            attribute_values = {attr: int(values[key]) for attr, key in zip(["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"], ATTRIBUTE_KEYS)}
            proficiencies = {attr: values[f"-PROF-{attr}-"] for attr in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]}

        # Generate outputs
        proficiency_bonus = calculate_proficiency_bonus(level)
        attributes_table = update_attribute_table(attribute_values, proficiencies, proficiency_bonus)
        skills_table = update_skills_table(attribute_values, proficiencies, proficiency_bonus, values)
        constitution_modifier = (attribute_values["Constitution"] - 10) // 2
        character_info = generate_character_info(character_name, race, class_name, level, speed, inspiration, current_xp, attribute_values, use_average_hp)
        window["-ATTRIBUTES-TABLE-"].update(attributes_table)
        window["-SKILLS-TABLE-"].update(skills_table)
        window["-CHARACTER-INFO-"].update(character_info)

        if values["-CASTER-"]:
            casting_stat = "Intelligence" if values["-CASTING-INT-"] else "Wisdom" if values["-CASTING-WIS-"] else "Charisma"
            spell_stats = calculate_spell_stats(attribute_values, casting_stat, proficiency_bonus)
            window["-SPELL-STATS-"].update(spell_stats)
            window["-SPELL-STATS-"].update(visible=True)

    except ValueError as e:
        sg.popup_error(str(e))