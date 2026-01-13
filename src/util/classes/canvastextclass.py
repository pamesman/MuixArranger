import customtkinter
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass
import tkinter
from src.util.classes.round_rectangle import round_rectangle_AA


class CanvasText(CTkBaseClass):
    def __init__(self,window,parent, text, location,corrector,  values, taula, croquis_en_us, dataframe, interval = None, sheet = None ,orientation= 0,color = "White", text_size = 9, list_len = 10):
        self.master = parent
        super().__init__(master = parent)
        self.window = window
        self.parent = parent
        self.text = croquis_en_us[text][:len(croquis_en_us[text].split(" ")[0]) + 2]
        self.toggle = False
        if croquis_en_us[text].strip() == "N. A." or croquis_en_us[text].strip() == "+":  # si no hi ha algu seleccionat
            self.text = text.split(" ")[0]
            self.text_color = self._apply_appearance_mode(("#333333","#AAAAAA"))
            self.color = ""
            self.outline = self._apply_appearance_mode(color)
        else:
            self.text = croquis_en_us[text][:len(croquis_en_us[text].split(" ")[0]) + 2].upper()
            self.text_color = "black"
            self.color = self._apply_appearance_mode(color)
            self.outline = self._apply_appearance_mode(("#333333","#000000"))
        self.color2 = color
        self.location = location
        self.corrector = corrector
        self.orientation = orientation
        self.values = [i.upper() for i in values]
        self.working_values = [i.upper() for i in values]
        self.working_values_heights = []
        self.taula = taula
        self.croquis_en_us = croquis_en_us
        self.dataframe = dataframe
        self.position = text
        self.interval = interval
        self.sheet = sheet
        self.highlight_color = (color[1], color[0])
        self.text_size = text_size
        self.list_len = list_len

        self.window_x = self.window.winfo_rootx()
        self.window_y = self.window.winfo_rooty()
        self.entry_width = 100
        self.entry_height = 20
        self.parent.update()
        self.canvas_width = self.parent.winfo_screenwidth()
        self.canvas_height = self.parent.winfo_screenheight()
        self.tag_width = 70
        if self.position.split(" ")[0] in ["Tap","Peu", "Colze"]:
            self.text_size = 8
            self.tag_width = 45
            self.text = self.text.split(" ")[0]



        self.span = (self.corrector[0][0]-self.corrector[0][1], self.corrector[1][0]-self.corrector[1][1])
        self.center = ((self.corrector[0][0]+self.corrector[0][1])/2,(self.corrector[1][0]+self.corrector[1][1])/2)

        self.x = self.parent.winfo_width()/2 + (self.location[0]-self.center[0])*self.parent.winfo_width()/20
        self.y = self.parent.winfo_height()/2 - (self.location[1]-self.center[1])*self.parent.winfo_height()/18




        self.txt = self.parent.create_text(self.x, self.y, angle = self.orientation,text=self.text, font=("Arial", self.text_size,"bold"), fill = self.text_color, tags = (self.text.split(" ")[0], self.position, "etiqueta", self.croquis_en_us["Nom"]))
        self.entry = customtkinter.CTkEntry(self.parent, width=self.entry_width)
        # if self.position.split(" ")[0] in ["Xicalla"]:
        self.textvar = tkinter.StringVar()
        self.entry.configure(textvariable = self.textvar )
        # Creating a Listbox and
        # attaching it to root window
        self.lb = tkinter.Listbox(self.parent, width=16 ,background="#2B2B2B", fg="#FFFFFF", bd= 0, relief="flat", activestyle="none", highlightthickness=0, justify="left" )
        self.lb.bind("<Button-1>", self.insertar_membre)





        self.entry.bind("<KeyRelease>", self.search_items)
        self.parent.tag_bind(self.txt, "<Enter>", self.on_focus)
        self.parent.tag_bind(self.txt, "<Leave>", self.on_defocus)
        self.parent.tag_bind(self.txt, "<Button-1>", self.on_click)
        self.parent.tag_bind(self.txt, "<Button-3>", self.on_right_click)

        self.shape = round_rectangle_AA(self.parent, self.x, self.y, angle=orientation, width=self.tag_width, fill=self.color, outline = self.outline, border_width=1, tags=("rectangle", self.position, self.text.split(" ")[0]),radius=10)[0]

        if self.croquis_en_us[self.position] == "+":
            self.toggle = True
            self.parent.itemconfig(self.shape, fill="", outline="")
            self.parent.itemconfig(self.txt, font=("Arial", 14), text="+")
            self.croquis_en_us[self.position] = "+"
            self.text = self.position

    def insertar_membre(self, value):
        # value = " ".join(value.split(" ")[:-1])

        value = self.lb.get(self.lb.nearest(value.y))

        if self.interval != None:
            self.interval.stop()
        self.text= value.title()
        for name in self.croquis_en_us.values():
            if self.text in name:
                self.text = name

        if self.text not in self.croquis_en_us.keys():
            self.croquis_en_us.update({list(self.croquis_en_us.keys())[list(self.croquis_en_us.keys()).index(self.position)]: self.text})
            self.taula.insert((list(self.croquis_en_us.keys()).index(self.position)) - 1, 1, self.text)
            try:
                self.taula.insert(list(self.croquis_en_us.keys()).index(self.position) - 1, 2, self.dataframe.loc[self.dataframe["Nom"] == self.text].iloc[0, 1])
            except:
                pass


        value = value[:len(value.split(" ")[0])+2]

        self.parent.itemconfig(self.txt, text=value)
        counter = tkinter.StringVar()
        self.parent.itemconfig(self.shape, outline = self._apply_appearance_mode(("#333333","#000000")), fill = self._apply_appearance_mode(self.color2))
        self.parent.itemconfig(self.txt, fill = "black")
        print(self.croquis_en_us["Nom"], "\n", self.position, ": ", self.text)
        if self.interval != None:
            self.drive_callback()
            self.interval.start()
        self.forget()

    def drive_callback(self):
        try:
            self.sheet.worksheet(self.croquis_en_us["Nom"]).update_cell(2, list(self.croquis_en_us.keys()).index(self.position)+1,  value=self.text)
        except:
            print("mistake was sucedido")

    def search_items(self, _event):
        search_value = self.entry.get()
        self.entry.focus_force()
        self.working_values = list(set(self.values) ^ set([i.upper() for i in list(self.croquis_en_us.values())[2:]]))
        if search_value == "" or search_value == " ":
            self.lb.delete(0, "end")
            try:
                self.working_values.sort(key = lambda x: self.dataframe.loc[self.dataframe["Nom"].str.upper() == x].iloc[0, 1], reverse=True)
            except:
                pass
            for i in self.working_values:
                self.lb.insert("end",i)
            self.lb.insert("end", self.textvar.get())
        else:
            value_to_display = []
            for value in self.working_values:
                if search_value.lower() in value.lower():
                    value_to_display.append(value)
            try:
                value_to_display.sort(key = lambda x: self.dataframe.loc[self.dataframe["Nom"].str.upper() == x].iloc[0, 1], reverse=True)
            except:
                pass
            self.lb.delete(0, "end")
            for i in value_to_display:
                self.lb.insert("end",i)
            self.lb.insert("end", self.textvar.get())


    def on_click(self, _event):
        if not self.toggle:
            self.working_values = list(set(self.values)^set([i.upper() for i in list(self.croquis_en_us.values())[2:]]))
            if "N. A." in list(self.working_values):
                self.working_values.remove("N. A.")
            self.working_values_heights = []
            try:
                self.working_values.sort(reverse=True,key = lambda x: self.dataframe.loc[self.dataframe['Nom'].str.upper() == x].iloc[0, 1])
            except:
                pass
            self.lb.place(x=self.parent.coords(self.txt)[0]- self.entry_width/2+2, y=self.parent.coords(self.txt)[1]+ self.entry_height-5)
            self.sb = tkinter.Scrollbar(self.parent)
            for i in self.working_values:
                self.lb.insert("end", i)
            self.lb.config(yscrollcommand=self.sb.set)
            self.sb.config(command=self.lb.yview)


            #self.ddm.open(x=self.parent.winfo_rootx() + self.parent.coords(self.txt)[0] - self.entry_width/2  + 5 +self.rectangle_fix[0], y=self.parent.winfo_rooty() + self.parent.coords(self.txt)[1]+ self.entry_height+self.rectangle_fix[1])
            self.entry.place(x=self.parent.coords(self.txt)[0], y=self.parent.coords(self.txt)[1], anchor="center")

            self.entry.focus_set()

            def forget(_event):
                self.focus_get()
                self.entry.place_forget()
                self.lb.place_forget()


            self.entry.bind("<FocusOut>", forget)

    def on_focus(self, _event):
        if not self.toggle:
            self.parent.itemconfig(self.shape, fill=self._apply_appearance_mode(self.highlight_color))

    def on_defocus(self, _event):
        if not self.toggle:
            if self.text.split(" ")[0] != self.position.split(" ")[0]:
                self.parent.itemconfig(self.shape, fill=self._apply_appearance_mode(self.color2))
                self.parent.itemconfig(self.txt, font=("Arial", self.text_size,"bold"))
            else:
                self.parent.itemconfig(self.shape, fill="")
                self.parent.itemconfig(self.txt, font=("Arial", self.text_size,"bold"))

    def on_right_click(self, _event):
        if self.position.split(" ")[0] not in ["Base", "Segona", "Tercera", "Alsadora", "Xicalla", "Quarta"]:
            if not self.toggle:
                self.toggle = True
                self.parent.itemconfig(self.shape, fill = "", outline = "")
                self.parent.itemconfig(self.txt, font=("Arial", 14), text = "+")
                self.croquis_en_us[self.position] = "+"
                self.text = self.position
            else:
                self.parent.itemconfig(self.shape, fill="", outline=self._apply_appearance_mode(self.color2))
                self.parent.itemconfig(self.txt, font=("Arial", self.text_size), text=self.position, fill = "#AAAAAA")
                self.croquis_en_us[self.position] = "N. A."
                self.toggle = False

