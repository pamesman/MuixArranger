import customtkinter
import src.membre as mem
from src.util.classes import SearchBox as SB


root = customtkinter.CTk()
root.geometry("600x600")





insertar_membre = lambda x : x


frame = SB.SearchBox(root, mem.working_list[:10], placeholder="Base", command= insertar_membre)
frame.pack()
frame2 = SB.SearchBox(root, mem.working_list[:20], placeholder="Base", command= insertar_membre, button_color="red", text_color="blue", fg_color = "green", border_color = "black")
frame2.pack()
#frame.combo._command = lambda x : print(x)
combobo = customtkinter.CTkComboBox(root, values = mem.working_list[:10],  command= insertar_membre, button_color="red", text_color="blue", fg_color = "green")
combobo.pack()











root.mainloop()