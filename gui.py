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

from ui.ui.fonts import HEADING_FONT


def main():
    window = tk.Tk()
    window.title("Mentor AI")
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    settings = load_settings()

    navigation_stack = []

    top_frame = tk.Frame(window, bg=DRACULA_WINDOW_BG)
    top_frame.pack(fill = "x")

    button1 = tk.Button(top_frame, text = "File")
    button1.pack(side = "left")


    main_frame = tk.Frame(window, bg=DRACULA_WINDOW_BG )
    main_frame.pack(fill="both", expand=True)

    left_frame = tk.Frame( main_frame,
        width=LEFT_PANEL_WIDTH,
        height=WINDOW_HEIGHT,
        bg=DRACULA_EDITOR_BG
    )

    left_frame.pack(side = "left" , fill="both",expand=True)

    right_frame = tk.Frame(main_frame,
        width=RIGHT_PANEL_WIDTH,
        height=700,
        bg= DRACULA_PANEL_BG )

    right_frame.pack(side="right",fill="both" ,expand =True)

    code_editor = tk.Text(
        left_frame,
        width=EDITOR_WIDTH,
        height=EDITOR_HEIGHT,
        bg=DRACULA_EDITOR_BG,
        fg=TEXT,
        font=CODE_FONT,
        insertbackground=EDITOR_CURSOR,
        selectbackground=EDITOR_SELECTION,
        borderwidth=0
    )
    code_editor.pack(fill="both")



    def new_session_gui():
        code_editor.delete("1.0", tk.END)



    def open_file_gui():
        content = open_file()

        if content is None:
            return

        code_editor.delete("1.0", tk.END)
        code_editor.insert("1.0", content)



    def save_file_gui():
        content = code_editor.get("1.0", tk.END)
        save_file(content)

    file_menu = tk.Menu(window, tearoff=0)

    file_menu.add_command(
        label="New Session",
        command=new_session_gui
    )

    file_menu.add_command(
        label="Open File",
        command=open_file_gui
    )

    file_menu.add_command(
        label="Save",
        command=save_file_gui
    )

    file_menu.add_separator()

    file_menu.add_command(
        label="Exit",
        command=lambda: exit_app(window)
    )



    def show_file_menu(event):
        file_menu.tk_popup(event.x_root, event.y_root)

    button1.bind("<Button-1>", show_file_menu)


    content_frame = tk.Frame(right_frame,  bg=DRACULA_PANEL_BG)
    content_frame.pack(fill = "both", expand= True)

    welcome_frame = tk.Frame(content_frame, bg=DRACULA_PANEL_BG)
    welcome_frame.pack(fill = "both" , expand = True)

    welcome_frame.columnconfigure(0, weight=1)

    title_label = tk.Label(
        welcome_frame,
        text="Mentor AI",
        bg=DRACULA_PANEL_BG,
        fg=TEXT,
        font=TITLE_FONT
    )
    title_label.grid(row=0, column=0)

    subtitle_label = tk.Label(
        welcome_frame,
        text="Think. Build. Learn.",
        bg=DRACULA_PANEL_BG,
        fg=TEXT_SECONDARY,
        font=BODY_FONT
    )
    subtitle_label.grid(row=1, column=0)

    goal_label = tk.Label(
        welcome_frame,
        text="What would you like to work on today?",
        bg=DRACULA_PANEL_BG,
        fg=TEXT,
        font=BODY_FONT
    )
    goal_label.grid(row=3, column=0)



    def plan_mode():
        clear_screen(welcome_frame)

        clear_screen(welcome_frame)

        back_button = tk.Button(
            welcome_frame,
            text="← Back",
            command=home_screen
        )
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

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

        text_box = tk.Text(welcome_frame,width = 50 , height= 7)
        text_box.grid(row=2, column=0, pady = 7)

        continue_button = tk.Button(welcome_frame, text = "Continue", command = lambda: continue_mode(text_box))
        continue_button.grid(row=3, column=0, pady = 7)




    def conversation_screen(project):
        clear_screen(welcome_frame)


        back_button = tk.Button(
            welcome_frame,
            text="← Back",
            command=plan_mode
        )
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        planning_session_label = tk.Label(
            welcome_frame,
            text="Planning Session",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=HEADING_FONT
        )
        planning_session_label.grid(row=0, column=0, pady=7)

        project_idea_label = tk.Label(
            welcome_frame,
            text="Project Idea",
            bg=DRACULA_PANEL_BG,
            fg=TEXT,
            font=BODY_FONT
        )
        project_idea_label.grid(row=1, column=0, pady=7)

        ai_explanaition_label = tk.Label(
            welcome_frame,
            text="Great! Let's understand your project together.",
            bg=DRACULA_PANEL_BG,
            fg=TEXT_SECONDARY,
            font=BODY_FONT
        )
        ai_explanaition_label.grid(row=3, column=0, pady=7)

        project_text_box = tk.Text(welcome_frame, width=50, height=7)
        project_text_box.grid(row=2, column=0, pady=7)

        project_text_box.insert("1.0", project)


        continue_button = tk.Button( welcome_frame,
            text="Continue",
            command=lambda: next_question(project_text_box)
        )
        continue_button.grid(row=4, column=0, pady=7)




    def next_question(project_text_box):
        project = project_text_box.get("1.0", "end").strip()
        print(project)



    def continue_mode(text_box):
        print("Continue clicked")

        project = text_box.get("1.0", "end").strip()
        conversation_screen(project)



    def clear_screen(frame):
        for widget in frame.winfo_children():
            widget.destroy()


    def home_screen():
        clear_screen(welcome_frame)

        title_label = tk.Label(welcome_frame, text="Mentor AI")
        title_label.grid(row=0, column=0)

        subtitle_label = tk.Label(welcome_frame, text="Think. Build. Learn.")
        subtitle_label.grid(row=1, column=0)

        goal_label = tk.Label(welcome_frame, text="What would you like to work on today?")
        goal_label.grid(row=3, column=0)

        goal_entry = tk.Entry(welcome_frame)
        goal_entry.grid(row=4, column=0)


        start_button = tk.Button(
            welcome_frame,
            text="Start",
            command=start_ai
        )
        start_button.grid(row=5, column=0)

        mode_frame = tk.Frame(welcome_frame)
        mode_frame.grid(row=6, column=0, pady=20)

        tk.Button(
            mode_frame,
            text="Start a New Project",
            command=plan_mode
        ).pack(fill="x", pady=7)

        tk.Button(
            mode_frame,
            text="Learn Mode",
            command=learn_mode
        ).pack(fill="x", pady=7)

        tk.Button(
            mode_frame,
            text="Debug Mode",
            command=debug_mode
        ).pack(fill="x", pady=7)

        tk.Button(
            mode_frame,
            text="Hint Mode",
            command=open_hint_mode
        ).pack(fill="x", pady=7)


    def back_to_home():
        home_screen()


    goal_entry = tk.Entry(welcome_frame)
    goal_entry.grid(row=4, column=0)

    def start_ai():
        print(goal_entry.get())

    start_button = tk.Button(welcome_frame, text = "Start",
                             command = start_ai)

    start_button.grid(row=5, column=0)

    mode_frame = tk.Frame(welcome_frame)
    mode_frame.grid(row=6, column=0, pady=20)

    project_button = tk.Button(mode_frame,
        text="Start a New Project"  ,command=plan_mode
    )
    project_button.pack(fill="x" , pady=7)

    def open_settings():

        clear_screen(welcome_frame)

        back_button = tk.Button(
            welcome_frame,
            text="← Back",
            command=home_screen
        )
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

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
            width=25
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
                "Light",
                "Dark",
                "System (Coming Soon)"
            ],
            state="readonly",
            width=25
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
            width=25
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

        save_button = tk.Button(
            welcome_frame,
            text="Save Settings",
            command=save_gui_settings
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

        reset_button = tk.Button(
            welcome_frame,
            text="Reset",
            command=reset_gui_settings
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

        mentor_ai_title_label = tk.Label(welcome_frame, text="Mentor AI")
        mentor_ai_title_label.grid(row=10, column=0, pady= 10)

        version1_label = tk.Label(welcome_frame, text="Version 1.0")
        version1_label.grid(row=11, column=0, pady=10)

        developer_label = tk.Label(welcome_frame, text="Developer")
        developer_label.grid(row=12, column=0, pady=7)

        founder_of_mentor_ai_label = tk.Label(welcome_frame, text="Sena DEMİRCİ")
        founder_of_mentor_ai_label.grid(row=13, column=0, pady=7)

        built_label = tk.Label(welcome_frame, text="Built with Python & Tkinter")
        built_label.grid(row=14, column=0, pady=7)


    settings_button = tk.Button(
        top_frame,
        text="⚙",
        font=("Arial", 16),
        command=open_settings,
        borderwidth=0
    )

    settings_button.pack(side="right", padx=15)


    def learn_mode():
        global learn_mode_text_box

        clear_screen(welcome_frame)

        back_button = tk.Button(
            welcome_frame,
            text="← Back",
            command=home_screen
        )
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

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

        learn_mode_text_box = tk.Text(welcome_frame, width=50, height=7)
        learn_mode_text_box.grid(row=2, column=0, pady=7)

        learn_mode_button = tk.Button(
            welcome_frame,
            text="Continue",
            command=start_learning
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

        back_button = tk.Button(
            welcome_frame,
            text="← Back",
            command=learn_mode
        )
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

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

        message_text = tk.Text(welcome_frame,width=60, height= 15)
        message_text.grid(row=3, column=0, pady=7)
        message_text.insert("1.0", ai_response)
        message_text.config(state = "disabled")

        scrollbar = tk.Scrollbar(welcome_frame)
        scrollbar.grid(row=3, column=1, sticky="ns")
        scrollbar.config(command=message_text.yview)
        message_text.config(yscrollcommand=scrollbar.set)

        input_frame = tk.Frame(welcome_frame)
        input_frame.grid(row=4, column=0, pady=20, sticky = "ew")
        input_frame.columnconfigure(0, weight=1)

        follow_up_text = tk.Text(input_frame, width= 50, height = 3)
        follow_up_text.grid(row=0, column=0,sticky="ew")

        send_button = tk.Button(input_frame, width = 3 , text = "↑" , command = ask_follow_up)
        send_button.grid(row=0, column=1,padx=5)

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

        back_button = tk.Button(
            welcome_frame,
            text="← Back",
            command=home_screen
        )

        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

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


        hint_mode_first_text_box = tk.Text(welcome_frame, width=50, height=4)
        hint_mode_first_text_box.grid(row=2, column=0, pady=7)

        hint_mode_problem_label = tk.Label(
            welcome_frame,
            text="Paste only the relevant code.",
            bg=DRACULA_PANEL_BG,
            fg=PRIMARY,
            font=SUBHEADING_FONT
        )
        hint_mode_problem_label.grid(row=3, column=0, pady=(10, 3))


        hint_mode_second_text_box = tk.Text(welcome_frame, width=50, height=4)
        hint_mode_second_text_box.grid(row=4, column=0, pady=(0, 10))


        hint_mode_second_text_box.insert(
            "1.0",
            "Example:\nI don't know why my loop never stops."
        )

        hint_mode_second_text_box.config(fg="gray")
        hint_mode_second_text_box.bind("<FocusIn>", clear_placeholder)

        hint_mode_code_label = tk.Label(
            welcome_frame,
            text="Paste only the relevant code."
        )
        hint_mode_code_label.grid(row=5, column=0, pady=(5, 3))

        hint_mode_third_text_box = tk.Text(welcome_frame,width=50,height=6
        )
        hint_mode_third_text_box.grid(row=6, column=0, pady=(0, 10))

        hint_mode_third_text_box.insert(
            "1.0",
            "Only include the code related to your problem."
        )

        hint_mode_third_text_box.config(fg="gray")
        hint_mode_third_text_box.bind("<FocusIn>", clear_placeholder)

        hint_mode_button = tk.Button(
            welcome_frame,
            text="Get Hint",
            command=start_hint_mode
        )

        hint_mode_button.grid(row=7, column=0, pady=10)

    def clear_placeholder(event):
        text_box = event.widget

        current_text = text_box.get("1.0", "end-1c")

        if current_text == "Example:\nI don't know why my loop never stops.":
            text_box.delete("1.0", "end")
            text_box.config(fg="black")

        elif current_text == "Only include the code related to your problem.":
            text_box.delete("1.0", "end")
            text_box.config(fg="black")

        elif current_text == "Paste only the code related to your issue.":
            text_box.delete("1.0", "end")
            text_box.config(fg="black")

        elif current_text == "Example:\nTypeError: unsupported operand type(s)...":
            text_box.delete("1.0", "end")
            text_box.config(fg="black")

    def restore_placeholder(event):
        text_box = event.widget

        if text_box.get("1.0", "end-1c").strip() == "":
            text_box.config(fg="gray")



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

        back_button = tk.Button(
            welcome_frame,
            text="← Back",
            command=open_hint_mode
        )

        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)


        title = tk.Label(welcome_frame, text="Hint Session")
        title.grid(row=0, column=0, pady=10)


        building_label = tk.Label(
            welcome_frame,
            text=f"Building: {building}"
        )
        building_label.grid(row=1, column=0, pady=7)


        hint_box = tk.Text(welcome_frame, width=60, height=15)
        hint_box.grid(row=2, column=0, pady=7)

        hint_box.insert("1.0", hint)
        hint_box.config(state="disabled")



        follow_up_label = tk.Label(
            welcome_frame,
            text="Still stuck? Ask for another hint."
        )
        follow_up_label.grid(row=3, column=0, pady=(15, 5))


        follow_up_box = tk.Text(
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


        follow_up_button = tk.Button(
            welcome_frame,
            text="Ask Again",
            command=ask_another_hint
        )

        follow_up_button.grid(row=5, column=0, pady=10)


    def debug_mode():

        clear_screen(welcome_frame)


        back_button = tk.Button(
            welcome_frame,
            text="← Back",
            command=home_screen
        )
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)


        debug_mode_label = tk.Label(welcome_frame, text="Debug Mode")
        debug_mode_label.grid(row = 0, column = 0, pady = 10)

        debug_mode_code_label = tk.Label(welcome_frame, text="Paste your code here.")
        debug_mode_code_label.grid(row = 1, column = 0, pady = 10)

        debug_mode_code_paste_text_box = tk.Text(welcome_frame, width=60, height=6)
        debug_mode_code_paste_text_box.grid(row=2 , column = 0, pady = 10)

        debug_mode_code_paste_text_box.insert("1.0", "Paste only the code related to your issue." )
        debug_mode_code_paste_text_box.config(fg="gray")
        debug_mode_code_paste_text_box.bind("<FocusIn>", clear_placeholder)


        debug_mode_error_explanation_label = tk.Label(welcome_frame , text="What error do you get?" "\n"
               "(Please paste the terminal explanation here)"
        )
        debug_mode_error_explanation_label.grid(row= 3,column=0, pady = 10)


        debug_mode_error_explanation_text_box = tk.Text(welcome_frame, width=60, height=15)
        debug_mode_error_explanation_text_box.grid(row=4 , column = 0, pady = 10)


        debug_mode_error_explanation_text_box.insert(
            "1.0",
            "Example:\nTypeError: unsupported operand type(s)..."
        )

        debug_mode_error_explanation_text_box.config(fg="gray")
        debug_mode_error_explanation_text_box.bind("<FocusIn>", clear_placeholder)

        debug_mode_error_explanation_text_box.config(fg="gray")
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


        debug_error_button = tk.Button(welcome_frame, text="Debug", command=start_debug)
        debug_error_button.grid(row=5, column=0, pady=10)



    def show_debug_session( code , error , debug_help ):
        clear_screen(welcome_frame)

        back_button = tk.Button(
            welcome_frame,
            text="← Back",
            command=debug_mode
        )
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        show_debug_session_label = tk.Label(welcome_frame, text="Debug Session")
        show_debug_session_label.grid(row = 0, column = 0, pady = 10)

        your_error_label = tk.Label(welcome_frame, text="Your Error")
        your_error_label.grid(row = 1, column = 0, pady = 10)

        error_box = tk.Text(welcome_frame, width=60, height=6)
        error_box.grid(row=2, column=0, pady=7)
        error_box.insert("1.0", error)
        error_box.config(state="disabled")

        ai_analysis_label = tk.Label(welcome_frame, text="AI Analysis")
        ai_analysis_label.grid(row = 3, column = 0, pady = 10)


        ai_analysis_text_box = tk.Text(welcome_frame, width=60, height=6)
        ai_analysis_text_box.grid(row=4 , column = 0, pady = 10)
        ai_analysis_text_box.insert("1.0", debug_help)
        ai_analysis_text_box.config(state="disabled")


        help_label = tk.Label(welcome_frame, text="Still need help?")
        help_label.grid(row = 5, column = 0, pady = 10)

        another_question_text_box = tk.Text(welcome_frame, width=60, height=4 )
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


        ask_again_button = tk.Button(
            welcome_frame,
            text="Ask Again",
            command=ask_another_debug
        )
        ask_again_button.grid(row=7, column=0, pady=10)


    learn_mode_button = tk.Button(
        mode_frame,
        text="Learn Mode",
        command=lambda: learn_mode
    )
    learn_mode_button.pack(fill="x", pady=7)


    debug_mode_button = tk.Button(
        mode_frame,
        text="Debug Mode",
        command=debug_mode
    )
    debug_mode_button.pack(fill="x", pady=7)



    hint_button = tk.Button(
        mode_frame,
        text="Hint Mode",
        command=lambda: open_hint_mode
    )
    hint_button.pack(fill="x", pady=7)

    navigation_stack.append(home_screen)

    window.mainloop()

main()