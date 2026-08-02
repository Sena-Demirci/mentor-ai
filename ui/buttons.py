import tkinter as tk

from ui.colors import *
from ui.fonts import *


def create_send_button(parent, command=None):

    button = tk.Button(
        parent,
        text="↑",
        command=command,
        bg=SEND_BUTTON,
        fg="white",
        activebackground=SEND_BUTTON_HOVER,
        activeforeground="white",
        relief="flat",
        bd=0,
        highlightthickness=0,
        font=("Segoe UI Symbol", 11, "bold"),
        cursor="hand2",
        padx=8,
        pady=4
    )

    return button