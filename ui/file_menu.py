import os
import tkinter as tk
from PIL import Image, ImageTk


TOP_FRAME_BG = "#181825"
BUTTON_HEIGHT = 56          # File/Settings butonları — okunaklı olması için büyütüldü
MENU_TARGET_WIDTH = 300     # dropdown menü genişliği (px) - PNG orijinal boyutuna göre ölçeklenir

# ui/file_menu.py -> proje kökü, ui/ klasörünün bir üstü.
# Bu sayede program hangi dizinden çalıştırılırsa çalıştırılsın
# (PyCharm, terminal, farklı cwd) assets yolu her zaman doğru bulunur.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets", "ai_card", "buttons")


def _asset_path(filename):
    return os.path.join(ASSETS_DIR, filename)


def create_file_button(parent, show_file_menu):

    image = Image.open(
        _asset_path("file_button.png")
    )

    ratio = BUTTON_HEIGHT / image.height

    image = image.resize(
        (
            int(image.width * ratio),
            BUTTON_HEIGHT
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
        padx=(10, 0)
    )

    button.bind(
        "<Button-1>",
        lambda event: show_file_menu(button)
    )

    return button


def create_settings_button(parent, open_settings):

    image = Image.open(
        _asset_path("settings_button.png")
    )

    ratio = BUTTON_HEIGHT / image.height

    image = image.resize(
        (
            int(image.width * ratio),
            BUTTON_HEIGHT
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
        padx=(0, 10)
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
    recent_projects,
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
        _asset_path("file_box.png")
    )

    # PNG genelde büyük çözünürlükte hazırlanır; menüyü ekranda
    # makul bir genişliğe indiriyoruz, tıklama alanlarını da
    # aynı oranla (scale) ölçekleyeceğiz.
    scale = MENU_TARGET_WIDTH / image.width
    menu_width = MENU_TARGET_WIDTH
    menu_height = int(image.height * scale)

    image = image.resize(
        (menu_width, menu_height),
        Image.Resampling.LANCZOS
    )

    photo = ImageTk.PhotoImage(image)

    canvas = tk.Canvas(
        menu_window,
        width=menu_width,
        height=menu_height,
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

    file_button.update_idletasks()

    x = file_button.winfo_rootx()

    y = (
        file_button.winfo_rooty()
        + file_button.winfo_height()
        - 5
    )

    menu_window.geometry(
        f"{menu_width}x{menu_height}+{x}+{y}"
    )

    def scaled(value):
        return value * scale

    canvas.create_rectangle(
        scaled(75),
        scaled(75),
        menu_width - scaled(75),
        scaled(150),
        fill="",
        outline="",
        tags="new_project"
    )

    canvas.create_rectangle(
        scaled(75),
        scaled(150),
        menu_width - scaled(75),
        scaled(240),
        fill="",
        outline="",
        tags="open_project"
    )

    canvas.create_rectangle(
        scaled(75),
        scaled(240),
        menu_width - scaled(75),
        scaled(320),
        fill="",
        outline="",
        tags="recent_projects"
    )

    canvas.create_rectangle(
        scaled(75),
        scaled(330),
        menu_width - scaled(75),
        scaled(410),
        fill="",
        outline="",
        tags="save_project"
    )

    canvas.create_rectangle(
        scaled(75),
        scaled(410),
        menu_width - scaled(75),
        menu_height - scaled(20),
        fill="",
        outline="",
        tags="exit"
    )

    def close_menu():
        # Global "dışarı tıklama" dinleyicisini kaldır, sonra menüyü yok et
        root.unbind_all("<Button-1>")
        if menu_window.winfo_exists():
            menu_window.destroy()

    canvas.tag_bind(
        "new_project",
        "<Button-1>",
        lambda event: (close_menu(), new_project())
    )

    canvas.tag_bind(
        "open_project",
        "<Button-1>",
        lambda event: (close_menu(), open_project())
    )

    canvas.tag_bind(
        "recent_projects",
        "<Button-1>",
        lambda event: (close_menu(), recent_projects())
    )

    canvas.tag_bind(
        "save_project",
        "<Button-1>",
        lambda event: (close_menu(), save_project())
    )

    canvas.tag_bind(
        "exit",
        "<Button-1>",
        lambda event: (close_menu(), exit_project())
    )

    def close_on_outside_click(event):
        # Tıklama menü penceresinin dışındaysa menüyü kapat
        try:
            if event.widget.winfo_toplevel() != menu_window:
                close_menu()
        except tk.TclError:
            pass  # menü zaten bir item tıklamasıyla kapanmış olabilir

    root.bind_all("<Button-1>", close_on_outside_click, add="+")