# Source - https://stackoverflow.com/a
# Posted by Ahmadofski
# Retrieved 2026-01-06, License - CC BY-SA 4.0

import tkinter as tk

import customtkinter


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()

canvas = tk.Canvas(root, height=200)  # Adjust the height as needed
canvas.pack(padx=20, pady=20)

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

combo_box = customtkinter.CTkComboBox(frame, values=["Java", "CSS", "Python", "PHP", "HTML", "C#", "JavaScript", "Ruby", "C", "C++"])
combo_box.pack(fill="x")

scrollbar = tk.Scrollbar(root, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

def on_tab_complete(event):
    available_options = ["Java", "CSS", "Python"]
    current_text = combo_box.get()
    completions = [option for option in available_options if option.lower().startswith(current_text.lower())]
    if completions:
        combo_box.configure(values=completions)
    else:
        combo_box.configure(values=(" "))

def call_on_tab_complete_twice(event):
    on_tab_complete(event)
    root.after(10, lambda: on_tab_complete(event))

combo_box.bind("<KeyPress>", call_on_tab_complete_twice)

root.mainloop()
