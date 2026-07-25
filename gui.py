import tkinter as tk
from openai_client import OpenAIClient
from logging import disable
from tkinter import messagebox


def main():
    window = tk.Tk()
    window.title("Mentor AI")
    window.geometry("1200x700")

    top_frame = tk.Frame(window, bg="#181818")
    top_frame.pack(fill = "x")
    button1 = tk.Button(top_frame, text = "File")
    button1.pack(side = "left")

    main_frame = tk.Frame(window)
    main_frame.pack(fill="both", expand=True)

    left_frame = tk.Frame(main_frame, width= 800, height=700)
    left_frame.pack(side = "left" , fill="both",expand=True)
    right_frame = tk.Frame(main_frame, width=400, height=700, bg="#dcdcdc")
    right_frame.pack(side="right",fill="both" ,expand =True)

    code_editor = tk.Text(left_frame, width = 100, height= 700)
    code_editor.pack(fill = "both")

    content_frame = tk.Frame(right_frame)
    content_frame.pack(fill = "both", expand= True)

    welcome_frame = tk.Frame(content_frame)
    welcome_frame.pack(fill = "both" , expand = True)

    welcome_frame.columnconfigure(0, weight=1)


    title_label=tk.Label(welcome_frame, text = "Mentor AI")
    title_label.grid(row=0, column=0)

    subtitle_label = tk.Label(welcome_frame, text="Think. Build. Learn.")
    subtitle_label.grid(row=1, column=0)

    goal_label = tk.Label(welcome_frame , text = "What would you like to work on today?")
    goal_label.grid(row=3, column=0)


    def plan_mode():
        clear_screen(welcome_frame)

        plan_it_label = tk.Label(welcome_frame, text="Let's Plan It!")
        plan_it_label.grid(row=0, column=0, pady=7)

        describe_label = tk.Label(welcome_frame, text = "What are you trying to build?")
        describe_label.grid(row=1, column=0, pady = 5)

        text_box = tk.Text(welcome_frame,width = 50 , height= 7)
        text_box.grid(row=2, column=0, pady = 7)

        continue_button = tk.Button(welcome_frame, text = "Continue", command = lambda: continue_mode(text_box))
        continue_button.grid(row=3, column=0, pady = 7)

    def conversation_screen(project):
        clear_screen(welcome_frame)

        planning_session_label = tk.Label(welcome_frame, text="Planning Session")
        planning_session_label.grid(row=0, column=0, pady=7)

        project_idea_label = tk.Label(welcome_frame, text="Project Idea")
        project_idea_label.grid(row=1, column=0, pady=7)

        ai_explanaition_label = tk.Label(welcome_frame, text="Great! Let's understand your project together.")
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
        text="Start a New Project"  , command=plan_mode
    )
    project_button.pack(fill="x" , pady=7)

    def learn_mode():
        global learn_mode_text_box

        clear_screen(welcome_frame)

        learn_mode_title_label = tk.Label(welcome_frame, text="Learn Mode")
        learn_mode_title_label.grid(row=0, column=0, pady=7)

        learn_mode_description_label = tk.Label(welcome_frame, text="Learn Mode Description")
        learn_mode_description_label.grid(row=1, column=0, pady=7)

        learn_mode_text_box = tk.Text(welcome_frame, width=50, height=7)
        learn_mode_text_box.grid(row=2, column=0, pady=7)

        learn_mode_button = tk.Button(welcome_frame,text="Continue",command = start_learning)
        learn_mode_button.grid(row=3, column=0 , pady=7)


    def start_learning():
        global follow_up_text
        global topic
        global ai_response
        global message_text

        topic =  learn_mode_text_box.get("1.0" , "end" ).strip()

        ai_response = generate_explanation(topic)

        clear_screen(welcome_frame)

        learn_session_label = tk.Label(welcome_frame, text="Learn Session")
        learn_session_label.grid(row=0, column=0, pady=7)

        today_label = tk.Label(welcome_frame, text="Today we'll learn:")
        today_label.grid(row=1, column=0, pady=7)

        topic_label = tk.Label(welcome_frame, text= topic)
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

        clear_screen(welcome_frame)

        hint_mode_title_label = tk.Label(welcome_frame, text="Hint Mode")
        hint_mode_title_label.grid(row=0, column=0, pady=7)

        hint_mode_question_label = tk.Label(welcome_frame, text="What are you building?")
        hint_mode_question_label.grid(row=1, column=0, pady=7)

        hint_mode_first_text_box = tk.Text(welcome_frame, width=50, height=4)
        hint_mode_first_text_box.grid(row=2, column=0, pady=7)

        hint_mode_problem_label = tk.Label(welcome_frame, text="Where are you stuck?")
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

        debug_error_button = tk.Button(welcome_frame, text="Debug", command=debug_mode)
        debug_error_button.grid(row=5, column=0, pady=10)

    def start_debug():
        print("Debug Mode started")

    learn_mode_button = tk.Button(
        mode_frame,
        text="Learn Mode",
        command=learn_mode
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
        command=open_hint_mode
    )
    hint_button.pack(fill="x", pady=7)




    window.mainloop()

main()