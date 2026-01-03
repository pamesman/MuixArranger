import pandas as pd


database = pd.read_excel("/home/paco/Desktop/100personas.ods")
assistents= pd.read_excel("/home/paco/Desktop/asistentes.ods")

taula_mestra = pd.DataFrame([],columns=["Nom","Muscle","Alçada","Braç","Posició"])
for i in assistents["Nom"]:
    if i in list(database["Nom"]):
        entrada = database.loc[database["Nom"] == i]
    else:
        entrada = pd.DataFrame([[i,0,0,0,"Nou"]],columns=["Nom","Muscle","Alçada","Braç","Posició"])
    taula_mestra = pd.concat([taula_mestra,entrada])

taula_mestra = taula_mestra.sort_values(by=["Muscle"], ascending=False)

taula_mestra = taula_mestra[taula_mestra["Nom"].str.contains("Z-") == False]

working_list = taula_mestra[["Nom", "Muscle"]]


list_nom = list(working_list["Nom"])
list_muscle = list(working_list["Muscle"])

#working_list = [str((list_nom[i]+" "+str(list_muscle[i]))) for i in range(len(list_nom))]
working_list = list_nom


