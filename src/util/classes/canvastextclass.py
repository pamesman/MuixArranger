import customtkinter
import tkinter
from customtkinter.windows.widgets.core_widget_classes import DropdownMenu, CTkBaseClass

from src.util.round_rectangle import round_rectangle_AA
import math
from src.API import credential_managing as drive


class CanvasText(CTkBaseClass):

    def __init__(self,window,parent, text, location,corrector,  values, taula, croquis_en_us, dataframe, interval = None ,orientation= 0,color = "White", text_size = 10, list_len = 10):
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
        self.interval = interval
        self.color = color
        self.higlight_color = (color[1],color[0])
        self.text_size = text_size
        self.list_len = list_len
        self.chosen = str
        if self.croquis_en_us[text].strip() != "N. A.":
            self.text = self.croquis_en_us[text][:len(self.croquis_en_us[text].split(" ")[0])+2]
        if self.text in self.croquis_en_us.values():
            self.position = list(self.croquis_en_us.keys())[list(self.croquis_en_us.values()).index(self.text)]
        else:
            self.position = self.text
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


        self.txt = self.parent.create_text(self.x, self.y, angle = self.orientation,text=self.text, font=("Arial", self.text_size,"bold"), fill = "black", tags = (self.text.split(" ")[0], self.position, "etiqueta", self.croquis_en_us["Nom"]))
        self.entry = customtkinter.CTkEntry(self.parent, width=self.entry_width)

        self.rectangle_fix = [(self.tag_width ** 2 + 20 ** 2) ** 0.5 * i * 0.5 for i in [math.cos(math.atan(20 / self.tag_width) - math.radians(self.orientation)),math.sin(math.atan(20 / self.tag_width) - math.radians(self.orientation))]]

        self.scroll_count = 0



        self.entry.bind("<KeyRelease>", self.search_items)
        self.parent.tag_bind(self.txt, "<Enter>", self.on_focus)
        self.parent.tag_bind(self.txt, "<Leave>", self.on_defocus)
        self.parent.tag_bind(self.txt, "<Button-1>", self.on_click)

        self.shape = round_rectangle_AA(self.parent, self.x, self.y, angle=orientation, width=self.tag_width, fill=self._apply_appearance_mode(self.color), border_width=0, tags=("rectangle", self.position, self.text.split(" ")[0]),radius=10)[0]

        #print(self.callback_list)
    def insertar_membre(self, value):
        # value = " ".join(value.split(" ")[:-1])
        self.interval.stop()
        self.chosen = value

        for name in self.croquis_en_us.values():
            if self.text in name:
                self.text = name

        if self.text not in self.croquis_en_us.keys():
            self.croquis_en_us.update({list(self.croquis_en_us.keys())[list(self.croquis_en_us.values()).index(self.text)]: value})
            self.taula.insert((list(self.croquis_en_us.values()).index(value)) - 1, 1, value)
            self.taula.insert(list(self.croquis_en_us.values()).index(value) - 1, 2,
                              self.dataframe.loc[self.dataframe["Nom"] == value].iloc[0, 1])
        else:
            self.croquis_en_us.update({list(self.croquis_en_us.keys())[list(self.croquis_en_us.keys()).index(self.text)]: value})
            self.taula.insert((list(self.croquis_en_us.keys()).index(self.text)) - 1, 1, value)
            self.taula.insert(list(self.croquis_en_us.keys()).index(self.text) - 1, 2,
                              self.dataframe.loc[self.dataframe["Nom"] == value].iloc[0, 1])



        value = value[:len(value.split(" ")[0])+2]

        self.parent.itemconfig(self.txt, text=value)
        counter = tkinter.StringVar()
        self.interval.start()
        counter.trace_add("unset", self.drive_callback)







    def drive_callback(self, var, index, mode):
        try:
            drive.sheet.worksheet(self.croquis_en_us["Nom"]).update_cell(2, list(self.croquis_en_us.keys()).index(self.text)+1,  value=self.chosen)
            print("activated")
        except:
            print("mistake was sucedido")
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
            try:
                value_to_display.sort(key = lambda x: self.dataframe.loc[self.dataframe["Nom"] == x].iloc[0, 1], reverse=True)
            except:
                pass
            self.ddm.configure(values=value_to_display[:self.list_len])

    def scroll_up(self, _event):
        self.entry.focus_force()
        self.scroll_count -= 1
        self.ddm.configure(values=self.working_values[self.scroll_count:self.list_len + self.scroll_count])
        self.ddm.open(
            x=self.parent.winfo_rootx() + self.parent.coords(self.text)[0] - self.entry_width / 2 + 5 +
              self.rectangle_fix[0],
            y=self.parent.winfo_rooty() + self.parent.coords(self.text)[1] + self.entry_height +
              self.rectangle_fix[1])
        self.entry.place(x=self.parent.coords(self.text)[0] + self.rectangle_fix[0],
                         y=self.parent.coords(self.text)[1] + self.rectangle_fix[1], anchor="center")

        self.entry.focus_force()
        print("up")

    def scroll_down(self, _event):
        self.entry.focus_force()
        self.scroll_count += 1
        self.ddm.configure(values=self.working_values[self.scroll_count:self.list_len + self.scroll_count])
        self.ddm.open(
            x=self.parent.winfo_rootx() + self.parent.coords(self.text)[0] - self.entry_width / 2 + 5 +
              self.rectangle_fix[0],
            y=self.parent.winfo_rooty() + self.parent.coords(self.text)[1] + self.entry_height +
              self.rectangle_fix[1])
        self.entry.place(x=self.parent.coords(self.text)[0] + self.rectangle_fix[0],
                         y=self.parent.coords(self.text)[1] + self.rectangle_fix[1], anchor="center")

        self.entry.focus_force()
        print("down")
    def on_click(self, _event):
            self.working_values = list(set(self.values)^set(list(self.croquis_en_us.values())[2:]))
            self.working_values.remove("N. A.")
            self.working_values_heights = []
            # print(self.location)
            try:
                self.working_values.sort(reverse=True,key = lambda x: self.dataframe.loc[self.dataframe['Nom'] == x].iloc[0, 1])
            except:
                pass
            self.ddm = DropdownMenu(master=self.parent, values=self.working_values[:self.list_len], command=self.insertar_membre)





            self.entry.bind("<Button-5>", self.scroll_down)
            self.entry.bind("<Button-4>", self.scroll_up)
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




