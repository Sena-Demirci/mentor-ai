import os
import re
import sys
import subprocess
import tempfile
import threading
import tkinter as tk
from openai_client import OpenAIClient
from logging import disable
from tkinter import messagebox
from tkinter import ttk

from settings_manager import *
from file_manager import *
from file_manager import open_file
from file_manager import save_file
from file_manager import exit_app

from ui.colors import *
from ui.fonts import *
from ui.sizes import *
from ui.ai_input import create_ai_input

from PIL import Image, ImageTk

from ui.file_menu import (
    create_file_button,
    create_settings_button,
    show_file_menu
)

from ui.gradient_button import create_gradient_button
from ui.icon_button import create_icon_button


# ==================================
# "AI ASSISTANT" KUTUSU TEMASI
# ==================================
# Başlangıç ekranındaki mor çerçeveli, koyu renkli AI Assistant kutusuyla
# aynı görünümü tüm beyaz metin kutularına (Text) uygulamak için kullanılır.
AI_BOX_BG = "#14121F"
AI_BOX_BORDER = "#8B5CF6"
AI_BOX_FG = "#EDEBF7"
AI_BOX_PLACEHOLDER_FG = "#8A8698"

# Mod butonlarının (gradyan PNG) ortalama tonuna yakın, düz butonlar için
# kullanılan tema renkleri - "Continue", "Debug", "Get Hint" vb.
BUTTON_BG = "#3B3A78"
BUTTON_HOVER_BG = "#4C4A96"
BUTTON_FG = "#FFFFFF"

# Mor "ışıltılı" geri (Back) butonu
BACK_BUTTON_BG = "#221E33"
BACK_BUTTON_HOVER_BG = "#332B4D"

DIVIDER_COLOR = "#3A3560"


# ==================================
# PYTHON SÖZ DİZİMİ RENKLENDİRME (SYNTAX HIGHLIGHTING)
# ==================================
# Dracula paletinden esinlenilmiş renkler. code_editor'ın selectbackground'ı
# (kullanıcının beğendiği taralı alan rengi) burada değiştirilmiyor.
SYNTAX_COLORS = {
    "comment": "#6B7280",
    "string": "#7FB77E",
    "decorator": "#D18B4A",
    "funcdef": "#61AFEF",
    "classdef": "#56B6C2",
    "number": "#B58DDB",
    "selfword": "#E0796E",
    "keyword": "#C2477E",
    "builtin": "#9AA5CE",
    "operator": "#8992A6",
}

# code_editor'daki normal metin (değişken adı, operatör, noktalama) için
# saf beyaz yerine kullanılan, gözü daha az yoran ton.
CODE_EDITOR_FG = "#ABB2BF"

_PYTHON_KEYWORDS = (
    r"False|None|True|and|as|assert|async|await|break|class|continue|"
    r"def|del|elif|else|except|finally|for|from|global|if|import|in|"
    r"is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield"
)

_PYTHON_BUILTINS = (
    r"print|len|range|str|int|float|list|dict|set|tuple|bool|open|type|"
    r"isinstance|super|input|enumerate|zip|map|filter|sorted|sum|min|max|"
    r"abs|round|object|Exception|ValueError|TypeError|KeyError|IndexError|"
    r"AttributeError|StopIteration|repr|hasattr|getattr|setattr"
)

_TOKEN_SPECS = [
    ("comment", r"#[^\n]*"),
    ("string", r"'''.*?'''|\"\"\".*?\"\"\"|'(?:[^'\\\n]|\\.)*'|\"(?:[^\"\\\n]|\\.)*\""),
    ("decorator", r"@\w+"),
    ("funcdef", r"(?<=\bdef )\w+"),
    ("classdef", r"(?<=\bclass )\w+"),
    ("number", r"\b\d+\.?\d*\b"),
    ("selfword", r"\b(?:self|cls)\b"),
    ("keyword", rf"\b(?:{_PYTHON_KEYWORDS})\b"),
    ("builtin", rf"\b(?:{_PYTHON_BUILTINS})\b"),
    ("operator", r"[+\-*/%=<>!&|^~:]+|[.,;\[\]{}()]"),
]

_PYTHON_TOKEN_REGEX = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in _TOKEN_SPECS),
    re.DOTALL
)


def configure_syntax_tags(text_widget, base_font):
    for tag, color in SYNTAX_COLORS.items():
        bold_tags = ("keyword", "funcdef", "classdef", "decorator")
        if tag in bold_tags:
            text_widget.tag_configure(
                tag, foreground=color,
                font=(base_font[0], base_font[1], "bold")
            )
        else:
            text_widget.tag_configure(tag, foreground=color)


def highlight_python_syntax(text_widget):
    for tag in SYNTAX_COLORS:
        text_widget.tag_remove(tag, "1.0", "end")

    content = text_widget.get("1.0", "end-1c")

    for match in _PYTHON_TOKEN_REGEX.finditer(content):
        tag = match.lastgroup
        start_index = f"1.0+{match.start()}c"
        end_index = f"1.0+{match.end()}c"
        text_widget.tag_add(tag, start_index, end_index)


def themed_textbox(parent, **kwargs):
    """
    Standart tk.Text yerine kullanılacak, AI Assistant kutusuyla aynı
    temaya sahip (koyu arkaplan + mor ince çerçeve) metin kutusu üretir.
    width/height gibi ekstra ayarlar kwargs ile geçilebilir.
    """
    defaults = dict(
        bg=AI_BOX_BG,
        fg=AI_BOX_FG,
        insertbackground=AI_BOX_FG,
        relief="flat",
        highlightthickness=1,
        highlightbackground=AI_BOX_BORDER,
        highlightcolor=AI_BOX_BORDER,
        wrap="word",
        padx=8,
        pady=8
    )
    defaults.update(kwargs)
    return tk.Text(parent, **defaults)


