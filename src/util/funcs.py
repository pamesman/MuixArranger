import io
import math
import tkinter
from tkinter import ttk
import customtkinter
import pandas as pd
import CTkMessagebox
from time import sleep, time


from src.util.classes.esquema import Esquema
from src.util.classes.canvastextclass import CanvasText
from src.util.classes.interval import Interval
from src.util.classes import CTkTable
from src.util import repertori as rep
import src.membre as mem
import src.util.image_export as ie
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
online = False
donotupdate = False

assistents_id, membres_id, sheet_id  = config_reader.get_config()
config_changed = True
unchanged_nagger = []
working_list, taula_mestra, assistents = mem.carregar_assistencia(membres_id,assistents_id)
# sheet_id = "1k9W_o-bCnOd113so2OqvDfQQPLZiUnD2P29Cnni6yXs"
tecnica = taula_mestra[taula_mestra["Permisos especials APP"].str.contains("TECNICA") == True]
tecnica_fora = set(tecnica["Àlies"])

update_batch = {}
countdown = 0


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



def update_tecnica():
    global tecnica_fora
    global croquis_in_use
    global taula_pack

    tecnica_fora_nova = set(set(list(tecnica["Àlies"]))-set(croquis_in_use.values()))
    if tecnica_fora == tecnica_fora_nova:
        return
    excloure = 0
    for i in taula_pack[6].winfo_children()[1:]:
        i.destroy()
    tecnica_fora = set(tecnica["Àlies"])-set(croquis_in_use.values())
    for i in tecnica_fora:
        customtkinter.CTkLabel(taula_pack[6], text= i).pack()

    pass


update_batch = {}
def batch_creator():
    global croquis_ref
    global croquis_in_use


    global updater
    global update_batch


    for entry in list(croquis_ref.keys()):
        update_batch.update({croquis_in_use["Nom"]: {}})
        if croquis_ref[entry] != croquis_in_use[entry]:



            print("change")
            update_batch[croquis_in_use["Nom"]].update({entry:croquis_in_use[entry]})
            drive_update2(update_batch)
            if croquis_in_use[entry] == "'+":
                croquis_in_use[entry] = "+"
            croquis_ref = croquis_in_use.copy()


        else:

            pass


observer1 = Interval(0.2, update_tecnica)
observer2 = Interval(1, batch_creator)

