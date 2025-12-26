import customtkinter
from src.util.classes.SearchBox import SearchBox

#from CTkScrollableDropdown import *


class LabelCB(customtkinter.CTkFrame):
    def __init__(self,parent,text, values,taula ,croquis_en_us,dataframe, filtre = None, color = None, text_size = 12):
        super().__init__(master=parent)
        self.text = text
        self.values = values
        self.croquis_en_us = croquis_en_us
        self.taula = taula
        self.filtre = filtre
        self.rowconfigure((0,1),weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.columnconfigure(0,weight=1)
        self.color = color
        self.dataframe = dataframe
        self._fg_color = ("#FFFFFF","#333333")

        #if text in ["Tap","Agulla","Tercera","Peu"]
        #customtkinter.CTkLabel(self, text = text).grid(row=1,column=0,sticky="nsew")
        self.combobox = SearchBox(self,
                                             #text_color = ("black","white"),
                                             text_color="black",
                                             values = self.values,
                                             border_color= self.color,
                                             button_color= self.color,
                                             button_hover_color= (self.color[1],self.color[0]),
                                             command = self.insertar_membre, fg_color = self.color,
                                             placeholder=self.text
                                             )
        self.combobox.grid(row=0,column=0,sticky="nsew")
        self.combobox._entry.insert(0,self.croquis_en_us[self.text])
        self.combobox.set(self.text)
        self.combobox.configure(corner_radius=3)

    def insertar_membre(self, value):

        self.combobox.comando(value)

        self.combobox.reset_placeholder(value)
        self.combobox._entry.insert(0, value)
        self.croquis_en_us.update({self.text: value})
        self.taula.insert(list(self.croquis_en_us).index(self.text)-1, 1, value)
        self.taula.insert(list(self.croquis_en_us).index(self.text)-1,2,self.dataframe.loc[self.dataframe["Nom"]==value].iloc[0,1])
        if value != self.text:
            self.combobox.configure(fg_color="green")