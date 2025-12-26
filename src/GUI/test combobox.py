import customtkinter
from customtkinter import CTkButton, CTkEntry
from CTkListbox import *
from customtkinter.windows.widgets.ctk_pacombobox2 import CTkPaComboBox2
from CTkScrollableDropdown  import CTkScrollableDropdown
import src.membre
from src.membre import working_list
a = ["Base1","Base2","Base3"]
root = customtkinter.CTk()
root.geometry("1280x720")
customtkinter.set_appearance_mode("dark")
values = working_list


def popup_make():
    def show_value(selected_value):
        print(selected_value)
        popup.destroy()


    def search_items(event):
        search_value = entry.get()
        listbox.popup()
        entry.focus_force()
        if search_value == "" or search_value == " ":
            listbox.configure(values=values)

        else:
            value_to_display = []
            for value in values:
                if search_value.lower() in value.lower():
                    value_to_display.append(value)
            listbox.configure(values=value_to_display)
    popup = customtkinter.CTkToplevel()
    popup.geometry("200x720")
    entry = CTkEntry(popup)

    entry.bind("<KeyRelease>", search_items)
    entry.pack()

    listbox = CTkScrollableDropdown(entry, values = values)
    #listbox = (CTkListbox(popup, command=show_value))
    #listbox.pack( expand=True, fill="both")



for i in a:
    button = customtkinter.CTkButton(root, text=i, command=popup_make).pack(pady=50)
cbb = CTkPaComboBox2(root, values = ["1111111111111111111111111111111"])
cbb.pack(pady=50)




#print(button.cget("text"))










root.mainloop()