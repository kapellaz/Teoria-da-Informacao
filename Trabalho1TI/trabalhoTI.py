
from scipy.io import wavfile
import numpy as np

import matplotlib.pyplot as plt
import huffmancodec as hf

import collections


A = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
     'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
     'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'W', 'Y', 'Z']
     

Ais = list(i for i in range(256))

    
# desenha um gráfico em função da informação que recebeu de um dicionario
def hist(dic, file):
    x = list(dic.keys())
    y = list(dic.values())
    plt.bar(x, y, width=0.6, color ='red')
    plt.xlabel("Alfabeto")
    plt.ylabel("Ocorrências")
    plt.title(file)
    plt.show()


#calcula a ocorrencia de cada letra do alfabeto
def ocorrencia(alfa, fonte):
    counts = collections.Counter(fonte)
    for char in alfa:
        if char not in counts.keys():
            counts[char] = 0
    counts = collections.OrderedDict(sorted(counts.items()))
    return counts


# recebe um texto e retorna-o dentro de uma lista
def readText(fich):
    lines = []
    with open(fich, "r") as fich:
        text = fich.read()
    for i in text:
        o = ord(i)
        if((o>64 and o<91)or(o>96 and o<123)):
            lines.append(i) 
    return lines


# recebe um ficheiro e cria o seu histograma de acordo com o seu alfabeto e tipo de ficheiro
def makeHist(fich):
    if fich[-3:] == 'bmp':
        d = plt.imread(fich)
        data = np.array(d).flatten()
        hist(ocorrencia(Ais, data), fich)
        
    elif fich[-3:] == 'wav':
        fs, dat = wavfile.read(fich)
        data = dat.flatten()
        hist(ocorrencia(Ais, data), fich)

    elif fich[-3:] == 'txt':
        data = readText(fich)
        hist(ocorrencia(A, data), fich)
        
 
# função que calcula a entropia
def entropia(data):
    counts = collections.Counter(data)
    probs = [float(c) / (len(data) ) for c in counts.values()]
    ent = -sum(probs * np.log2(probs))
    return ent


# função que imprime a entropia, variancia, numero médio e entropia de 2 simbolos
def printInfo(p):
    if p[-3:] == 'bmp':
        d = plt.imread(p)
        data = np.array(d).flatten()
    if p[-3:] == 'wav':
        fs, data = wavfile.read(p)
    if p[-3:] == 'txt':
        data = readText(p)


    print('Entropia: {}'.format(entropia(data)))
    print('Numero medio de bits: {}'.format(numMedBits(data)))
    print('Variancia: {}'.format(variancia(data)))
    print('Entropia2: {}'.format(entropia2S(data)))


#funcao que calcula o numero medio de bits
def numMedBits(data):
    codec = hf.HuffmanCodec.from_data(data)
    t = codec.get_code_table()
    counts =  collections.Counter(data)
    num = 0
    
    for i in counts:
        #numero de ocorrencias * bitsize
        num+=counts[i]*t[i][0]
    return(num/len(data))


#função que calcula a variancia
def variancia(data):
    codec = hf.HuffmanCodec.from_data(data)
    t = codec.get_code_table()
    #ocorrencias
    counts = collections.Counter(data)
    var=0
    for i in counts:
        var+=counts[i]*(t[i][0]**2)
    var=var/len(data)-(numMedBits(data))**2
    return var


#função que calcula a entropia de 2 simbolos
def entropia2S(data):
    if len(data) <= 1:
        return 0
    counts = {}
    for j in range(1, len(data), 2):
        d = (data[j - 1], data[j])
        if d in counts:
            counts[d] += 1
        else:
            counts[d] = 1

    probs = [float(c) / (len(data) / 2) for c in counts.values()]
    ent = -sum(probs * np.log2(probs))
    return ent / 2


def getData(fich):
    fs, data = wavfile.read(fich)
    return data


def linearGraph(infoM, title):
    stepsN = np.arange(int(len(infoM)))
    plt.figure()
    plt.title(title)
    plt.plot(stepsN, infoM,stepsN, infoM,'.')
    plt.show()


def infoMutua(query, target, alfa, step):
    comp = len(query)
    ran = ((int)(((len(target)-comp)/step)) + 1)

    info = np.zeros(ran)

    index = 0
    
    for i in range(ran):
        
        infoM = 0

        matrizB = np.zeros((len(alfa), len(alfa)))
        probQuery = np.zeros(len(alfa))
        probSplitedTarget = np.zeros(len(alfa))
        splitedTarget = target[i*step:comp + (i*step)]

        for j in range(comp):
            #query corresponde às linhas da matriz
            matrizB[query[j], splitedTarget[j]] +=1
            probQuery[query[j]] += 1
            probSplitedTarget[splitedTarget[j]] +=1

        
        probQuery = probQuery / comp
        probSplitedTarget = probSplitedTarget / comp 
        matrizB = matrizB / comp

        for x in range(len(alfa)):
            for y in range(len(alfa)):
                if((probQuery[x]*probSplitedTarget[y] > 0) & (matrizB[x][y] > 0)):
                    infoM += ((matrizB[x][y]) * np.log2((matrizB[x][y])/(probQuery[x]*probSplitedTarget[y])))

        

        info[index] = infoM
        index +=1

    return info


def simulador(lista, query):
    evolucao = []
    qData = getData(query)
    for song in lista:
        target = getData(song)
        alfa = np.arange(256)
        infom = infoMutua(qData, target, alfa ,(int)(len(qData)/4))
        linearGraph(infom, song)
        evolucao.append(max(infom))

    linearGraph(evolucao, "Evolução")
    return evolucao

        
def main():
    sounds = ["Song01.wav", "Song02.wav", "Song03.wav", "Song04.wav", "Song05.wav", "Song06.wav", "Song07.wav"]
    sounds2 = ["target01 - repeat.wav", "target02 - repeatNoise.wav"]
    files = ["english.txt", "kid.bmp", "homer.bmp", "homerBin.bmp", "guitarSolo.wav"]

    for file in files:
        print(file)
        printInfo(file)
        makeHist(file)
        print('\n')

    simulador(sounds2, "guitarSolo.wav")
    evo = simulador(sounds, "guitarSolo.wav")
    evo = np.array(evo)
    print("Ranking (ordem decrescente):")
    for i in range(len(evo)):
        indx = np.argmax(evo)
        print(sounds[indx], evo[indx])
        evo[indx] = 0


if __name__ == "__main__":
    main()
