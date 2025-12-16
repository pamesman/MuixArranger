from tabulate import tabulate
import pandas as pd
t = pd.read_excel("/home/paco/Desktop/100personas.ods")
#Figura: Cada una de les diferents estructures muixarangueres, te un nom identificatiu i un nombre de participants, cadascun amb el seu rol. Quan parlem de termes com esquema i croquis, sera referit a la idea d'una Figura
#esquema: Composició simplificada de una figura muixeranguera, el esquema de una figura presenta el numero de persones en cada posició. Es una classe amb cada posició siguent un atribut d'aquesta
#Repertori: Un diccionari dels diferents Esquemes(Figures), de forma {n:esquema}
#Croquis: Instància realitzable d'una figura, explicita una persona per a cada rol en forma de diccionari
#Assaig: Un Assaig es un diccionari composat per croquis(dict), agafant com a clau el seu nom {nom:croquis}
class Esquema:
    figures_rep = 0
    def __init__(self, nom, base, segona, tercera, quarta, alsadora, xicalla, mans, vents, laterals, tap, agulla, peu, puntal, crossa, genoll, contrafort, guia, passadora, recollidora):
        self.nom = nom
        self.base = base
        self.segona = segona
        self.tercera = tercera
        self.quarta = quarta
        self.alsadora = alsadora
        self.xicalla = xicalla
        self.mans = mans
        self.vents = vents
        self.laterals = laterals
        self.agulla = agulla
        self.peu = peu
        self.tap = tap
        self.passadora = passadora
        self.recollidora = recollidora
        self.genoll = genoll
        self.contrafort = contrafort
        self.guia = guia
        self.puntal = puntal
        self.crossa = crossa
        type(self).figures_rep += 1
    def afegir_xicalla(self):
        self.xicalla += 1
    def graella(self):
        print("bases:", self.base, " segones:", self.segona, " terceres:", self.tercera, " quartes:", self.quarta, " alsadores:", self.alsadora, " xiquetes:", self.xicalla, " mans:", self.mans, " vents:", self.vents, " laterals:", self.laterals, " taps:", self.tap, " agulles:", self.agulla, " peus:", self.peu, " puntals:",self.puntal," crosses:", self.crossa, " genolls:", self.genoll, " contraforts:", self.contrafort, " guies:", self.guia, " passadores:", self.passadora, " recollidores:",
              self.recollidora)
    def afegir_rengle(self):
        if self.mans != 0:
            if self.base == 1:
                self.mans += 2
            else:
                self.mans += self.base
        else:
            pass
        if self.vents != 0:
            if self.base == 1:
                self.vents += 2
            else:
                self.vents += self.base
        else:
            pass
        if self.laterals != 0:
            if self.base == 1:
                self.laterals += 4
            else:
                self.laterals += 2*self.base
        else:
            pass
"""
Hola jo del futur. Segurament vingues a afegir un nou atribut a aquesta classe per no morirte a lhora de fer els croquis 
(una lista de posicions per a botons amirite?) et recorde que per a que no es trenque al menys una part del visualitzador de croquis,
 hauràs d'afegir correccions a ALMENYS fer_croquis 
"""
assaig = {}

alta_de_5 = Esquema("Alta de 5",6, 6, 3, 0, 1, 1, 24, 19, 6, 8, 3, 4, 0, 0, 0, 0, 0, 1, 0)
banc = Esquema("Banc",1, 2, 0, 0, 1, 1, 4, 4, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0)
branca_de_morera = Esquema("Branca de Morera",2, 1, 0, 0, 1, 1, 8, 10, 12, 16, 0, 0, 1, 0, 0, 0, 0, 0, 0)
campana = Esquema("Campana",4, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
castell = Esquema("Castell",3, 3, 3, 0, 0, 1, 18, 15, 24, 12, 3, 0, 0, 0, 0, 0, 0, 1, 0)
cinc_en_un_peu = Esquema("Cinc en un peu",1, 2, 0, 0, 1, 1, 6, 6, 8, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)
encontre = Esquema("Encontre",4, 2, 0, 0, 1, 1, 6, 6, 12, 8, 0, 0, 0, 0, 0, 0, 0, 1, 0)
figuereta = Esquema("Figuereta",6, 3, 1, 0, 0, 0, 12, 12, 6, 10, 0, 4, 0, 0, 0, 0, 0, 1, 1)
marieta = Esquema("Marieta",4, 4, 0, 0, 0, 1, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2)
piloto = Esquema("Pilotó",4, 4, 2, 0, 0, 1, 16, 16, 0, 24, 4, 0, 0, 0, 0, 0, 0, 1, 0)
quatre_en_un_peu = Esquema("Quatre en un peu",1, 2, 0, 0, 0, 1, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0)
roscana = Esquema("Roscana",6, 3, 0, 0, 1, 1, 12, 12, 6, 8, 0, 4, 0, 0, 0, 0, 0, 1, 0)
senia_brasos = Esquema("Sènia (Braçps)",8, 4, 0, 0, 0, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0)
senia_p4 = Esquema("Sènia/P4",1, 1, 0, 0, 1, 1, 9, 8, 12, 16, 0, 0, 0, 0, 0, 0, 0, 1, 0)
torreta = Esquema("Torreta",4, 2, 0, 0, 1, 1, 10, 10, 16, 16, 0, 4, 0, 0, 0, 0, 0, 1, 0)
volantinera = Esquema("Volantinera",6, 6, 3, 1, 0, 0, 24, 18, 0, 14, 3, 4, 0, 6, 0, 0, 0, 1, 0)
xopera = Esquema("Xopera",4, 4, 2, 0, 1, 1, 16, 16, 16, 20, 2, 4, 0, 0, 0, 0, 0, 1, 0)
dummy = Esquema("troubleshooting",0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)

repertori = {1:alta_de_5,
             2:banc,
             3:branca_de_morera,
             4:campana,
             5:castell,
             6:cinc_en_un_peu,
             7:encontre,
             8:figuereta,
             9:marieta,
             10:piloto,
             11:quatre_en_un_peu,
             12:roscana,
             13:senia_brasos,
             14:senia_p4,
             15:torreta,
             16:volantinera,
             17:xopera,
             18:dummy}
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

    for i in range (1,len(posicions)):
        if nombre[i] == 0:
            pass
        else:
            for h in range (0,nombre[i]):
                clau = str(posicions[i]).capitalize() + " " + str(h + 1)
                producte.update({str(clau): "sense assignar"})
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
    lista = [[key,value] for key,value in croquis_generat.items()]
    return lista

def construir_croquis(croquis_generat):
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






