import json
import os

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "model": "gpt-4.1-mini",
    "theme": "Light",
    "font_size": "Medium"
}


def load_settings():

    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)


def save_settings(settings):

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def reset_settings():

    save_settings(DEFAULT_SETTINGS)