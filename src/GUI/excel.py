import pandas as pd
import src.Figures as fig
t = pd.read_excel("/home/paco/Desktop/100personas.ods") #Guarda el excel
for i in range(0,len(t["Nom"])):
    print(str(t["Nom"][i]),str(t["Muscle"][i]))
