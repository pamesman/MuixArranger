import math

def round_rectangle_AA(parent, x,y,width=50,height=20,radius=5, angle = 0,outline="black",fill="", border_width=0, tags=None):
    x1 = x-width/2
    x2 = x+width/2
    y1 = y-height/2
    y2 = y+height/2
    angle = math.radians(angle)
    outline2 = ""
    if border_width == 0:
        outline = ""
        outline2 = ""
    def round_rectangle(parent, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]
        def rotator(points, angle, center):
            lista_punts=[]
            x0 = center[0]
            y0 = center[1]
            for i in range(int(len(points)/2)):
                x = points[2*i]-x0
                y = points[2*i+1]-y0
                lista_punts.append(x*math.cos(angle)+y*math.sin(angle)+x0)
                lista_punts.append(y*math.cos(angle)-x*math.sin(angle)+y0)
            return lista_punts
        points = rotator(points, angle, (x,y))


        return parent.create_polygon(points, **kwargs, smooth=True, tags = tags)


    my_rectangle0 = round_rectangle(parent, x1, y1, x2, y2, radius=radius, outline=outline2, fill=fill, width=border_width+0.5)
    my_rectangle = round_rectangle(parent, x1, y1, x2, y2, radius=radius, outline=outline, fill="", width=border_width)

    return my_rectangle,my_rectangle0
