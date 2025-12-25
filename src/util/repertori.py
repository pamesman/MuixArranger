from src.util.classes.esquema import Esquema


#Definir cada figura: Nom/Posicions/Coordenades
alta_de_5 = Esquema("Alta de 5",6, 6, 3, 0, 1, 1, 24, 19, 6, 8, 3, 4, 0, 0, 0, 0, 0, 1, 0)
banc = Esquema("Banc",1, 2, 0, 0, 1, 1, 4, 4, 4, 0, 0, 4, 0, 0, 0, 0, 0, 1, 0)
branca_de_morera = Esquema("Branca de Morera",2, 1, 0, 0, 1, 1, 8, 10, 12, 16, 0, 0, 1, 0, 0, 0, 0, 0, 0)
campana = Esquema("Campana",4, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
castell = Esquema("Castell",3, 3, 3, 0, 0, 1, 18, 15, 24, 12, 3, 0, 0, 0, 0, 0, 0, 1, 0)
cinc_en_un_peu = Esquema("Cinc en un peu",1, 2, 0, 0, 1, 1, 6, 6, 8, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)
encontre = Esquema("Encontre",4, 2, 0, 0, 1, 1, 6, 6, 12, 8, 0, 0, 0, 0, 0, 0, 0, 1, 0)
figuereta = Esquema("Figuereta",6, 3, 1, 0, 0, 0, 12, 12, 6, 10, 0, 4, 0, 0, 0, 0, 0, 1, 1)
marieta = Esquema("Marieta",4, 4, 0, 0, 0, 2, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2)
piloto = Esquema("Pilotó",4, 4, 2, 0, 0, 1, 16, 16, 0, 24, 4, 0, 0, 0, 0, 0, 0, 1, 0)
quatre_en_un_peu = Esquema("Quatre en un peu",1, 2, 0, 0, 0, 1, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0)
roscana = Esquema("Roscana",6, 3, 0, 0, 1, 1, 12, 12, 6, 8, 0, 4, 0, 0, 0, 0, 0, 1, 0)
senia_brasos = Esquema("Sènia (Braçps)",8, 4, 0, 0, 0, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0)
senia_p4 = Esquema("Sènia/P4",1, 1, 0, 0, 1, 1, 9, 8, 12, 16, 0, 0, 0, 0, 0, 0, 0, 1, 0)
torreta = Esquema("Torreta",4, 2, 0, 0, 1, 1, 12, 10, 16, 24, 0, 4, 0, 0, 0, 0, 0, 1, 0, colze=4)
volantinera = Esquema("Volantinera",6, 6, 3, 1, 0, 0, 24, 18, 0, 14, 3, 4, 0, 6, 0, 0, 0, 1, 0)
xopera = Esquema("Xopera",4, 4, 2, 0, 1, 1, 16, 16, 16, 16, 2, 6, 0, 0, 0, 0, 0, 1, 0)
dummy = Esquema("troubleshooting",0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)
#aixecat
#altar, p3, palmera, palmerar, retaule, vano
#canya
#tudell
#encontret
#enterros
#guionet wtf is this
#remat llotja
#llotja
#m d titagues
#maria alta
#morera
#p3
#piló de titaigues 1,2
#pilotó 2
#oberta
#tomasina:remat
#tomasina
#trobada





#Definir coordenades
alta_de_5.coordenades = None
banc.coordenades = [(0, 0), (-5, -3), (-4, -3), (-4.5, -2.5), (-4.5, -3.5), (1, 0), (-2, 0), (2, 0), (-2, 0), (0, 1), (0, -1), (0, 2), (0, -2), (1, 1), (1, -1), (-1, -1), (-1, 1), (-2, 1), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5), (-0.5, 0.5)]
branca_de_morera.coordenades = None
campana.coordenades = [(-1.5,-1.5),(-1.5,1.5),(1.5,1.5),(1.5,-1.5),(0,-0.5),(-0.5,0.5),(0.5,0.5),(0,0),(-2.5,0),(0,2.5),(+2.5,0),(0,-2.5)]
castell.coordenades = None
cinc_en_un_peu.coordenades = [(0,0),(6,0),(8,0),(7, 0.5),(7, 1.5),(-2,0),(2,0),(-3,0),(3,0),(-4,0),(4,0),(0,1),(0,-1),(0,2),(0,-2),(0,3),(0,-3),(-1,1),(1,1),(1,-1),(-1,-1),(-2,2),(2,2),(2,-2),(-2,-2),(7,-3),(-1,0),(1,0)]
encontre.coordenades = None
figuereta.coordenades = None
marieta.coordenades = [(1,0.5),(1,-0.5),(-1,-0.5),(-1, 0.5),   (2, 0.5),(2, -0.5),(-2, -0.5),(-2, 0.5),   (-3,-3),(-3,-2),   (3, 0.5),   (3, -0.5), (-3, -0.5), (-3, 0.5),   (0,1.5),(0,-1.5),   (-1,2),   (0,0),(1,-2)]
piloto.coordenades = None
quatre_en_un_peu.coordenades = [(0,0),  (-2,-3),(2,-3),  (0, -2.5),  (-2,0),(2,0),  (0,1),(0,-1),   (0,2.5),   (-1,0),(1,0),]
roscana.coordenades = None
senia_brasos.coordenades = None
senia_p4.coordenades = None
torreta.coordenades = [(1, 1), (1, -1), (-1, -1), (-1, 1), (9.7, 0), (8.3, 0), (9, 1.5), (9, 2), (2, 0), (-2, 0), (3, 0), (-3, 0), (4, 0), (-4, 0), (5, 0), (-5, 0), (6, 0), (-6, 0), (7, 0), (-7, 0), (0, 2), (0, -2), (0, 3), (0, -3), (0, 4), (0, -4), (0, 5), (0, -5), (0, 6), (0, -6), (2, 2), (2, -2), (-2, -2), (-2, 2), (3, 3), (3, -3), (-3, -3), (-3, 3), (4, 4), (4, -4), (-4, -4), (-4, 4), (5, 5), (5, -5), (-5, -5), (-5, 5), (0.5, 1.5), (0.5, -1.5), (-0.5, -1.5), (-0.5, 1.5), (1, 2), (1, -2), (-1, -2), (-1, 2), (1.5, 3), (1.5, -3), (-1.5, -3), (-1.5, 3), (2, 4), (2, -4), (-2, -4), (-2, 4), (2, 1), (2, -1), (-2, -1), (-2, 1), (3, 1.5), (3, -1.5), (-3, -1.5), (-3, 1.5), (4, 2), (4, -2), (-4, -2), (-4, 2), (9, 5), (1, 1.5), (1, -1.5), (-1, -1.5), (-1, 1.5)]
volantinera.coordenades = None
xopera.coordenades = [(1, 1), (1, -1), (-1, -1), (-1, 1),   (10,1),(10,-1),(8,-1),(8,1),   (9.7,0),(8.3,0),   (9,1.5),   (9,2),   (2, 1), (2, -1), (-2, -1), (-2, 1), (3, 1.5), (3, -1.5), (-3, -1.5), (-3, 1.5), (4, 2), (4, -2), (-4, -2), (-4, 2), (5, 2.5), (5, -2.5), (-5, -2.5), (-5, 2.5),   (0, 2), (0, -2), (0, 3), (0, -3), (0, 4), (0, -4), (0, 5), (0, -5), (2.5, 0), (-2.5, 0), (3.5, 0), (-3.5, 0), (4.5, 0), (-4.5, 0), (5.5, 0), (-5.5, 0), (1.5, 2), (1.5, -2), (-1.5, -2), (-1.5, 2), (2, 3), (2, -3), (-2, -3), (-2, 3), (2.5, 4), (2.5, -4), (-2.5, -4), (-2.5, 4), (3, 5), (3, -5), (-3, -5), (-3, 5),   (0.5,0),(-0.5,0),   (1.5, 0), (-1.5, 0),(0.5, 1.5), (0.5, -1.5), (-0.5, -1.5), (-0.5, 1.5),    (1.5, 4.5), (1.5, -4.5), (-1.5, -4.5), (-1.5, 4.5), (2, 5.5), (2, -5.5), (-2, -5.5), (-2, 5.5), (3.5, 3.5), (3.5, -3.5), (-3.5, -3.5), (-3.5, 3.5), (4.5, 4), (4.5, -4), (-4.5, -4), (-4.5, 4),        (9,5)]
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

