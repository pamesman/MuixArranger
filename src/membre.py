import io
import os
import sys

import pandas as pd

from src.API.drive import download_file

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def carregar_assistencia(id_membres, id_assistents):
    try:
        database = pd.read_excel(io.BytesIO(download_file(real_file_id=id_membres)))
        assistents = pd.read_excel(io.BytesIO(download_file(id_assistents)))
    except:
        id_membres = resource_path("100personas.ods")
        id_assistents = resource_path("asistentes.ods")
        database = pd.read_excel(id_membres)
        assistents= pd.read_excel(id_assistents)
    taula_mestra = pd.DataFrame([],columns=["Nom","Àlies","Alçada espatlles","Muscle","Alçada","Braç","Posició"])
    for i in assistents["Àlies"]:
        if i in list(database["Àlies"]):
            entrada = database.loc[database["Àlies"] == i]
        else:
            entrada = pd.DataFrame([[i,i,0,0,0,"Nou"]],columns=["Nom","Àlies","Alçada espatlles","Muscle","Alçada","Braç","Posició"])
        taula_mestra = pd.concat([taula_mestra,entrada])

    taula_mestra = taula_mestra.sort_values(by=["Alçada espatlles"], ascending=False)

    taula_mestra = taula_mestra[taula_mestra["Àlies"].str.contains("Z-") == False]
    working_list = taula_mestra[["Àlies", "Alçada espatlles"]]


    list_nom = list(working_list["Àlies"])
    list_muscle = list(working_list["Alçada espatlles"])

    #working_list = [str((list_nom[i]+" "+str(list_muscle[i]))) for i in range(len(list_nom))]
    working_list = list_nom
    return working_list, taula_mestra




