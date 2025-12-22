from calendar import error

import pandas as pd
t = pd.read_excel("/home/paco/Desktop/100personas.ods")

taula_mestra = t.sort_values(by=["Muscle"], ascending=False)

taula_mestra = taula_mestra[taula_mestra["Nom"].str.contains("Z-") == False]

working_list = taula_mestra[["Nom", "Muscle"]]

#print(t[["Nom","Muscle"]])

lista = [[t["Nom"][i],int(t["Muscle"][i]),int(t["Alçada"][i])] for i in range(len(t["Nom"])) if "Z-" not in str(t["Nom"][i])] #fa una llista de llistes dels components, elimina els "Z-"

working_list = list(working_list["Nom"])
