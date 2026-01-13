def rotator (list_of_tuples):
    a = []
    for point in list_of_tuples:
        a.append(point)
        a.append((point[0],point[1]+6))
        # a.append((-point[0],-point[1]))
        #a.append((-point[0],point[1]))
    return a

print(rotator([(-3, -3), (-1, -3), (1, -3), (3, -3), (5, -3), (7, -3), (9, -3), (11, -3), (13, -3), (15, -3), (-3, -2.5), (-1, -2.5), (1, -2.5), (3, -2.5), (5, -2.5), (7, -2.5), (9, -2.5), (11, -2.5), (13, -2.5), (15, -2.5)]))
b = "Base 1"
print(b.split("\n")[0])
b.split("\n")[0]
a = ["hi","bye"]
print(a[0].upper())
#Esquema("Xopera",4, 4, 2, 0, 1, 1, 16, 16, 16, 16, 2, 4, 0, 0, 0, 0, 0, 1, 0)