import tkinter
import customtkinter
from PIL import Image
from customtkinter import CTkButton
import CTkMessagebox
import math
from src.util.classes.canvastextclass import CanvasText
from src.API import credential_managing as drive
from src.util.classes.interval import Interval

#from CTkScrollableDropdown import *
from src.util.classes import CTkTable


import src.membre as membre
from src.util import repertori as rep
import src.util.funcs as f





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
#INICIALITZACIÓ DE VARIABLES
assaig = {}
croquis_in_use = {}
#FUNCIONS
"""
GESTIONA REDIMENSIONS DEL CROQUIS
"""
def resize(event):
    canvas2.config(width=event.width - croquis_frame.cget("corner_radius") * 4,
                   height=event.height - croquis_frame.cget("corner_radius") * 2)
    global old_width
    global old_height
    w1 = old_width
    w2 = event.width - croquis_frame.cget("corner_radius") * 4
    h1 = old_height
    h2 = event.height - croquis_frame.cget("corner_radius") * 2
    for i in canvas2.find_withtag("etiqueta"):
        x = canvas2.coords(i)[0]
        y = canvas2.coords(i)[1]
        canvas2.coords(i, x * w2 / w1, y * h2 / h1)
    for i in canvas2.find_withtag("rectangle"):
        x = canvas2.coords(i)[8]*0.5+canvas2.coords(i)[28]*0.5
        y = canvas2.coords(i)[9]*0.5+canvas2.coords(i)[29]*0.5
        canvas2.move(i,  (w2 / w1-1)*x,  (h2 / h1-1)*y)
    old_height = event.height - croquis_frame.cget("corner_radius") * 2
    old_width = event.width - croquis_frame.cget("corner_radius") * 4

### CROQUIS TAB ###

frame = customtkinter.CTkFrame(master=tabview.tab("Croquis"))
frame.place(relx=0.5,rely=0.5,anchor="c",relheight=1, relwidth=1)

#FIGURES
repertori_frame = customtkinter.CTkScrollableFrame(frame)
repertori_frame.place(relx=.01,rely=.07, relheight=0.92,relwidth=0.1,anchor="nw")


#TAULA
taula_frame = customtkinter.CTkScrollableFrame(frame)
taula_frame.place(relx = .79, rely = .5, anchor = "w", relheight = .98, relwidth = 0.2)

taula = CTkTable.CTkTable(taula_frame, column = 3, row = 2, values = [[]], header_color = "#7393B3", font = ("Liberation Sans", 12), corner_radius = 5)
taula_name = customtkinter.CTkLabel(taula_frame, text = "")
taula_namefig = customtkinter.CTkLabel(taula_frame, text = "")
taula_name.pack()
taula_namefig.pack()
taula.pack(expand = True,  pady = 20)


#CROQUIS
croquis_frame = customtkinter.CTkFrame(frame, fg_color = ("#FFFFFF", "#333333"))
croquis_frame.place(relx = 0.12, rely = 0.5, anchor ="w", relheight = 0.98, relwidth = .66)
croquis_frame.update()
old_height = croquis_frame.winfo_height() - croquis_frame.cget("corner_radius") * 2
old_width = croquis_frame.winfo_width() - croquis_frame.cget("corner_radius") * 4
croquis_frame.bind("<Configure>", resize)
canvas2 = tkinter.Canvas(croquis_frame, width=old_width, height=old_height, bg=croquis_frame._apply_appearance_mode(("black", "#333333")), highlightthickness=0)
canvas2.place(relx=0.5, rely=0.5, anchor="center")

#Darkmode
def canviar_apariencia():
    if customtkinter.get_appearance_mode() == "Dark":
        customtkinter.set_appearance_mode("light")

    else:
        customtkinter.set_appearance_mode("dark")
    canvas2.config(bg=frame._apply_appearance_mode(("#FFFFFF","#333333")))
CTkButton(frame,text = "☀ / ☾",command=canviar_apariencia, width = 20,fg_color =rep.main_color, hover_color=rep.inv_color).place(relx=1, rely=1, anchor="se")



