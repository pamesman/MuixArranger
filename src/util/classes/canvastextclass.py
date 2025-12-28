import tkinter
import customtkinter
from customtkinter.windows.widgets.core_widget_classes import DropdownMenu
import time


class CanvasText():
    def __init__(self,window,parent, text, location,  values, taula, croquis_en_us, dataframe, orientation= 0,color = "White", text_size = 12, list_len = 10):
        self.window = window
        self.parent = parent
        self.text = text
        self.location = location
        self.orientation = orientation
        self.values = values
        self.taula = taula
        self.croquis_en_us = croquis_en_us
        self.dataframe = dataframe
        self.color = color
        self.text_size = text_size
        self.list_len = list_len

        self.window_x = self.window.winfo_rootx()
        self.window_y = self.window.winfo_rooty()
        self.entry_width = 100
        self.entry_height = 20
        self.parent.update()
        self.canvas_width = self.parent.winfo_screenwidth()
        self.canvas_height = self.parent.winfo_screenheight()
        self.x = self.parent.winfo_width()/2 + self.location[0]*self.parent.winfo_width()/15
        self.y = self.parent.winfo_height()/2 + self.location[1]*self.parent.winfo_height()/15


        self.txt = self.parent.create_text(self.x, self.y, angle = self.orientation,text=self.text, font=("Arial", 12), fill = self.color, tags = (self.text, "etiqueta"))
        self.entry = customtkinter.CTkEntry(self.parent, width=self.entry_width)
        self.ddm = DropdownMenu(master=self.parent, values=self.values[:self.list_len], command=self.insertar_membre)

        self.entry.bind("<KeyRelease>", self.search_items)
        self.parent.tag_bind(self.txt, "<Enter>", self.on_focus)
        self.parent.tag_bind(self.txt, "<Leave>", self.on_defocus)
        self.parent.tag_bind(self.txt, "<Button-1>", self.on_click)


    def insertar_membre(self, value):
        self.croquis_en_us.update({self.text: value})
        self.taula.insert(list(self.croquis_en_us).index(self.text) - 1, 1, value)
        self.taula.insert(list(self.croquis_en_us).index(self.text) - 1, 2,
                          self.dataframe.loc[self.dataframe["Nom"] == value].iloc[0, 1])
        self.parent.itemconfig(self.txt, text=value)



    def search_items(self, event):
        print("Searching")
        search_value = self.entry.get()
        # ddm._clicked()
        self.entry.focus_force()
        if search_value == "" or search_value == " ":
            self.ddm.configure(values=self.values[:self.list_len])
        else:
            value_to_display = []
            for value in self.values:
                if search_value.lower() in value.lower():
                    value_to_display.append(value)
            self.ddm.configure(values=value_to_display[:self.list_len])

    def on_click(self, event):
            self.parent.update()
            self.window.update()
            print(self.x, self.y, self.window_x, self.window_y)

            self.ddm.open(x=self.parent.winfo_rootx() + self.x - self.entry_width/2  + 5, y=self.parent.winfo_rooty() + self.y+ self.entry_height)
            self.entry.place(x=self.x, y=self.y, anchor="center")
            self.entry.focus_set()

            def forget(event):
                self.entry.place_forget()

            self.entry.bind("<FocusOut>", forget)

    def on_focus(self, event):
            self.parent.itemconfig(self.txt, fill="#C6E8AC", font=("Arial", 14))
            time.sleep(0.008)
            self.parent.itemconfig(self.txt, fill="#C6E8AC", font=("Arial", 16))


    def on_defocus(self, event):
            self.parent.itemconfig(self.txt, fill="#C6E8AC", font=("Arial", 14))
            time.sleep(0.08)
            self.parent.itemconfig(self.txt, fill=self.color, font=("Arial", 13))
            time.sleep(0.08)
            self.parent.itemconfig(self.txt, fill=self.color, font=("Arial", 12))




