import customtkinter
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass
import tkinter
from src.util.classes.round_rectangle import round_rectangle_AA


class CanvasText(CTkBaseClass):
    def __init__(self,window,parent, text, location,corrector,  values, taula, croquis_en_us, dataframe, interval = None, sheet = None ,orientation= 0,color = "White", text_size = 10, list_len = 10, tag_width = 70, mini = False):
        self.master = parent
        super().__init__(master = parent)
        self.window = window
        self.parent = parent
        self.position = text    #Base 1, Mans 13, etc.
        self.color2 = color
        self.text = text
        self.text_color = ""
        if self.text in list(croquis_en_us.keys()):
            # Tractament diferencial si hi ha o no algú seleccionat:
            if croquis_en_us[text].strip() == "N. A.":
                self.text = text.split(" ")[0]  #El text es "Base, Mans etc.
                self.color = "" #Rectangle sense fill
                self.outline = self._apply_appearance_mode(self.color2)
                self.text_color = self._apply_appearance_mode(("#333333","#AAAAAA"))
            else:
                self.text = croquis_en_us[text] #El text es la persona
                self.color = self._apply_appearance_mode(color)
                self.outline = self._apply_appearance_mode(("#333333", "#000000"))
                self.text_color = "black"



        self.location = location #Coordenades
        self.corrector = corrector  #Centra la figura
        self.orientation = orientation

        self.span = (self.corrector[0][0] - self.corrector[0][1],self.corrector[1][0] - self.corrector[1][1])
        self.center = ((self.corrector[0][0] + self.corrector[0][1]) / 2,(self.corrector[1][0] + self.corrector[1][1]) / 2)

        self.span_x = max(self.span[0]+0.5, 10)


        self.values = values    #Asistents
        self.taula = taula
        self.croquis_en_us = croquis_en_us
        self.dataframe = dataframe  #Database

        #Online funcionalitat
        self.interval = interval    #El actualitzador recurrent
        self.sheet = sheet  #On guardar el output online

        #Estil

        self.highlight_color = (color[1], color[0])


        self.text_size_ref = int(text_size * 16 / self.span_x)

        self.entry_width = 100
        self.entry_height = 20
        self.tag_width = tag_width
        self.list_len = list_len    #Num. ítems al dropdown

        self.aspect_ratio = 11 / 36

        if self.position.split(" ")[0] in ["Base"]:
            self.aspect_ratio = 14/34
            self.tag_width = self.tag_width * 0.94



        if self.position.split(" ")[0] in ["Tap","Peu", "Colze"]:   #Etiquetes més menudes per a estes posicions
            self.text_size_ref = int(self.text_size_ref * 8/11)
            self.tag_width = self.tag_width * 0.7

        if self.position.split(" ")[0] in ["Agulla"]:
            self.aspect_ratio = self.aspect_ratio * 0.6

        self.tag_width = self.tag_width * (16 / self.span_x)
        self.tag_height = self.tag_width * self.aspect_ratio
        self.min_text_size = max(self.text_size_ref * 7 / len(self.text), 8)
        self.text_size = min(self.text_size_ref, int(self.min_text_size))
        self.mini = mini

        #GEOMETRIA
        self.parent.update()    #Necessari o el parent te dimensions 0x0
        self.canvas_width = self.parent.winfo_screenwidth()
        self.canvas_height = self.parent.winfo_screenheight()



        self.x = self.parent.winfo_width() * (0.5 + (self.location[0]-self.center[0])/(self.span_x * 1.1))
        self.y = self.parent.winfo_height() * (0.5 - (self.location[1]-self.center[1])/(self.span_x * 1.1))



        if self.mini:
            self.text = ""

        #Creació dels widgets
        self.txt = self.parent.create_text(
                                           self.x,
                                           self.y,
                                           angle = self.orientation,
                                           text = self.text,
                                           font = ("Arial", self.text_size,"bold"),
                                           fill = self.text_color,
                                           tags = (self.text.split(" ")[0], self.position, "etiqueta", self.croquis_en_us["Nom"])
                                           )
        self.shape = round_rectangle_AA(
                                        self.parent,
                                        self.x,
                                        self.y,
                                        angle = orientation,
                                        width = self.tag_width,
                                        height = self.tag_height,
                                        fill = self.color,
                                        outline = self.outline,
                                        border_width = 1,
                                        tags = ("rectangle", self.position, self.text.split(" ")[0]),
                                        radius = 5
                                        )

        self.entry = customtkinter.CTkEntry(self.parent, width=self.entry_width)
        self.textvar = tkinter.StringVar()
        self.entry.configure(textvariable = self.textvar )
        self.lb = tkinter.Listbox(self.parent.master, width=12 ,background="#2B2B2B", fg="#FFFFFF", bd= 0, relief="flat", activestyle="none", highlightthickness=0, justify="left" )

        self.lb.bind("<Button-1>", self.insertar_membre)
        self.entry.bind("<KeyRelease>", self.search_items)
        self.entry.bind("<Escape>", self.forget)
        self.parent.tag_bind(self.txt, "<Enter>", self.on_focus)
        self.parent.tag_bind(self.txt, "<Leave>", self.on_defocus)
        self.parent.tag_bind(self.txt, "<Button-1>", self.on_click)
        if self.position in list(self.croquis_en_us.keys()):
            self.parent.tag_bind(self.txt, "<Button-3>", self.on_right_click)


        self.toggle = False
        if self.croquis_en_us[self.position] == "+":
            self.parent.itemconfig(self.shape, fill="", outline="")
            self.parent.itemconfig(self.txt, font=( "Arial", 14), text="+", fill=self._apply_appearance_mode(("#333333","#AAAAAA")))
            self.toggle = True
        def locate(event):
            x = (event.x/self.parent.winfo_width()-0.5)*(self.span_x*1.1)+self.center[0]
            y = (event.y/self.parent.winfo_height()-0.5)*(self.span_x*1.1)-self.center[1]
            print(x, y)
        self.parent.bind("<Button-1>", locate)

    def insertar_membre(self, value):
        value = self.lb.get(self.lb.nearest(value.y))

        if self.interval != None:
            self.interval.stop()
        self.text= value
        for name in self.croquis_en_us.values():
            if self.text == name:
                self.text = name

        if self.text not in self.croquis_en_us.keys():
            self.croquis_en_us.update({list(self.croquis_en_us.keys())[list(self.croquis_en_us.keys()).index(self.position)]: self.text})
            # self.taula.insert((list(self.croquis_en_us.keys()).index(self.position)) - 1, 1, self.text)
            current_values = self.taula.item((list(self.croquis_en_us.keys()).index(self.position)) - 1).get("values")
            current_values[1] = self.text
            try:
                current_values[2] = self.dataframe.loc[self.dataframe["Àlies"] == self.text].iloc[0, 2]
            except:
                pass
            self.taula.item((list(self.croquis_en_us.keys()).index(self.position)) - 1, values=current_values)


        self.min_text_size = max( self.text_size_ref * 7/len(value), 8)
        self.text_size= min(self.text_size_ref, int(self.min_text_size))
        self.parent.itemconfig(self.txt, text=value, font = ("Arial", self.text_size, "bold"))
        self.parent.itemconfig(self.shape, outline = self._apply_appearance_mode(("#333333","#000000")), fill = self._apply_appearance_mode(self.color2))

        self.parent.itemconfig(self.txt, fill = "black")
        # print(self.croquis_en_us["Nom"], "\n", self.position, ": ", self.text)
        # if self.interval != None:
            # self.drive_callback()
            # self.interval.start()
        self.forget()

    # def drive_callback(self):
    #     print(self.text)
    #     try:
    #         self.sheet.worksheet(self.croquis_en_us["Nom"]).update_cell(2, list(self.croquis_en_us.keys()).index(self.position)+1,  value=self.text)
    #         print("exito")
    #     except:
    #         print("mistake was sucedido")

    def search_items(self, _event):
        search_value = self.entry.get()
        self.entry.focus_force()
        self.working_values = list(set(self.values) ^ set([i.upper() for i in list(self.croquis_en_us.values())[2:]]))
        if search_value == "" or search_value == " ":
            self.lb.delete(0, "end")
            try:
                self.working_values.sort(key = lambda x: self.dataframe.loc[self.dataframe["Àlies"].str.upper() == x].iloc[0, 2], reverse=True)
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
                value_to_display.sort(key = lambda x: self.dataframe.loc[self.dataframe["Àlies"].str.upper() == x].iloc[0, 2], reverse=True)
            except:
                pass
            self.lb.delete(0, "end")
            for i in value_to_display:
                self.lb.insert("end",i)
            self.lb.insert("end", self.textvar.get())


    def on_click(self, _event):
        self.entry.delete(0, "end")
        print(self.text)
        print(self.location)
        print(self.orientation)
        if not self.toggle:
            self.working_values = list(set(self.values)^set([i.upper() for i in list(self.croquis_en_us.values())[2:]]))
            if "N. A." in list(self.working_values):
                self.working_values.remove("N. A.")

            try:
                self.working_values.sort(reverse=True,key = lambda x: self.dataframe.loc[self.dataframe["Àlies"].str.upper() == x].iloc[0, 2])
            except:
                pass
            #Configurar el dropdown:
            self.lb.place(x=self.parent.coords(self.txt)[0]- self.entry_width/3+15,
                          y=self.parent.coords(self.txt)[1]+ self.entry_height*2-5)
            self.sb = tkinter.Scrollbar(self.parent)
            self.lb.delete(0, "end")
            for i in self.working_values:
                self.lb.insert("end", i)
            self.lb.config(yscrollcommand=self.sb.set)
            self.sb.config(command=self.lb.yview)

            #Debugging per a windows laptops
            # print(_event.x, ",", _event.y)
            # print(self.parent.coords(self.txt)[0], ",", self.parent.coords(self.txt)[1])
            # print(self.parent.coords(self.txt)[0]- self.entry_width/2+2, ",", self.parent.coords(self.txt)[1]+ self.entry_height-5)

            self.entry.place(x=self.parent.coords(self.txt)[0], y=self.parent.coords(self.txt)[1], anchor="center")

            self.entry.focus_set()

            def forget(_event):
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
            elif self.text.split(" ")[0] == "+":
                self.parent.itemconfig(self.shape, fill="")
            else:
                self.parent.itemconfig(self.shape, fill="")
        else:
                self.parent.itemconfig(self.shape, fill="")


    def on_right_click(self, _event, downloading = False):
        if self.position.split(" ")[0] not in ["Base", "Segona", "Tercera", "Alsadora", "Quarta"]:
            if not self.toggle:
                self.toggle = True
                self.text = "'+"
                self.parent.itemconfig(self.shape, fill = "", outline = "")
                self.parent.itemconfig(self.txt, font=("Arial", 14), text = "+", fill =self._apply_appearance_mode(("#333333","#AAAAAA") ))
                self.croquis_en_us[self.position] = self.text
                current_values = self.taula.item((list(self.croquis_en_us.keys()).index(self.position)) - 1).get("values")
                current_values[1] = "+"
                self.taula.item((list(self.croquis_en_us.keys()).index(self.position)) - 1, values = current_values)
            else:
                self.parent.itemconfig(self.shape, fill="", outline=self._apply_appearance_mode(self.color2))

                self.text = self.position.split(" ")[0]
                self.parent.itemconfig(self.txt, text = self.text,font = ("Arial", self.text_size,"bold"), fill = self._apply_appearance_mode(("#333333","#AAAAAA")))
                self.croquis_en_us[self.position] = "N. A."

                current_values = self.taula.item((list(self.croquis_en_us.keys()).index(self.position)) - 1).get("values")
                current_values[1] = self.text
                self.taula.item((list(self.croquis_en_us.keys()).index(self.position)) - 1, values = current_values)

                self.toggle = False

            if self.interval != None and not downloading:
                self.interval.stop()
                #self.drive_callback()
                self.interval.start()

