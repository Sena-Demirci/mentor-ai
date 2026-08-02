import tkinter as tk

from ui.colors import *
from ui.fonts import *
from ui.sizes import *



from ui.buttons import create_send_button



def create_ai_input(parent):
    card = tk.Frame(
        parent,
        width=AI_INPUT_WIDTH,
        height=AI_INPUT_HEIGHT,
        bg=AI_CARD_BG
    )

    card.pack_propagate(False)

    # ==========================
    # Header
    # ==========================

    header_frame = tk.Frame(
        card,
        bg=AI_CARD_BG
    )

    header_frame.pack(
        fill="x",
        pady=(0, 12)
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
        card,
        bg=AI_CARD_BG,
        fg=TEXT,
        font=AI_INPUT_FONT,
        borderwidth=0,
        highlightthickness=0,
        insertbackground=EDITOR_CURSOR
    )

    input_text.pack(
        fill="x",
        pady=(0, 12)
    )

    input_text.config(height=6)

    bottom_frame = tk.Frame(
        card,
        bg=AI_CARD_BG
    )

    bottom_frame.pack(
        fill="x",
        pady=(0, 10)
    )


    send_button = create_send_button(
        bottom_frame)

    send_button.pack(
        side="right",
        ipadx=2,
        ipady=1
    )





    return card