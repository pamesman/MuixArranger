from tabulate import tabulate

#Figura: Cada una de les diferents estructures muixarangueres, te un nom identificatiu i un nombre de participants, cadascun amb el seu rol. Quan parlem de termes com esquema i croquis, sera referit a la idea d'una Figura
#esquema: Composició simplificada de una figura muixeranguera, el esquema de una figura presenta el numero de persones en cada posició. Es una classe amb cada posició siguent un atribut d'aquesta
#Repertori: Un diccionari dels diferents Esquemes(Figures), de forma {n:esquema}
#Croquis: Instància realitzable d'una figura, explicita una persona per a cada rol en forma de diccionari
#Assaig: Un Assaig es un diccionari composat per croquis(dict), agafant com a clau el seu nom {nom:croquis}

assaig = {}


paleta_oficial = Esquema("Paleta", "#EAD1DC","#FF9900","#F6B26B", "#F6B26B","#FCE5CD","#FFE59A","#e0ecf7","#E0EEDB","#E0EEDB","#EEEEEE","#EEEEEE","#EEEEEE","#FF9900","#D5A6BD","#C27BA0", "#B4A7D6","#FFFFFF","#FFFFFF","#FFFFFF")
paleta_oficial_oscura = Esquema("PaletaD","#D09CB4","#C87800","#F39533","#F39533","#F39533","#F1B300","#81B2DE","#9DC98D","#BABABA","#959595","#959595","#959595","#9DC98D","#BF789B","#B55E8B","#8D79C1","#8D79C1","#8D79C1","#8D79C1")
palette = list(vars(paleta_oficial).values())
palette_d = list(vars(paleta_oficial_oscura).values())

repertori2 = {}
for name in repertori.values():
    repertori2.update({name.nom:name})


def filter_dict(d, filterstring, exclude: bool):
    """
    Filtre genéric per a diccionaris
    funciona amb entrades de valors == filterstring
    si vol ferse que busque entrades que continguen filtersting
    canviar "==" por "in" i "!=" por "not in"

    inputs: diccionari, frase a filtrar, booleana per determinar si excloure(True) o Buscar(False) les entrades amb la string
    output: diccionari
    """
    for key, val in d.items():
        if exclude:
            if filterstring == str(val):
                continue
            yield key, val
        else:
            if filterstring != str(val):
                continue
            yield key, val

def fetch_esquema(figura):
    """
    Agafa com a input el esquema de la figura que se vol,
    La transforma en un diccionari Posició:Nombre
    Filtra posicions on el nombre=0
    Input: esquema
    Output: diccionari
    """
    andamiatge = vars(figura)
    filter_string = "0"
    excloure = True
    andamiatge_compact = {}
    for key, value in filter_dict(andamiatge, filter_string, excloure):
        andamiatge_compact.update({key:value})
    return andamiatge_compact #Retorna un diccionari


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


def visualitzar_croquis(croquis_generat: dict):
    figura = repertori2[croquis_generat["Figura"]]
    nombre = list(vars(figura).values())
    posicions = list(vars(figura).keys())
    stringoutput = str()
    print(croquis_generat["Nom"]+"\n\n"+"Figura: " + figura.nom+"\n")
    for i in range (1,len(posicions)):
        if nombre[i] == 0:
            pass
        else:
            for h in range (0,nombre[i]):
                clau = str(posicions[i])+" "+str(h+1)
                stringoutput += str(clau) + ":"+str(croquis_generat[str(clau)]) + "\n"
            stringoutput += "\n"
    print(stringoutput)

def croquis_to_table(croquis_generat:dict):
    listah = [["Posició", "Nom","Alçada"]]
    lista = [[key,value] for key,value in croquis_generat.items()]
    return listah+lista[2:]

#def construir_croquis(croquis_generat):
    llista_escollits = list()
    for n in range(2,len(croquis_generat)):
        posicio = list(croquis_generat.keys())[n]
        print("Queden " + str(len(croquis_generat) - n) + " posicions per cobrir")
        print("Escollix qui ocuparà la posició " + posicio + ":")
        if "base" in posicio:
            print(tabulate(t.drop(llista_escollits)[t["Posició"] == "Base"][["Nom", "Alçada"]], headers="keys", tablefmt="psql"))
            new_value = input()

        elif "alsadora" in posicio:
            print(tabulate(t.drop(llista_escollits)[t["Posició"] == "Alçadora"][["Nom", "Alçada"]], headers="keys", tablefmt="psql"))
            new_value = input()
        elif "xicalla" in posicio:
            print(tabulate(t.drop(llista_escollits)[["Nom", "Alçada"]][t["Posició"] == "Xicalla"], headers="keys", tablefmt="psql"))
            new_value = input()
        else:
            print(tabulate(t.drop(llista_escollits)[["Nom", "Alçada"]], headers="keys", tablefmt="psql"))
            new_value = input()
        llista_escollits.append(int(new_value))
        print(llista_escollits)
        croquis_generat.update({posicio: t.loc[int(new_value),"Nom"]})
    visualitzar_croquis(croquis_generat)
    return croquis_generat






