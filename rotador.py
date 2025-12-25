def rotator (list_of_tuples):
    a = []
    for point in list_of_tuples:
        a.append(point)
        a.append((point[0],-point[1]))
        a.append((-point[0],-point[1]))
        a.append((-point[0],point[1]))
    return a

print(rotator([(1,1.5)]))
b = "Base 1"
print(b.split("\n")[0])
b.split("\n")[0]
#Esquema("Xopera",4, 4, 2, 0, 1, 1, 16, 16, 16, 16, 2, 4, 0, 0, 0, 0, 0, 1, 0)