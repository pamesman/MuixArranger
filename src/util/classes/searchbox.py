from tkinter import *
import src.membre as mem
import customtkinter
import CTkScrollableDropdown as ctk
ws = Tk()
ws.title("Python Guides")
ws.geometry("200x200")

def search_items(event):

    search_value = combo._entry.get()
    combo._clicked()
    combo.focus_force()
    if search_value == "" or search_value == " ":
        combo.configure(values = item_names)
    else:
        value_to_display = []
        for value in item_names:
            if search_value.lower() in value.lower():
                value_to_display.append(value)


        combo.configure(values = value_to_display)
item_names = mem.working_list[:30]

combo = customtkinter.CTkComboBox(ws)
combo.set("")
#ctk.CTkScrollableDropdown(combo, values= item_names)
combo.configure(values = item_names)
combo.place(relx=0.5, rely=0.5, anchor=CENTER)

variable=StringVar()

combo._entry.configure(textvariable = "abooga")
combo._entry.bind("<KeyRelease>",search_items)


ws.mainloop()