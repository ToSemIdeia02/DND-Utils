import PySimpleGUI as sg
from attribute_logic import (
    calculate_modifier,
    update_attribute_table,
    update_skills_table,
    calculate_spell_stats,
    calculate_proficiency_bonus,
    generate_character_info,
    generate_full_output,
)

# Define the layout of the GUI
sg.theme('DarkBlue')  # Set a dark theme

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
attribute_keys = ["-STR-", "-DEX-", "-CON-", "-INT-", "-WIS-", "-CHA-"]

# First column: Character Info and Attributes sections
first_column = [
    # Character Info Section
    [sg.Text("General Character Info", font=("Arial", 14), justification="center")],
    [sg.Text("Name"), sg.Input(key="-CHARACTER-NAME-", size=(20, 1))],
    [sg.Text("Race"), sg.Input(key="-RACE-", size=(20, 1))],
    [sg.Text("Class"), sg.Combo(
        ["Barbarian", "Fighter", "Paladin", "Ranger", "Sorcerer", "Wizard",
         "Bard", "Cleric", "Druid", "Monk", "Rogue", "Warlock", "Artificer"],
        key="-CLASS-", size=(20, 1), readonly=True)],  # Dropdown list for classes
    [sg.Text("Level"), sg.Input(key="-LEVEL-", size=(5, 1))],
    [sg.Text("Speed (ft)"), sg.Input(key="-SPEED-", size=(5, 1))],
    [sg.Text("Inspiration"), sg.Checkbox("", key="-INSPIRATION-")],
    [sg.Text("Current XP"), sg.Input(key="-CURRENT-XP-", size=(10, 1))],
    [sg.Checkbox("Use Average HP", key="-USE-AVERAGE-HP-", default=True)],
    
    # Attributes Section
    [sg.Text("Attributes", font=("Arial", 14), justification="center")],
    [sg.Button("Standard Array", size=(12, 1), key="-STANDARD-ARRAY-")],
    [sg.Checkbox("Input as String", key="-STRING-MODE-", enable_events=True)],
    [sg.Input(key="-ATTRIBUTES-STRING-", size=(30, 1), visible=False, tooltip="Enter values as: STR, DEX, CON, INT, WIS, CHA",
              text_color="gray", default_text="STR, DEX, CON, INT, WIS, CHA")],
    [sg.Text("STR", key="-TEXT-STR-", visible=True), sg.Input(key="-STR-", size=(5, 1)), sg.Checkbox("Proficient", key="-PROF-STR-", visible=True)],
    [sg.Text("DEX", key="-TEXT-DEX-", visible=True), sg.Input(key="-DEX-", size=(5, 1)), sg.Checkbox("Proficient", key="-PROF-DEX-", visible=True)],
    [sg.Text("CON", key="-TEXT-CON-", visible=True), sg.Input(key="-CON-", size=(5, 1)), sg.Checkbox("Proficient", key="-PROF-CON-", visible=True)],
    [sg.Text("INT", key="-TEXT-INT-", visible=True), sg.Input(key="-INT-", size=(5, 1)), sg.Checkbox("Proficient", key="-PROF-INT-", visible=True)],
    [sg.Text("WIS", key="-TEXT-WIS-", visible=True), sg.Input(key="-WIS-", size=(5, 1)), sg.Checkbox("Proficient", key="-PROF-WIS-", visible=True)],
    [sg.Text("CHA", key="-TEXT-CHA-", visible=True), sg.Input(key="-CHA-", size=(5, 1)), sg.Checkbox("Proficient", key="-PROF-CHA-", visible=True)],
    [sg.Checkbox("Caster", key="-CASTER-", enable_events=True)],
    [sg.Text("Casting Stat", visible=False, key="-CASTING-STAT-LABEL-"),
     sg.Radio("INT", "CASTING_STAT", key="-CASTING-INT-", visible=False),
     sg.Radio("WIS", "CASTING_STAT", key="-CASTING-WIS-", visible=False),
     sg.Radio("CHA", "CASTING_STAT", key="-CASTING-CHA-", visible=False)],
]

