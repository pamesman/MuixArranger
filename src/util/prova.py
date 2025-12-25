import tkinter as tk
a = tk.StringVar("cavalo")
def chivato():
    print("me han cambiado muaaaaaaa")
trace_add(a,"write",chivato)

a = "aaa"
