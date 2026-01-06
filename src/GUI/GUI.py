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
updater = None

#assaig = {Nom: [croquis, figura, botó]}


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

"""
Darkmode
"""
def canviar_apariencia():
    if customtkinter.get_appearance_mode() == "Dark":
        customtkinter.set_appearance_mode("light")

    else:
        customtkinter.set_appearance_mode("dark")
    canvas2.config(bg=frame._apply_appearance_mode(("#FFFFFF","#333333")))

### CROQUIS TAB ###

frame = customtkinter.CTkFrame(master=tabview.tab("Croquis"))
frame.place(relx=0.5,rely=0.5,anchor="c",relheight=1, relwidth=1)

#Gestiona Connectivitat
online = False
connection = CTkMessagebox.CTkMessagebox(title="Connectivitat",
                               message="Vols treballar en línia o desconectat?",
                               option_1= "Online",
                               option_2 = "Offline" )
if connection.get() == "Online":
    online = True
if connection.get() == "Offline":
    pass


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

#Darkmode Button
CTkButton(frame,text = "☀ / ☾",command=canviar_apariencia, width = 20,fg_color =rep.main_color, hover_color=rep.inv_color).place(relx=1, rely=1, anchor="se")





def assaig_button_press(nom):
    global croquis_in_use
    global canvas2


    croquis_in_use = assaig[nom]["Croquis"]
    figura = assaig[nom]["Figura"]
    taula.update_values(f.croquis_to_table(croquis_in_use, membre.taula_mestra))
    canvas2.delete("all")
    fer_dibuix(figura.coordenades, croquis_in_use, figura.centraor())
    namer.delete(0, "end")
    namer.configure(placeholder_text=croquis_in_use["Nom"])
    taula_namefig.configure(text="Figura: " + croquis_in_use["Figura"])
    taula_name.configure(text="Id: " + croquis_in_use["Nom"])
    pass

def inicialitzar_figura(selected_fig, downloading = False):


    global assaig
    global croquis_in_use
    global croquis_loading
    if online:
        print("parant updater")
        updater.stop()
    repertori_label.set("Afegir figura")    #Restaura combobox
        #Activa "namer"
    namer.configure(state="normal")
    namer_button.configure(state="normal")
    counter = 1    #contador per a numerar el nom genèric de la figura creada
    for figura in assaig.keys():
        if selected_fig in assaig[figura]["Croquis"]["Figura"]:
            counter += 1
    if not downloading:
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
                assaig[answer]["Butó"].destroy()
                del assaig[answer]
            if alerta.get() == "Cancelar":
                return
        #busca quin ESQUEMA conté el NOM selected_fig
        for figura in rep.repertori.values():
            if selected_fig == figura.nom:
                if answer != "" :
                    croquis_in_use = f.fer_croquis(figura, answer)
                else:
                    croquis_in_use = f.fer_croquis(figura, str(selected_fig) +" "+ str(counter))

                break
    else:
        croquis_in_use = croquis_loading

    canvas2.delete("all")

    if online:
        updater.stop()
        try:
            drive.sheet.add_worksheet(title = croquis_in_use["Nom"], cols = len(croquis_in_use.keys()) ,rows=5)
            drive.sheet.worksheet(croquis_in_use["Nom"]).update(range_name=str("R1C1:R5C"+str(len(croquis_in_use.keys()))), values=[list(croquis_in_use.keys()),list(croquis_in_use.values())])
        except:
            pass
        updater.start()




    button = customtkinter.CTkButton(repertori_frame, text=croquis_in_use["Nom"],
                                     command=lambda nom = croquis_in_use["Nom"]:assaig_button_press(nom),
                                     fg_color = rep.main_color,hover_color=rep.inv_color, font = ("Arial", 14,"bold"))
    button._text_label.place(x=0, rely = 0.5, anchor = "w")
    button.pack(pady=5)
    """"""
    figura = rep.repertori2[croquis_in_use["Figura"]]
    assaig.update({croquis_in_use["Nom"]: {"Figura":figura, "Croquis":croquis_in_use,"Butó":button} })
    """"""
    if not downloading:
        assaig_button_press(croquis_in_use["Nom"])

    return croquis_in_use

repertori_label = customtkinter.CTkComboBox(frame,
                                            fg_color=rep.main_color, button_color=rep.main_color, button_hover_color=rep.inv_color, corner_radius=5, font=("Liberation Sans",16, "bold"), border_width= 0,
                                            values = [i.nom for i in rep.repertori.values()],
                                            command = inicialitzar_figura)
repertori_label.set("Afegir figura")
repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.1*0.99)




"""
Per dibuixar la figura
"""

