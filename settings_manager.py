import json
import os


SETTINGS_FILE = "settings.json"


DEFAULT_SETTINGS = {
    "model": "gpt-4.1-mini",
    "theme": "Dark",
    "font_size": "Medium"
}


def load_settings():

    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    with open(SETTINGS_FILE, "r") as file:
        settings = json.load(file)

    # Uygulamanın mevcut UI'ı Dracula/dark olduğu için
    # eski "Light" kaydını Dark'a çevir.
    if settings.get("theme") == "Light":
        settings["theme"] = "Dark"
        save_settings(settings)

    return settings


def save_settings(settings):

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def reset_settings():

    save_settings(DEFAULT_SETTINGS)