buttonlist1 = {}
registre_labels = []
def crear_figura(selected_fig):
    global registre_labels
    global buttonlist1
    repertori_label.set("Afegir figura")    #Restaura combobox
        #Activa "namer"
    namer.configure(state="normal")
    namer_button.configure(state="normal")
    counter = 1    #contador per a numerar el nom genèric de la figura creada
    for figura in assaig.keys():
        if selected_fig in assaig[figura]["Figura"]:
            counter += 1
        #Demana nom al user
    dialog_nom = customtkinter.CTkInputDialog(text=f"Com vols identificar aquest/a {selected_fig}?",title="Nomena la figura", placeholder_text = str(selected_fig) + str(counter))
    answer = dialog_nom.get_input()
        #Comprovació: noms repetits
    if answer in assaig.keys():
        alerta = CTkMessagebox.CTkMessagebox(title="Alerta",
                               message="Ja hi ha una figura en aquest nom, estàs segur que vols sobreescriure-la?",
                               option_1= "Sobreescriu",
                               option_2 = "Cancelar" )
        if alerta.get() == "Sobreescriu":
            buttonlist1[answer].destroy()
        if alerta.get() == "Cancelar":
            return
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

    canvas2.delete("all")
    assaig.update({croquis_in_use["Nom"]: croquis_in_use})

    #ONLINE SYNCING
    # try:


    drive.sheet.batch_update()
    drive.sheet.add_worksheet(title = croquis_in_use["Nom"], cols = len(croquis_in_use.keys()) ,rows=5)
    drive.sheet.worksheet(croquis_in_use["Nom"]).update(range_name=str("R1C1:R5C"+str(len(croquis_in_use.keys()))), values=[list(croquis_in_use.keys()),list(croquis_in_use.values())])
        # drive.sheet.worksheet(croquis_in_use["Nom"]).update(range_name = "A1:"+A, values =list(map(list, zip(*[croquis_in_use.keys(),croquis_in_use.values()]))) )
        #[[[i] for i in list(croquis_in_use.keys())],[[i] for i in list(croquis_in_use.values())]]
    print("done")
    # except:
    print("not done")

    def assaig_button_press(nom):
        global croquis_in_use
        global canvas2
        Interval(5, up_to_date).start()
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
    buttonlist1.update({croquis_in_use["Nom"]: button})
    return croquis_in_use

repertori_label = customtkinter.CTkComboBox(frame,
                                            fg_color=rep.main_color, button_color=rep.main_color, button_hover_color=rep.inv_color, corner_radius=5, font=("Liberation Sans",16, "bold"), border_width= 0,
                                            values = [i.nom for i in rep.repertori.values()],
                                            command = crear_figura)
repertori_label.set("Afegir figura")
repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.1*0.99)




"""
Per dibuixar la figura
"""

def fer_dibuix(listadecoordenades:list, croquiss:dict, corrector: tuple):
    global updater
    counter = 0

    netejadora = [[],[]]
    croquis_frame.update()

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
                              interval = updater,
                              orientation = -orientation,
                              color =rep.palette[rep.rols.index(i.split(" ")[0])],list_len=10)

        counter += 1
        for child in croquis_frame.winfo_children():
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
namer = customtkinter.CTkEntry(croquis_frame, placeholder_text="Nom de Figura-X", font=("Liberation Sans", 16, "bold"), state="disabled")
def actualitzar_nom_figura():
    buttonlist1[croquis_in_use["Nom"]].configure(text=namer.get())
    buttonlist1.update({namer.get(): buttonlist1[croquis_in_use["Nom"]]})
    del buttonlist1[croquis_in_use["Nom"]]
    croquis_in_use["Nom"] = namer.get()


    taula.update_values(f.croquis_to_table(croquis_in_use, membre.taula_mestra))
    taula_namefig.configure(text="Figura: "+croquis_in_use["Figura"])
    taula_name.configure(text="Id: " + namer.get())
namer_button = customtkinter.CTkButton(croquis_frame, text="Actualitzar nom", font=("Liberation Sans", 14, "bold"), height= 28, command= actualitzar_nom_figura, state="disabled", fg_color = rep.main_color, hover_color=rep.inv_color)
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
            taula_frame.place(relx=.99, rely=.5, anchor="e", relheight=.98, relwidth=0.01)
            croquis_frame.place(relx = 0.12, rely=0.5, anchor="w", relheight=0.98, relwidth=0.87)
            expand_is_on2 = True
        else:
            taula_frame.place(relx=.99, rely=.5, anchor="e", relheight=.98, relwidth=0.2)
            croquis_frame.place(relx=0.12, rely=0.5, anchor="w", relheight=0.98, relwidth=.66)
            expand_is_on2 = False
    else:
        if not expand_is_on2:
            taula_frame.place(relx=.99, rely=.5, anchor="e", relheight=.98, relwidth=0.01)
            croquis_frame.place(relx = 0.07, rely=0.5, anchor="w", relheight=0.98, relwidth=0.92)
            expand_is_on2 = True
        else:
            taula_frame.place(relx=.99, rely=.5, anchor="e", relheight=.98, relwidth=0.2)
            croquis_frame.place(relx=0.07, rely=0.5, anchor="w", relheight=0.98, relwidth=0.71)
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
            croquis_frame.place(relx=0.07, rely=0.5, anchor="w", relheight=0.98, relwidth=.71)
            repertori_frame.place(relx=.01, rely=.07, relheight=0.92, relwidth=0.05, anchor="nw")
            repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.05*0.99)


            expand_is_on = True
        else:
            croquis_frame.place(relx=0.12, rely=0.5, anchor="w", relheight=0.98, relwidth=.66)
            repertori_frame.place(relx=.01, rely=.07, relheight=0.92, relwidth=0.1, anchor="nw")
            repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.1*0.99)

            expand_is_on = False
    else:
        if not expand_is_on:
            croquis_frame.place(relx=0.07, rely=0.5, anchor="w", relheight=0.98, relwidth=0.92)
            repertori_frame.place(relx=.01,rely=.07, relheight=0.92,relwidth=0.05,anchor="nw")
            repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.05*0.99)

            expand_is_on = True
        else:
            croquis_frame.place(relx=0.12, rely=0.5, anchor="w", relheight=0.98, relwidth=.87)
            repertori_frame.place(relx=.01, rely=.07, relheight=0.92, relwidth=0.1, anchor="nw")
            repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.1)

            expand_is_on = False
