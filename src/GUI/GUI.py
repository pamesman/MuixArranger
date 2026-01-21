import os
import sys
import platform
import tkinter
import customtkinter
from PIL import ImageTk
from customtkinter import CTkButton
import CTkMessagebox
from screeninfo import get_monitors

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
root.iconphoto(True,tkinter.PhotoImage(file=resource_path("icon.png")))
root.iconpath = ImageTk.PhotoImage(file = resource_path("icon.png"))
root.wm_iconbitmap()
root.iconphoto(True,root.iconpath)
root.title("MuixArranger")
customtkinter.set_appearance_mode("dark") #set theme

#splash screen
splash = tkinter.Toplevel()

splash.overrideredirect(True)   #borra titlebar
splash.geometry('%dx%d+%d+%d' % (858,620,m.width/2-411.5,m.height/3-150))
splash.wm_attributes("-topmost", True)
pic = ImageTk.PhotoImage(file=resource_path("bannerunix.png"))
if "Win" in platform.system():
    splash.wm_attributes("-disabled", True)
    splash.wm_attributes("-transparentcolor", "#333333")
else:
    splash.geometry('%dx%d+%d+%d' % (205,277,m.width/2-100,m.height/3-150))
banner = tkinter.Label(splash,bg="#333333", image= pic,  highlightthickness = 0)
banner.pack(fill="both", expand="yes")



root.wm_attributes("-fullscreen",True)



tabview = customtkinter.CTkTabview(master=root,  segmented_button_selected_color = rep.main_color, segmented_button_selected_hover_color=rep.main_color, segmented_button_unselected_hover_color=rep.inv_color, segmented_button_unselected_color="grey" )
tabview.place(relx = 0.5, rely = 0.5, anchor="c", relheight=.99, relwidth=.99)
croquis = tabview.add("Croquis")  # add tab at the end
assaig_tab = tabview.add("Assaig")  # add tab at the end


### CROQUIS TAB ###
frame = customtkinter.CTkFrame(master=tabview.tab("Croquis"))
frame.place(relx=0.5,rely=0.5,anchor="c",relheight=1, relwidth=1)

#FIGURES
repertori_frame = customtkinter.CTkScrollableFrame(frame)
repertori_frame.place(relx=.01,rely=.07, relheight=0.92,relwidth=0.1,anchor="nw")
repertori_label = customtkinter.CTkComboBox(frame,
                                            fg_color=rep.main_color, button_color=rep.main_color, button_hover_color=rep.inv_color, corner_radius=5, font=("Liberation Sans",16, "bold"), border_width= 0,
                                            values = [i.nom for i in rep.repertori.values()],
                                            command = lambda x : f.inicialitzar_figura({"Figura":x}, repertori_label, frame_catalog, online= online),
                                            state = "readonly")
repertori_label.set("Afegir figura")
repertori_label.place(relx=0.01,rely=0.01,anchor="nw", relheight=0.05, relwidth=0.1*0.99)

#CROQUIS
croquis_frame = customtkinter.CTkFrame(frame, fg_color = ("#FFFFFF", "#333333"))
croquis_frame.place(relx = 0.12, rely = 0.5, anchor ="w", relheight = 0.98, relwidth = .66)
croquis_frame.update()


#NOM FIGURA
namer = customtkinter.CTkEntry(croquis_frame, placeholder_text="Nom de Figura-X", font=("Liberation Sans", 16, "bold"), state="disabled")
namer_button = customtkinter.CTkButton(croquis_frame, text="Actualitzar nom", font=("Liberation Sans", 14, "bold"), height= 28, command= f.actualitzar_nom_figura, state="disabled", fg_color = rep.main_color, hover_color=rep.inv_color)
namer_button.place(relx = 0.42,rely = 0.01,  anchor= "nw")
namer.place(relx=0.01, rely=0.01, relwidth=0.4)

deleter = customtkinter.CTkButton(croquis_frame, text="Eliminar figura", font=("Liberation Sans", 14, "bold"), height= 28, command= lambda x=0 : f.eliminar_figura(x), state="disabled", fg_color = rep.main_color, hover_color=rep.inv_color)
deleter.place(relx = 0.88,rely = 0.01,  anchor= "nw")

#Taula tècnica
tec_frame = customtkinter.CTkFrame(croquis_frame)
tec_frame.place(relx = .99, rely = .99, relwidth = 0.1, relheight = 0.25, anchor = "se")
tec_label = customtkinter.CTkLabel(tec_frame, text= "Fora de figura", font=("Liberation Sans", 14, "bold", "underline"))
tec_label.pack()

#TAULA
taula_frame = customtkinter.CTkScrollableFrame(frame)
taula_frame.place(relx = .79, rely = .99, anchor = "sw", relheight = .93, relwidth = 0.2)

taula_name = customtkinter.CTkLabel(taula_frame, text = "")
taula_namefig = customtkinter.CTkLabel(taula_frame, text = "")
taula_name.pack()
taula_namefig.pack()

taula = 0
taula_pack = [taula, taula_name, taula_namefig, namer, namer_button, deleter, tec_frame]
f.pass_variable(taula_pack)

frame_catalog = [repertori_frame, croquis_frame, taula_frame]

#Darkmode Button
CTkButton(frame,text = "○|●",
          command = f.canviar_apariencia,
          width = 20,fg_color =rep.main_color, hover_color=rep.inv_color, font = ("Liberation Sans", 16, "bold")).place(relx=.79, rely=.01, anchor="nw", relheight=0.04, relwidth=0.0225)
CTkButton(frame,text = "⨯",
          command = lambda x = root : f.close_app(0,x),
          width = 20,fg_color ="grey", hover_color= "red", font = ("Liberation Sans", 16, "bold")).place(relx=.99, rely=.01, anchor="ne", relheight=0.04, relwidth=0.0225)

#Popup Connectivitat
connection = CTkMessagebox.CTkMessagebox(title="Connectivitat",
                               message="Vols treballar en línia o desconectat?",
                               option_1= "Online",
                               option_2 = "Offline" )
if connection.get() == "Online":
    online = True
    f.connect(repertori_label, frame_catalog, splash)
else:
    splash.after(500, splash.destroy)
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
###ASSAIG TAB
###
assaig_frame = customtkinter.CTkFrame(master=tabview.tab("Assaig"), border_color="black", border_width=1)
assaig_frame.place(relx = 0.5, rely = 0.5, relwidth = 1, relheight = 1, anchor = "center")
assaig_frame2 = customtkinter.CTkScrollableFrame(master=assaig_frame, fg_color=("#AAAAAA", "#333333"), corner_radius = 0, border_color="black", border_width=0)
assaig_frame2.place(relx = .99, rely = 0.5, relheight = .99, relwidth = 2/3, anchor = "e")
assaig_frame3 = customtkinter.CTkScrollableFrame(master=assaig_frame, fg_color=("#AAAAAA", "#333333"), corner_radius = 5, border_color="black", border_width=0)
assaig_frame3.place(relx = .005, rely = 0.99, relheight = 0.5, relwidth = 1-2/3-0.02, anchor = "sw")
uppdate_assaig = customtkinter.CTkButton(assaig_frame, text="Actualitzar assaig",  fg_color = rep.main_color, width = 30, height= 10,command=lambda x=3: f.actualitzar_assaig_output(x, assaig_frame2, frame_catalog))
assaig_frame.update()

uppdate_assaig.place(relx = 1/3-0.05, rely = 0.05, anchor = "e")


root.mainloop()


