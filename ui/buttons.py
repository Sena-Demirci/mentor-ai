import tkinter as tk

from ui.colors import *
from ui.fonts import *


def create_send_button(parent, command=None):

    button = tk.Button(
        parent,
        text="↑",
        command=command,
        bg="#BD93F9",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        width=2,
        height=1,
        borderwidth=0,
        cursor="hand2",
        activebackground="#C9A7FF",
        activeforeground="white"
    )

    return button