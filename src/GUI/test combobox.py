import customtkinter
from customtkinter import CTkButton
from CTkListbox import *
import src.Membre
from src.Membre import working_list
a = ["Base1","Base2","Base3"]
root = customtkinter.CTk()
root.geometry("1280x720")
customtkinter.set_appearance_mode("dark")
def show_value(selected_value):
    print(selected_value)
    popup.exit()
def popup():
    popup = customtkinter.CTkToplevel()
    popup.geometry("200x720")
    listbox = (CTkListbox(popup, command=show_value))
    listbox.place(relx=0.5, rely=0.5,anchor="center",relwidth=1,relheight=1)
    for i in range(len(working_list)):
        listbox.insert(i,working_list[i])
for i in a:
    button = customtkinter.CTkButton(root, text=i, command=popup).pack(pady=50)


#print(button.cget("text"))










root.mainloop()