# main.py
from src.gui import create_window
import PySimpleGUI as sg

if __name__ == "__main__":
    # Create and run the GUI window
    window = create_window()
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
    window.close()