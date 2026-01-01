import tkinter
import customtkinter
from PIL import Image
from customtkinter import CTkButton
import CTkMessagebox
import math
from src.util.classes.canvastextclass import CanvasText


#from CTkScrollableDropdown import *
from src.util.classes import CTkTable


import src.membre as membre
from src.util import repertori as rep
import src.util.funcs as f




llistadebutons = {}
#estableix parent window
image=customtkinter.CTkImage(light_image=Image.open("icon.png"))
root = customtkinter.CTk()
root.geometry("1280x720")
root.iconphoto(False,tkinter.PhotoImage(file="icon.png"))
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

croquis_in_use = {}
registre_labels = []
frame_qv = customtkinter.CTkFrame(frame, fg_color=("#FFFFFF","#333333"))
frame_qv.place(relx = 0.12,rely=0.5,anchor="w",relheight=0.98, relwidth=.66)
frame_qv.update()
old_height = frame_qv.winfo_height()-frame_qv.cget("corner_radius")*2
old_width = frame_qv.winfo_width()-frame_qv.cget("corner_radius")*4
canvas2 = tkinter.Canvas(frame_qv, width=old_width, height=old_height, bg=frame_qv._apply_appearance_mode(("black","#333333")), highlightthickness=0)
canvas2.place(relx=0.5, rely=0.5, anchor="center")


def resize(event):
    canvas2.config(width=event.width - frame_qv.cget("corner_radius") * 4,
                   height=event.height - frame_qv.cget("corner_radius") * 2)
    global old_width
    global old_height
    w1 = old_width
    w2 = event.width - frame_qv.cget("corner_radius") * 4
    h1 = old_height
    h2 = event.height - frame_qv.cget("corner_radius") * 2
    for i in canvas2.find_withtag("etiqueta"):
        x = canvas2.coords(i)[0]
        y = canvas2.coords(i)[1]
        canvas2.coords(i, x * w2 / w1, y * h2 / h1)
    for i in canvas2.find_withtag("rectangle"):
        x = canvas2.coords(i)[8]*0.5+canvas2.coords(i)[28]*0.5
        y = canvas2.coords(i)[9]*0.5+canvas2.coords(i)[29]*0.5

        canvas2.move(i,  (w2 / w1-1)*x,  (h2 / h1-1)*y)
    old_height = event.height - frame_qv.cget("corner_radius") * 2
    old_width = event.width - frame_qv.cget("corner_radius") * 4

frame_qv.bind("<Configure>", resize)
buttonlist1 = {}
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
    canvas2.delete("all")
    assaig.update({croquis_in_use["Nom"]: croquis_in_use})

    def assaig_button_press(nom):
        global croquis_in_use
        global canvas2
        croquis_in_use = assaig[nom]
        taula.update_values(f.croquis_to_table(croquis_in_use, membre.taula_mestra))
        canvas2.delete("all")

        fer_dibuix(coordenades, croquis_in_use, corrector)
        namer.delete(0, "end")
        namer.configure(placeholder_text=croquis_in_use["Nom"])
        taula_namefig.configure(text="Figura: " + croquis_in_use["Figura"])
        taula_name.configure(text="Id: " + croquis_in_use["Nom"])
        pass
    namer.configure(placeholder_text=croquis_in_use["Nom"])


    taula.update_values(f.croquis_to_table(croquis_in_use, membre.taula_mestra))

    taula_namefig.configure(text="Figura: " + croquis_in_use["Figura"])
    taula_name.configure(text="Id: " + croquis_in_use["Nom"])
    registre_labels = [fer_dibuix(coordenades, croquis_in_use, corrector)]
    button = customtkinter.CTkButton(repertori_frame, text=croquis_in_use["Nom"],
                                     command=lambda nom = croquis_in_use["Nom"]:assaig_button_press(nom),
                                     fg_color = rep.main_color,hover_color=rep.inv_color, font = ("Arial", 14,"bold"))
    button._text_label.place(x=0, rely = 0.5, anchor = "w")
    button.pack(pady=5)
    global buttonlist1
    buttonlist1.update({croquis_in_use["Nom"]: button})
    return croquis_in_use

repertori_label = customtkinter.CTkComboBox(frame,
                                            fg_color=rep.main_color, button_color=rep.main_color,button_hover_color=rep.inv_color,corner_radius=5, font=("Liberation Sans",16, "bold"), border_width= 0,
                                            values = [i.nom for i in rep.repertori.values()],
                                            command = figure_press)