button_expand = customtkinter.CTkButton(croquis_frame,
                                        text = "<",
                                        height = 10,
                                        width = 10,
                                        corner_radius= 15,
                                        command = minimizar,
                                        fg_color =rep.main_color, hover_color=rep.inv_color)
                                        #repertori_frame._parent_frame.forget())

button_expand2 = customtkinter.CTkButton(croquis_frame,
                                         text = ">",
                                         height = 10,
                                         width = 10,
                                         corner_radius= 15,
                                         command = minimizar2,
                                         fg_color =rep.main_color, hover_color=rep.inv_color)
                                        #repertori_frame._parent_frame.forget())
button_expand.place(rely = 0.5, relx = .005, anchor="w")
button_expand2.place(rely = 0.5, relx = .995, anchor="e")

#Conexió on startup


def carregar_figura(croquis):

    def assaig_button_press(nom):
        updater.start()
        global croquis_in_use
        global canvas2
        Interval(5, up_to_date).start()
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
    coordenades = rep.repertori2[croquis_in_use["Figura"]].coordenades
    corrector = rep.repertori2[croquis_in_use["Figura"]].centraor()
    #registre_labels = [fer_dibuix(coordenades, croquis_in_use, corrector)]

    button = customtkinter.CTkButton(repertori_frame, text=croquis_in_use["Nom"],
                                     command=lambda nom = croquis_in_use["Nom"]:assaig_button_press(nom),
                                     fg_color = rep.main_color,hover_color=rep.inv_color, font = ("Arial", 14,"bold"))
    button._text_label.place(x=0, rely = 0.5, anchor = "w")
    button.pack(pady=5)
    buttonlist1.update({croquis_in_use["Nom"]: button})


for i in range(len(drive.sheet.worksheets()[1:])):
    croquis_in_use = drive.sheet.get_worksheet(i+1)
    croquis_in_use = croquis_in_use.get_all_records()[0]
    assaig.update({croquis_in_use["Nom"]:croquis_in_use})
    carregar_figura(croquis_in_use)


def up_to_date():
    global assaig
    global croquis_in_use
    worksheet_list = drive.sheet.worksheets()[1:]
    named_worksheet_list = [str(i).split("'")[1] for i in worksheet_list]
    if len(worksheet_list) != len(assaig):
        print("canvi en el numero de figuras")
    for i in range(len(named_worksheet_list)):
        print(i)
        print(named_worksheet_list[i])
        print(worksheet_list[i])
        if croquis_in_use["Nom"] == named_worksheet_list[i]:
            croquis_cloud = drive.sheet.get_worksheet(i+1).get_all_records()[0]
            if croquis_in_use == croquis_cloud:
                print("Nada canvio")
            else:
                print("canvió la figura")
                diferencia = set(croquis_cloud.values()) - set(croquis_in_use.values())
                print(diferencia)
                croquis_in_use = croquis_cloud
                for change in diferencia:
                    print(change)
                    target_ID = list(croquis_in_use.values()).index(change)
                    print("targetID",target_ID)
                    target_data = [list(croquis_in_use.keys())[target_ID],list(croquis_in_use.values())[target_ID]]
                    print("Target data",target_data)
                    target_drawing =canvas2.find_withtag(target_data[0])
                    print("Target drawing",target_drawing)
                    canvas2.itemconfig(target_drawing[-1], text = target_data[1])
                    taula.insert(target_ID -1, 1, target_data[1])
                    taula.insert(target_ID -1, 2,
                                      membre.taula_mestra.loc[membre.taula_mestra["Nom"] == target_data[1]].iloc[0, 1])
                assaig.update({croquis_in_use["Nom"]: croquis_in_use})




updater = Interval(5, up_to_date)





root.mainloop()