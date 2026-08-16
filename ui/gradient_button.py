"""
ui/gradient_button.py
======================
"Start a New Project / Learn Mode / Debug Mode / Hint Mode" butonları için
LEARN, DEBUG, HINT, PLAN MODE BUTTON.txt dosyasındaki gradyan tasarıma uygun,
PNG arka planlı, tıklanabilir buton bileşeni.

Kullanım:
    from ui.gradient_button import create_gradient_button

    btn = create_gradient_button(parent, "Learn Mode", learn_mode)
    btn.pack(fill="x", pady=7)
"""

import os
import tkinter as tk
from PIL import Image, ImageTk

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_PATH = os.path.join(
    PROJECT_ROOT, "assets", "ai_card", "buttons", "mode_button_bg.png"
)

TEXT_COLOR = "#FFFFFF"
FONT = ("Segoe UI", 12, "bold")

_bg_image_cache = None


def _load_bg_image():
    global _bg_image_cache
    if _bg_image_cache is None:
        _bg_image_cache = Image.open(ASSET_PATH)
    return _bg_image_cache


def create_gradient_button(parent, text, command, width=None, height=None):
    """
    parent   : içine yerleştirileceği widget
    text     : buton üzerinde görünecek yazı
    command  : tıklanınca çağrılacak fonksiyon (parametresiz)
    width/height : verilmezse PNG'nin doğal boyutu kullanılır
    """
    source_image = _load_bg_image()

    w = width or source_image.width
    h = height or source_image.height

    image = source_image.resize((w, h), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    canvas = tk.Canvas(
        parent,
        width=w,
        height=h,
        bg=parent.cget("bg"),
        bd=0,
        highlightthickness=0,
        cursor="hand2"
    )

    canvas.create_image(0, 0, anchor="nw", image=photo)
    canvas.image = photo  # referansı canlı tut

    canvas.create_text(
        w // 2,
        h // 2,
        text=text,
        fill=TEXT_COLOR,
        font=FONT
    )

    def on_click(event):
        command()

    def on_enter(event):
        canvas.config(cursor="hand2")

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<Enter>", on_enter)

    return canvas