repertori_label.set("Afegir figura")
repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.1*0.99)




"""
Per dibuixar la figura
"""

def fer_dibuix(listadecoordenades:list, croquiss:dict, corrector: tuple):
    counter = 0
    netejadora = [[],[]]
    frame_qv.update()

    for i in croquiss.keys():
        if i == "Nom" :
            netejadora[0].append(croquiss[i])
            continue
        if i == "Figura":
            continue

        coord = listadecoordenades[counter]
        if i.split(" ")[0] not in ["Segona", "Tercera","Quarta","Xicalla", "Alsadora", "Passadora", "Recollidora"]:
            sc = -0
            try:
                if coord[1] >= sc:
                    orientation = math.degrees(math.atan(coord[0] / (coord[1]-sc)))
                elif coord[1] <= -sc:
                    orientation = math.degrees(math.atan(coord[0] / (coord[1]+sc)))
                else:
                    orientation = math.degrees(math.atan(coord[0] / (coord[1])))
            except:
                if coord[0] > 0:
                    orientation = 90
                if coord[0] < 0:
                    orientation = -90
                if coord[0] == 0:
                    orientation = 0
        else:
            orientation = 0

        CanvasText(root, canvas2,
                              i, listadecoordenades[counter],corrector,
                              membre.working_list, taula, croquiss, membre.taula_mestra,
                              orientation = -orientation,
                              color =rep.palette[rep.rols.index(i.split(" ")[0])],list_len=10)

        counter += 1
        for child in frame_qv.winfo_children():
            if type(child) == customtkinter.CTkButton or type(child) == customtkinter.CTkEntry:
                continue

    try:
        canvas2.tag_raise("Base", "Tap")
    except:
        pass
    try:
        canvas2.tag_raise("Base", "Peu")
    except:
        pass
    try:
        canvas2.tag_lower("Tap", "Mans")
    except:
        pass
    try:
        canvas2.tag_raise("Mans", "Vents")
    except:
        pass
    canvas2.tag_lower("rectangle", "etiqueta")
    registre_labels.append(netejadora)
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

#NOM FIGURA
namer = customtkinter.CTkEntry(frame_qv, placeholder_text= "Nom de Figura-X", font=("Liberation Sans",16,"bold"),state="disabled")
def actualitzar_nom_figura():
    buttonlist1[croquis_in_use["Nom"]].configure(text=namer.get())
    buttonlist1.update({namer.get(): buttonlist1[croquis_in_use["Nom"]]})
    del buttonlist1[croquis_in_use["Nom"]]
    croquis_in_use["Nom"] = namer.get()


    taula.update_values(f.croquis_to_table(croquis_in_use, membre.taula_mestra))
    taula_namefig.configure(text="Figura: "+croquis_in_use["Figura"])
    taula_name.configure(text="Id: " + namer.get())
namer_button = customtkinter.CTkButton(frame_qv, text="Actualitzar nom",font=("Liberation Sans",14,"bold"),height= 28, command= actualitzar_nom_figura, state="disabled", fg_color = rep.main_color, hover_color=rep.inv_color)
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
                                        command = minimizar,
                                        fg_color =rep.main_color, hover_color=rep.inv_color)
                                        #repertori_frame._parent_frame.forget())

button_expand2 = customtkinter.CTkButton(frame_qv,
                                        text = ">",
                                        height = 10,
                                        width = 10,
                                        corner_radius= 15,
                                        command = minimizar2,
                                        fg_color =rep.main_color, hover_color=rep.inv_color)
                                        #repertori_frame._parent_frame.forget())
button_expand.place(rely = 0.5, relx = .005, anchor="w")
button_expand2.place(rely = 0.5, relx = .995, anchor="e")



def canviar_apariencia():
    if customtkinter.get_appearance_mode() == "Dark":
        customtkinter.set_appearance_mode("light")

    else:
        customtkinter.set_appearance_mode("dark")
    canvas2.config(bg=frame._apply_appearance_mode(("#FFFFFF","#333333")))
CTkButton(frame,text = "☀ / ☾",command=canviar_apariencia, width = 20,fg_color =rep.main_color, hover_color=rep.inv_color).place(relx=1, rely=1, anchor="se")




root.mainloop()