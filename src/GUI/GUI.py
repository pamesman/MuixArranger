from tkinter import PhotoImage
import customtkinter
from PIL import Image
from customtkinter import CTkButton
import CTkMessagebox


#from CTkScrollableDropdown import *
from src.util.classes import CTkTable
from src.util.classes.labelcb import LabelCB

import src.membre as membre
from src.util import repertori as rep
import src.util.funcs as f




llistadebutons = {}
#estableix parent window
image=customtkinter.CTkImage(light_image=Image.open("icon.png"))
root = customtkinter.CTk()
root.geometry("1280x720")
root.iconphoto(False,PhotoImage(file="icon.png"))
root.title("Crokiss")
customtkinter.set_appearance_mode("dark") #set theme

tabview = customtkinter.CTkTabview(master=root)
tabview.place(relx = 0.5, rely = 0.5, anchor="c", relheight=.99, relwidth=.99)

croquis = tabview.add("Croquis")  # add tab at the end
#assaig = tabview.add("Assaig")  # add tab at the end

assaig = {}


### CROQUIS TAB ###

frame = customtkinter.CTkFrame(master=tabview.tab("Croquis"))
frame.place(relx=0.5,rely=0.5,anchor="c",relheight=1, relwidth=1)
#REPERTORI
repertori_frame = customtkinter.CTkScrollableFrame(frame)
repertori_frame.place(relx=.01,rely=.07, relheight=0.92,relwidth=0.1,anchor="nw")


#Frame per a taula croquis
croquis_frame = customtkinter.CTkScrollableFrame(frame)
croquis_frame.place(relx=.79, rely=.5, anchor="w", relheight=.98, relwidth=0.2)
dictionario = [["Posició","Nom","Alçada"],
               ["Base1","Oriol",137,4,5,6],
               ["Base2","Lua",302,4,5,6],
               ["Alçadora","Toni Ciscar",113,4,5,6],
               ["Xicalla","Guillem Antich",140,4,5,6]]
taula = CTkTable.CTkTable(croquis_frame, column= 3, row=2, values=[[]], header_color="#7393B3", font=("Liberation Sans", 12), corner_radius=5)

taula_name = customtkinter.CTkLabel(croquis_frame, text="")
taula_name.pack()
taula_namefig = customtkinter.CTkLabel(croquis_frame, text="")
taula_namefig.pack()
taula.pack(expand=True,  pady=20)

#def taula_update():
#    f.croquis_to_table(croquis_in_use,membre.taula_mestra)
#Posibilitat de estalviar memoria? Comprovar quant ha canviat el croquis d'abans a ara i input vs update
croquis_in_use = {}
#croquis_in_use.trace_add("write",taula_update)
registre_labels = []

def figure_press(selected_fig):
    global registre_labels
    repertori_label.set("Afegir figura")
    namer.configure(state="normal")
    namer_button.configure(state="normal")
    counter = 1
    #contador per a numerar el nom genèric de la figura creada
    for figura in assaig.keys():
        if selected_fig in assaig[figura]["Figura"]:
            counter += 1
    dialog_nom = customtkinter.CTkInputDialog(text=f"Com vols identificar aquest/a {selected_fig}?",
                                              title="Nomena la figura", placeholder_text = str(selected_fig) + str(counter))


    answer = dialog_nom.get_input()
    if answer in assaig.keys():
        alerta = CTkMessagebox.CTkMessagebox(title="Alerta",
                               message="Ja hi ha una figura en aquest nom, estàs segur que vols sobreescriure-la?",
                               option_1= "Sobreescriu",
                               option_2 = "Cancelar" )
        if alerta.get() == "Sobreescriu":
            pass
        if alerta.get() == "Cancelar":
            pass
    #busca quin ESQUEMA conté el NOM selected_fig
    for figura in rep.repertori.values():
        global croquis_in_use
        coordenades = []
        corrector = ()
        if selected_fig == figura.nom:
            coordenades = figura.coordenades
            corrector = figura.centraor()
            if answer != "" :
                croquis_in_use = f.fer_croquis(figura, answer)
            else:
                croquis_in_use = f.fer_croquis(figura, str(selected_fig) +" "+ str(counter))
            break
        else:

            pass
    for i in registre_labels:
        for j in i[1]:
            j.destroy()
    assaig.update({croquis_in_use["Nom"]: croquis_in_use})

    def assaig_button_press(nom):
        croquis_in_use = assaig[nom]
        taula.update_values(f.croquis_to_table(croquis_in_use, membre.taula_mestra))
        for i in registre_labels:
            if i[0][0] != nom:
                for j in i[1]:
                    j.destroy()

        fer_dibuix(coordenades, croquis_in_use, corrector)
        pass

    namer.configure(placeholder_text=croquis_in_use["Nom"])

    taula.update_values(f.croquis_to_table(croquis_in_use, membre.taula_mestra))

    taula_namefig.configure(text="Figura: " + croquis_in_use["Figura"])
    taula_name.configure(text="Id: " + croquis_in_use["Nom"])
    registre_labels = [fer_dibuix(coordenades, croquis_in_use, corrector)]
    button = customtkinter.CTkButton(repertori_frame, text=croquis_in_use["Nom"],
                                     command=lambda nom = croquis_in_use["Nom"]:assaig_button_press(nom),
                                     fg_color="#C03530", font = ("Arial", 12))
    button._text_label.place(x=0, rely = 0.5, anchor = "w")
    button.pack(pady=5)
    return croquis_in_use

