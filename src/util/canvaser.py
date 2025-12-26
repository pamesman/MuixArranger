
import figures as fig
import funcs
# Source - https://stackoverflow.com/a
# Posted by PM 2Ring, modified by community. See post 'Timeline' for change history
# Retrieved 2025-12-25, License - CC BY-SA 3.0

from tkinter import *
import math

WIDTH = 1400
HEIGHT = 1400
CANVAS_MID_X = WIDTH/2
CANVAS_MID_Y = HEIGHT/2
SIDE = WIDTH/4

root = Tk()
canvas = Canvas(root, bg="white", height=HEIGHT, width=WIDTH)
canvas.pack(expand=YES, fill=BOTH)

vertices = [
    [CANVAS_MID_X - SIDE/2, CANVAS_MID_Y - SIDE/2],
    [CANVAS_MID_X + SIDE/2, CANVAS_MID_Y - SIDE/2],
    [CANVAS_MID_X + SIDE/2, CANVAS_MID_Y + SIDE/2],
    [CANVAS_MID_X - SIDE/2, CANVAS_MID_Y + SIDE/2],
]

def rotate(points, angle, center,color):
    angle = math.radians(angle)
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    cx, cy = center
    new_points = []
    for x_old, y_old in points:
        x_old -= cx
        y_old -= cy
        x_new = x_old * cos_val - y_old * sin_val
        y_new = x_old * sin_val + y_old * cos_val
        new_points.append([x_new + cx, y_new + cy])
    canvas.create_polygon(new_points, fill=color)
    return new_points

def draw_square(points, color="red"):
    canvas.create_polygon(points, fill=color)

def test():
    old_vertices = [[150, 150], [250, 150], [250, 250], [150, 250]]
    print ("vertices: ", vertices, "should be: ", old_vertices)
    print (vertices == old_vertices)

#draw_square(vertices, "blue")

center = (0,0)
#rotate(vertices, -10, center,"green")
#rotate(vertices, -20, center,"yellow")
test()
#draw_square(new_square)
canvas.create_text((400,400),angle='60',anchor='ne',text="hi babe",font="Arial")
for i in range(1,10):
    canvas.create_text((400+3**(1/2)/2*15*i,400+1/2*15*i),angle='60',anchor='ne',text="Toni Ciscar",font="Arial")

mainloop()
