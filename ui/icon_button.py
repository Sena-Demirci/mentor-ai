"""
ui/icon_button.py
==================
AI Assistant kutusundaki gönder butonuyla aynı ruhta (mor, dairesel),
tek bir PNG ikonu gösteren küçük tıklanabilir buton. Learn Session
ekranındaki "yukarı ok" gönder butonu için kullanılır.
"""

import os
import tkinter as tk
from PIL import Image, ImageTk

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(PROJECT_ROOT, "assets", "ai_card", "buttons")

_image_cache = {}


def _load(filename, size):
    key = (filename, size)
    if key not in _image_cache:
        path = os.path.join(ASSET_DIR, filename)
        image = Image.open(path).resize((size, size), Image.LANCZOS)
        _image_cache[key] = ImageTk.PhotoImage(image)
    return _image_cache[key]


def create_icon_button(parent, filename, command, size=40):
    photo = _load(filename, size)

    label = tk.Label(
        parent,
        image=photo,
        bg=parent.cget("bg"),
        bd=0,
        highlightthickness=0,
        cursor="hand2"
    )
    label.image = photo

    label.bind("<Button-1>", lambda event: command())

    return label