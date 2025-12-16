
import customtkinter as ctk
def combobox_gen(parent,relx = 0.5,rely = 0.5,subcategoria = None,):
    def combobox_callback(choice):
        print("combobox dropdown clicked:", choice)
    combobox_var = ctk.StringVar(value="option 2")
    combobox = ctk.CTkComboBox(parent, values=["option 1", "option 2"],
                                         command=combobox_callback, variable=combobox_var)
    combobox_var.set("option 2")
    combobox.place(relx = relx,rely = rely,anchor="s")