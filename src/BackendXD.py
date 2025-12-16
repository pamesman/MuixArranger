import pandas as pd
import Figures as fig

t = pd.read_excel("/home/paco/Desktop/100personas.ods") #Guarda el excel

print("Benvingut a Crokiss, l'aplicació de fer croquis de muxieranga \n"
      )
#resposta = (input(" Vols començar amb el croquis? [Y/n]")
 #           or "Y")
#if resposta != "Y":
#    print("Entendible, que tingues un bon dia")
#    exit()
#else:
pass
print("Perfecte, començem...")

#aci posar un loop mentre es vuiga continuar fent figures
looper = "Y"
while looper != "N" or looper != "n":
    print("Aquesta es una llista de les figures disponibles:")
    for key, value in fig.repertori.items():
        print(key,value.nom)
    #Açò en el GUI tindrà forma d'una llista de figures a clickar, o bé tabs
    selected_fig = int(input("Escriu el nombre identificador de la figura que vols muntar: \n"))
    selected_fig = fig.repertori[selected_fig]
    nom_figura = selected_fig.nom
    print("Has seleccionat la "+nom_figura+".")
    #Al GUI açò pot quedar bé en un requadret dels lower córners amb la informació
    print('La figura "' +nom_figura+'" està composada per:')
    esquema_mini = fig.fetch_esquema(selected_fig) #diccionari, Busca l'esquema de la figura demanada, lleva les posicions nules i el presenta
    del esquema_mini["nom"]
    print('\n'.join("{}: {}".format(k, v) for k, v in esquema_mini.items())+"\n") #Formateja el diccionari bonico pal print
    #Al GUI açò sera un entry, pot ser opcional posar el nom fins al moment de guardarlo
    nom = input("Escriu el nom identificador d'aquesta figura (per exemple: "+nom_figura +"-1)\n")
    while nom in fig.assaig.keys():
        sino = input("Ja existeix una figura anomenada " + nom + " en aquest assaig, vols sobreescriurela? [y/N]" or "N")
        if sino == "N" or sino == "n":
            nom = input("Escriu el nom identificador d'aquesta figura (per exemple: "+nom_figura +"-1)\n")
        else:
            break

    croquis = fig.fer_croquis(selected_fig, nom)
    print(fig.visualitzar_croquis(croquis))
    print("Hora de muntar la figura!!")
    #GUI: Seran els buttons/labels/requadrets, ja ordenats com en el croquis real, l'ordre llavors no està determinat
    fig.assaig.update({nom:fig.construir_croquis(croquis)})


    looper = input("Vols fer un altra figura? [y,N]"
                   or "N")
    if looper == "N" or looper == "n":
        break
    else:
        input("Serà simultania a l'anterior?[y/N]" or "N")
print("Ací està l'assaig que has preparat:")
for key in fig.assaig.keys():
    fig.visualitzar_croquis(fig.assaig[key])