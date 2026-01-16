import io
import math
import tkinter
import customtkinter
import pandas as pd
import CTkMessagebox

from src.util.classes.esquema import Esquema
from src.util.classes.canvastextclass import CanvasText
from src.util.classes.interval import Interval
from src.util.classes import CTkTable
from src.util import repertori as rep
import src.membre as mem
from src.API.drive import download_file
from src.API.credential_managing import spreadsheet_connection
import config_reader





assaig = {}
croquis_in_use = {}
croquis_loading = {}



taula_pack = []
expand_is_on = False
expand_is_on2 = False

updater = None
sheet = None

assistents_id, membres_id, sheet_id  = config_reader.get_config()
config_changed = True
unchanged_nagger = []
working_list, taula_mestra = mem.carregar_assistencia(membres_id,assistents_id)
# sheet_id = "1k9W_o-bCnOd113so2OqvDfQQPLZiUnD2P29Cnni6yXs"


if assistents_id == "1nMrNL_sKmcuHPmbOImELO9qfEAAmiFVmukd3PQ3xjNg":
    config_changed = False
    unchanged_nagger.append("id_assistents")
if membres_id == "1aGMczw57F5TkF5QNUm-LzcHNTOnLS3F0KY9R4pQk_SE":
    config_changed = False
    unchanged_nagger.append("id_membres")
if sheet_id == "1k9W_o-bCnOd113so2OqvDfQQPLZiUnD2P29Cnni6yXs":
    config_changed = False
    unchanged_nagger.append("id_assaig")
if sheet_id == "1KJrjm34obf6L2BtFBC8WsB2rVpQMFcusIDVeTMu5MmU":
    config_changed = False
    unchanged_nagger.append("id_assaig")

def pass_variable (anything):
    global taula_pack
    taula_pack = anything

def connect(combobox, parents, splash):
    global updater
    global croquis_loading
    global sheet
    global taula_pack
    global online
    online = True
    sheet, drive = spreadsheet_connection(sheet_id)
    updater = Interval(1, lambda x=combobox: up_to_date(combobox, parents))

    result = pd.read_excel(io.BytesIO(download_file(real_file_id=sheet_id)), sheet_name=None)
    figures = list(result.keys())[1:]
    for i in figures:
        precroquis = result[i].to_dict()
        croquis_loading = {}
        try:
            for j in precroquis:
                croquis_loading.update({j:precroquis[j][0]})
            print("Descarregant",croquis_loading["Figura"],":",croquis_loading["Nom"])
            inicialitzar_figura(croquis_loading["Figura"],combobox, parents, online = True,downloading = True)
        except:
            sheet.del_worksheet(i)
    splash.destroy()
    # if not config_changed:
    #     nagger = CTkMessagebox.CTkMessagebox(title="Paràmetres sense configurar",
    #                                          message=f"Encara estàs utilitzant els valors per defecte de: \n{unchanged_nagger}\nrecorda editar el axiu 'config.txt' per sincronitzar-te amb la resta de la colla i tècnica",
    #                                          option_1="Ok",
    #                                          option_2="Ok, pesat")

    updater.start()

def fer_croquis(figura: Esquema,nom: str):
    """
    input: Esquema + string
    output: diccionari
    !!!Versió fusionada de fer croquis i visualitzar: genera una string per presentar els resultats pero que no s'actualitza en actualitzar el esquema amb update
    Agafa l'objecte esquema de la figura demanada, extrau les variables amb vars().values() i vars().keys()
    Crea un diccionari amb el nom individual de la figura, id de la figura a fer i una entrada per a cada una de les posicions
    """
    producte = {"Nom":nom}
    posicions = list(vars(figura).keys())
    nombre = list(vars(figura).values())
    producte.update({"Figura":nombre[0]})
    stringoutput = str()
    for i in range (1,len(posicions)-1):
        if nombre[i] == 0:
            continue
        for h in range (0,nombre[i]):
            clau = str(posicions[i]).capitalize() + " " + str(h + 1)
            producte.update({str(clau): "N. A."})
            stringoutput += str(clau) + ":" + str(producte[str(clau)]) + "\n"
        stringoutput += "\n\n"
    return producte