def styled_button(parent, text, command, **kwargs):
    """
    Uygulama genelinde kullanılan, mod butonlarıyla aynı renk ailesinden
    (koyu mor/lacivert) ama normal buton boyutunda düz bir buton üretir.
    "Continue", "Debug", "Get Hint", "Save Settings" vb. için kullanılır.
    """
    defaults = dict(
        text=text,
        command=command,
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        activebackground=BUTTON_HOVER_BG,
        activeforeground=BUTTON_FG,
        relief="flat",
        bd=0,
        padx=16,
        pady=6,
        cursor="hand2",
        font=("Segoe UI", 10, "bold")
    )
    defaults.update(kwargs)
    button = tk.Button(parent, **defaults)

    button.bind("<Enter>", lambda e: button.config(bg=BUTTON_HOVER_BG))
    button.bind("<Leave>", lambda e: button.config(bg=BUTTON_BG))

    return button


def create_back_button(parent, command):
    """
    Tüm ekranlarda kullanılan "← Back" butonunu, mor ışıltılı çerçeveli
    ortak stille üretir ve her yerde aynı şekilde sol üst köşeye yerleştirir.
    """
    button = tk.Button(
        parent,
        text="← Back",
        command=command,
        bg=BACK_BUTTON_BG,
        fg=AI_BOX_FG,
        activebackground=BACK_BUTTON_HOVER_BG,
        activeforeground=AI_BOX_FG,
        relief="flat",
        bd=0,
        padx=14,
        pady=5,
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
        highlightthickness=1,
        highlightbackground=AI_BOX_BORDER,
        highlightcolor=AI_BOX_BORDER
    )

    button.bind("<Enter>", lambda e: button.config(bg=BACK_BUTTON_HOVER_BG))
    button.bind("<Leave>", lambda e: button.config(bg=BACK_BUTTON_BG))

    button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
    return button


def apply_dark_combobox_theme(window):
    """
    ttk.Combobox varsayılan olarak beyaz/açık temalıdır. Uygulamanın
    geri kalanıyla aynı koyu + mor tema burada uygulanır.
    """
    style = ttk.Style(window)
    # "clam" cross-platform, saf Tk temasıdır ve ttk.Style renk ayarlarını
    # (fieldbackground, arrowcolor vb.) native Windows temasının aksine
    # tam olarak uygular.
    style.theme_use("clam")

    style.configure(
        "Dark.TCombobox",
        fieldbackground=AI_BOX_BG,
        background=AI_BOX_BG,
        foreground=AI_BOX_FG,
        arrowcolor=AI_BOX_FG,
        bordercolor=AI_BOX_BORDER,
        lightcolor=AI_BOX_BG,
        darkcolor=AI_BOX_BG,
        selectbackground=AI_BOX_BG,
        selectforeground=AI_BOX_FG,
        relief="flat"
    )

    style.map(
        "Dark.TCombobox",
        fieldbackground=[("readonly", AI_BOX_BG)],
        foreground=[("readonly", AI_BOX_FG)],
        selectbackground=[("readonly", AI_BOX_BG)],
        selectforeground=[("readonly", AI_BOX_FG)]
    )

    # Açılır listenin (popdown) rengi ayrı bir mekanizmayla ayarlanır.
    window.option_add("*TCombobox*Listbox.background", AI_BOX_BG)
    window.option_add("*TCombobox*Listbox.foreground", AI_BOX_FG)
    window.option_add("*TCombobox*Listbox.selectBackground", AI_BOX_BORDER)
    window.option_add("*TCombobox*Listbox.selectForeground", AI_BOX_FG)


