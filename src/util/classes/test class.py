import customtkinter
import tkinter
from customtkinter.windows.widgets.core_widget_classes import DropdownMenu
import src.membre as mem



root = customtkinter.CTk()
root.geometry("600x300")
c = tkinter.Canvas(root, width=600, height=600, bg="#333333")
c.place(x=0, y=0)
#x=300
#y=150
root.update()

croquis_fake = {"Base1":None, "Base 2":None}
window_x =root.winfo_rootx()
window_y =root.winfo_y()
entry_width = 100
entry_height = 20
values = mem.working_list
list_len = 10
#command = command
counter = 1

def creation(i):
    global counter
    txt = c.create_text(300*counter, 150*counter, text=i, font=("Arial", 12), fill="white", tags = "Base 1")
    counter += 0.2
    entry = customtkinter.CTkEntry(root, width=entry_width)
    def seleccio(event):
        print(event)
        c.itemconfig(txt, text=event)

    ddm = DropdownMenu(master = c,values = values[:list_len], command = seleccio)


    def search_items(event):
        print("Searching")
        search_value = entry.get()
        #ddm._clicked()
        entry.focus_force()
        if search_value == "" or search_value == " ":
            ddm.configure(values=values[:list_len])
        else:
            value_to_display = []
            for value in values:
                if search_value.lower() in value.lower():
                    value_to_display.append(value)
            ddm.configure(values=value_to_display[:list_len])
    def on_click(event):
        y = c.coords(txt)[1]
        x = c.coords(txt)[0]
        windowx = root.winfo_rootx()
        windowy = root.winfo_y()


        ddm.open(x=windowx+x-entry_width/2+5, y=windowy+y+entry_height/2)
        entry.place(x = x, y = y, anchor="center")
        entry.focus_set()

        def forget(event):
            entry.place_forget()

        entry.bind("<FocusOut>", forget)


    def on_focus(event):
        c.itemconfig(txt, fill="#C6E8AC", font=("Arial", 16))



    def on_defocus(event):
        c.itemconfig(txt, fill="white", font = ("Arial",12))
    entry.bind("<KeyRelease>",search_items)
    c.tag_bind(txt, "<Enter>", on_focus)
    c.tag_bind(txt, "<Leave>", on_defocus)
    c.tag_bind(txt, "<Button-1>", on_click)

for i in croquis_fake.keys():

    creation(i)







root.mainloop()