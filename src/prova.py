import customtkinter
import tkinter as tk

root = customtkinter.CTk()


def raise_frame():
    print("run")
    # frame1.tk.call("raise", frame1._w, None)
    frame1.tk.call("lower", frame1._w, label)

def lower_frame():
    frame1.tk.call("lower", frame1._w, None)


button1 = customtkinter.CTkButton(root, text = "1", command = raise_frame)
button2 = customtkinter.CTkButton(root, text = "2", command = lower_frame)
button1.pack()
button2.pack()
frame = customtkinter.CTkFrame(root, width = 400, height = 400, fg_color = "blue")
frame.pack()
frame1 = customtkinter.CTkCanvas(frame, width = 400, height = 400, background = "black")
frame1.place(x=0, y=0, anchor="nw")
frame2 = customtkinter.CTkCanvas(frame, width = 400, height = 400, background = "gray")
frame2.place(x=0, y=0, anchor="nw")
label = customtkinter.CTkLabel(frame, text = "Croquis", text_color = "red")
label.place(relx = 0.5, rely = 0.5)












root.mainloop()