def _enable_windows_dpi_awareness():
    """
    Windows, DPI farkındalığı bildirilmeyen Tkinter pencerelerini
    kendi ölçekleyip piksel piksel büyütür; sonuç bulanık/pikselli
    ikonlar ve metinlerdir. Bu fonksiyon uygulamayı DPI-aware yapar,
    böylece Windows arayüzü kendisi bulanıklaştırmadan native
    çözünürlükte çizer.
    """
    if sys.platform != "win32":
        return

    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            import ctypes
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def main():

    _enable_windows_dpi_awareness()

    window = tk.Tk()

    window.title("Mentor AI")

    window.geometry(
        f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
    )

    apply_dark_combobox_theme(window)

    settings = load_settings()

    # Eski settings.json dosyalarında kalmış olabilecek "Light" gibi artık
    # var olmayan bir tema değerini sessizce "Dark"a çeviriyoruz.
    if settings.get("theme") not in ("Dark", "System (Coming Soon)"):
        settings["theme"] = "Dark"
    ai_client = OpenAIClient()
    planning_history = []
    navigation_stack = []

    # ==================================
    # TOP FRAME
    # ==================================

    top_frame = tk.Frame(
        window,
        bg="#181825",
        height=64
    )

    top_frame.pack(
        fill="x",
        side="top"
    )

    top_frame.pack_propagate(False)

    # ==================================
    # MAIN FRAME
    # ==================================

    main_frame = tk.Frame(
        window,
        bg=DRACULA_WINDOW_BG
    )

    main_frame.pack(
        fill="both",
        expand=True
    )

    left_frame = tk.Frame( main_frame,
        width=LEFT_PANEL_WIDTH,
        height=WINDOW_HEIGHT,
        bg=DRACULA_EDITOR_BG
    )

    left_frame.pack(side = "left" , fill="both",expand=True)

    # Sol (kod editörü) ve sağ (mentor) panel arasındaki ince ayırıcı çizgi
    divider = tk.Frame(main_frame, width=2, bg=DIVIDER_COLOR)
    divider.pack(side="left", fill="y")

    right_frame = tk.Frame(main_frame,
        width=RIGHT_PANEL_WIDTH,
        height=700,
        bg= DRACULA_PANEL_BG )

    right_frame.pack(side="right",fill="both" ,expand =True)

    # ==================================
    # CODE EDITOR + SATIR NUMARALARI
    # ==================================

    # --- Araç çubuğu: Run butonu + hata/durum etiketi ---
    editor_toolbar = tk.Frame(left_frame, bg="#1E1F2E", height=36)
    editor_toolbar.pack(side="top", fill="x")
    editor_toolbar.pack_propagate(False)

    run_button = tk.Button(
        editor_toolbar,
        text="▶ Run",
        bg="#2E7D46",
        fg="#FFFFFF",
        activebackground="#379754",
        activeforeground="#FFFFFF",
        relief="flat",
        bd=0,
        padx=14,
        pady=3,
        cursor="hand2",
        font=("Segoe UI", 9, "bold")
    )
    run_button.pack(side="left", padx=10, pady=5)
    run_button.bind("<Enter>", lambda e: run_button.config(bg="#379754"))
    run_button.bind("<Leave>", lambda e: run_button.config(bg="#2E7D46"))

    editor_status_label = tk.Label(
        editor_toolbar,
        text="",
        bg="#1E1F2E",
        fg=TEXT_SECONDARY,
        font=("Segoe UI", 9)
    )
    editor_status_label.pack(side="left", padx=10)

    # --- Terminal paneli (Run çıktısı stdout/stderr burada gösterilir) ---
    terminal_frame = tk.Frame(left_frame, bg="#12131C", height=170)
    terminal_frame.pack(side="bottom", fill="x")
    terminal_frame.pack_propagate(False)

    terminal_header = tk.Label(
        terminal_frame,
        text="Terminal",
        bg="#12131C",
        fg=TEXT_SECONDARY,
        font=("Segoe UI", 9, "bold"),
        anchor="w"
    )
    terminal_header.pack(fill="x", padx=10, pady=(6, 2))

    terminal_output = tk.Text(
        terminal_frame,
        bg="#12131C",
        fg=CODE_EDITOR_FG,
        insertbackground=CODE_EDITOR_FG,
        font=CODE_FONT,
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        wrap="word",
        state="disabled"
    )
    terminal_output.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    terminal_output.tag_configure("stdout_text", foreground=CODE_EDITOR_FG)
    terminal_output.tag_configure("stderr_text", foreground="#E06C75")
    terminal_output.tag_configure("info_text", foreground="#61AFEF")

    def write_to_terminal(text, tag="stdout_text"):
        terminal_output.config(state="normal")
        terminal_output.insert("end", text, tag)
        terminal_output.see("end")
        terminal_output.config(state="disabled")

    def clear_terminal():
        terminal_output.config(state="normal")
        terminal_output.delete("1.0", "end")
        terminal_output.config(state="disabled")

    def run_code():
        code = code_editor.get("1.0", "end-1c")

        clear_terminal()
        write_to_terminal("Running...\n", "info_text")
        run_button.config(state="disabled")

        def worker():
            tmp_path = None
            try:
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    suffix=".py",
                    delete=False,
                    encoding="utf-8"
                ) as tmp_file:
                    tmp_file.write(code)
                    tmp_path = tmp_file.name

                result = subprocess.run(
                    [sys.executable, tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                window.after(
                    0,
                    lambda: show_run_result(result.stdout, result.stderr)
                )

            except subprocess.TimeoutExpired:
                window.after(
                    0,
                    lambda: show_run_result(
                        "", "Execution timed out (10 second limit).\n"
                    )
                )
            except Exception as exc:
                window.after(0, lambda: show_run_result("", str(exc) + "\n"))
            finally:
                if tmp_path:
                    try:
                        os.remove(tmp_path)
                    except OSError:
                        pass

        threading.Thread(target=worker, daemon=True).start()

    def show_run_result(stdout_text, stderr_text):
        clear_terminal()

        if stdout_text:
            write_to_terminal(stdout_text, "stdout_text")

        if stderr_text:
            write_to_terminal(stderr_text, "stderr_text")

        if not stdout_text and not stderr_text:
            write_to_terminal("(no output)\n", "info_text")

        run_button.config(state="normal")

    run_button.config(command=run_code)

    editor_container = tk.Frame(left_frame, bg=DRACULA_EDITOR_BG)
    editor_container.pack(fill="both", expand=True)

    line_numbers = tk.Text(
        editor_container,
        width=4,
        padx=6,
        bg="#1E1F2E",
        fg="#6B7089",
        font=CODE_FONT,
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        state="disabled",
        takefocus=0
    )
    line_numbers.pack(side="left", fill="y")

    code_editor = tk.Text(
        editor_container,
        width=EDITOR_WIDTH,
        height=EDITOR_HEIGHT,
        bg=DRACULA_EDITOR_BG,
        fg=CODE_EDITOR_FG,
        font=CODE_FONT,
        insertbackground=EDITOR_CURSOR,
        selectbackground=EDITOR_SELECTION,
        borderwidth=0,
        wrap="none"
    )
    code_editor.pack(side="left", fill="both", expand=True)

    configure_syntax_tags(code_editor, CODE_FONT)

    # Söz dizimi hatası olan satırı işaretlemek için kullanılan etiket
    # (hafif kırmızı arkaplan + alt çizgi).
    code_editor.tag_configure(
        "error_line",
        underline=True,
        background="#3A2328"
    )

    def update_line_numbers(event=None):
        line_count = int(code_editor.index("end-1c").split(".")[0])

        line_numbers.config(state="normal")
        line_numbers.delete("1.0", "end")
        line_numbers.insert(
            "1.0",
            "\n".join(str(n) for n in range(1, line_count + 1))
        )
        line_numbers.config(state="disabled")

        # Kod editörüyle aynı kaydırma konumunda kalsın
        line_numbers.yview_moveto(code_editor.yview()[0])

    def on_code_editor_scroll(*args):
        line_numbers.yview_moveto(code_editor.yview()[0])

    def check_syntax_errors():
        code_editor.tag_remove("error_line", "1.0", "end")

        code = code_editor.get("1.0", "end-1c")

        if not code.strip():
            editor_status_label.config(text="", fg=TEXT_SECONDARY)
            return

        try:
            compile(code, "<code_editor>", "exec")
            editor_status_label.config(text="No syntax errors", fg="#7FB77E")
        except SyntaxError as error:
            line_no = error.lineno or 1
            code_editor.tag_add("error_line", f"{line_no}.0", f"{line_no}.end")
            editor_status_label.config(
                text=f"Line {line_no}: {error.msg}",
                fg="#E06C75"
            )

    def on_code_editor_change(event=None):
        update_line_numbers()
        highlight_python_syntax(code_editor)
        check_syntax_errors()

    code_editor.bind("<KeyRelease>", on_code_editor_change)
    code_editor.bind("<MouseWheel>", lambda e: window.after(1, on_code_editor_scroll))
    code_editor.bind("<ButtonRelease>", lambda e: window.after(1, update_line_numbers))
    code_editor.bind("<Configure>", on_code_editor_change)

    update_line_numbers()
    highlight_python_syntax(code_editor)
    check_syntax_errors()



    def new_session_gui():
        code_editor.delete("1.0", tk.END)
        highlight_python_syntax(code_editor)
        update_line_numbers()
        check_syntax_errors()


    def open_file_gui():
        content = open_file()

        if content is None:
            return

        code_editor.delete("1.0", tk.END)
        code_editor.insert("1.0", content)
        highlight_python_syntax(code_editor)
        update_line_numbers()
        check_syntax_errors()



    def save_file_gui():
        content = code_editor.get("1.0", tk.END)
        save_file(content)



    content_frame = tk.Frame(right_frame,  bg=DRACULA_PANEL_BG)
    content_frame.pack(fill = "both", expand= True)

    welcome_frame = tk.Frame(content_frame, bg=DRACULA_PANEL_BG)
    welcome_frame.pack(fill = "both" , expand = True)

    welcome_frame.columnconfigure(0, weight=1)



    def plan_mode():
        clear_screen(welcome_frame)
        planning_history.clear()

        back_button = create_back_button(welcome_frame, home_screen)

        plan_it_label = tk.Label(
            welcome_frame,
            text="Let's Plan It!",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=HEADING_FONT
        )
        plan_it_label.grid(row=0, column=0, pady=7)

        describe_label = tk.Label(
            welcome_frame,
            text="What are you trying to build?",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=BODY_FONT
        )
        describe_label.grid(row=1, column=0, pady = 5)

        text_box = themed_textbox(welcome_frame, width=50, height=7)
        text_box.grid(row=2, column=0, pady = 7)

        continue_button = styled_button(welcome_frame, "Continue", lambda: continue_mode(text_box))
        continue_button.grid(row=3, column=0, pady = 7)

    def conversation_screen(project):

        clear_screen(welcome_frame)

        # Geri butonu ve AI çağrısı SIRALAMASI önemli: AI çağrısı hata
        # verirse (kota/ağ vb.) bile kullanıcının geri dönebileceği bir
        # buton her zaman ekranda olsun diye bunu en başta oluşturuyoruz.
        back_button = create_back_button(
            welcome_frame,
            plan_mode
        )

        planning_history.clear()

        planning_history.append({
            "role": "user",
            "content": project
        })

        try:
            first_response = ai_client.get_planning_response(
                planning_history
            )
        except Exception:
            first_response = (
                "I couldn't reach the AI right now.\n\n"
                "This usually means the OpenAI API key has no available "
                "quota/credits, or there is no internet connection.\n"
                "Please check your OpenAI account billing or your "
                "connection, then try again."
            )

        planning_history.append({
            "role": "assistant",
            "content": first_response
        })

        planning_session_label = tk.Label(
            welcome_frame,
            text="Planning Session",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=HEADING_FONT
        )
        planning_session_label.grid(row=1, column=0, pady=(10, 5))

        project_idea_label = tk.Label(
            welcome_frame,
            text="Project Idea",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=SUBHEADING_FONT
        )
        project_idea_label.grid(row=2, column=0, pady=(5, 5))

        project_text_box = themed_textbox(
            welcome_frame,
            width=50,
            height=5
        )

        project_text_box.insert(
            "1.0",
            project
        )

        project_text_box.config(
            state="disabled"
        )

        project_text_box.grid(row=3, column=0, pady=(0, 10))

        ai_explanation_label = tk.Label(
            welcome_frame,
            text="Mentor AI",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=SUBHEADING_FONT
        )
        ai_explanation_label.grid(row=4, column=0, pady=(5, 5))

        ai_response_box = themed_textbox(
            welcome_frame,
            width=50,
            height=8
        )

        ai_response_box.insert(
            "1.0",
            first_response
        )

        ai_response_box.config(
            state="disabled"
        )

        ai_response_box.grid(row=5, column=0, pady=(0, 10))

        response_label = tk.Label(
            welcome_frame,
            text="Your Response",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=SUBHEADING_FONT
        )

        response_label.grid(row=6, column=0, pady=(5, 5))

        user_response_box = themed_textbox(
            welcome_frame,
            width=50,
            height=5
        )

        user_response_box.grid(row=7, column=0, pady=(0, 10))

        def send_planning_message():
            user_message = user_response_box.get(
                "1.0",
                "end"
            ).strip()

            if not user_message:
                messagebox.showwarning(
                    "Empty Input",
                    "Please enter something first."
                )
                return

            planning_history.append({
                "role": "user",
                "content": user_message
            })

            try:
                response = ai_client.get_planning_response(
                    planning_history
                )
            except Exception:
                response = (
                    "I couldn't reach the AI right now.\n\n"
                    "This usually means the OpenAI API key has no "
                    "available quota/credits, or there is no internet "
                    "connection. Please check and try again."
                )

            planning_history.append({
                "role": "assistant",
                "content": response
            })

            ai_response_box.config(
                state="normal"
            )

            ai_response_box.delete(
                "1.0",
                "end"
            )

            ai_response_box.insert(
                "1.0",
                response
            )

            ai_response_box.config(
                state="disabled"
            )

            user_response_box.delete(
                "1.0",
                "end"
            )

        continue_button = styled_button(
            welcome_frame,
            "Continue",
            send_planning_message
        )

        continue_button.grid(row=8, column=0, pady=(5, 10))

    def continue_mode(text_box):

        project = text_box.get(
            "1.0",
            "end"
        ).strip()

        if not project:
            messagebox.showwarning(
                "Empty Input",
                "Please describe what you want to build."
            )
            return

        conversation_screen(project)



    def clear_screen(frame):
        for widget in frame.winfo_children():
            widget.destroy()


    def home_screen():
        clear_screen(welcome_frame)

        title_label = tk.Label(
            welcome_frame,
            text="✦ Mentor AI ✦",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=TITLE_FONT
        )
        title_label.grid(row=0, column=0, pady=(30, 2))

        title_accent = tk.Frame(welcome_frame, width=90, height=3, bg=AI_BOX_BORDER)
        title_accent.grid(row=1, column=0, pady=(0, 10))

        subtitle_label = tk.Label(
            welcome_frame,
            text="Think. Build. Learn.",
            bg=DRACULA_PANEL_BG,
            fg=AI_BOX_BORDER,
            font=BODY_FONT
        )
        subtitle_label.grid(row=2, column=0)

        goal_label = tk.Label(
            welcome_frame,
            text="What would you like to work on today?",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=BODY_FONT
        )
        goal_label.grid(row=3, column=0, pady=(14, 0))

        def start_ai(text):

            if not text:
                messagebox.showwarning(
                    "Empty Input",
                    "Please enter something first."
                )
                return

            try:
                intent = ai_client.classify_intent(text)
            except Exception:
                messagebox.showerror(
                    "Connection Error",
                    "I couldn't reach the AI right now.\n\n"
                    "This usually means the OpenAI API key has no "
                    "available quota/credits, or there is no internet "
                    "connection. Please check and try again."
                )
                return

            if intent == "PLANNING":
                conversation_screen(text)
            else:
                direct_answer_screen(text)

        def direct_answer_screen(question):

            clear_screen(welcome_frame)

            back_button = create_back_button(
                welcome_frame,
                home_screen
            )

            title_label = tk.Label(
                welcome_frame,
                text="Mentor AI",
                bg=DRACULA_PANEL_BG,
                fg=PRIMARY,
                font=HEADING_FONT
            )

            title_label.grid(row=1, column=0, pady=(20, 10))

            question_label = tk.Label(
                welcome_frame,
                text="Your Question",
                bg=DRACULA_PANEL_BG,
                fg=TEXT,
                font=SUBHEADING_FONT
            )

            question_label.grid(row=2, column=0, pady=(10, 5))

            question_box = themed_textbox(
                welcome_frame,
                width=60,
                height=5
            )

            question_box.insert(
                "1.0",
                question
            )

            question_box.grid(row=3, column=0, pady=(0, 15))

            try:
                answer = ai_client.get_a_direct_answer(question)
            except Exception:
                answer = (
                    "I couldn't reach the AI right now.\n\n"
                    "This usually means the OpenAI API key has no "
                    "available quota/credits, or there is no internet "
                    "connection. Please check and try again."
                )

            answer_label = tk.Label(
                welcome_frame,
                text="Mentor AI",
                bg=DRACULA_PANEL_BG,
                fg=PRIMARY,
                font=SUBHEADING_FONT
            )

            answer_label.grid(row=4, column=0, pady=(10, 5))

            answer_box = themed_textbox(
                welcome_frame,
                width=70,
                height=12
            )

            answer_box.insert(
                "1.0",
                answer
            )

            answer_box.config(
                state="disabled"
            )

            answer_box.grid(row=5, column=0, pady=(0, 20))

        ai_input = create_ai_input(welcome_frame, on_send=start_ai)

        ai_input.grid(
            row=4,
            column=0,
            padx=20,
            pady=20
        )

        mode_frame = tk.Frame(welcome_frame, bg=DRACULA_PANEL_BG)
        mode_frame.grid(row=5, column=0, pady=20)

        create_gradient_button(
            mode_frame,
            "Start a New Project",
            plan_mode
        ).pack(pady=7)

        create_gradient_button(
            mode_frame,
            "Learn Mode",
            learn_mode
        ).pack(pady=7)

        create_gradient_button(
            mode_frame,
            "Debug Mode",
            debug_mode
        ).pack(pady=7)

        create_gradient_button(
            mode_frame,
            "Hint Mode",
            open_hint_mode
        ).pack(pady=7)


    def back_to_home():
        home_screen()

    def open_settings():

        clear_screen(welcome_frame)

        back_button = create_back_button(welcome_frame, home_screen)

        settings_title = tk.Label(
            welcome_frame,
            text="Settings",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=TITLE_FONT
        )

        settings_title.grid(row=0, column=0, pady=(15, 20))

        ai_label = tk.Label(
            welcome_frame,
            text="AI Model",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=BODY_FONT
        )

        ai_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20
        )

        model_combobox = ttk.Combobox(
            welcome_frame,
            values=[
                "GPT-4.1 Mini"
            ],
            state="readonly",
            width=25,
            style="Dark.TCombobox"
        )


        model_combobox.grid(
            row=2,
            column=0,
            padx=20,
            pady=(5, 20),
            sticky="w"
        )

        # ---------------- Appearance ----------------

        theme_label = tk.Label(
            welcome_frame,
            text="Theme",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=BODY_FONT
        )

        theme_label.grid(
            row=3,
            column=0,
            sticky="w",
            padx=20
        )

        theme_combobox = ttk.Combobox(
            welcome_frame,
            values=[
                "Dark",
                "System (Coming Soon)"
            ],
            state="readonly",
            width=25,
            style="Dark.TCombobox"
        )

        theme_combobox.grid(
            row=4,
            column=0,
            padx=20,
            pady=(5, 20),
            sticky="w"
        )

        font_label = tk.Label(
            welcome_frame,
            text="Font Size",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=BODY_FONT
        )

        font_label.grid(
            row=5,
            column=0,
            sticky="w",
            padx=20
        )

        font_combobox = ttk.Combobox(
            welcome_frame,
            values=[
                "Small",
                "Medium",
                "Large"
            ],
            state="readonly",
            width=25,
            style="Dark.TCombobox"
        )

        font_combobox.grid(
            row=6,
            column=0,
            padx=20,
            pady=(5, 20),
            sticky="w"
        )

        model_combobox.set(settings["model"])
        theme_combobox.set(settings["theme"])
        font_combobox.set(settings["font_size"])


        def save_gui_settings():
            settings["model"] = model_combobox.get()
            settings["theme"] = theme_combobox.get()
            settings["font_size"] = font_combobox.get()

            save_settings(settings)

            messagebox.showinfo(
                "Settings",
                "Settings saved successfully."
            )

        save_button = styled_button(
            welcome_frame,
            "Save Settings",
            save_gui_settings
        )
        save_button.grid(
            row=7,
            column=0,
            pady=20
        )

        def reset_gui_settings():

            reset_settings()

            settings.clear()
            settings.update(load_settings())

            model_combobox.set(settings["model"])
            theme_combobox.set(settings["theme"])
            font_combobox.set(settings["font_size"])

            messagebox.showinfo(
                "Settings",
                "Settings restored to default."
            )

        reset_button = styled_button(
            welcome_frame,
            "Reset",
            reset_gui_settings
        )

        reset_button.grid(row=8, column=0, pady=5)

        about_title = tk.Label(
            welcome_frame,
            text="About",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=HEADING_FONT
        )

        about_title.grid(row=9, column=0, pady=12)

        mentor_ai_title_label = tk.Label(
            welcome_frame, text="Mentor AI", bg=DRACULA_PANEL_BG, fg=TEXT
        )
        mentor_ai_title_label.grid(row=10, column=0, pady= 10)

        version1_label = tk.Label(
            welcome_frame, text="Version 1.0", bg=DRACULA_PANEL_BG, fg=TEXT_SECONDARY
        )
        version1_label.grid(row=11, column=0, pady=10)

        developer_label = tk.Label(
            welcome_frame, text="Developer", bg=DRACULA_PANEL_BG, fg=TEXT_SECONDARY
        )
        developer_label.grid(row=12, column=0, pady=7)

        founder_of_mentor_ai_label = tk.Label(
            welcome_frame, text="Sena DEMİRCİ", bg=DRACULA_PANEL_BG, fg=TEXT
        )
        founder_of_mentor_ai_label.grid(row=13, column=0, pady=7)

        built_label = tk.Label(
            welcome_frame, text="Built with Python & Tkinter", bg=DRACULA_PANEL_BG, fg=TEXT_SECONDARY
        )
        built_label.grid(row=14, column=0, pady=7)

    # ==================================
    # FILE BUTTON
    # ==================================

    def show_recent_projects():
        messagebox.showinfo(
            "Recent Projects",
            "This feature is coming soon."
        )

    file_button = create_file_button(
        top_frame,
        lambda button: show_file_menu(
            button,
            new_session_gui,
            open_file_gui,
            show_recent_projects,
            save_file_gui,
            lambda: exit_app(window)
        )
    )

    # ==================================
    # SETTINGS BUTTON
    # ==================================

    settings_button = create_settings_button(
        top_frame,
        open_settings
    )


    def learn_mode():
        global learn_mode_text_box

        clear_screen(welcome_frame)

        back_button = create_back_button(welcome_frame, home_screen)

        learn_mode_title_label = tk.Label(
            welcome_frame,
            text="Learn Mode",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=HEADING_FONT
        )

        learn_mode_title_label.grid(row=0, column=0, pady=7)

        learn_mode_description_label = tk.Label(
            welcome_frame,
            text="Learn Mode Description",
            bg=DRACULA_PANEL_BG,
            fg=TEXT_SECONDARY,
            font=BODY_FONT
        )
        learn_mode_description_label.grid(row=1, column=0, pady=7)

        learn_mode_text_box = themed_textbox(welcome_frame, width=50, height=7)
        learn_mode_text_box.grid(row=2, column=0, pady=7)

        learn_mode_button = styled_button(
            welcome_frame,
            "Continue",
            start_learning
        )
        learn_mode_button.grid(row=3, column=0, pady=7)

    def start_learning():
        global follow_up_text
        global topic
        global ai_response
        global message_text

        topic =  learn_mode_text_box.get("1.0" , "end" ).strip()

        ai_response = generate_explanation(topic)

        clear_screen(welcome_frame)

        back_button = create_back_button(welcome_frame, learn_mode)

        learn_session_label = tk.Label(
            welcome_frame,
            text="Learn Session",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=HEADING_FONT
        )
        learn_session_label.grid(row=0, column=0, pady=7)

        today_label = tk.Label(
            welcome_frame,
            text="Today we'll learn:",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=BODY_FONT
        )
        today_label.grid(row=1, column=0, pady=7)

        topic_label = tk.Label(
            welcome_frame,
            text=topic,
            bg=DRACULA_PANEL_BG,
            fg=PRIMARY,
            font=SUBHEADING_FONT
        )
        topic_label.grid(row=2, column=0, pady=7)

        message_text = themed_textbox(welcome_frame, width=60, height=15)
        message_text.grid(row=3, column=0, pady=7)
        message_text.insert("1.0", ai_response)
        message_text.config(state = "disabled")

        scrollbar = tk.Scrollbar(welcome_frame)
        scrollbar.grid(row=3, column=1, sticky="ns")
        scrollbar.config(command=message_text.yview)
        message_text.config(yscrollcommand=scrollbar.set)

        input_frame = tk.Frame(welcome_frame, bg=DRACULA_PANEL_BG)
        input_frame.grid(row=4, column=0, pady=20, sticky = "ew")
        input_frame.columnconfigure(0, weight=1)

        follow_up_text = themed_textbox(input_frame, width=50, height=3)
        follow_up_text.grid(row=0, column=0,sticky="ew")

        send_button = create_icon_button(
            input_frame,
            "up_arrow_button.png",
            ask_follow_up,
            size=40
        )
        send_button.grid(row=0, column=1, padx=5)

    def ask_follow_up():
        question = follow_up_text.get("1.0", "end").strip()

        answer = generate_follow_up(
            topic,
            ai_response,
            question
        )

        message_text.config(state="normal")

        message_text.insert("end", "\n\nYou:\n")
        message_text.insert("end", question)

        message_text.insert("end", "\n\nMentor AI:\n")
        message_text.insert("end", answer)

        message_text.config(state="disabled")

        follow_up_text.delete("1.0", "end")


    def generate_explanation(topic):
        from openai_client import OpenAIClient

        client = OpenAIClient()
        return client.get_learning_explanation(topic)

    def generate_follow_up(topic, explanation, question):
        from openai_client import OpenAIClient

        client = OpenAIClient()

        return client.get_follow_up_answer(
            topic,
            explanation,
            question
        )

    def open_hint_mode():
        global hint_mode_first_text_box
        global hint_mode_second_text_box
        global hint_mode_third_text_box

        print("Hint Mode opened")

        clear_screen(welcome_frame)

        back_button = create_back_button(welcome_frame, home_screen)

        hint_mode_title_label = tk.Label(
            welcome_frame,
            text="Hint Mode",
            bg=DRACULA_PANEL_BG,
            fg=PRIMARY,
            font=SUBHEADING_FONT
        )
        hint_mode_title_label.grid(row=0, column=0, pady=7)

        hint_mode_question_label = tk.Label(
            welcome_frame,
            text="What Are You Building? ",
            bg=DRACULA_PANEL_BG,
            fg=PRIMARY,
            font=SUBHEADING_FONT
        )
        hint_mode_question_label.grid(row=1, column=0, pady=7)


        hint_mode_first_text_box = themed_textbox(welcome_frame, width=50, height=4)
        hint_mode_first_text_box.grid(row=2, column=0, pady=7)

        hint_mode_problem_label = tk.Label(
            welcome_frame,
            text="Paste only the relevant code.",
            bg=DRACULA_PANEL_BG,
            fg=PRIMARY,
            font=SUBHEADING_FONT
        )
        hint_mode_problem_label.grid(row=3, column=0, pady=(10, 3))


        hint_mode_second_text_box = themed_textbox(welcome_frame, width=50, height=4)
        hint_mode_second_text_box.grid(row=4, column=0, pady=(0, 10))


        hint_mode_second_text_box.insert(
            "1.0",
            "Example:\nI don't know why my loop never stops."
        )

        hint_mode_second_text_box.config(fg=AI_BOX_PLACEHOLDER_FG)
        hint_mode_second_text_box.bind("<FocusIn>", clear_placeholder)

        hint_mode_code_label = tk.Label(
            welcome_frame,
            text="Paste only the relevant code.",
            bg=DRACULA_PANEL_BG,
            fg=PRIMARY,
            font=SUBHEADING_FONT
        )
        hint_mode_code_label.grid(row=5, column=0, pady=(5, 3))

        hint_mode_third_text_box = themed_textbox(welcome_frame, width=50, height=6)
        hint_mode_third_text_box.grid(row=6, column=0, pady=(0, 10))

        hint_mode_third_text_box.insert(
            "1.0",
            "Only include the code related to your problem."
        )

        hint_mode_third_text_box.config(fg=AI_BOX_PLACEHOLDER_FG)
        hint_mode_third_text_box.bind("<FocusIn>", clear_placeholder)

        hint_mode_button = styled_button(
            welcome_frame,
            "Get Hint",
            start_hint_mode
        )

        hint_mode_button.grid(row=7, column=0, pady=10)

    def clear_placeholder(event):
        text_box = event.widget

        current_text = text_box.get("1.0", "end-1c")

        if current_text == "Example:\nI don't know why my loop never stops.":
            text_box.delete("1.0", "end")
            text_box.config(fg=AI_BOX_FG)

        elif current_text == "Only include the code related to your problem.":
            text_box.delete("1.0", "end")
            text_box.config(fg=AI_BOX_FG)

        elif current_text == "Paste only the code related to your issue.":
            text_box.delete("1.0", "end")
            text_box.config(fg=AI_BOX_FG)

        elif current_text == "Example:\nTypeError: unsupported operand type(s)...":
            text_box.delete("1.0", "end")
            text_box.config(fg=AI_BOX_FG)

    def restore_placeholder(event):
        text_box = event.widget

        if text_box.get("1.0", "end-1c").strip() == "":
            text_box.config(fg=AI_BOX_PLACEHOLDER_FG)



    def start_hint_mode():
        print("Hint Mode started")

        building = hint_mode_first_text_box.get("1.0", "end").strip()
        problem = hint_mode_second_text_box.get("1.0", "end").strip()
        code = hint_mode_third_text_box.get("1.0", "end").strip()

        if building == "":
            messagebox.showwarning(
                "Missing Information",
                "Please describe what you are building."
            )
            return

        if problem.strip() == "" or problem == "Example:\nI don't know why my loop never stops.":
            messagebox.showwarning(
                "Missing Information",
                "Please explain where you are stuck."
            )
            return

        if code.strip() == "" or code == "Only include the code related to your problem.":
            messagebox.showwarning(
                "Missing Information",
                "Please paste the relevant code."
            )
            return

        client = OpenAIClient()

        hint = client.get_a_hint(
            building,
            problem,
            code
        )

        show_hint_session(
            building,
            problem,
            code,
            hint
        )

    def show_hint_session(building, problem, code, hint):
        print("show_hint_session called")
        clear_screen(welcome_frame)

        back_button = create_back_button(welcome_frame, open_hint_mode)


        title = tk.Label(welcome_frame, text="Hint Session", bg=DRACULA_PANEL_BG, fg=TEXT, font=HEADING_FONT)
        title.grid(row=0, column=0, pady=10)


        building_label = tk.Label(
            welcome_frame,
            text=f"Building: {building}",
            bg=DRACULA_PANEL_BG,
            fg=TEXT_SECONDARY
        )
        building_label.grid(row=1, column=0, pady=7)


        hint_box = themed_textbox(welcome_frame, width=60, height=15)
        hint_box.grid(row=2, column=0, pady=7)

        hint_box.insert("1.0", hint)
        hint_box.config(state="disabled")



        follow_up_label = tk.Label(
            welcome_frame,
            text="Still stuck? Ask for another hint.",
            bg=DRACULA_PANEL_BG,
            fg=TEXT_SECONDARY
        )
        follow_up_label.grid(row=3, column=0, pady=(15, 5))


        follow_up_box = themed_textbox(
            welcome_frame,
            width=60,
            height=4
        )
        follow_up_box.grid(row=4, column=0, pady=5)


        def ask_another_hint():
            follow_up_question = follow_up_box.get("1.0", "end").strip()

            if not follow_up_question:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter a follow-up question."
                )
                return



            client = OpenAIClient()

            new_hint = client.get_follow_up_hint(
                building,
                problem,
                code,
                hint,
                follow_up_question
            )


            hint_box.config(state="normal")
            hint_box.delete("1.0", "end")
            hint_box.insert("1.0", new_hint)
            hint_box.config(state="disabled")


        follow_up_button = styled_button(
            welcome_frame,
            "Ask Again",
            ask_another_hint
        )

        follow_up_button.grid(row=5, column=0, pady=10)


    def debug_mode():

        clear_screen(welcome_frame)


        back_button = create_back_button(welcome_frame, home_screen)


        debug_mode_label = tk.Label(welcome_frame, text="Debug Mode", bg=DRACULA_PANEL_BG, fg=TEXT, font=HEADING_FONT)
        debug_mode_label.grid(row = 0, column = 0, pady = 10)

        debug_mode_code_label = tk.Label(welcome_frame, text="Paste your code here.", bg=DRACULA_PANEL_BG, fg=TEXT_SECONDARY)
        debug_mode_code_label.grid(row = 1, column = 0, pady = 10)

        debug_mode_code_paste_text_box = themed_textbox(welcome_frame, width=60, height=6)
        debug_mode_code_paste_text_box.grid(row=2 , column = 0, pady = 10)

        debug_mode_code_paste_text_box.insert("1.0", "Paste only the code related to your issue." )
        debug_mode_code_paste_text_box.config(fg=AI_BOX_PLACEHOLDER_FG)
        debug_mode_code_paste_text_box.bind("<FocusIn>", clear_placeholder)


        debug_mode_error_explanation_label = tk.Label(
            welcome_frame,
            text="What error do you get?" "\n" "(Please paste the terminal explanation here)",
            bg=DRACULA_PANEL_BG,
            fg=TEXT_SECONDARY
        )
        debug_mode_error_explanation_label.grid(row= 3,column=0, pady = 10)


        debug_mode_error_explanation_text_box = themed_textbox(welcome_frame, width=60, height=15)
        debug_mode_error_explanation_text_box.grid(row=4 , column = 0, pady = 10)


        debug_mode_error_explanation_text_box.insert(
            "1.0",
            "Example:\nTypeError: unsupported operand type(s)..."
        )

        debug_mode_error_explanation_text_box.config(fg=AI_BOX_PLACEHOLDER_FG)
        debug_mode_error_explanation_text_box.bind("<FocusIn>", clear_placeholder)


        def start_debug():
            print("Debug Mode started")

            code = debug_mode_code_paste_text_box.get("1.0", "end").strip()
            error = debug_mode_error_explanation_text_box.get("1.0", "end").strip()


            if code == "" or code == "Paste only the code related to your issue.":
                messagebox.showwarning(
                    "Missing Information",
                    "Please paste the relevant code here."

                )
                return
            if error == "" or error == "Example:\nTypeError: unsupported operand type(s)...":
                messagebox.showwarning(
                    "Missing Information",
                    "Please describe the error."
                )
                return

            client = OpenAIClient()
            debug_help = client.get_debug_help(code, error)
            show_debug_session(code, error, debug_help)


        debug_error_button = styled_button(welcome_frame, "Debug", start_debug)
        debug_error_button.grid(row=5, column=0, pady=10)



    def show_debug_session( code , error , debug_help ):
        clear_screen(welcome_frame)

        back_button = create_back_button(welcome_frame, debug_mode)

        show_debug_session_label = tk.Label(welcome_frame, text="Debug Session", bg=DRACULA_PANEL_BG, fg=TEXT, font=HEADING_FONT)
        show_debug_session_label.grid(row = 0, column = 0, pady = 10)

        your_error_label = tk.Label(welcome_frame, text="Your Error", bg=DRACULA_PANEL_BG, fg=TEXT_SECONDARY)
        your_error_label.grid(row = 1, column = 0, pady = 10)

        error_box = themed_textbox(welcome_frame, width=60, height=6)
        error_box.grid(row=2, column=0, pady=7)
        error_box.insert("1.0", error)
        error_box.config(state="disabled")

        ai_analysis_label = tk.Label(welcome_frame, text="AI Analysis", bg=DRACULA_PANEL_BG, fg=TEXT_SECONDARY)
        ai_analysis_label.grid(row = 3, column = 0, pady = 10)


        ai_analysis_text_box = themed_textbox(welcome_frame, width=60, height=6)
        ai_analysis_text_box.grid(row=4 , column = 0, pady = 10)
        ai_analysis_text_box.insert("1.0", debug_help)
        ai_analysis_text_box.config(state="disabled")


        help_label = tk.Label(welcome_frame, text="Still need help?", bg=DRACULA_PANEL_BG, fg=TEXT_SECONDARY)
        help_label.grid(row = 5, column = 0, pady = 10)

        another_question_text_box = themed_textbox(welcome_frame, width=60, height=4)
        another_question_text_box.grid(row=6 , column = 0, pady = 10)


        def ask_another_debug():
            print("Ask Again clicked")
            follow_up_question = another_question_text_box.get("1.0", "end").strip()


            if not follow_up_question:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter a follow-up question."
                )
                return

            client = OpenAIClient()

            new_debug_help = client.get_follow_up_debug(
                code,
                error,
                debug_help,
                follow_up_question
            )
            print(new_debug_help)


            ai_analysis_text_box.config(state="normal")
            ai_analysis_text_box.delete("1.0", "end")
            ai_analysis_text_box.insert("1.0", new_debug_help)
            ai_analysis_text_box.config(state="disabled")


        ask_again_button = styled_button(
            welcome_frame,
            "Ask Again",
            ask_another_debug
        )
        ask_again_button.grid(row=7, column=0, pady=10)


    navigation_stack.append(home_screen)

    home_screen()

    window.mainloop()

main()