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

    def start_screen():
        clear_screen(welcome_frame)

        plan_button = tk.Button(welcome_frame, text="Plan It", command=plan_mode)
        plan_button.grid(row=2, column=0, pady=7)

        perspective_button = tk.Button(welcome_frame, text="Different Perspectives")
        perspective_button.grid(row=3, column=0, pady=7)

        concept_button = tk.Button(welcome_frame, text="Concepts You May Need")
        concept_button.grid(row=4, column=0, pady=7)

        begin_button = tk.Button(welcome_frame, text="Let's begin")
        begin_button.grid(row=5, column=0, pady=7)

        start_label = tk.Label(welcome_frame, text = "Where Should I start?")
        start_label.grid(row = 0, column = 0)

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

    def continue_mode(text_box):
        print("Continue clicked")



    def clear_screen(frame):
        for widget in frame.winfo_children():
            widget.destroy()


    goal_entry = tk.Entry(welcome_frame)
    goal_entry.grid(row=4, column=0)

    start_button = tk.Button(welcome_frame, text = "Start", command=start_screen)
    start_button.grid(row=5, column=0)

    window.mainloop()
main()