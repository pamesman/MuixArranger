

import funcs
# Source - https://stackoverflow.com/a
# Posted by PM 2Ring, modified by community. See post 'Timeline' for change history
# Retrieved 2025-12-25, License - CC BY-SA 3.0

from tkinter import *
import math
import repertori as rep

WIDTH = 1400
HEIGHT = 1400
CANVAS_MID_X = WIDTH/2
CANVAS_MID_Y = HEIGHT/2
SIDE = WIDTH/4

root = Tk()
canvas = Canvas(root, bg="gray", height=HEIGHT, width=WIDTH)
canvas.pack(expand=YES, fill=BOTH)


for i in rep.repertori:
    try:
        for j in rep.repertori[i].coordenades:

            canvas.create_text(i*110, 400, text=rep.repertori[i].nom)
            canvas.create_oval(10*j[0]+i*110, -10*(j[1])+500,10*(j[0])+i*110, -(j[1])*10+500, fill="red")
    except:
        pass



mainloop()
