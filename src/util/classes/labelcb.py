import customtkinter
import src.Figures as fig
from CTkScrollableDropdown import *



class LabelCB(customtkinter.CTkFrame):
    def __init__(self,parent,text, values,taula ,croquis_en_us, filtre = None, color = None):
        super().__init__(master=parent)
        self.text = text
        self.values = values
        self.croquis_en_us = croquis_en_us
        self.taula = taula
        self.filtre = filtre
        self.rowconfigure((0,1),weight=1)
        self.grid_rowconfigure(1,weight=0)
        self.columnconfigure(0,weight=1)
        self.color = color



        customtkinter.CTkLabel(self, text = text).grid(row=1,column=0,sticky="nsew")
        combobox = customtkinter.CTkPaComboBox(self,
                                             values = self.values,
                                             border_color= self.color,
                                             button_color= self.color,
                                             command = self.insertar_membre, fg_color = self.color,
                                             )
        combobox.grid(row=0,column=0,sticky="nsew")
        combobox.set(self.text)

    def insertar_membre(self, value):
        self.croquis_en_us.update({self.text: value})
        self.taula.insert(list(self.croquis_en_us).index(self.text),1,value)