def drive_update2(update):
    global sheet
    for i in list(update.keys()):
        for k in list(update[i].keys()):
            print("Figura,Posicio, Data")
            print(i,k, update[i][k])
            print("updating excel...")
            sheet.worksheet(i).update_cell(2, list(assaig[i]["Croquis"].keys()).index(k)+1,  value=update[i][k])
            print("exito")


            # except:
            #     print("mistake was sucedido")

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
            inicialitzar_figura(croquis_loading,combobox, parents, online = True,downloading = True)
        except:
            sheet.del_worksheet(i)
    global croquis_in_use
    croquis_in_use = None
    splash.destroy()
    # if not config_changed:
    #     nagger = CTkMessagebox.CTkMessagebox(title="Paràmetres sense configurar",
    #                                          message=f"Encara estàs utilitzant els valors per defecte de: \n{unchanged_nagger}\nrecorda editar el axiu 'config.txt' per sincronitzar-te amb la resta de la colla i tècnica",
    #                                          option_1="Ok",
    #                                          option_2="Ok, pesat")


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
    canvas = tkinter.Canvas(parent[1], bg=parent[1]._apply_appearance_mode(("#FFFFFF", "#333333")), width= parent[1].winfo_width()- parent[1].cget("corner_radius") * 4 - 25, height= parent[1].winfo_height()- parent[1].cget("corner_radius") * 2 - 30, highlightthickness = 0)
    if skip:
        canvas.pack(expand = tkinter.YES, fill = tkinter.BOTH)
    else:
        canvas.place(relx = 0.5, rely = 0.5, anchor = "center")
        canvas.tk.call("lower", canvas._w, None)

    if not skip:
        for figura in list(assaig.keys())[:-1]:
            assaig[figura]["Taula"].pack_forget()

        parent[1].bind("<Configure>", lambda event: resize(event, canvas))
        ttk.Style().configure("Treeview",
                              rowheight=30,
                              background = parent[1]._apply_appearance_mode(("#EEEEEE", "#333333")),
                              foreground = parent[1]._apply_appearance_mode(("black","white")),
                              fieldbackground = parent[1]._apply_appearance_mode(("#EEEEEE", "#333333")),
                              borderwidth = 0,
                              highlightthickness = 0,
                              relief = "flat"
                              )
        ttk.Style().configure("Treeview.Heading",
                              background = "#F1B300",
                              borderwidth=0,
                              highlightthickness=0,
                              relief="flat",

                              )

        treeview = ttk.Treeview(parent[2] , height = len(croquiss.keys())-2,show = "headings", selectmode="none",style="Treeview")
        treeview.tag_configure('impar', background=parent[1]._apply_appearance_mode(("#D6D6D6", "#3F3F3F")))
        treeview['columns'] = ("Posició", "Nom", "Alçada espatlles")
        treeview.bind('<Motion>', 'break')

        treeview.column("#0",width = 0, stretch = False)
        treeview.column("Posició", width = 100)
        treeview.column("Nom", width = 100, anchor="w")
        treeview.column("Alçada espatlles", width = 100, anchor = "center")

        treeview.heading("Posició", text = "Posició")
        treeview.heading("Nom", text = "Nom")
        treeview.heading("Alçada espatlles",text = "Espatlles")

        treeview.pack(pady = 20)
        treeview_counter = 0

        for valuelist in croquis_to_table(croquiss, taula_mestra):
            if treeview_counter == 0:
                treeview_counter = 1
                continue
            if treeview_counter % 2 == 1:
                tag = "impar"
            else:
                tag = "par"
            treeview.insert('', 'end', treeview_counter, values=valuelist, tags=tag)
            treeview_counter += 1
        assaig[croquiss["Nom"]].update({"Canvas":canvas, "Taula":treeview})
        taula_pack[2].configure(text="Figura: " + croquiss["Figura"])
        taula_pack[1].configure(text="Id: " + croquiss["Nom"])




    counter = 0
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
        if croquiss["Figura"] in ["Alta de 5", "Xopera", "Torreta", "Pilotó","Marieta", "Maria Alta","Volantinera", "Figuereta", "Roscana"]:
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



        CanvasText(canvas.master.master.master,
                   canvas,
                   i, coord,corrector,
                   working_list,
                   assaig[croquiss["Nom"]]["Taula"],
                   croquiss,
                   taula_mestra,
                   interval = updater,
                   sheet = sheet,
                   orientation = -orientation,
                   color =rep.palette[rep.rols.index(i.split(" ")[0])],
                   list_len=10)



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
    return canvas


def assaig_button_press(nom, assaig):
    global croquis_in_use
    global taula_pack
    global observer1
    # global observer2
    global croquis_ref


    if online:
        updater.start()
    if croquis_in_use == assaig[nom]["Croquis"] and croquis_in_use != None:
        return
    croquis_in_use = assaig[nom]["Croquis"]
    croquis_ref = croquis_in_use.copy()
    for figura in list(assaig.keys()):
        assaig[figura]["Taula"].pack_forget()

    assaig[nom]["Canvas"].tk.call("lower", assaig[nom]["Canvas"]._w, taula_pack[3])
    assaig[nom]["Taula"].pack()


    #Activa "namer"
    taula_pack[3].configure(state="normal")
    taula_pack[4].configure(state="normal")
    taula_pack[5].configure(state="normal")

    taula_pack[3].delete(0, "end")
    taula_pack[3].configure(placeholder_text=croquis_in_use["Nom"])
    taula_pack[2].configure(text="Figura: " + croquis_in_use["Figura"])
    taula_pack[1].configure(text="Id: " + croquis_in_use["Nom"])

    #taula tècnica
    excloure = 0
    for i in taula_pack[6].winfo_children()[1:]:
        try:
            i.destroy()
        except:
            pass

    tecnica_fora = set(tecnica["Àlies"])-set(croquis_in_use.values())
    for i in tecnica_fora:
        customtkinter.CTkLabel(taula_pack[6], text= i).pack()
    observer1.start()
    if online:
        observer2.start()

