def rotator (list_of_tuples):
    a = []
    for point in list_of_tuples:
        point = (point[1],point[0])
        a.append(point)
        a.append((point[0],-point[1]))
        a.append((-point[0],-point[1]))
        a.append((-point[0],point[1]))
        # a.append((point[1],point[0]))
    return a

print(rotator([(3,1.5),(3.5,1.75), (4,2)]))
b = "Base 1"
print(b.split("\n")[0])
b.split("\n")[0]
a = ["hi","bye"]
print(a[0].upper())
#Esquema("Xopera",4, 4, 2, 0, 1, 1, 16, 16, 16, 16, 2, 4, 0, 0, 0, 0, 0, 1, 0)