from tkinter import filedialog


def open_file():

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Python Files", "*.py"),
            ("Text Files", "*.txt"),
            ("Markdown Files", "*.md"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def save_file(content):

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("Markdown Files", "*.md"),
            ("Python Files", "*.py"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        return

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def exit_app(window):
    window.destroy()