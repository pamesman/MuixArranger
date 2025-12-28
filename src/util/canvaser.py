import tkinter as tk
old_coords = (400,400)

root = tk.Tk()
root.geometry("400x400")

c = tk.Canvas(root)
c.pack(fill="both", expand=True)
#c.bind("<Configure>", redraw)
item = c.create_line(0,0,400,400)
item2 = c.create_oval(400,200,410,210)


def redraw(event):
    global old_coords
    c.coords(item, 0, 0, event.width, event.height)
    ratiox = event.width / old_coords[0]
    ratioy = event.height / old_coords[1]
    c.coords(item2, c.coords(item2)[0] * ratiox, c.coords(item2)[1] * ratioy, c.coords(item2)[2] * ratiox,
             c.coords(item2)[3] * ratioy)
    old_coords = (event.width, event.height)
for i in range(10):

    item2 = c.create_oval(20*i,20*i,21*i,21*i, tags = "red")
    c.bind("<Configure>", redraw)

for item in c.gettags("red"):
    print(".")
    print(item)





root.mainloop()