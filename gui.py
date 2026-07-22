import tkinter as tk
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
    welcome_frame.rowconfigure(6, weight=1)

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


    def debug_mode():
        print("coming soon")

    def start_learning():


        topic =  learn_mode_text_box.get("1.0" , "end" ).strip()

        ai_response = generate_explanation(topic)

        clear_screen(welcome_frame)

        learn_session_label = tk.Label(welcome_frame, text="Learn Session")
        learn_session_label.grid(row=0, column=0, pady=7)

        today_label = tk.Label(welcome_frame, text="Today we'll learn:")
        today_label.grid(row=1, column=0, pady=7)

        topic_label = tk.Label(welcome_frame, text= topic)
        topic_label.grid(row=2, column=0, pady=7)

        message_label = tk.Label(welcome_frame, text=ai_response)
        message_label.grid(row=3, column=0, pady=7)

    def generate_explanation(topic):
        return f"Let's learn about {topic}!"


    def start_debugging():
        pass

    learn_mode_button = tk.Button(mode_frame,text="Learn Mode", command = learn_mode)
    learn_mode_button.pack(fill="x" , pady=7)

    debug_mode_button = tk.Button(mode_frame,text="Debug Mode",command = debug_mode)
    debug_mode_button.pack(fill="x" , pady=7)

    window.mainloop()

main()