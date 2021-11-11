import time
import random
import sys
from multiprocessing import Process

sys.setrecursionlimit(2000)

def mochila(itens, resto_Atual, capacidadeTotal, limS = 0, limMaior = -1, i = 0, resto_Anterior = 1, interesse = 0, maiorInteresse = -1, path = [], maiorPath = []):
    #caso ache um limitante superior maior, o limitante muda
    if limS > limMaior:
        limMaior = limS
    if i > 0:
        path.append((resto_Anterior - resto_Atual) // itens[i-1][0])
        #caso ache um interesse maior, a melhor solução muda
        if interesse > maiorInteresse:
            maiorPath = path.copy()
            maiorInteresse = interesse
    if i < len(itens):
        i = i - 1
        #calculo do limitante superior de cada galho
        if len(path) != 0 and path[i] != 0:
            limS = 0
            aux = 1
            while aux < i + 1:
                limS = limS + (path[aux] * itens[aux][1])
                aux = aux + 1
            limS = limS + itens[i][1] * (path[i] - 1)
            limS = limS + (itens[i + 1][1]) / (itens[i + 1][0])
            aux2 = 1
            aux3 = 0
            while aux2 < i + 1:
                aux3 = aux3 + (itens[aux2][0] * path[aux2])
                aux2 = aux2 + 1
            limS = limS * (capacidadeTotal - (aux3 + itens[i][0] * (path[i] - 1)))
        i = i + 1
        #expande os galhos caso seja o primeiro (obrigatorio expandir), ou o limitante superior seja maior que o anterior
        if len(path) == 0 or limS > limMaior:
            for nGalhos in range(resto_Atual//itens[i][0] +1, 0, -1):
                #chama a mesma função recursivamente, passando quanto espaço sobrou para inserir mais itens e o interesse atual
                maiorPath,maiorInteresse = mochila(itens, resto_Atual-itens[i][0] * (nGalhos - 1), capacidadeTotal, limS, limMaior, i + 1, resto_Atual, (nGalhos - 1) * itens[i][1] + interesse, maiorInteresse, path, maiorPath)
                path.pop()
                if i == len(itens)-1:
                    break
    #retorna a melhor quantidade de itens na mochila e o maior interesse gerado
    return maiorPath, maiorInteresse

def mochilaE(itens, resto_Atual, i = 0, resto_Anterior = 1, interesse = 0, maiorInteresse = -1, path = [], maiorPath = []):
    f1 = open("c:\\Users\\ENZO\\Desktop\\Pasta Compartilhada Drive\\vsCode Windows\\MatDisc\\mochila100.txt", "a")
    if i > 0:
        path.append((resto_Anterior - resto_Atual) // itens[i-1][0])
        #caso ache um interesse maior, a melhor solução muda
        if interesse > maiorInteresse:
            maiorPath = path.copy()
            maiorInteresse = interesse
            f1.write(f"Melhor path exalstivo = {maiorPath}, interesse = {maiorInteresse}\n\n")
    if i < len(itens):
        #expansão dos todos os galhos da arvore
        for nGalhos in range(resto_Atual//itens[i][0] +1, 0, -1):
            #chama a mesma função recursivamente, passando quanto espaço sobrou para inserir mais itens e o interesse atual
            maiorPath,maiorInteresse = mochilaE(itens, resto_Atual-itens[i][0] * (nGalhos - 1), i + 1, resto_Atual, (nGalhos - 1) * itens[i][1] + interesse, maiorInteresse, path, maiorPath)
            path.pop()
            if i == len(itens)-1:
                break
    return maiorPath, maiorInteresse

if __name__ == '__main__':
    f1 = open("c:\\Users\\ENZO\\Desktop\\Pasta Compartilhada Drive\\vsCode Windows\\MatDisc\\mochila100.txt", "a")
    #realizado 10 testes para cada 10, 100, 1000 itens na mochila
    for i in range(0,1):
        itens = []
        auxItens = []
        #quantidade de itens
        nElementos = 10
        #capacidade da mochila
        capacidade = 20
        capacidadeTotal = capacidade
        #leitura dos pesos e interesses de cada item
        for i in range(nElementos):
            objetos = []
            objetos.append(random.randint(2,10))
            objetos.append(random.randint(1,10))
            itens.append(objetos)
            auxItens.append(objetos)
        aux = 0
        #ordenação dos itens de melhor para pior na ordem de interesse dividido por peso
        for i in range(nElementos):
            for j in range(nElementos):
                if(j > i):
                    if(itens[j][1]/itens[j][0] > itens[i][1]/itens[i][0]):
                        aux = itens[i][1]
                        itens[i][1] = itens[j][1]
                        itens[j][1] = aux
                        aux = itens[i][0]
                        itens[i][0] = itens[j][0]
                        itens[j][0] = aux
        f1.write(f"{itens}\n\n")
        #chama o procedimento do metodo de limitante superior
        a, b = mochila(itens, capacidade, capacidadeTotal)
        while len(a) != nElementos:
            a.append(0)
        f1.write(f"Melhor path = {a}, interesse = {b}\n--------------------------------------------------\n")
        #chama o procedimento do metodo exaustivo, terminando apos duas horas maximas de execução
        kill = Process(target=mochilaE, args=(auxItens, capacidade), name='Process_mochilaE')
        kill.start()
        kill.join(7200)
        kill.terminate()
    f1.close