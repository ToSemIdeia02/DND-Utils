# gui.py
import PySimpleGUI as sg
from .layout import create_first_column, create_second_column, create_third_column, create_fourth_column
from .events import handle_standard_array, handle_convert_event
from .constants import ATTRIBUTE_KEYS

# Set theme and create layout
sg.theme('DarkBlue')

# Create columns
first_column = create_first_column()
second_column = create_second_column()
third_column = create_third_column()
fourth_column = create_fourth_column()

# Combine columns into bottom section
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

# Top section with buttons
top_section = [
    [
        sg.Button("Convert to .md", size=(15, 2), key="-CONVERT-", pad=((0, 10), (20, 20))),
        sg.Button("Copy All", size=(15, 2), key="-COPY-ALL-", pad=((10, 0), (20, 20))),
    ],
]

# Final layout
layout = [
    [sg.Column(top_section, justification="center", expand_x=True)],
    [sg.Column(bottom_section, expand_x=True, expand_y=True)],
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

    if event == "-STANDARD-ARRAY-":
        handle_standard_array(window)

    if event == "-CONVERT-":
        handle_convert_event(values, window)

    # Handle other events (copy buttons, etc.)
    if event == "-COPY-ATTRIBUTES-":
        attributes_text = window["-ATTRIBUTES-TABLE-"].get()
        window.TKroot.clipboard_clear()
        window.TKroot.clipboard_append(attributes_text)
        sg.popup("Attributes table copied to clipboard!")

    # Add similar handlers for other copy buttons...

window.close()