import tkinter as tk
def main():
    window = tk.Tk()
    window.title("Mentor AI")
    window.geometry("1200x700")

    code_editor = tk.Text(window, width=80, height=40)
    ai_output = tk.Text(window, width=40, height=30, state="disabled")
    button_frame = tk.Frame(window)

    window.columnconfigure(0, weight=2)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0 , weight=1)
    window.rowconfigure(1, weight=0)

    btn_hint = tk.Button(button_frame, text="Get Hint")
    btn_hint.pack(side="top", padx=5, pady=5)
    btn_question = tk.Button(button_frame, text="Get Question")
    btn_question.pack(side="top", padx=5 , pady=5)
    btn_solution= tk.Button(button_frame, text="Get Solution")
    btn_solution.pack(side="top" , padx= 5, pady = 5)


    code_editor.grid(row=0, column=0, rowspan=2, sticky="nsew")
    ai_output.grid(row=0, column=1, sticky="nsew")
    button_frame.grid(row=1, column=1, sticky="nsew")


    window.mainloop()

if __name__ == "__main__":
    main()