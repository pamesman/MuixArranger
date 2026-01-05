def rotator (list_of_tuples):
    a = []
    for point in list_of_tuples:
        a.append(point)
        # a.append((point[0],-point[1]))
        # a.append((-point[0],-point[1]))
        a.append((-point[0],point[1]))
    return a

print(rotator([(1,3),(2.5,1.01),(2.5,-1.01),(3,-1.2),(1.5,-4),(1.67,-4.5),(1.83,-5),(1.63, -5.6),(2.2,-5.4)]))
b = "Base 1"
print(b.split("\n")[0])
b.split("\n")[0]
a = ["hi","bye"]
print(a[0].upper())
#Esquema("Xopera",4, 4, 2, 0, 1, 1, 16, 16, 16, 16, 2, 4, 0, 0, 0, 0, 0, 1, 0)