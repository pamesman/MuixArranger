import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import pandas as pd


root = tk.Tk()
root.config(bg="#3D505B")
root.geometry("1280x720")



#crear grid
def gridmake(parent,X,Y):
    for i in range(0,X):
        parent.columnconfigure(i,weight=1)
        print(i)
    for i in range(0,Y):
        parent.rowconfigure(i,weight=1)
        print(i)
    #crea un canvas per cell per a que existeixen totes
    for i in range(0,X):

        for h in range(0,Y):
            id_h = h
            cv = Canvas(root,  bg = '#3D505B')
            cv.grid(row=h, column=i, padx=0, pady=0)
            coordinates = str(i) + "x"+ str(h)
            cv.create_text(5, 8, font="Times 6 italic bold", anchor="w",
                           text= coordinates)

            print(i,h)
            print(cv.grid_info())
            cv.bind("<Button-1>",lambda event: print(cv.grid_info()))
    Canvas(root,bg = "#3D505B")
    #cv.grid(row=0,column=0, columnspan=X, rowspan=Y, sticky="NSEW")
    
def Make_CanvH(parent,X,Y,text,bgcolor):
    cv = Canvas(parent,  bg = bgcolor)
    cv.grid(row=Y,column=X, columnspan=3,sticky="N",padx=2,pady=2)
    cv.create_text(30,20,fill="darkblue",font="Times 12 italic bold",anchor="w",
                    text=text)
def Make_CanvV(parent,X,Y,text,bgcolor):
    cv = Canvas(parent,  bg = bgcolor,)
    cv.grid(row=Y,column=X, rowspan=3,sticky="N",padx=2,pady=2)
    cv.create_text(30,20,fill="darkblue",font="Times 12 italic bold",anchor="w",
                    text=text)



gridmake(root,50,30)
#testing

Make_CanvH(root,22,18,"Bases","red")
Make_CanvH(root,25,18,"Bases","red")
Make_CanvV(root,21,15,"Bases","red")
Make_CanvV(root,21,12,"Bases","red")
Make_CanvV(root,28,15,"Bases","red")
Make_CanvV(root,28,12,"Bases","red")

#Make_Canv(frame1,2,2,"Bases","red")
Make_CanvH(root,1,10,"Bases","red")
Make_CanvH(root,1,11,"Bases","red")
Make_CanvV(root,1,5,"bases","red")


root.mainloop()
