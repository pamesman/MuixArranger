from customtkinter import CTkScrollableFrame

from labelcb import  LabelCB
import customtkinter
import src.Membre as mem
import CTkTable
import src.Figures as fig
from src.util.classes import labelcb

root = customtkinter.CTk()
root.geometry("600x600")
frame = CTkScrollableFrame(root)
frame.place(x=0,y=0,relwidth=0.45,relheight=1)
frame2 = customtkinter.CTkFrame(root)
frame2.place(relx = 1,rely = 1,relwidth=0.5,relheight=1, anchor= "se")
customtkinter.set_appearance_mode("dark")
cq = fig.fer_croquis(fig.repertori[1], "N.A")
taule = CTkTable.CTkTable(frame, column= 3,row=10, header_color="#7393B3", font=("Liberation Sans",12), corner_radius=5)
taule.configure(values = [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]])
taule.pack(pady=20)
for i in ["Base 1", "Base 2", "Base 3"]:
    labelcb.LabelCB(frame2,i,mem.working_list,taule,cq).pack(expand=True, fill="both", pady=20)











root.mainloop()