repertori_label = customtkinter.CTkComboBox(frame,
                                            fg_color="#36454F", button_color="#36454F",corner_radius=5, font=("Liberation Sans",16, "bold"), border_width= 0,
                                            values = [i.nom for i in rep.repertori.values()],
                                            command = figure_press)
repertori_label.set("Afegir figura")
repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.1*0.99)

buttonlist1 = []

"""
Per dibuixar la figura
"""

def fer_dibuix(listadecoordenades:list, croquiss:dict, corrector: tuple):
    counter = 0
    netejadora = [[],[]]
    for i in croquiss.keys():
        if i == "Nom" :
            netejadora[0].append(croquiss[i])
            continue
        if i == "Figura":
            continue
        combobox = LabelCB(frame_qv,
                           i,
                           membre.working_list[:25],
                           taula,
                           croquiss,
                           membre.taula_mestra,
                           color= (rep.palette[rep.rols.index(i.split(" ")[0])+1],rep.palette_d[rep.rols.index(i.split(" ")[0])+1]))

        coord = listadecoordenades[counter]
        #CTkScrollableDropdown(attach=combobox, values=[ident +" "+ i for i in membre.working_list[0:25+int(coord[1])]], width=200)
        llistadebutons.update({i:combobox}) #no se si açò es util
        netejadora[1].append(combobox)
        for j in ["Tap","Agulla","Peu","Colze"]:
            if j in combobox.text:
                relwidth = 1/30
                #combobox.configure(font)
                break
            else:
                relwidth = 1/20
        combobox.place(relx =0.5+ (coord[0]-(corrector[0][0]+corrector[0][1])/2)/(corrector[0][0]-corrector[0][1])/1.2*(len(croquiss.keys())+15)/100 ,
                       rely = 0.5 - (coord[1]-(corrector[1][0]+corrector[1][1])/2)/(corrector[1][0]-corrector[1][1])/1.2*(len(croquiss.keys())+15)/200  ,

                        #relx=coord[0]/15+1/15,
                       #rely=1-(coord[1]/11)-3/11, anchor="w",
                       relwidth=relwidth,
                       relheight = 2/45/2,
                       anchor = "center"
                       )

        counter += 1
        for child in frame_qv.winfo_children():
            if type(child) == customtkinter.CTkButton or type(child) == customtkinter.CTkEntry:
                continue
            #child.place_forget()
    registre_labels.append(netejadora)
    #print(f"length registe = {len(registre_labels)}")
    #for i in registre_labels:
     #   print(i[0])
    return netejadora

"""
figure_press funciona per als side buttons amb les figures del repertori. Agafa el butto, forma el croquis per a displayearlo en la taula i l'afegeix a un 
"working_Set", que guarda el progrés que s'haja fet en cada figura abans de commitearlos a Assaig.
OJO!!! No guarda cap nom en particular, nom="nomdelafigura"
"""



"""
Falta funcionalitat: canviar també el contingut de croquis frame
"""

"""
A l'apartat repertori es genera 1 buttó per cada figura al diccionari "repertori", i s'asocia a el command definit per la funció de dalt
"""
#for i in rep.repertori.keys():
#    def button_pressed():
#        print(buttonlist1)
#    button = customtkinter.CTkButton(repertori_frame,text = rep.repertori[i].nom, command=lambda iden=i: figure_press(iden),
#                                     fg_color=paleta[1],)
#    button.pack(padx=2,pady=8,expand=True)
#    buttonlist1.append(button)




#CROQUIS