def fer_dibuix(listadecoordenades:list, croquiss:dict, corrector: tuple):
    global updater
    counter = 0


    # croquis_frame.update()

    for i in croquiss.keys():
        if i == "Nom" or i == "Figura":
            continue

        coord = listadecoordenades[counter]

        sc = -0
        if croquiss["Figura"] in ["Alta de 5", "Xopera", "Torreta", "Pilotó","Marieta", "Volantinera", "Figuereta"]:
            sc = 1

        try:
            if coord[1] > sc:
                # orientation = math.degrees(math.atan(coord[0] / (coord[1]-sc)))
                orientation = math.degrees(math.atan(coord[0] / (coord[1])))
                coord = [coord[0],coord[1]+sc/1.5]
            elif coord[1] < -sc:
                # orientation = math.degrees(math.atan(coord[0] / (coord[1]+sc)))
                orientation = math.degrees(math.atan(coord[0] / (coord[1])))
                coord = [coord[0], coord[1] - sc/1.5]

            elif sc >= coord[1] >= -sc:
                if coord[0] > 0:
                    orientation = 90
                if coord[0] < 0:
                    orientation = -90
                if coord[0] == 0:
                    orientation = 0


        except:
            if coord[0] > 0:
                orientation = 90
            if coord[0] < 0:
                orientation = -90
            if coord[0] == 0:
                orientation = 0
        if i.split(" ")[0] in ["Segona"]:
            if assaig[croquiss["Nom"]]["Figura"].segona == 6 or assaig[croquiss["Nom"]]["Figura"].segona == 4:
                x = int(i.split(" ")[1])
                orientation = 3 * x ** 5 - 63.75 * x ** 4 + 502.5 * x ** 3 - 1781.25 * x ** 2 + 2689.5 * x - 1260

            if assaig[croquiss["Nom"]]["Figura"].segona == 3 or assaig[croquiss["Nom"]]["Figura"].segona == 2:
                x = int(i.split(" ")[1])
                orientation = 135 * x ** 2 - 585 * x + 540
            if assaig[croquiss["Nom"]]["Figura"].segona == 1:
                orientation = 0
        if i.split(" ")[0] in ["Tercera"]:
            if assaig[croquiss["Nom"]]["Figura"].tercera == 3 or assaig[croquiss["Nom"]]["Figura"].tercera == 2:
                x = int(i.split(" ")[1])
                orientation = 135 * x ** 2 - 585 * x + 540
            if assaig[croquiss["Nom"]]["Figura"].tercera == 1:
                orientation = 0

        if i.split(" ")[0] in ["Xicalla","Alsadora"]:
            orientation = 0
        if croquiss["Figura"] == "Encontre" and i.split(" ")[0] in "Base":
            orientation = 0



        CanvasText(root, canvas2,
                              i, coord,corrector,
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



#NOM FIGURA
namer = customtkinter.CTkEntry(croquis_frame, placeholder_text="Nom de Figura-X", font=("Liberation Sans", 16, "bold"), state="disabled")
def actualitzar_nom_figura():
    assaig[croquis_in_use["Nom"]]["Butó"].configure(text=namer.get())
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



def up_to_date():
    print("run")
    global assaig
    global croquis_in_use
    worksheet_list = drive.sheet.worksheets()[1:]
    named_worksheet_list = [str(i).split("'")[1] for i in worksheet_list]
    if len(worksheet_list) != len(assaig):
        for i in assaig:
            if i not in named_worksheet_list:
                assaig[i]["Butó"].destroy()
                del assaig[i]
        for i in named_worksheet_list:
            if i not in assaig:
                croquis_cloud = drive.sheet.get_worksheet(named_worksheet_list.index(i) + 1).get_all_records()[0]
                inicialitzar_figura(croquis_cloud["Figura"],downloading=True)




    for i in range(len(named_worksheet_list)):

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
                    target_ID = list(croquis_in_use.values()).index(change)
                    target_data = [list(croquis_in_use.keys())[target_ID],list(croquis_in_use.values())[target_ID]]
                    target_drawing =canvas2.find_withtag(target_data[0])
                    canvas2.itemconfig(target_drawing[-1], text = target_data[1].upper())
                    canvas2.itemconfig(target_drawing[0], fill = frame._apply_appearance_mode(rep.palette[list(croquis_in_use.keys())[target_ID]])   )
                    taula.insert(target_ID -1, 1, target_data[1])
                    taula.insert(target_ID -1, 2,
                                      membre.taula_mestra.loc[membre.taula_mestra["Nom"] == target_data[1]].iloc[0, 1])
                assaig[croquis_in_use["Nom"]].update({"Croquis": croquis_in_use})

if online:
    updater = Interval(5, up_to_date)
    worksheet_list = drive.sheet.worksheets()[1:]
    named_worksheet_list = [str(i).split("'")[1] for i in worksheet_list]
    for i in worksheet_list:
        try:
            croquis_loading = i.get_all_records()[0]
            print("Descarregant",croquis_loading["Figura"],":",croquis_loading["Nom"])
            inicialitzar_figura(croquis_loading["Figura"], downloading = True)

        except:
             drive.sheet.del_worksheet(i)

    updater.start()



root.mainloop()