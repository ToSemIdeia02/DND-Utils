# layout.py
from .constants import STANDARD_ARRAY, SKILL_MAPPING, ATTRIBUTE_KEYS  # Relative import
import PySimpleGUI as sg

def create_first_column():
    return [
        [sg.Text("General Character Info", font=("Arial", 14), justification="center")],
        [sg.Text("Name"), sg.Input(key="-CHARACTER-NAME-", size=(20, 1))],
        [sg.Text("Race"), sg.Input(key="-RACE-", size=(20, 1))],
        [sg.Text("Class"), sg.Combo(
            ["Barbarian", "Fighter", "Paladin", "Ranger", "Sorcerer", "Wizard",
             "Bard", "Cleric", "Druid", "Monk", "Rogue", "Warlock", "Artificer"],
            key="-CLASS-", size=(20, 1), readonly=True)],
        [sg.Text("Level"), sg.Input(key="-LEVEL-", size=(5, 1))],
        [sg.Text("Speed (ft)"), sg.Input(key="-SPEED-", size=(5, 1))],
        [sg.Text("Inspiration"), sg.Checkbox("", key="-INSPIRATION-")],
        [sg.Text("Current XP"), sg.Input(key="-CURRENT-XP-", size=(10, 1))],
        [sg.Checkbox("Use Average HP", key="-USE-AVERAGE-HP-", default=True)],
        [sg.HorizontalSeparator(pad=((0, 0), (10, 10)))],
        [sg.Text("Attributes", font=("Arial", 14), justification="center")],
        [sg.Button("Standard Array", size=(12, 1), key="-STANDARD-ARRAY-")],
        [sg.Checkbox("Input as String", key="-STRING-MODE-", enable_events=True)],
        [sg.Input(key="-ATTRIBUTES-STRING-", size=(30, 1), visible=False, tooltip="Enter values as: STR, DEX, CON, INT, WIS, CHA",
                  text_color="gray", default_text="STR, DEX, CON, INT, WIS, CHA")],
    ] + [
        [sg.Text(attr, key=f"-TEXT-{attr[1:-1]}-", visible=True),
         sg.Input(key=attr, size=(5, 1)),
         sg.Checkbox("Proficient", key=f"-PROF-{attr[1:-1]}-", visible=True)]
        for attr in ATTRIBUTE_KEYS
    ] + [
        [sg.Checkbox("Caster", key="-CASTER-", enable_events=True)],
        [sg.Text("Casting Stat", visible=False, key="-CASTING-STAT-LABEL-"),
         sg.Radio("INT", "CASTING_STAT", key="-CASTING-INT-", visible=False),
         sg.Radio("WIS", "CASTING_STAT", key="-CASTING-WIS-", visible=False),
         sg.Radio("CHA", "CASTING_STAT", key="-CASTING-CHA-", visible=False)],
    ]

def create_second_column():
    return [
        [sg.Text("Skills", font=("Arial", 14), justification="center")]
    ] + [
        [sg.Text(skill, size=(16, 1)),
         sg.Checkbox("Proficient", key=f"-PROF-{skill}-", enable_events=True),
         sg.Checkbox("Expertise", key=f"-EXPERT-{skill}-", enable_events=True)]
        for skill in SKILL_MAPPING.keys()
    ]

def create_third_column():
    return [
        [sg.Text("Attributes Table", font=("Arial", 14))],
        [sg.Multiline(size=(40, 10), key="-ATTRIBUTES-TABLE-", disabled=True, expand_x=True, expand_y=True)],
        [sg.Button("Copy Attributes", size=(15, 1), key="-COPY-ATTRIBUTES-")],
        [sg.Text("Skills Table", font=("Arial", 14))],
        [sg.Multiline(size=(40, 15), key="-SKILLS-TABLE-", disabled=True, expand_x=True, expand_y=True)],
        [sg.Button("Copy Skills", size=(15, 1), key="-COPY-SKILLS-")],
    ]

def create_fourth_column():
    return [
        [sg.Text("Character Info", font=("Arial", 14))],
        [sg.Multiline(size=(30, 10), key="-CHARACTER-INFO-", disabled=True, expand_x=True, expand_y=True)],
        [sg.Button("Copy Character Info", size=(15, 1), key="-COPY-CHARACTER-INFO-")],
        [sg.Text("Spell Stats", font=("Arial", 14))],
        [sg.Multiline(size=(30, 10), key="-SPELL-STATS-", disabled=True, expand_x=True, expand_y=True, visible=False)],
        [sg.Button("Copy Spell Stats", size=(15, 1), key="-COPY-SPELL-STATS-")],
    ]