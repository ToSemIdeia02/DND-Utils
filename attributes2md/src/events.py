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

        # Determine whether to use string input or individual fields
        if values["-STRING-MODE-"]:
            raw_values = values["-ATTRIBUTES-STRING-"].strip().split(",")
            if len(raw_values) != 6:
                raise ValueError("Please enter exactly 6 values separated by commas.")
            attribute_values = {
                "Strength": int(raw_values[0].strip()),
                "Dexterity": int(raw_values[1].strip()),
                "Constitution": int(raw_values[2].strip()),
                "Intelligence": int(raw_values[3].strip()),
                "Wisdom": int(raw_values[4].strip()),
                "Charisma": int(raw_values[5].strip()),
            }
            proficiencies = {attr: False for attr in attribute_values.keys()}
        else:
            attribute_values = {
                "Strength": int(values["-STR-"]),
                "Dexterity": int(values["-DEX-"]),
                "Constitution": int(values["-CON-"]),
                "Intelligence": int(values["-INT-"]),
                "Wisdom": int(values["-WIS-"]),
                "Charisma": int(values["-CHA-"]),
            }
            proficiencies = {
                "Strength": values["-PROF-STR-"],
                "Dexterity": values["-PROF-DEX-"],
                "Constitution": values["-PROF-CON-"],
                "Intelligence": values["-PROF-INT-"],
                "Wisdom": values["-PROF-WIS-"],
                "Charisma": values["-PROF-CHA-"],
            }

        # Validate attribute values
        for key, value in attribute_values.items():
            if not isinstance(value, int):
                raise ValueError(f"Invalid value for {key}: {value}. Please enter integers only.")

        # Calculate proficiency bonus based on level
        proficiency_bonus = calculate_proficiency_bonus(level)

        # Generate updated tables
        attributes_table = update_attribute_table(attribute_values, proficiencies, proficiency_bonus)
        skills_table = update_skills_table(attribute_values, proficiencies, proficiency_bonus, values)

        # Update the output boxes
        window["-ATTRIBUTES-TABLE-"].update(attributes_table)
        window["-SKILLS-TABLE-"].update(skills_table)

        # Generate character info
        constitution_modifier = (attribute_values["Constitution"] - 10) // 2
        character_info = generate_character_info(
            character_name, race, class_name, level, speed, inspiration, current_xp, attribute_values, use_average_hp
        )
        window["-CHARACTER-INFO-"].update(character_info)

        # If caster is enabled, calculate spell stats
        if values["-CASTER-"]:
            if values["-CASTING-INT-"]:
                casting_stat = "Intelligence"
            elif values["-CASTING-WIS-"]:
                casting_stat = "Wisdom"
            elif values["-CASTING-CHA-"]:
                casting_stat = "Charisma"
            else:
                raise ValueError("Please select a casting stat.")
            spell_stats = calculate_spell_stats(attribute_values, casting_stat, proficiency_bonus)
            window["-SPELL-STATS-"].update(spell_stats)
            window["-SPELL-STATS-"].update(visible=True)

    except ValueError as e:
        sg.popup_error(str(e))


def handle_copy_attributes_event(window):
    attributes_text = window["-ATTRIBUTES-TABLE-"].get()
    window.TKroot.clipboard_clear()
    window.TKroot.clipboard_append(attributes_text)
    sg.popup("Attributes table copied to clipboard!")


def handle_copy_skills_event(window):
    skills_text = window["-SKILLS-TABLE-"].get()
    window.TKroot.clipboard_clear()
    window.TKroot.clipboard_append(skills_text)
    sg.popup("Skills table copied to clipboard!")


def handle_copy_character_info_event(window):
    character_info_text = window["-CHARACTER-INFO-"].get()
    window.TKroot.clipboard_clear()
    window.TKroot.clipboard_append(character_info_text)
    sg.popup("Character info copied to clipboard!")


def handle_copy_spell_stats_event(window):
    spell_stats_text = window["-SPELL-STATS-"].get()
    window.TKroot.clipboard_clear()
    window.TKroot.clipboard_append(spell_stats_text)
    sg.popup("Spell stats copied to clipboard!")


def handle_copy_all_event(values, window):
    try:
        character_info = window["-CHARACTER-INFO-"].get()
        attributes_table = window["-ATTRIBUTES-TABLE-"].get()
        skills_table = window["-SKILLS-TABLE-"].get()
        spell_stats = window["-SPELL-STATS-"].get() if values["-CASTER-"] else ""

        full_output = (
            f"\n{character_info}\n\n"
            f"\n{attributes_table}\n\n"
            f"\n{skills_table}\n\n"
            f"\n{spell_stats}"
        )

        window.TKroot.clipboard_clear()
        window.TKroot.clipboard_append(full_output)
        sg.popup("All outputs copied to clipboard!")
    except Exception as e:
        sg.popup_error(f"Error copying outputs: {str(e)}")
        
def handle_caster_event(values, window):
    # Toggle visibility of the casting stat label and radio buttons
    window["-CASTING-STAT-LABEL-"].update(visible=values["-CASTER-"])
    window["-CASTING-INT-"].update(visible=values["-CASTER-"])
    window["-CASTING-WIS-"].update(visible=values["-CASTER-"])
    window["-CASTING-CHA-"].update(visible=values["-CASTER-"])

    # Refresh the window to handle layout changes dynamically
    window.refresh()  # Force the GUI to recalculate the layout