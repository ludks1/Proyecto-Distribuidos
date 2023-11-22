import random
MD = [[0 for _ in range(4)] for _ in range(4)]

for x in range(4):
    for y in range(x+1, 4):
        MD[x][y] = random.randint(1, 100)
        MD[y][x] = MD[x][y]

for fila in MD:
    print(fila)

nombre_archivo = "datos_matriz.txt"

with open(nombre_archivo, "w") as archivo:
    for fila in MD:
        archivo.write(" ".join(map(str, fila)) + "\n")
