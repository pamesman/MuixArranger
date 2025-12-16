#Esquema: Composició simplificada de una figura muixeranguera, l'Esquema de una figura presenta el numero de persones en cada posició. Es una classe amb cada posició siguent un atribut d'aquesta
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