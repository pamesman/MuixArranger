import customtkinter
root = customtkinter.CTk()
root.geometry("1280x720")
def funcioncilla(douple):
    print("otro,",object)


    print(combo.winfo_id())


for i in range(0,2):
    combo = customtkinter.CTkComboBox(root,values=["a","b","c","d","e","f","g","h","i"])
    combo.configure(command=lambda obj=combo : funcioncilla((obj, obj)))

    combo.place(relx=0.5+i/10, rely=0.5+i/10)
    entrada = [combo.winfo_id(),""]













root.mainloop()