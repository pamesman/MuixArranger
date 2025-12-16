# hello_world.py
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from pandas.core.common import not_none

root = tk.Tk()
root.geometry("1280x720")
root.pack_propagate(False)
root.title("Crokiss")
root.configure(bg="blue")
root.resizable(width=0, height=0)

checkexcel = tk.BooleanVar(root,False)

notebook = ttk.Notebook(root) #gestiona diferents displays (els tabs)


#creant cada tab
Apuntats = Frame(notebook)
Figura = Frame(notebook)
Assaig = Frame(notebook)

#Tabs per a les figures
notebook2 = ttk.Notebook(Figura)
Marieta = Frame(notebook2)
P4 = Frame(notebook2)


notebook.add(Apuntats, text='Apuntats')
notebook.add(Figura, text='Figura')
notebook.add(Assaig, text='Assaig')
notebook.pack(expand=YES, fill= BOTH)
notebook2.add(Marieta, text="Marieta")
notebook2.add(P4, text="P4")
notebook2.pack(expand=YES, fill= BOTH)

#
#mostrar excel en tab "apuntats"
#
#marc pal display

frame1 = tk.LabelFrame(Apuntats, text = "Assistents al assaig")
frame1.place(relheight=0.7, relwidth=.9, relx=0.05)

#marc per explorar larxiu
file_frame = tk.LabelFrame(Apuntats, text = "Carregar Excel")
file_frame.place(height=100, relwidth=1, rely=0.65,relx=0)

#Marc per a les posibles figures (per implementar)
marc_disponibles = tk.LabelFrame(Figura, text = "Disponibles")
marc_disponibles.place(relheight=0.95, relwidth=.1, relx=.9)

#Butó afegir figura al assaig

#Botons
button1 = tk.Button (file_frame, text =  "Explorar Arxiu", command=lambda: File_dialog())
button1.place(rely=0.5, relx=0)

button2 = tk.Button(file_frame, text = "Carregar Arxiu", command=lambda: Load_excel_data())
button2.place(rely=0.5, x=120)

label_file = ttk.Label(file_frame,text="No s'ha seleccionat cap arxiu")
label_file.place(rely=0, relx=0)

#Treeview


tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1)

#scrollbar
treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview)
tv1.configure(yscrollcommand=treescrolly.set)
treescrolly.pack(side="right", fill="y")

treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)
tv1.configure(xscrollcommand=treescrollx.set)
treescrollx.pack(side="bottom", fill="x")



def File_dialog():
    filename = filedialog.askopenfilename(initialdir="/home/paco/",
                                          title="Triar Arxiu",
                                          filetypes=((".ods",".ods"),(".xlsx",".xlsx"),("All files","*.*")))
    label_file["text"] = filename
def Load_excel_data():
    file_path = label_file["text"]
    try:
        excel_filename = r"{}".format(file_path)
        df = pd.read_excel(excel_filename)
        global Bases
        Bases = df[df["Posició"]!="Base"]
        checkexcel.set(True)

    except ValueError:
        tk.messagebox.showerror("Informació", "Arxiu invàlid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Informació",f"Arxiu {file_path} no trobat")
    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("", "end", values=row)
    return None

def clear_data():
    tv1.delete(*tv1.get_children())


#Figura labels

#P4
P4_B = ttk.Label(P4, text="B").place(x=600, y=350)
P4_S = ttk.Label(P4, text="S").place(x=50, y=500)
P4_A = ttk.Label(P4, text="A").place(x=50, y=520)
#Seleccionador de posició
def P4_B_label_clicked(event):


P4_B.bind("<Button-1>", P4_B_label_clicked)

#Marieta
MarietaCanvas = tk.Canvas(Marieta, width=280, height=20, bg="blue")
MarietaCanvas.place(relheight=1, relwidth=1)

Base2 = StringVar(value="Base")
Base1 = MarietaCanvas.create_text(5, 200, anchor="w", text="Base", angle=90)


root.wait_variable(checkexcel)


Base2DD = ttk.Combobox(Marieta, textvariable="Base", values=[*Bases["Nom"]]).place(relx=0.5, rely=0.5)

Base3 = ttk.Label(Marieta, text="Base")
Base4 = ttk.Label(Marieta, text="Base")


Base3.place(y=200, x=700)
Base4.place(y=400, x=700)
Alsadora1 = ttk.Label(Figura, text="Alçadora")
Alsadora2 = ttk.Label(Figura, text="Alçadora")


root.mainloop() #fa apareixer la finestra
