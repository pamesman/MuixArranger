

import customtkinter

from customtkinter.windows.widgets.core_widget_classes import DropdownMenu, CTkBaseClass


from src.util.round_rectangle import round_rectangle_AA
import math


class CanvasText(CTkBaseClass):

    def __init__(self,window,parent, text, location,corrector,  values, taula, croquis_en_us, dataframe, orientation= 0,color = "White", text_size = 10, list_len = 10):
        self.master = parent
        super().__init__(master = parent)
        self.window = window
        self.parent = parent
        self.text = text
        self.location = location
        self.corrector = corrector
        self.orientation = orientation
        self.values = values
        self.working_values = values
        self.working_values_heights = []
        self.taula = taula
        self.croquis_en_us = croquis_en_us
        self.dataframe = dataframe
        self.color = color
        self.higlight_color = (color[1],color[0])
        self.text_size = text_size
        self.list_len = list_len
        if self.croquis_en_us[text].strip() != "N. A.":
            self.text = self.croquis_en_us[text][:len(self.croquis_en_us[text].split(" ")[0])+2]

        self.window_x = self.window.winfo_rootx()
        self.window_y = self.window.winfo_rooty()
        self.entry_width = 100
        self.entry_height = 20
        self.parent.update()
        self.canvas_width = self.parent.winfo_screenwidth()
        self.canvas_height = self.parent.winfo_screenheight()
        self.tag_width = 70
        if self.text.split(" ")[0] in ["Tap","Peu"]:
            self.tag_width = 45

        self.span = (self.corrector[0][0]-self.corrector[0][1], self.corrector[1][0]-self.corrector[1][1])
        self.center = ((self.corrector[0][0]+self.corrector[0][1])/2,(self.corrector[1][0]+self.corrector[1][1])/2)

        self.x = self.parent.winfo_width()/2 + (self.location[0]-self.center[0])*self.parent.winfo_width()/20
        self.y = self.parent.winfo_height()/2 - (self.location[1]-self.center[1])*self.parent.winfo_height()/20


        self.txt = self.parent.create_text(self.x, self.y, angle = self.orientation,text=self.text, font=("Arial", self.text_size,"bold"), fill = "black", tags = (self.text.split(" ")[0], self.text, "etiqueta", self.croquis_en_us["Nom"]))
        self.entry = customtkinter.CTkEntry(self.parent, width=self.entry_width)

        self.rectangle_fix = [(self.tag_width ** 2 + 20 ** 2) ** 0.5 * i * 0.5 for i in [math.cos(math.atan(20 / self.tag_width) - math.radians(self.orientation)),math.sin(math.atan(20 / self.tag_width) - math.radians(self.orientation))]]




        self.entry.bind("<KeyRelease>", self.search_items)
        self.parent.tag_bind(self.txt, "<Enter>", self.on_focus)
        self.parent.tag_bind(self.txt, "<Leave>", self.on_defocus)
        self.parent.tag_bind(self.txt, "<Button-1>", self.on_click)

        self.shape = round_rectangle_AA(self.parent, self.x, self.y, angle=orientation, width=self.tag_width, fill=self._apply_appearance_mode(self.color), border_width=0, tags=("rectangle", self.text, self.text.split(" ")[0]),radius=10)[0]
        print(self._get_appearance_mode())
        #print(self.callback_list)
    def insertar_membre(self, value):
        # value = " ".join(value.split(" ")[:-1])
        self.croquis_en_us.update({self.text: value})
        self.taula.insert(list(self.croquis_en_us).index(self.text) - 1, 1, value)
        self.taula.insert(list(self.croquis_en_us).index(self.text) - 1, 2,
                          self.dataframe.loc[self.dataframe["Nom"] == value].iloc[0, 1])
        value = value[:len(value.split(" ")[0])+2]
        self.parent.itemconfig(self.txt, text=value)




    def search_items(self, _event):
        search_value = self.entry.get()
        self.entry.focus_force()
        if search_value == "" or search_value == " ":
            self.ddm.configure(values=self.working_values[:self.list_len])
        else:
            value_to_display = []
            for value in self.working_values:
                if search_value.lower() in value.lower():
                    value_to_display.append(value)
            value_to_display.sort(key = lambda x: self.dataframe.loc[self.dataframe["Nom"] == x].iloc[0, 1], reverse=True)
            self.ddm.configure(values=value_to_display[:self.list_len])

    def on_click(self, _event):
            self.working_values = list(set(self.values)^set(list(self.croquis_en_us.values())[2:]))
            self.working_values.remove("N. A.")
            self.working_values_heights = []
            print(self.location)
            self.working_values.sort(reverse=True,key = lambda x: self.dataframe.loc[self.dataframe['Nom'] == x].iloc[0, 1])

            self.ddm = DropdownMenu(master=self.parent, values=self.working_values[:self.list_len], command=self.insertar_membre)

            self.parent.update()
            self.window.update()

            self.ddm.open(x=self.parent.winfo_rootx() + self.parent.coords(self.text)[0] - self.entry_width/2  + 5 +self.rectangle_fix[0], y=self.parent.winfo_rooty() + self.parent.coords(self.text)[1]+ self.entry_height+self.rectangle_fix[1])
            self.entry.place(x=self.parent.coords(self.text)[0]+self.rectangle_fix[0], y=self.parent.coords(self.text)[1]+self.rectangle_fix[1], anchor="center")

            self.entry.focus_set()

            def forget(_event):
                self.entry.place_forget()

            self.entry.bind("<FocusOut>", forget)


    def on_focus(self, _event):
            self.parent.itemconfig(self.shape, fill=self._apply_appearance_mode(self.higlight_color))


    def on_defocus(self, _event):

            self.parent.itemconfig(self.shape, fill=self._apply_appearance_mode(self.color))
            self.parent.itemconfig(self.txt, fill="black", font=("Arial", self.text_size,"bold"))




