import os
import sys

import tkinter
from time import sleep
import customtkinter
from PIL import Image, ImageTk
from customtkinter import CTkButton
import CTkMessagebox
from screeninfo import get_monitors
from src.util.classes import CTkTable


from src.util import repertori as rep
import src.util.funcs as f

online = False

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



#estableix parent window
root = customtkinter.CTk()
for monitor in get_monitors():
   m = monitor
root.geometry(str(m.width) + "x" + str(m.height))
root.iconphoto(False,tkinter.PhotoImage(file=resource_path("icon.png")))
root.title("MuixArranger")
customtkinter.set_appearance_mode("dark") #set theme

#splash screen
splash = tkinter.Toplevel()
# splash.overrideredirect(True)   #borra titlebar
# splash.geometry('%dx%d+%d+%d' % (858,300,m.width/2-411.5,m.height/3-150))
# splash.attributes('-alpha', 0)
# pic = Image.open(resource_path("banner.png"))
# pic = pic.resize((858,300))
# pic = ImageTk.PhotoImage(pic)
# banner = tkinter.Label(splash, image = pic)
# banner.pack()
#


root.wm_attributes("-fullscreen",False)



tabview = customtkinter.CTkTabview(master=root)
tabview.place(relx = 0.5, rely = 0.5, anchor="c", relheight=.99, relwidth=.99)
croquis = tabview.add("Croquis")  # add tab at the end
#assaig = tabview.add("Assaig")  # add tab at the end

### CROQUIS TAB ###
frame = customtkinter.CTkFrame(master=tabview.tab("Croquis"))
frame.place(relx=0.5,rely=0.5,anchor="c",relheight=1, relwidth=1)

#FIGURES
repertori_frame = customtkinter.CTkScrollableFrame(frame)
repertori_frame.place(relx=.01,rely=.07, relheight=0.92,relwidth=0.1,anchor="nw")
repertori_label = customtkinter.CTkComboBox(frame,
                                            fg_color=rep.main_color, button_color=rep.main_color, button_hover_color=rep.inv_color, corner_radius=5, font=("Liberation Sans",16, "bold"), border_width= 0,
                                            values = [i.nom for i in rep.repertori.values()],
                                            command = lambda x : f.inicialitzar_figura(x, repertori_label, repertori_frame, canvas2, online= online))
repertori_label.set("Afegir figura")
repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.1*0.99)

#CROQUIS
croquis_frame = customtkinter.CTkFrame(frame, fg_color = ("#FFFFFF", "#333333"))
croquis_frame.place(relx = 0.12, rely = 0.5, anchor ="w", relheight = 0.98, relwidth = .66)
croquis_frame.update()
croquis_frame.bind("<Configure>", lambda event : f.resize(event, canvas2))
canvas2 = tkinter.Canvas(croquis_frame, width=croquis_frame.winfo_width() - croquis_frame.cget("corner_radius") * 4,
                         height=croquis_frame.winfo_height() - croquis_frame.cget("corner_radius") * 2,
                         bg=croquis_frame._apply_appearance_mode(("black", "#333333")), highlightthickness=0)
canvas2.place(relx=0.5, rely=0.5, anchor="center")

#NOM FIGURA
namer = customtkinter.CTkEntry(croquis_frame, placeholder_text="Nom de Figura-X", font=("Liberation Sans", 16, "bold"), state="disabled")
namer_button = customtkinter.CTkButton(croquis_frame, text="Actualitzar nom", font=("Liberation Sans", 14, "bold"), height= 28, command= f.actualitzar_nom_figura, state="disabled", fg_color = rep.main_color, hover_color=rep.inv_color)
namer_button.place(relx = 0.42,rely = 0.01,  anchor= "nw")
namer.place(relx=0.01, rely=0.01, relwidth=0.4)

deleter = customtkinter.CTkButton(croquis_frame, text="Eliminar figura", font=("Liberation Sans", 14, "bold"), height= 28, command= lambda x=canvas2 : f.eliminar_figura(x), state="disabled", fg_color = rep.main_color, hover_color=rep.inv_color)
deleter.place(relx = 0.88,rely = 0.01,  anchor= "nw")

#TAULA
taula_frame = customtkinter.CTkScrollableFrame(frame)
taula_frame.place(relx = .79, rely = .5, anchor = "w", relheight = .98, relwidth = 0.2)
taula = CTkTable.CTkTable(taula_frame, column = 3, row = 2, values = [[]], header_color = "#7393B3", font = ("Liberation Sans", 12), corner_radius = 5)
taula_name = customtkinter.CTkLabel(taula_frame, text = "")
taula_namefig = customtkinter.CTkLabel(taula_frame, text = "")
taula_name.pack()
taula_namefig.pack()
taula.pack(expand = True,  pady = 20)
taula_pack = [taula, taula_name, taula_namefig, namer, namer_button, deleter]
f.pass_variable(taula_pack)

#Darkmode Button
CTkButton(frame,text = "☀ / ☾",
          command=lambda x = canvas2: f.canviar_apariencia(x),
          width = 20,fg_color =rep.main_color, hover_color=rep.inv_color).place(relx=1, rely=1, anchor="se")

#Popup Connectivitat
connection = CTkMessagebox.CTkMessagebox(title="Connectivitat",
                               message="Vols treballar en línia o desconectat?",
                               option_1= "Online",
                               option_2 = "Offline" )
if connection.get() == "Online":
    online = True
    f.connect(repertori_label, repertori_frame, canvas2, splash)
else:
    splash.after(3000, splash.destroy)
#botó per expandir croquis zone
button_expand = customtkinter.CTkButton(croquis_frame,
                                        text = "<",
                                        height = 10,
                                        width = 10,
                                        corner_radius= 15,
                                        fg_color =rep.main_color, hover_color=rep.inv_color)
button_expand.configure(command = lambda x = button_expand: f.minimizar(x, croquis_frame, repertori_frame, repertori_label))
                                        #repertori_frame._parent_frame.forget())

button_expand2 = customtkinter.CTkButton(croquis_frame,
                                         text = ">",
                                         height = 10,
                                         width = 10,
                                         corner_radius= 15,
                                         fg_color =rep.main_color, hover_color=rep.inv_color)
                                        #repertori_frame._parent_frame.forget())
button_expand2.configure(command = lambda x = button_expand2: f.minimizar2(x, croquis_frame, taula_frame))
button_expand.place(rely = 0.5, relx = .005, anchor="w")
button_expand2.place(rely = 0.5, relx = .995, anchor="e")
root.mainloop()