def fer_dibuix(parent, listadecoordenades:list, croquiss:dict, corrector: tuple, skip = False):
    global sheet
    global updater
    global taula_pack
    global taula_mestra
    global assaig
    canvas = tkinter.Canvas(parent[1], bg=parent[1]._apply_appearance_mode(("#AAAAAA", "#333333")), width= parent[1].winfo_width()- parent[1].cget("corner_radius") * 4 - 25, height= parent[1].winfo_height()- parent[1].cget("corner_radius") * 2 - 30, highlightthickness = 0)
    canvas.place(relx = 0.5, rely = 0.5, anchor = "center")
    taula_pack[3].lift()
    taula_pack[4].lift()
    taula_pack[5].lift()
    for figura in list(assaig.keys())[:-1]:
        assaig[figura]["Taula"].pack_forget()

    parent[1].bind("<Configure>", lambda event: resize(event, canvas))
    taula = CTkTable.CTkTable(parent[2], column=3, row=2, values= [[]], header_color="#7393B3",
                              font=("Liberation Sans", 12), corner_radius=5)
    taula.update_values(croquis_to_table(croquiss, taula_mestra))
    taula.pack()
    assaig[croquiss["Nom"]].update({"Canvas":canvas, "Taula":taula})




    counter = 0
    for i in croquiss.keys():

        if i == "Nom" or i == "Figura":
            continue
        coord = listadecoordenades[counter]
        counter += 1
        if croquiss[i] == "N. A." and skip == True:
            continue
        if croquiss[i] == "+" and skip == True:
            continue

        sc = 0
        if croquiss["Figura"] in ["Alta de 5", "Xopera", "Torreta", "Pilotó","Marieta", "Volantinera", "Figuereta"]:
            sc = 1

        try:
            if coord[1] > sc:
                orientation = math.degrees(math.atan(coord[0] / (coord[1])))
                coord = [coord[0],coord[1]+sc/1.5]
            elif coord[1] < -sc:
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

        #Exceptions
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

        if "P3" in croquiss["Figura"]:
            orientation = 0
        if "P2" in croquiss["Figura"]:
            orientation = 0



        CanvasText(canvas.master.master.master, canvas,
                              i, coord,corrector,
                              working_list, assaig[croquiss["Nom"]]["Taula"], croquiss, taula_mestra,
                              interval = updater, sheet = sheet,
                              orientation = -orientation,
                              color =rep.palette[rep.rols.index(i.split(" ")[0])],list_len=10)



    try:
        canvas.tag_raise("Base", "Tap")
    except:
        pass
    try:
        canvas.tag_raise("Base", "Peu")
    except:
        pass
    try:
        canvas.tag_lower("Tap", "Mans")
    except:
        pass
    try:
        canvas.tag_raise("Mans", "Vents")
    except:
        pass
    try:
        canvas.tag_lower("rectangle", "etiqueta")
    except:
        pass


def assaig_button_press(nom, assaig):
    global croquis_in_use
    global taula_pack
    if croquis_in_use == assaig[nom]["Croquis"]:
        return
    croquis_in_use = assaig[nom]["Croquis"]
    for i in list(assaig.keys()):
        assaig[i]["Canvas"].place_forget()   #Amaga tot
        assaig[i]["Taula"].pack_forget()
    assaig[nom]["Canvas"].place(relx = 0.5, rely = 0.5, anchor="center" ) #Mostra this one
    assaig[nom]["Taula"].pack()

    taula_pack[3].lift()
    taula_pack[4].lift()
    taula_pack[5].lift()


    #Activa "namer"
    taula_pack[3].configure(state="normal")
    taula_pack[4].configure(state="normal")
    taula_pack[5].configure(state="normal")

    taula_pack[3].delete(0, "end")
    taula_pack[3].configure(placeholder_text=croquis_in_use["Nom"])
    taula_pack[2].configure(text="Figura: " + croquis_in_use["Figura"])
    taula_pack[1].configure(text="Id: " + croquis_in_use["Nom"])

