from src.util.classes.esquema import Esquema


#Definir cada figura: Nom/Posicions/Coordenades
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

#Definir coordenades
alta_de_5.coordenades = 7
banc.coordenades = 7
branca_de_morera.coordenades = 7
campana.coordenades = [(-1.5,-1.5),(-1.5,1.5),(1.5,1.5),(1.5,-1.5),(0,-0.5),(-0.5,0.5),(0.5,0.5),(0,0),(-2.5,0),(0,2.5),(-2.5,0),(0,-2.5)]
castell.coordenades = None
cinc_en_un_peu.coordenades = None
encontre.coordenades = None
figuereta.coordenades = None
marieta.coordenades = None
piloto.coordenades = None
quatre_en_un_peu.coordenades = None
roscana.coordenades = None
senia_brasos.coordenades = None
senia_p4.coordenades = None
torreta.coordenades = None
volantinera.coordenades = None
xopera.coordenades = None
dummy.coordenades = None


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

