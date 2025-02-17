# gui.py
import PySimpleGUI as sg
from .layout import create_first_column, create_second_column, create_third_column, create_fourth_column
from .events import (handle_standard_array, 
                    handle_convert_event, 
                    handle_copy_all_event,
                    handle_copy_attributes_event,
                    handle_copy_character_info_event,
                    handle_copy_skills_event,
                    handle_copy_spell_stats_event,
                    handle_caster_event, 
                    update_skills_table)	
from .constants import ATTRIBUTE_KEYS, STANDARD_ARRAY
from attribute_logic import calculate_spell_stats, calculate_proficiency_bonus, generate_character_info, generate_full_output



# Set theme and create layout
sg.theme('DarkBlue')

# Create columns
first_column = create_first_column()
second_column = create_second_column()
third_column = create_third_column()
fourth_column = create_fourth_column()

# Combine all columns into the bottom section
bottom_section = [
    [
        sg.Column(first_column, element_justification="center", expand_x=True, expand_y=True),
        sg.VSeparator(),
        sg.Column(second_column, element_justification="center", expand_x=True, expand_y=True),
        sg.VSeparator(),
        sg.Column(third_column, element_justification="center", expand_x=True, expand_y=True),
        sg.VSeparator(),
        sg.Column(fourth_column, element_justification="center", expand_x=True, expand_y=True),
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
# Create window
window = sg.Window("D&D 5e Character Sheet Generator", layout, finalize=True, size=(1400, 800), resizable=True)

# Expand elements
window["-ATTRIBUTES-TABLE-"].expand(True, True)
window["-SKILLS-TABLE-"].expand(True, True)
window["-SPELL-STATS-"].expand(True, True)

# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "-CONVERT-":
        handle_convert_event(values, window)

    if event == "-COPY-ATTRIBUTES-":
        handle_copy_attributes_event(window)

    if event == "-COPY-SKILLS-":
        handle_copy_skills_event(window)

    if event == "-COPY-CHARACTER-INFO-":
        handle_copy_character_info_event(window)

    if event == "-COPY-SPELL-STATS-":
        handle_copy_spell_stats_event(window)

    if event == "-COPY-ALL-":
        handle_copy_all_event(values, window)
        
    if event == "-STANDARD-ARRAY-":
        handle_standard_array(window)
    
    if event == "-CASTER-":
        handle_caster_event(values, window)

window.close()