def inicialitzar_figura(selected_fig, combobox_to_reset, parents, online = False, downloading = False):
    global assaig
    global croquis_in_use
    global croquis_loading
    if online:
        print("Parant updater")
        try:
            updater.stop()
        except:
            pass
    combobox_to_reset.set("Afegir figura")    #Restaura combobox
    counter = 1    #contador per a numerar el nom genèric de la figura creada
    for figura in assaig.keys():
        if selected_fig in assaig[figura]["Croquis"]["Figura"]:
            counter += 1
    if not downloading:
            #Demana nom al user NOMES quan no ve la figura d'internet
        dialog_nom = customtkinter.CTkInputDialog(text=f"Com vols identificar aquest/a {selected_fig}?",title="Nomena la figura")
        dialog_nom.geometry(f"+500+500")
        answer = dialog_nom.get_input()
        if answer == None:
            return
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
                    croquis_in_use = fer_croquis(figura, answer)
                else:
                    croquis_in_use = fer_croquis(figura, str(selected_fig) +" "+ str(counter))

                break
    else:
        croquis_in_use = croquis_loading

    if online:
        try: #crea nova pagina per a la figura nova
            sheet.add_worksheet(title = croquis_in_use["Nom"], cols = 150 ,rows=5)
            sheet.worksheet(croquis_in_use["Nom"]).update(range_name=str("R1C1:R5C"+str(len(croquis_in_use.keys()))), values=[list(croquis_in_use.keys()),list(croquis_in_use.values())])
        except:
            pass
    button = customtkinter.CTkButton(parents[0], text=croquis_in_use["Nom"],
                                     command=lambda nom=croquis_in_use["Nom"]: assaig_button_press(nom, assaig),
                                     fg_color=rep.main_color, hover_color=rep.inv_color, font=("Arial", 14, "bold"))
    button.pack(pady=5)
    """"""
    figura = rep.repertori2[croquis_in_use["Figura"]]
    assaig.update({croquis_in_use["Nom"]: {"Figura": figura, "Croquis": croquis_in_use, "Butó": button}})
    """"""
    fer_dibuix(parents, figura.coordenades, croquis_in_use, figura.centraor())
    if not downloading:
        assaig_button_press(croquis_in_use["Nom"], assaig= assaig)

    return croquis_in_use

def eliminar_figura(canvas):
    global assaig
    global croquis_in_use
    global sheet
    global taula_pack
    global updater
    if online:
        updater.stop()
    alerta = CTkMessagebox.CTkMessagebox(title="Alerta",
                                         message="Estas segur que vols borrar la figura?",
                                         option_1="Eliminar",
                                         option_2="Cancelar")

    if alerta.get() == "Cancelar":
        if online:
            updater.start()
        return
    if alerta.get() == "Eliminar":
        trash = croquis_in_use["Nom"]
        assaig_button_press(list(assaig.keys())[0], assaig= assaig)
        assaig[trash]["Butó"].destroy()
        assaig[trash]["Canvas"].destroy()
        assaig[trash]["Taula"].destroy()

        del assaig[trash]


        taula_pack[2].configure(text="Figura: ")
        taula_pack[1].configure(text="Id: ")
        if online:
            sheet.del_worksheet(sheet.worksheet(trash))
            updater.start()

def actualitzar_nom_figura():
    global taula_pack
    assaig[croquis_in_use["Nom"]]["Butó"].configure(text=taula_pack[3].get())
    if online:
        sheet.worksheet(croquis_in_use["Nom"]).update_cell(2, 1,value=taula_pack[3].get())
        sheet.worksheet(croquis_in_use["Nom"]).update_title(taula_pack[3].get())
    croquis_in_use["Nom"] = taula_pack[3].get()


    # taula_pack[0].update_values(croquis_to_table(croquis_in_use, taula_mestra)) #cuarentena
    taula_pack[2].configure(text="Figura: "+croquis_in_use["Figura"])
    taula_pack[1].configure(text="Id: " + taula_pack[3].get())

def croquis_to_table(croquis_generat:dict,dt = None):
    listah = [["Posició", "Nom","Muscle"]]
    croquis_intern = croquis_generat.copy()
    del croquis_intern["Nom"]
    del croquis_intern["Figura"]
    lista = []
    for key, value in croquis_intern.items():
        try:
            lista.append([key, value, dt.loc[dt["Àlies"] == value].iloc[0, 2]])
        except:
            lista.append([key, value, 0])

    return listah+lista

