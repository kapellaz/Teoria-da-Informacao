import time
import gzip
import huffman
import bz2
import RLE
import MTF
import os
import io
import LZW
import BWT
from LZ77 import LZ77Compressor
import matplotlib.pyplot as plt
import numpy as np


def data(fich):
    with open(fich, "r") as fich:
        text = fich.read()
    return text

def intToString(l):
    s = ''
    for n in l:
        s += str(n)
    return s

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')



def gzipcompress(fich):
    print("Gzip compression")
    read = fich
    fich = fich[:-4] + "Compressed.txt"
    write = os.path.join("CompressionProject", "GZIP", fich)
    a = data(read)
    start = time.time()
    with gzip.open(write, "wb") as output:
            with io.TextIOWrapper(output, encoding='utf-8') as encode:
                encode.write(a)
    end = time.time()

    with gzip.open(write, 'rb') as ip:
        with io.TextIOWrapper(ip, encoding='utf-8') as decoder:
            # Let's read the content using read()
            content = decoder.read()
    print("{} seconds".format(end-start))
    print(f"The file {write} now contains {os.stat(write).st_size} bytes")
    print(f"The file {read} contains {os.stat(read).st_size} bytes")
    print("racio: {} (read/write)".format(os.stat(read).st_size/os.stat(write).st_size))
    print("\n")
    return os.stat(read).st_size/os.stat(write).st_size, end-start


def huffcompress(fich):
    print("Huffman compression")
    read = fich
    fich = fich[:-4] + "Compressed.txt"
    write = os.path.join("CompressionProject", "HUFFMAN", fich)
    d = data(read)
    start = time.time()
    encoding, tree = huffman.Huffman_Encoding(d)
    end = time.time()
    a = bitstring_to_bytes(encoding)
    with open(write , "wb") as f:
        f.write(a)
    print("{} seconds".format(end-start))
    print(f"The file {write} now contains {os.stat(write).st_size} bytes")
    print(f"The file {read} contains {os.stat(read).st_size} bytes")
    print("racio: {} (read/write)".format(os.stat(read).st_size/os.stat(write).st_size))
    print("\n")
    return os.stat(read).st_size/os.stat(write).st_size, end-start


def lzwComp(fich):
    print("LZW compression")
    read = fich
    fich = fich[:-4] + "Compressed.txt"
    write = write = os.path.join("CompressionProject", "LZW", fich)
    d = data(read)
    start = time.time()
    coded = LZW.LZWcompress(d)
    end = time.time()

    with open(write,"w") as f:
        for n in coded:
            f.write(str(n))
    print("{} seconds".format(end-start))
    print(f"The file {write} now contains {os.stat(write).st_size} bytes")
    print(f"The file {read} contains {os.stat(read).st_size} bytes")
    print("racio: {} (read/write)".format(os.stat(read).st_size/os.stat(write).st_size))
    print("\n")
    return os.stat(read).st_size/os.stat(write).st_size, end-start



def mtf_huff(fich):
    print("MTF+HUFF compression")
    read= fich
    fich = fich[:-4] + "Compressed.txt"
    write = write = os.path.join("CompressionProject", "MTF-HM", fich)
    d = data(read)
    start = time.time()
    mtf = intToString(MTF.encode(d))
    encoding, tree = huffman.Huffman_Encoding(mtf)
    end = time.time()
    print("time: {} seconds".format(end-start))
    a = bitstring_to_bytes(encoding)
    with open(write , "wb") as f:
        f.write(a)
    print("{} seconds".format(end-start))
    print(f"The file {write} now contains {os.stat(write).st_size} bytes")
    print(f"The file {read} contains {os.stat(read).st_size} bytes")
    print("racio: {} (read/write)".format(os.stat(read).st_size/os.stat(write).st_size))
    print("\n")
    return os.stat(read).st_size/os.stat(write).st_size, end-start


def bzip2compression(fich):
    print("Bzip2 compression")
    read= fich
    fich = fich[:-4] + "Compressed.txt"
    write = write = os.path.join("CompressionProject", "bzip2", fich)

    with open(read ,'rb') as f:
        start = time.time()
        tarbz2contents = bz2.compress(f.read(), 9)
        end = time.time()
    with open(write, "wb") as f:
        f.write(tarbz2contents)

    print("{} seconds".format(end-start))
    print(f"The file {write} now contains {os.stat(write).st_size} bytes")
    print(f"The file {read} contains {os.stat(read).st_size} bytes")
    print("racio: {} (read/write)".format(os.stat(read).st_size/os.stat(write).st_size))
    print("\n")
    return os.stat(read).st_size/os.stat(write).st_size, end-start
  

