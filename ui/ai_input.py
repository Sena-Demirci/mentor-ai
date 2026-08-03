import tkinter as tk

from ui.colors import *
from ui.fonts import *
from ui.sizes import *
from PIL import Image, ImageTk




from ui.buttons import create_send_button



def create_ai_input(parent):
    card = tk.Frame(
        parent,
        width=AI_INPUT_WIDTH,
        height=AI_INPUT_HEIGHT,
        bg=AI_CARD_BG,
        highlightbackground="#8B5CF6",
        highlightthickness=1
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

    assistant_image = Image.open("assets/ai_card/titles/assistant_title.png")

    new_width = 120
    ratio = new_width / assistant_image.width
    new_height = int(assistant_image.height * ratio)

    assistant_image = assistant_image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    assistant_photo = ImageTk.PhotoImage(assistant_image)

    card.assistant_photo = assistant_photo

    assistant_label = tk.Label(
        header_frame,
        image=assistant_photo,
        bg=AI_CARD_BG,
        bd=0,
        highlightthickness=0
    )

    assistant_label.pack(side="left")

    pro_image = Image.open("assets/ai_card/badges/pro_badge.png")

    new_width = 60
    ratio = new_width / pro_image.width
    new_height = int(pro_image.height * ratio)

    pro_image = pro_image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    pro_photo = ImageTk.PhotoImage(pro_image)

    card.pro_photo = pro_photo

    pro_label = tk.Label(
        header_frame,
        image=pro_photo,
        bg=AI_CARD_BG,
        bd=0,
        highlightthickness=0
    )

    pro_label.pack(
        side="right",
        padx=(0 , 20)
    )

    gpt_image = Image.open("assets/ai_card/badges/gpt4.png")

    new_width = 85
    ratio = new_width / gpt_image.width
    new_height = int(gpt_image.height * ratio)

    gpt_image = gpt_image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    gpt_photo = ImageTk.PhotoImage(gpt_image)

    card.gpt_photo = gpt_photo

    gpt_label = tk.Label(
        header_frame,
        image=gpt_photo,
        bg=AI_CARD_BG,
        bd=0,
        highlightthickness=0
    )

    gpt_label.pack(
        side="right",
        padx=(0, 0.1)
    )

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