def resize( event, canvas):
    """
    GESTIONA REDIMENSIONS DEL CROQUIS (canvas)
    """

    old_height = canvas.winfo_height()
    old_width = canvas.winfo_width()
    w1 = old_width
    w2 = event.width - canvas.master.cget("corner_radius") * 4
    h1 = old_height
    h2 = event.height - canvas.master.cget("corner_radius") * 2
    canvas.config(width = w2, height = h2)
    for i in canvas.find_withtag("etiqueta"):
        x = canvas.coords(i)[0]
        y = canvas.coords(i)[1]
        canvas.coords(i, x * w2 / w1, y * h2 / h1)
    for i in canvas.find_withtag("rectangle"):
        x = canvas.coords(i)[8] * 0.5 + canvas.coords(i)[28] * 0.5
        y = canvas.coords(i)[9] * 0.5 + canvas.coords(i)[29] * 0.5
        canvas.move(i, (w2 / w1-1) * x,  (h2 / h1-1) * y)

def canviar_apariencia(canvas):
    """
    Darkmode
    """
    print("new one being ran")
    if customtkinter.get_appearance_mode() == "Dark":
        customtkinter.set_appearance_mode("light")

    else:
        customtkinter.set_appearance_mode("dark")

    canvas.config(bg=canvas.master._apply_appearance_mode(("#FFFFFF","#333333")))

def up_to_date(combobox_to_reset, parents):
    global assaig
    global croquis_in_use
    global taula_pack
    result = pd.read_excel(io.BytesIO(download_file(real_file_id=sheet_id)), sheet_name=None)
    figures = list(result.keys())[1:]
    if len(figures) != len(assaig):
        print("ha canviat el nombre d figures")
        assaig_to_remove = []
        for i in assaig:
            if i not in figures:
                print(f"borrant {i}")
                assaig_to_remove.append(i)
        for i in assaig_to_remove:
            assaig[i]["Butó"].destroy()
            del assaig[i]
        for i in figures:
            if i not in assaig:
                print(f"figura nova {i}")
                croquis_cloud = sheet.get_worksheet(figures.index(i) + 1).get_all_records()[0]
                inicialitzar_figura(croquis_cloud["Figura"],combobox_to_reset, parents, downloading = False, online = True)

    for i in range(len(figures)):
        canvas = assaig[croquis_in_use["Nom"]]["Canvas"]
        if croquis_in_use["Nom"] == figures[i]:
            precroquis = result[figures[i]]
            croquis_cloud = {}
            for j in precroquis:
                croquis_cloud.update({j:precroquis[j][0]})
            if croquis_in_use != croquis_cloud:
                print(croquis_in_use, croquis_cloud)
                print("canvió la figura")
                diferencia = set(croquis_cloud.values()) - set(croquis_in_use.values())
                print(diferencia)
                croquis_in_use = croquis_cloud
                for change in diferencia:
                    target_ID = list(croquis_in_use.values()).index(change)
                    target_data = [list(croquis_in_use.keys())[target_ID],list(croquis_in_use.values())[target_ID]]
                    target_drawing =canvas.find_withtag(target_data[0])
                    print(target_data)
                    canvas.itemconfig(target_drawing[-1], text = target_data[1].upper()[:len(target_data[1].upper().split(" ")[0])+2], fill = "black")

                    canvas.itemconfig(target_drawing[0], fill = canvas.master._apply_appearance_mode(rep.palette[rep.rols.index(list(croquis_in_use.keys())[target_ID].split(" ")[0])]) )
                    assaig[croquis_in_use["Nom"]]["Taula"].insert(target_ID -1, 1, target_data[1])
                    try:
                        assaig[croquis_in_use["Nom"]]["Taula"].insert(target_ID -1, 2,
                                      taula_mestra.loc[taula_mestra["Àlies"] == target_data[1]].iloc[0, 2])
                    except:
                        pass
                assaig[croquis_in_use["Nom"]].update({"Croquis": croquis_in_use})

def minimizar(button_expand, croquis_frame, repertori_frame, repertori_label):
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
def minimizar2(button_expand2, croquis_frame, taula_frame):
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

def actualitzar_assaig_output(_event, frame):
    global assaig
    contador = 0
    for i in frame.winfo_children():
        if contador < 2:
            contador = +1
            continue
        i.destroy()
    for i in list(assaig.keys()):
        canvas = customtkinter.CTkCanvas(frame, bg="white", width=frame.winfo_width(), height=frame.winfo_width())
        canvas.pack(pady=10)
        fer_dibuix(canvas,assaig[i]["Figura"].coordenades, assaig[i]["Croquis"], assaig[i]["Figura"].centraor(),skip = True)