def inicialitzar_figura(croquis, combobox_to_reset, parents, online = False, downloading = False):
    global assaig
    global croquis_loading
    selected_fig = croquis["Figura"]

    if online:
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
                    croquis = fer_croquis(figura, answer)
                else:
                    croquis = fer_croquis(figura, str(selected_fig) +" "+ str(counter))

                break
    else:
        croquis = croquis_loading

    if online:
        try: #crea nova pagina per a la figura nova
            sheet.add_worksheet(title = croquis["Nom"], cols = 150 ,rows=5)
            sheet.worksheet(croquis["Nom"]).update(range_name=str("R1C1:R5C"+str(len(croquis.keys()))), values=[list(croquis.keys()),list(croquis.values())])
        except:
            pass
    button = customtkinter.CTkButton(parents[0],
                                     text=croquis["Nom"],
                                     command=lambda nom=croquis["Nom"]: assaig_button_press(nom, assaig),
                                     fg_color=rep.main_color,
                                     hover_color=rep.inv_color,
                                     font=("Arial", 14, "bold"))
    button.pack(pady=5)
    """"""
    figura = rep.repertori2[croquis["Figura"]]
    assaig.update({croquis["Nom"]: {"Figura": figura, "Croquis": croquis, "Butó": button}})
    """"""
    fer_dibuix(parents, figura.coordenades, croquis, figura.centraor())
    if not downloading:
        croquis_nom = croquis["Nom"]
        croquis = None
        assaig_button_press(croquis_nom, assaig= assaig)

    return croquis

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
    """

    :param croquis_generat:
    :param dt:
    :return:
    """
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

def canviar_apariencia():
    """
    Darkmode
    """
    if customtkinter.get_appearance_mode() == "Dark":
        customtkinter.set_appearance_mode("light")

    else:
        customtkinter.set_appearance_mode("dark")
    for i in assaig:
        assaig[i]["Canvas"].config(bg=assaig[i]["Canvas"].master._apply_appearance_mode(("#FFFFFF","#333333")))
        for j in assaig[i]["Canvas"].find_withtag("rectangle"):
            color = assaig[i]["Canvas"].itemconfig(j, "fill")[4]
            if color == "":
                continue
            for k in rep.palette:
                if k == (None,None):
                    continue
                if color == k[0]:
                    newfill = k[1]
                    break
                elif color == k[1]:
                    newfill = k[0]
                    break
            assaig[i]["Canvas"].itemconfig(j, fill = newfill)


def up_to_date(combobox_to_reset, parents):
    global assaig
    global croquis_in_use
    global taula_pack
    global updater
    start = time()
    updater.stop()
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
                croquis_cloud = sheet.get_worksheet(figures.index(i)+1).get_all_records()[0]
                global croquis_loading
                croquis_loading = croquis_cloud.copy()
                inicialitzar_figura(croquis_loading,combobox_to_reset, parents, downloading = True, online = True)

    for i in range(len(figures)):
        canvas = assaig[croquis_in_use["Nom"]]["Canvas"]
        if croquis_in_use["Nom"] == figures[i]:
            precroquis = result[figures[i]]
            croquis_cloud = {}
            for j in precroquis:
                croquis_cloud.update({j:precroquis[j][0]})
            if croquis_in_use != croquis_cloud:

                print("canvió la figura")
                print(donotupdate)
                print(croquis_in_use)
                print(croquis_cloud)
                diferencia = set(croquis_cloud.values()) - set(croquis_in_use.values())
                print("diferencia")
                print(diferencia)

                for change in diferencia:
                    target_ID = list(croquis_cloud.values()).index(change)
                    target_data = [list(croquis_cloud.keys())[target_ID],list(croquis_cloud.values())[target_ID]]
                    target_drawing =canvas.find_withtag(target_data[0])

                    canvas.itemconfig(target_drawing[-1], text = target_data[1].upper()[:len(target_data[1].upper().split(" ")[0])+2], fill = "black")

                    canvas.itemconfig(target_drawing[0], fill = canvas.master._apply_appearance_mode(rep.palette[rep.rols.index(list(croquis_cloud.keys())[target_ID].split(" ")[0])]) )

                    current_values = assaig[croquis_cloud["Nom"]]["Taula"].item(target_ID - 1).get("values")
                    current_values[1] = target_data[1]
                    croquis_in_use.update({target_data[0]:target_data[1]})
                    print("target data")
                    print(target_data[1])
                    try:
                        current_values[2] = taula_mestra.loc[taula_mestra["Àlies"] == target_data[1]].iloc[0, 2]
                    except:
                        pass
                    assaig[croquis_in_use["Nom"]]["Taula"].item(target_ID - 1, values=current_values)
                assaig[croquis_in_use["Nom"]].update({"Croquis": croquis_in_use})

    up_to_date_running = False
    end = time()
    print(end-start)
    updater.start()


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

