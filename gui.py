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
    main_frame.pack()

    left_frame = tk.Frame(main_frame, width= 800, height=700)
    left_frame.pack(side = "left" , expand=True)
    right_frame = tk.Frame(main_frame, width=400, height=700, bg="#dcdcdc")
    right_frame.pack(side="right", expand =True)

    code_editor = tk.Text(left_frame, width = 100, height= 700)
    code_editor.pack(fill = "both")

    content_frame = tk.Frame(right_frame)
    content_frame.pack(fill = "both", expand= True)

    welcome_frame = tk.Frame(content_frame)
    welcome_frame.pack(fill = "both" , expand = True)

    response_frame = tk.frame(content_frame)
    response_frame.pack(fill="both",expand=True)

    history_frame = tk.Frame(content_frame)
    history_frame.pack(fill="both", expand=True)

    window.mainloop()
main()