def lz77Compression(fich):
    print("LZ77 compression")
    read= fich
    fich = fich[:-4] + "Compressed.txt"
    write = write = os.path.join("CompressionProject", "LZ77", fich)
    compressor = LZ77Compressor(window_size=20)
    start = time.time()
    compressor.compress(read, write)
    end = time.time()

    print("{} seconds".format(end-start))
    print(f"The file {write} now contains {os.stat(write).st_size} bytes")
    print(f"The file {read} contains {os.stat(read).st_size} bytes")
    print("racio: {} (read/write)".format(os.stat(read).st_size/os.stat(write).st_size))
    print("\n")
    return os.stat(read).st_size/os.stat(write).st_size, end-start



def bwt_rle(fich):
    print("BTW + RLE compression")
    read = fich
    fich = fich[:-4] + "Compressed.txt"
    write = write = os.path.join("CompressionProject", "bwtrle", fich)

    texto = data(read)

    start = time.time()
    with open(write, "w") as f:
        f.close
    for i in range(0,len(texto),5000):#divisão em Blocos
        bwttry=BWT.bwt_tranf(texto[i-5000:i])
        new_data = RLE.rle_encode(bwttry)
        with open(write,"a+") as f:
            for n in new_data:
                f.write(str(n))
    end = time.time()
    print("{} seconds".format(end-start))
    print(f"The file {write} now contains {os.stat(write).st_size} bytes")
    print(f"The file {read} contains {os.stat(read).st_size} bytes")
    print("racio: {} (read/write)".format(os.stat(read).st_size/os.stat(write).st_size))
    print("\n")
    return os.stat(read).st_size/os.stat(write).st_size, end-start



def graficoBarras(gzip,huffman,bzip2,lzw,mtf_huffan,lz77, bwt_rle,tipo):
    barWidth = 0.10
    
    plt.figure(figsize=(10,5))
    r1 = np.arange(len(gzip))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]
    r5 = [x + barWidth for x in r4]
    r6 = [x + barWidth for x in r5]
    r7 = [x + barWidth for x in r6]


    plt.bar(r1,gzip,color='yellow',width=barWidth,label = 'gzip')
    plt.bar(r2,huffman,color='blue',width=barWidth,label = 'huffman')
    plt.bar(r3, bzip2, color='black', width=barWidth, label='bzip2')
    plt.bar(r4, lzw, color='red', width=barWidth, label='lzw')
    plt.bar(r5, mtf_huffan, color='green', width=barWidth, label='mtf_huffman')
    plt.bar(r6, lz77, color='pink', width=barWidth, label='lz77')
    plt.bar(r7, bwt_rle, color='orange', width=barWidth, label='bwt_rle')


    plt.xlabel('Ficheiros')
    plt.xticks([r + barWidth*2 for r in range(len(bwt_rle))],['finance.csv','Bible.txt','random.txt','jquery-3.6.0.js'])
    plt.ylabel(tipo +' de Compressão')
    plt.title('Representação do '+tipo+' de compressão para os métodos envolvidos')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    ficheiros = ["finance.csv", "bible.txt", "random.txt", "jquery-3.6.0.js"]
    listaraciogzip = []
    listaTempogzip = []
    listaraciohuffman = []
    listaTempohuffman = []
    listaraciolzw = []
    listaTempolzw = []
    listaraciomtf_hf = []
    listaTempomtf_hf = []
    listaraciobzip2 = []
    listaTempobzip2 = []
    listaraciolz77 = []
    listaTempolz77 = []
    listaraciobwtrle = []
    listaTempobwtrle = []
    for fich in ficheiros:
        print("Compressão para "+fich)
        a, b = gzipcompress(fich)
        c, d = huffcompress(fich)
        e, f = lzwComp(fich)
        g, h = mtf_huff(fich)
        i, j = bzip2compression(fich)
        k, l = lz77Compression(fich)
        m, n = bwt_rle(fich)

        listaraciogzip.append(a)
        listaTempogzip.append(b)
        listaraciohuffman.append(c)
        listaTempohuffman.append(d)
        listaraciolzw.append(e)
        listaTempolzw.append(f)
        listaraciomtf_hf.append(g)
        listaTempomtf_hf.append(h)
        listaraciobzip2.append(i)
        listaTempobzip2.append(j)
        listaraciolz77.append(k)
        listaTempolz77.append(l)
        listaraciobwtrle.append(m)
        listaTempobwtrle.append(n)
        print("\n")

    graficoBarras(listaraciogzip, listaraciohuffman, listaraciobzip2, listaraciolzw, listaraciomtf_hf, listaraciolz77, listaraciobwtrle, "racio")
    graficoBarras(listaTempogzip, listaTempohuffman, listaTempobzip2, listaTempolzw, listaTempomtf_hf,listaTempolz77, listaTempobwtrle, "tempo")

    