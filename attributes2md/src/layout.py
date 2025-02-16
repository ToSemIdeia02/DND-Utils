# layout.py
from .constants import STANDARD_ARRAY, SKILL_MAPPING, ATTRIBUTE_KEYS  # Relative import
import PySimpleGUI as sg

def create_first_column():
    # First column: General character info and attributes
    first_column = [
        # General Character Info Section
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
        
        # Horizontal Separator
        [sg.HorizontalSeparator(pad=((0, 0), (10, 10)))],  # Faint horizontal bar 
        
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
    return first_column

def create_second_column():
    # Second column: Input fields for attributes with proficiency checkboxes
    second_column = [
        [sg.Text("Skills", font=("Arial", 14), justification="center")]
    ] + [
        [sg.Text(skill, size=(16, 1)),
         sg.Checkbox("Proficient", key=f"-PROF-{skill}-", enable_events=True),
         sg.Checkbox("Expertise", key=f"-EXPERT-{skill}-", enable_events=True)]
        for skill in SKILL_MAPPING.keys()
    ]
    return second_column

def create_third_column():
    # Third column: Output boxes for tables
    third_column = [
        [sg.Text("Attributes Table", font=("Arial", 14))],
        [sg.Multiline(size=(40, 10), key="-ATTRIBUTES-TABLE-", disabled=True, expand_x=True, expand_y=True)],
        [sg.Button("Copy Attributes", size=(15, 1), key="-COPY-ATTRIBUTES-")],
        [sg.Text("Skills Table", font=("Arial", 14))],
        [sg.Multiline(size=(40, 15), key="-SKILLS-TABLE-", disabled=True, expand_x=True, expand_y=True)],
        [sg.Button("Copy Skills", size=(15, 1), key="-COPY-SKILLS-")],
    ]
    return third_column


def create_fourth_column():
    # Fourth column: Output boxes for Character Info and Spell Stats
    fourth_column = [
        [sg.Text("Character Info", font=("Arial", 14))],
        [sg.Multiline(size=(30, 10), key="-CHARACTER-INFO-", disabled=True, expand_x=True, expand_y=True)],
        [sg.Button("Copy Character Info", size=(15, 1), key="-COPY-CHARACTER-INFO-")],
        [sg.Text("Spell Stats", font=("Arial", 14))],
        [sg.Multiline(size=(30, 10), key="-SPELL-STATS-", disabled=True, expand_x=True, expand_y=True, visible=False)],
        [sg.Button("Copy Spell Stats", size=(15, 1), key="-COPY-SPELL-STATS-")],
    ]
    return fourth_column