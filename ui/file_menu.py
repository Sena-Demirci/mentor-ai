import tkinter as tk
from PIL import Image, ImageTk


TOP_FRAME_BG = "#181825"


def create_file_button(parent, show_file_menu):

    image = Image.open(
        "assets/ai_card/buttons/file_button.png"
    )

    ratio = 60 / image.height

    image = image.resize(
        (
            int(image.width * ratio),
            60
        ),
        Image.Resampling.LANCZOS
    )

    photo = ImageTk.PhotoImage(image)

    button = tk.Label(
        parent,
        image=photo,
        bg=TOP_FRAME_BG,
        bd=0,
        highlightthickness=0,
        cursor="hand2"
    )

    button.image = photo

    button.pack(
        side="left",
        padx=(12, 0)
    )

    button.bind(
        "<Button-1>",
        lambda event: show_file_menu(button)
    )

    return button


def create_settings_button(parent, open_settings):

    image = Image.open(
        "assets/ai_card/buttons/settings_button.png"
    )

    ratio = 60 / image.height

    image = image.resize(
        (
            int(image.width * ratio),
            60
        ),
        Image.Resampling.LANCZOS
    )

    photo = ImageTk.PhotoImage(image)

    button = tk.Label(
        parent,
        image=photo,
        bg=TOP_FRAME_BG,
        bd=0,
        highlightthickness=0,
        cursor="hand2"
    )

    button.image = photo

    button.pack(
        side="right",
        padx=(0, 12)
    )

    button.bind(
        "<Button-1>",
        lambda event: open_settings()
    )

    return button


def show_file_menu(
    file_button,
    new_project,
    open_project,
    save_project,
    exit_project
):

    root = file_button.winfo_toplevel()

    menu_window = tk.Toplevel(root)

    menu_window.overrideredirect(True)

    menu_window.configure(
        bg="#1F202B"
    )

    image = Image.open(
        "assets/ai_card/buttons/file_menu.png"
    )

    photo = ImageTk.PhotoImage(image)

    canvas = tk.Canvas(
        menu_window,
        width=image.width,
        height=image.height,
        bg="#1F202B",
        bd=0,
        highlightthickness=0
    )

    canvas.pack()

    canvas.create_image(
        0,
        0,
        anchor="nw",
        image=photo
    )

    menu_window.photo = photo

    x = file_button.winfo_rootx()

    y = (
        file_button.winfo_rooty()
        + file_button.winfo_height()
        - 5
    )

    menu_window.geometry(
        f"{image.width}x{image.height}+{x}+{y}"
    )

    canvas.create_rectangle(
        75,
        75,
        image.width - 75,
        150,
        fill="",
        outline="",
        tags="new_project"
    )

    canvas.create_rectangle(
        75,
        150,
        image.width - 75,
        240,
        fill="",
        outline="",
        tags="open_project"
    )

    canvas.create_rectangle(
        75,
        330,
        image.width - 75,
        410,
        fill="",
        outline="",
        tags="save_project"
    )

    canvas.create_rectangle(
        75,
        410,
        image.width - 75,
        image.height - 20,
        fill="",
        outline="",
        tags="exit"
    )

    canvas.tag_bind(
        "new_project",
        "<Button-1>",
        lambda event: (
            menu_window.destroy(),
            new_project()
        )
    )

    canvas.tag_bind(
        "open_project",
        "<Button-1>",
        lambda event: (
            menu_window.destroy(),
            open_project()
        )
    )

    canvas.tag_bind(
        "save_project",
        "<Button-1>",
        lambda event: (
            menu_window.destroy(),
            save_project()
        )
    )

    canvas.tag_bind(
        "exit",
        "<Button-1>",
        lambda event: (
            menu_window.destroy(),
            exit_project()
        )
    )