def actualitzar_assaig_output(_event, frame, parents):
    global assaig
    try:
        for canvas in frame.winfo_children():
            canvas.destroy()
    except:
        pass

    print("run")
    frame.update()
    contador = 0
    canvas_list_to_print = []
    for i in frame.winfo_children()[2:]:
        i.destroy()
    for i in list(assaig.keys()):
        frame.update()
        frame2 = customtkinter.CTkFrame(frame, height=frame.master.winfo_height()*3/3, width= frame.master.winfo_height()*4/3)
        frame2.pack(pady = 20)
        frame2.update()
        canvas_list_to_print.append(fer_dibuix([None, frame2], assaig[i]["Figura"].coordenades, assaig[i]["Croquis"], assaig[i]["Figura"].centraor(),skip = True))
        canvas_list_to_print[-1].create_text(frame.master.winfo_height()*2/3,
                                           70,
                                           angle = 0,
                                           text = assaig[i]["Croquis"]["Figura"],
                                           font = ("Arial", 25,"bold"),
                                           fill = "black"
                                           )

    print_assaig = customtkinter.CTkButton(frame.master.master.master, fg_color = rep.main_color ,text="Guardar assaig en pdf", width=30, height=10,command=lambda x = canvas_list_to_print: ie.prompt(x))
    print_assaig.place(relx = 1/3-0.05, rely = 0.1, anchor = "e")

def close_app(_event, main):
    global observer1
    global observer2
    global updater
    try:
        observer1.stop()
    except:
        pass
    try:
        observer2.stop()
    except:
        pass
    try:
        updater.stop()
    except:
        pass
    main.destroy()

def seguiment_actualitzar (pare):
    global assaig
    global assistents
    children_counter = 0
    for child in pare.winfo_children()[1:]:
        child.destroy()
    seguiment = [[i for i in assaig]]
    seguiment[0].insert(0,"/")

    for persona in assistents:
        seguiment_individual = [persona]
        for figura in assaig:
            if persona not in list(assaig[figura]["Croquis"].values()):
                seguiment_individual.append("")
            else:
                indexx = list(assaig[figura]["Croquis"].values()).index(persona)
                posició = list(assaig[figura]["Croquis"].keys())[indexx]
                seguiment_individual.append(posició)
        seguiment.append(seguiment_individual)
    seguimentTV = ttk.Treeview(pare, height= len(seguiment))

    seguimentTV.tag_configure('impar', background=pare._apply_appearance_mode(("#D6D6D6", "#3F3F3F")))
    seguimentTV['columns'] = seguiment[0]
    seguimentTV.bind('<Motion>', 'break')
    seguimentTV.column("#0", width=0, stretch=False)
    for i in seguiment[0]:

        seguimentTV.column(i, width=100, anchor = "center")
        seguimentTV.heading(i, text=i, )

    treeview_counter = 1
    for valor in seguiment[1:]:
        if treeview_counter % 2 == 1:
            tag = "impar"
        else:
            tag = "par"
        seguimentTV.insert('', 'end', treeview_counter, values=valor, tags=tag)
        treeview_counter += 1
    seguimentTV.pack()
