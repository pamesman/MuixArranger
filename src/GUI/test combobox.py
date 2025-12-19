import customtkinter
root = customtkinter.CTk()
root.geometry("1280x720")
def funcioncilla(obj):
    print(obj)

    print(diccionario)

diccionario = {}
for i in range(0,2):
    combo = customtkinter.CTkButton(root,text="hi")
    combo.configure(command=lambda obj=combo.winfo_id() : funcioncilla(obj))
    diccionario.update({i:combo})
    combo.place(relx=0.5+i/10, rely=0.5+i/10)
    print(combo.winfo_id())
#print(<customtkinter.windows.widgets.ctk_button.CTkButton object .!ctkbutton2>)













root.mainloop()