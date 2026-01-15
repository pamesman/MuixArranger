# MUIXARRANGER 📝
MuixArranger és un eina pensada per facilitar el procés de fer-ne croquis muixarangers

# 📖GUIA DEL USUARI:

*  * *

## 1.CONNECTIVITAT

Aquesta aplicació pot utilitzar-se de manera online o offline (decidit a cada inici d'aplicació).

En mode "online", l'applicació es conecta a tres fulls de càclul de google drive (1. assaig, 2.assistencia, 3.base de dades) [Per a més detalls, llegir `Abans de començar.txt`]. En mode "offline", l'aplicació intenta conectar-se als fulls de càlcul 'assaig' i 'assistènica' i si no ho aconssegueix, utilitza uns valors locals predeterminats.


*  *  * 

## 2.FUNCIONAMENT
    
En iniciar el programa, l'aplicació es sincronitza, si escau, amb l'assaig en desenvolupament i el carrega.
    
   
###    AFEGIR FIGURA

Mitjançant el botó "Afegir figura" s'obri un desplegable amb les figures disponibles. En seleccionar una, l'app demana un nom pel qual identificar-la i la representa en pantalla per a editar el seu croquis
        
  ⚠️ **IMPORTANT**: Actualment, les figures `Roscana` i `Sènia (braçps)` no están programades. Seleccionar-les pot produir errors. En cas de fer-ho en mode online, podria corrompre l'arxiu !!!
    
    
###    EDICIÓ DE FIGURA

Quan es crea una nova figura, apareix un croquis buit en pantalla. Fent CLIC en cada posició, es pot anar assignant persones als respectius llocs. Les membres de la colla apareixen en una llista per ordre d'alçada (Muscle), i es poden cercar escrivint el seu nom en la entrada de text. Per afegir xicalla o persones que no es troben registrades a la base de dades, es pot escriure el seu nom i seleccionar del desplegable. Per tal d'evitar duplicats, les persones que ja participen en la figura desapareixen de la llista de selecció.

Es poden AMAGAR posicions de pinya mitjançant un `CLIC DRET`, per tal de que no ocupin espai. Un segon clic dret les rehabilita.


*  *  *

# ⚠️AQUESTA APLICACIÓ ES TROBA EN DESENVOLUPAMENT⚠️

No es extrany que trobeu bugs i problemes durant la normal utilització del programa. Si podeu, comuniqueu-me el que trobeu pels mitjans que considereu adients.

Sugerencies, tant de canvis com de noves funcionalitats son benvingudes. 

Planejats pero encara no implementat tenim els seguents ítems:
- Ampliació del repertori: (Morera, Trobada, Dolçaina, Tudell, Canya etc.)
- Composicions (Retaules, Palmerals, Enterros, etc.)
- Figures simultànies


*  *  *

# SETUP PER AL CORRECTE FUNCIONAMENT:

*  *  *

### 1. Localitzar (al drive):

- Excel membres de la colla:

        Han de presentar les columnes `Àlies` i `Alçada espatlles`
 - Excel assistents a l'assaig
 
        Ha de presentar la columna `Àlies`
- Excel d'assaig/actuació
    
        Ha de estar en blanc
      


### 2. Compartir:
    
Els arxius de l'apartat anterior han de compartir-se amb:
            
                        `muixarranger-api@muixarranger.iam.gserviceaccount.com`
    
  (en cas de reutilitzar cap dels excels, no és necessari tornar a compartir)


### 3. Guardar l'ID dels excels al arxiu config.txt, al directori d'instalació (Segurament 'C:\Program Files\MuixArranger')
    
L'ID es troba al url del full de càlcul i sol tindre aquest aspecte: `1KJrjm34obf6L2BtFBC8WsB2rVpQMFcusIDVeTMu5MmU`

         https://docs.google.com/spreadsheets/d/     ID     /edit?gid=0#gid=0
                                                 ^^^^^^^^^^^


### 4. Iniciar el programa!