# Second column: Skills section
second_column = [
    [sg.Text("Skills", font=("Arial", 14), justification="center")],
]
for skill in SKILL_MAPPING.keys():
    second_column.append([
        sg.Text(skill, size=(16, 1)),
        sg.Checkbox("Proficient", key=f"-PROF-{skill}-", enable_events=True),
        sg.Checkbox("Expertise", key=f"-EXPERT-{skill}-", enable_events=True)
    ])

# Third column: Attributes Table and Skills Table
third_column = [
    [sg.Text("Attributes Table", font=("Arial", 14))],
    [sg.Multiline(size=(40, 10), key="-ATTRIBUTES-TABLE-", disabled=True, expand_x=True, expand_y=True)],
    [sg.Button("Copy Attributes", size=(15, 1), key="-COPY-ATTRIBUTES-")],
    [sg.Text("Skills Table", font=("Arial", 14))],
    [sg.Multiline(size=(40, 15), key="-SKILLS-TABLE-", disabled=True, expand_x=True, expand_y=True)],
    [sg.Button("Copy Skills", size=(15, 1), key="-COPY-SKILLS-")],
]

# Fourth column: Character Info and Spell Stats
fourth_column = [
    [sg.Text("Character Info", font=("Arial", 14))],
    [sg.Multiline(size=(30, 10), key="-CHARACTER-INFO-", disabled=True, expand_x=True, expand_y=True)],
    [sg.Button("Copy Character Info", size=(15, 1), key="-COPY-CHARACTER-INFO-")],
    [sg.Text("Spell Stats", font=("Arial", 14))],
    [sg.Multiline(size=(30, 10), key="-SPELL-STATS-", disabled=True, expand_x=True, expand_y=True, visible=False)],
    [sg.Button("Copy Spell Stats", size=(15, 1), key="-COPY-SPELL-STATS-")],
]

# Combine all columns into the bottom section
bottom_section = [
    [
        sg.Column(first_column, element_justification="center", expand_x=True, expand_y=True),
        sg.VSeparator(),
        sg.Column(second_column, element_justification="center", expand_x=True, expand_y=True, key="-SECOND-COLUMN-"),
        sg.VSeparator(),
        sg.Column(third_column, element_justification="center", expand_x=True, expand_y=True, key="-THIRD-COLUMN-"),
        sg.VSeparator(),
        sg.Column(fourth_column, element_justification="center", expand_x=True, expand_y=True, key="-FOURTH-COLUMN-"),
    ]
]

# Define the top section with buttons
top_section = [
    [
        sg.Button("Convert to .md", size=(15, 2), key="-CONVERT-", pad=((0, 10), (20, 20))),
        sg.Button("Copy All", size=(15, 2), key="-COPY-ALL-", pad=((10, 0), (20, 20))),
    ],
]

# Combine all sections into the final layout
layout = [
    [sg.Column(top_section, justification="center", expand_x=True)],  # Top section with buttons
    [sg.Column(bottom_section, expand_x=True, expand_y=True)],        # Bottom section with columns
]

# Create the window
window = sg.Window(
    "D&D 5e Character Sheet Generator",
    layout,
    finalize=True,
    size=(1400, 800),  # Initial size of the window
    resizable=True,    # Make the window resizable
)

# Expand elements to fill available space
window["-ATTRIBUTES-TABLE-"].expand(True, True)  # Attributes table expands horizontally and vertically
window["-SKILLS-TABLE-"].expand(True, True)      # Skills table expands horizontally and vertically
window["-SPELL-STATS-"].expand(True, True)       # Spell stats expand horizontally and vertically

# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    # Handle the switch for string input mode
    if event == "-STRING-MODE-":
        # Toggle visibility of the string input field, text labels, and proficiency checkboxes
        window["-ATTRIBUTES-STRING-"].update(visible=values["-STRING-MODE-"])
        for attr in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]:
            window[f"-TEXT-{attr}-"].update(visible=not values["-STRING-MODE-"])  # Hide/show text labels
            window[f"-{attr}-"].update(visible=not values["-STRING-MODE-"])       # Hide/show input fields
            window[f"-PROF-{attr}-"].update(visible=not values["-STRING-MODE-"])  # Hide/show proficiency checkboxes

    if event == "-CASTER-":
        # Toggle visibility of the casting stat label and checkboxes
        window["-CASTING-STAT-LABEL-"].update(visible=values["-CASTER-"])
        window["-CASTING-INT-"].update(visible=values["-CASTER-"])
        window["-CASTING-WIS-"].update(visible=values["-CASTER-"])
        window["-CASTING-CHA-"].update(visible=values["-CASTER-"])

        # Refresh the window to handle layout changes dynamically
        window.refresh()  # Force the GUI to recalculate the layout <button class="citation-flag" data-index="4">

    if event == "-STANDARD-ARRAY-":
        # Fill the attribute fields with the standard array values
        for i, key in enumerate(["-STR-", "-DEX-", "-CON-", "-INT-", "-WIS-", "-CHA-"]):
            window[key].update(STANDARD_ARRAY[i])

    if event == "-CONVERT-":
        try:
            # Get general character info
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
                # Parse the string input
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
                proficiencies = {attr: False for attr in attribute_values.keys()}  # No proficiencies in string mode
            else:
                # Get attribute values from individual input fields
                attribute_values = {
                    "Strength": int(values["-STR-"]),
                    "Dexterity": int(values["-DEX-"]),
                    "Constitution": int(values["-CON-"]),
                    "Intelligence": int(values["-INT-"]),
                    "Wisdom": int(values["-WIS-"]),
                    "Charisma": int(values["-CHA-"]),
                }

                # Get proficiency information from checkboxes
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
                # Determine the selected casting stat
                if values["-CASTING-INT-"]:
                    casting_stat = "Intelligence"
                elif values["-CASTING-WIS-"]:
                    casting_stat = "Wisdom"
                elif values["-CASTING-CHA-"]:
                    casting_stat = "Charisma"
                else:
                    raise ValueError("Please select a casting stat.")

                # Calculate spell stats using the logic in attribute_logic.py
                spell_stats = calculate_spell_stats(attribute_values, casting_stat, proficiency_bonus)
                window["-SPELL-STATS-"].update(spell_stats)
                window["-SPELL-STATS-"].update(visible=True)

        except ValueError as e:
            sg.popup_error(str(e))
        
    if event == "-COPY-ATTRIBUTES-":
        # Copy the Attributes table to clipboard
        attributes_text = window["-ATTRIBUTES-TABLE-"].get()
        window.TKroot.clipboard_clear()
        window.TKroot.clipboard_append(attributes_text)
        sg.popup("Attributes table copied to clipboard!")

    if event == "-COPY-SKILLS-":
        # Copy the Skills table to clipboard
        skills_text = window["-SKILLS-TABLE-"].get()
        window.TKroot.clipboard_clear()
        window.TKroot.clipboard_append(skills_text)
        sg.popup("Skills table copied to clipboard!")

    if event == "-COPY-SPELL-STATS-":
        # Copy the Spell Stats to clipboard
        spell_stats_text = window["-SPELL-STATS-"].get()
        window.TKroot.clipboard_clear()
        window.TKroot.clipboard_append(spell_stats_text)
        sg.popup("Spell stats copied to clipboard!")

    if event == "-COPY-CHARACTER-INFO-":
        # Copy the Character Info to clipboard
        character_info_text = window["-CHARACTER-INFO-"].get()
        window.TKroot.clipboard_clear()
        window.TKroot.clipboard_append(character_info_text)
        sg.popup("Character info copied to clipboard!")
    
    if event == "-COPY-ALL-":
        try:
            # Retrieve the generated outputs
            character_info = window["-CHARACTER-INFO-"].get()
            attributes_table = window["-ATTRIBUTES-TABLE-"].get()
            skills_table = window["-SKILLS-TABLE-"].get()
            spell_stats = window["-SPELL-STATS-"].get() if values["-CASTER-"] else ""

            # Generate the full output
            full_output = generate_full_output(character_info, attributes_table, skills_table, spell_stats)

            # Copy the full output to the clipboard
            window.TKroot

            window.TKroot.clipboard_clear()
            window.TKroot.clipboard_append(full_output)
            sg.popup("All outputs copied to clipboard!")
        except Exception as e:
            sg.popup_error(f"Error copying outputs: {str(e)}")

    if event == "-STANDARD-ARRAY-":
        # Fill the attribute fields with the standard array values
        for i, key in enumerate(["-STR-", "-DEX-", "-CON-", "-INT-", "-WIS-", "-CHA-"]):
            window[key].update(STANDARD_ARRAY[i])
        
        
# Close the window
window.close()