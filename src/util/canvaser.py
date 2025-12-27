import tkinter as tk

def redraw(event):
    c.coords(item, 0, 0, event.width, event.height)
    c.coords(item2, 200, 200, event.width, event.height)

root = tk.Tk()
root.geometry("400x400")

c = tk.Canvas(root)
c.pack(fill="both", expand=True)
c.bind("<Configure>", redraw)
item = c.create_line(0,0,400,400)
item2 = c.create_oval(200,200,210,210)

root.mainloop()