#colorinchis
paleta_oficial = Esquema("Paleta", "#EAD1DC","#FF9900","#F6B26B", "#F6B26B","#FCE5CD","#FFE59A","#e0ecf7","#E0EEDB","#E0EEDB","#EEEEEE","#EEEEEE","#EEEEEE","#FF9900","#D5A6BD","#C27BA0", "#B4A7D6","#FFFFFF","#FFFFFF","#FFFFFF", colze = "#81B2DE")
paleta_oficial_oscura = Esquema("PaletaD","#D09CB4","#C87800","#F39533","#F39533","#F39533","#F1B300","#81B2DE","#9DC98D","#BABABA","#959595","#959595","#959595","#9DC98D","#BF789B","#B55E8B","#8D79C1","#8D79C1","#8D79C1","#8D79C1",colze = "#81B2DE")

palette = list(vars(paleta_oficial).values())
palette_d = list(vars(paleta_oficial_oscura).values())

rols = ['Base', 'Segona', 'Tercera', 'Quarta', 'Alsadora', 'Xicalla', 'Mans', 'Vents', 'Laterals',  'Tap','Agulla', 'Peu', 'Puntal', 'Crossa','Genoll', 'Contrafort', 'Guia','Passadora', 'Recollidora', "Colze" ]
print(len(torreta.coordenades))
