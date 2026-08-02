import tkinter as tk

from ui.colors import *
from ui.sizes import *


class AICard(tk.Frame):

    def __init__(self, parent):

        super().__init__(
            parent,
            width=AI_INPUT_WIDTH,
            height=AI_INPUT_HEIGHT,
            bg=DRACULA_PANEL_BG,
            highlightthickness=0,
            bd=0
        )

        self.pack_propagate(False)

        self.card = tk.Frame(
            self,
            bg=AI_CARD_BG,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        self.card.pack(
            fill="both",
            expand=True
        )

        self.content = tk.Frame(
            self.card,
            bg=AI_CARD_BG
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=16
        )