from tkinter import PhotoImage
import pandas as pd
import customtkinter

from PIL import Image
from CTkScrollableDropdown import *
import CTkTable


import src.Figures as fig

t = pd.read_excel("/home/paco/Desktop/100personas.ods") #Guarda el excel, açò eu ha de fer el backend
#estableix parent window
image=customtkinter.CTkImage(light_image=Image.open("icon.png"))
root = customtkinter.CTk()
root.geometry("1280x720")
root.iconphoto(False,PhotoImage(file="icon.png"))
#set theme
customtkinter.set_appearance_mode("dark")
button = customtkinter.CTkButton(root)
#button.place(relx=0.5,rely=0.5,anchor="center")
tabview = customtkinter.CTkTabview(master=root)
tabview.place(relx = 0.5, rely = 0.5, anchor="c", relheight=.99, relwidth=.99)

croquis = tabview.add("Croquis")  # add tab at the end
assaig = tabview.add("Assaig")  # add tab at the end


#tabs = CTkSegmentedButton(root,values=["Croquis","Assaig/Actuació"],corner_radius=50, font=("Liberation Sans",24,"bold"),border_width=4)
#tabs.place(relx=0.5,rely=0.025,anchor="n",relwidth=0.99, relheight=0.05)
#def tabs_callback(tabs):

#CROQUIS TAB
frame = customtkinter.CTkFrame(master=tabview.tab("Croquis"))
frame.place(relx=0.5,rely=0.5,anchor="c",relheight=1, relwidth=1)
#REPERTORI
repertori_frame = customtkinter.CTkScrollableFrame(frame)
repertori_frame.place(relx=.01,rely=.07, relheight=0.92,relwidth=0.1,anchor="nw")
#repertori_frame2 = customtkinter.CTkFrame(frame)
#repertori_frame2.place(relheight=0.09,relwidth=0.1,relx=.01,rely=.01,anchor="nw")
repertori_label = customtkinter.CTkLabel(frame, text= "Figures", fg_color="#36454F",corner_radius=5, font=("Liberation Sans",18, "bold"))
repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.1*0.99)


buttonlist1 = []
working_set = {}
croquis_in_use = {}


"""
figure_press funciona per als side buttons amb les figures del repertori. Agafa el butto, forma el croquis per a displayearlo en la taula i l'afegeix a un 
"working_Set", que guarda el progrés que s'haja fet en cada figura abans de commitearlos a Assaig.
OJO!!! No guarda cap nom en particular, nom="nomdelafigura"
"""
def figure_press(figureid):
    print("pressed",fig.repertori[figureid].nom)
    namer.configure(state="normal")
    namer_button.configure(state="normal")
    global croquis_in_use
    croquis_in_use= fig.fer_croquis(fig.repertori[figureid],fig.repertori[figureid].nom)
    taula.update_values(fig.croquis_to_table(croquis_in_use))
    taula_namefig.configure(text="Figura: " + croquis_in_use["Figura"])
    taula_name.configure(text="Id: " + croquis_in_use["Nom"])
    if fig.repertori[figureid].nom not in working_set:
        working_set.update({fig.repertori[figureid].nom:croquis_in_use})
    print(working_set)
    return croquis_in_use
"""
Falta funcionalitat: canviar també el contingut de croquis frame
"""

"""
A l'apartat repertori es genera 1 buttó per cada figura al diccionari "repertori", i s'asocia a el command definit per la funció de dalt
"""
for i in fig.repertori.keys():
    def button_pressed():
        print(buttonlist1)
    button = customtkinter.CTkButton(repertori_frame,text = fig.repertori[i].nom, command=lambda iden=i: figure_press(iden))
    button.pack(padx=2,pady=8,expand=True)
    buttonlist1.append(button)




#Frame per a taula croquis
Croquis_frame = customtkinter.CTkScrollableFrame(frame)
Croquis_frame.place(relx=.99,rely=.5,anchor="e",relheight=.98, relwidth=0.2)
dictionario = [["Posició","Nom","Alçada"],["Base1","Oriol",137,4,5,6],["Base2","Lua",302,4,5,6],["Alçadora","Toni Ciscar",113,4,5,6],["Xicalla","Guillem Antich",140,4,5,6]]
taula = CTkTable.CTkTable(Croquis_frame, column= 3,row=60,values=dictionario, header_color="#7393B3", font=("Liberation Sans",12), corner_radius=5)

taula_name = customtkinter.CTkLabel(Croquis_frame, text="Figura:")
taula_name.pack()
taula_namefig = customtkinter.CTkLabel(Croquis_frame, text="Id:")
taula_namefig.pack()
taula.pack(expand=True,  pady=20)
#CROQUIS

frame_qv = customtkinter.CTkFrame(frame)
frame_qv.place(relx = 0.45,rely=0.5,anchor="c",relheight=0.98, relwidth=.66)
#NOM FIGURA
namer = customtkinter.CTkEntry(frame_qv, placeholder_text= "Nom de Figura-X", font=("Liberation Sans",24,"bold"),state="disabled")
def actualitzar_nom_figura():
    croquis_in_use["Nom"] = namer.get()
    taula.update_values(fig.croquis_to_table(croquis_in_use))
    print(croquis_in_use)
    taula_namefig.configure(text="Figura: "+croquis_in_use["Figura"])
    taula_name.configure(text="Id: " + namer.get())
namer_button = customtkinter.CTkButton(frame_qv, text="Actualitzar nom",font=("Liberation Sans",18,"bold"),height= 34, command= actualitzar_nom_figura, state="disabled")
namer_button.place(relx = 0.42,rely = 0.01,  anchor= "nw")

namer.place(relx=0.01, rely=0.01, relwidth=0.4)

#Butó confirmar figura per al assaig
button = customtkinter.CTkButton(frame_qv, text="Afegir",font=("Liberation Sans",18,"bold"),corner_radius=500, width=20,height=20, image=image)
button.pack(side="bottom", anchor="se", padx=10, pady=10)





root.mainloop()