frame_qv = customtkinter.CTkFrame(frame, fg_color=("#FFFFFF","#333333"))
frame_qv.place(relx = 0.12,rely=0.5,anchor="w",relheight=0.98, relwidth=.66)
#NOM FIGURA
namer = customtkinter.CTkEntry(frame_qv, placeholder_text= "Nom de Figura-X", font=("Liberation Sans",16,"bold"),state="disabled")
def actualitzar_nom_figura():
    croquis_in_use["Nom"] = namer.get()
    taula.update_values(f.croquis_to_table(croquis_in_use, membre.taula_mestra))
    taula_namefig.configure(text="Figura: "+croquis_in_use["Figura"])
    taula_name.configure(text="Id: " + namer.get())
namer_button = customtkinter.CTkButton(frame_qv, text="Actualitzar nom",font=("Liberation Sans",14,"bold"),height= 28, command= actualitzar_nom_figura, state="disabled")
namer_button.place(relx = 0.42,rely = 0.01,  anchor= "nw")

namer.place(relx=0.01, rely=0.01, relwidth=0.4)

#botó per expandir croquis zone
expand_is_on = False
expand_is_on2 = False
def minimizar2():
    global expand_is_on
    global expand_is_on2
    if not expand_is_on2:
        button_expand2.configure(text="<")
    else:
        button_expand2.configure(text=">")

    if not expand_is_on:
        if not expand_is_on2:
            croquis_frame.place(relx=.99, rely=.5, anchor="e", relheight=.98, relwidth=0.01)
            frame_qv.place(relx = 0.12,rely=0.5,anchor="w",relheight=0.98, relwidth=0.87)
            expand_is_on2 = True
        else:
            croquis_frame.place(relx=.99, rely=.5, anchor="e", relheight=.98, relwidth=0.2)
            frame_qv.place(relx=0.12, rely=0.5, anchor="w", relheight=0.98, relwidth=.66)
            expand_is_on2 = False
    else:
        if not expand_is_on2:
            croquis_frame.place(relx=.99, rely=.5, anchor="e", relheight=.98, relwidth=0.01)
            frame_qv.place(relx = 0.07,rely=0.5,anchor="w",relheight=0.98, relwidth=0.92)
            expand_is_on2 = True
        else:
            croquis_frame.place(relx=.99, rely=.5, anchor="e", relheight=.98, relwidth=0.2)
            frame_qv.place(relx=0.07, rely=0.5, anchor="w", relheight=0.98, relwidth=0.71)
            expand_is_on2 = False

def minimizar():
    global expand_is_on
    global expand_is_on2
    if not expand_is_on:
        button_expand.configure(text=">")
    else:
        button_expand.configure(text="<")

    if not expand_is_on2:
        if not expand_is_on:
            frame_qv.place(relx=0.07, rely=0.5, anchor="w", relheight=0.98, relwidth=.71)
            repertori_frame.place(relx=.01, rely=.07, relheight=0.92, relwidth=0.05, anchor="nw")
            repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.05*0.99)


            expand_is_on = True
        else:
            frame_qv.place(relx=0.12, rely=0.5, anchor="w", relheight=0.98, relwidth=.66)
            repertori_frame.place(relx=.01, rely=.07, relheight=0.92, relwidth=0.1, anchor="nw")
            repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.1*0.99)

            expand_is_on = False
    else:
        if not expand_is_on:
            frame_qv.place(relx=0.07, rely=0.5, anchor="w", relheight=0.98, relwidth=0.92)
            repertori_frame.place(relx=.01,rely=.07, relheight=0.92,relwidth=0.05,anchor="nw")
            repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.05*0.99)

            expand_is_on = True
        else:
            frame_qv.place(relx=0.12, rely=0.5, anchor="w", relheight=0.98, relwidth=.87)
            repertori_frame.place(relx=.01, rely=.07, relheight=0.92, relwidth=0.1, anchor="nw")
            repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.1)

            expand_is_on = False
button_expand = customtkinter.CTkButton(frame_qv,
                                        text = "<",
                                        height = 10,
                                        width = 10,
                                        corner_radius= 15,
                                        command = minimizar)
                                        #repertori_frame._parent_frame.forget())

button_expand2 = customtkinter.CTkButton(frame_qv,
                                        text = ">",
                                        height = 10,
                                        width = 10,
                                        corner_radius= 15,
                                        command = minimizar2)
                                        #repertori_frame._parent_frame.forget())
button_expand.place(rely = 0.5, relx = .005, anchor="w")
button_expand2.place(rely = 0.5, relx = .995, anchor="e")



def canviar_apariencia():
    if customtkinter.get_appearance_mode() == "Dark":
        customtkinter.set_appearance_mode("light")
    else:
        customtkinter.set_appearance_mode("dark")
CTkButton(frame,text = "☀ / ☾",command=canviar_apariencia, width = 20).place(relx=1, rely=1, anchor="se")




root.mainloop()