from src.util.classes.esquema import Esquema

"""
input: Esquema + string
output: diccionari
"""
def fer_croquis(figura: Esquema,nom: str):
    """
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
            pass
        else:
            for h in range (0,nombre[i]):
                clau = str(posicions[i]).capitalize() + " " + str(h + 1)
                producte.update({str(clau): "N. A."})
                stringoutput += str(clau) + ":" + str(producte[str(clau)]) + "\n"
            stringoutput += "\n\n"
    return producte


def croquis_to_table(croquis_generat:dict,dt = None):
    listah = [["Posició", "Nom","Muscle"]] #header
    try:
        lista = [[key,value,int(dt[dt[value].str.contains(value) == True]["Muscle"])] for key,value in croquis_generat.items()]
    except:
        lista = [[key,value] for key,value in croquis_generat.items()]  # posició,persona,empty
    return listah+lista[2:]
