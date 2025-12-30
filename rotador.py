def rotator (list_of_tuples):
    a = []
    for point in list_of_tuples:
        #a.append(point)
        #a.append((point[0],-point[1]))
        a.append((-point[0],-point[1]))
        #a.append((-point[0],point[1]))
    return a

print(rotator([(1.5, 0.86), (-1.5, 0.86), (2, 1.15), (-2, 1.15), (2.5, 1.44), (-2.5, 1.44), (3, 1.73), (-3, 1.73), (3.5, 2), (-3.5, 2), (0,-1.5),(0,-2),(0,-2.5),(0,-3),(0,-3.5)]))
b = "Base 1"
print(b.split("\n")[0])
b.split("\n")[0]
#Esquema("Xopera",4, 4, 2, 0, 1, 1, 16, 16, 16, 16, 2, 4, 0, 0, 0, 0, 0, 1, 0)