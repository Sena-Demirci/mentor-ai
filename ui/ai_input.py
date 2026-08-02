import tkinter as tk

from ui.colors import *
from ui.fonts import *
from ui.sizes import *

from ui.buttons import create_send_button


def create_ai_input(parent):

    ai_chat_frame = tk.Frame(
        parent,
        width=AI_INPUT_WIDTH,
        height=AI_INPUT_HEIGHT,
        bg=DRACULA_AI_INPUT_BG,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    ai_chat_frame.grid_propagate(False)

    # ==========================
    # Header
    # ==========================

    header_frame = tk.Frame(
        ai_chat_frame,
        bg=DRACULA_AI_INPUT_BG
    )

    header_frame.pack(
        fill="x",
        padx=12,
        pady=(10, 5)
    )

    ai_label = tk.Label(
        header_frame,
        text="AI Assistant",
        bg=DRACULA_AI_INPUT_BG,
        fg=PRIMARY,
        font=AI_HEADER_FONT
    )

    ai_label.pack(side="left")

    model_label = tk.Label(
        header_frame,
        text="GPT-4.1 Mini",
        bg=BORDER,
        fg=TEXT,
        font=AI_BADGE_FONT,
        padx=8,
        pady=2
    )

    model_label.pack(side="right")

    # ==========================
    # Text Area
    # ==========================

    input_text = tk.Text(
        ai_chat_frame,
        bg=DRACULA_AI_INPUT_BG,
        fg=TEXT,
        font=AI_INPUT_FONT,
        borderwidth=0,
        highlightthickness=0,
        insertbackground=EDITOR_CURSOR
    )

    input_text.pack(
        fill="x",
        padx=12,
        pady=(0, 10)
    )

    input_text.config(height=6)

    bottom_frame = tk.Frame(
        ai_chat_frame,
        bg=DRACULA_AI_INPUT_BG
    )

    bottom_frame.pack(
        fill="x",
        padx=12,
        pady=(0, 10)
    )

    send_button = create_send_button(bottom_frame)

    send_button.pack(side="right")

    return ai_chat_frame