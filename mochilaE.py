import time
import random
import sys
sys.setrecursionlimit(2000)

def mochilaE(itens, resto_Atual, i = 0, resto_Anterior = 1, interesse = 0, maiorInteresse = -1, path = [], maiorPath = []):
    if i > 0:
        path.append((resto_Anterior - resto_Atual) // itens[i-1][0])
        if interesse > maiorInteresse:
            maiorPath = path.copy()
            maiorInteresse = interesse
    if i < len(itens):
        for nGalhos in range(resto_Atual//itens[i][0] +1, 0, -1):
            maiorPath,maiorInteresse = mochilaE(itens, resto_Atual-itens[i][0] * (nGalhos - 1), i + 1, resto_Atual, (nGalhos - 1) * itens[i][1] + interesse, maiorInteresse, path, maiorPath)
            path.pop()
            if i == len(itens)-1:
                break
    return maiorPath, maiorInteresse


itens = []
nElements = 10
capacity = 20
for i in range(nElements):
    objetos = []
    print(f"{i+1}° Elemento")
    objetos.append(random.randint(2,10))
    objetos.append(random.randint(1,10))
    print(objetos)
    itens.append(objetos)
a, b = mochilaE(itens, capacity)
while len(a) != nElements:
    a.append(0)
print(f"Melhor path = {a}, interesse = {b}")