import numpy as np
from numpy import random
import time
import matplotlib.pyplot as plt
import math


# Algoritmo que faz a relaxaçao superficial
# E usado junto da deposicao aleatoria, para atingir o ponto de rugosidade
def do_relaxacao_superficial(deposicao, posicao):

    maior = len(deposicao) - 1
    menor = 1

    if posicao != maior and posicao != menor:
        if deposicao[posicao + 1] > deposicao[posicao - 1]:
            possivel_posicao = posicao - 1
        else:
            possivel_posicao = posicao + 1

        #menor local ou valor igual a possível posição
        if deposicao[posicao] <= deposicao[possivel_posicao]:
            deposicao[posicao] = deposicao[posicao] + 1
        else:
            deposicao[possivel_posicao] = deposicao[possivel_posicao] + 1
    else:
        if posicao == maior:
            possivel_posicao = posicao - 1
        else:
            possivel_posicao = posicao + 1

        if deposicao[posicao] <= deposicao[possivel_posicao]:
            deposicao[posicao] = deposicao[posicao] + 1
        else:
            deposicao[possivel_posicao] = deposicao[possivel_posicao] + 1

    return deposicao

# Algoritmo que faz a deposicao balistica
# E usado junto da deposicao aleatoria, para atingir o ponto de rugosidade
def do_deposicao_balistica(deposicao, posicao):

    maior = len(deposicao) - 1
    menor = 1

    if posicao != maior and posicao != menor:
        if deposicao[posicao + 1] < deposicao[posicao - 1]:
            posicao_maior_igual = posicao - 1
        else:
            posicao_maior_igual = posicao + 1

        #maior local ou valor igual a possível posição
        if deposicao[posicao] >= deposicao[posicao_maior_igual]:
            deposicao[posicao] = deposicao[posicao] + 1
        else:
            deposicao[posicao] = deposicao[posicao_maior_igual]
    else:
        if posicao == maior:
            posicao_maior_igual = posicao - 1
        else:
            posicao_maior_igual = posicao + 1

        if deposicao[posicao] >= deposicao[posicao_maior_igual]:
            deposicao[posicao] = deposicao[posicao] + 1
        else:
            deposicao[posicao] = deposicao[posicao_maior_igual]

    return deposicao


#ainda em desenvolvimento
def simulacao_da(tamanho_amostra, beta):

    arr = []
    for i in range(tamanho_amostra):
        arr.append(np.power(i, beta))

    return arr

# Cálculo da rugosidade. É determinado pelas fórmulas descritas no mestrado
# A rugosidade é determinada pelo desvio médio das alturas (parece bastante com o RMSE)
def rugosidade(deposicao):

    tamanho_deposicao = len(deposicao)
    #print(tamanho_amostra)
    erro = 0
    contador = 0
    media = altura_media(deposicao)
    for i in range(1, tamanho_deposicao):
        erro = erro + np.power((deposicao[i] - media), 2)
        contador = contador + 1

    #print(math.sqrt(erro/(tamanho_deposicao - 1)))
    return math.sqrt(erro/(tamanho_deposicao - 1))

#Altura média da deposição
def altura_media(deposicao):

    tamanho_deposicao = len(deposicao)
    soma = 0
    for i in range(1, tamanho_deposicao):
        soma = soma + deposicao[i]

    return soma/(tamanho_deposicao - 1)


# Criação de valores aleatórios
def lcg(modulo, a, b, aleatorio):
    num_aleatorio = (aleatorio * a + b) % modulo
    return num_aleatorio

#Criador da deposição.
# tipo_deposicao = 0 -> Deposição Aleatória
# tipo_deposicao = 1 -> Deposição Aleatória com Relaxação Superficial
# tipo_deposicao = 2 -> Deposição Balística
# l = tamanho da amostra
# tempo = sempre em 10^tempo

def do_deposicao(l=200, tempo=5, tipo_deposicao = 0):

    m = np.power(2, 31)
    a = 843314861
    b = 453816693
    deposicao = np.zeros(l+1)
    tempo_fim = np.power(10, tempo)
    semente = 0
    aleatorio = lcg(m, a, b, semente)

    contador = 0
    arr_grafico = []
    while(contador < tempo_fim):
        for i in range(l):
            x3 = (l - 1) / m * aleatorio + 1
            x3 = round(x3)
            if tipo_deposicao == 1:
                deposicao = do_relaxacao_superficial(deposicao, x3)
            elif tipo_deposicao == 2:
                deposicao = do_deposicao_balistica(deposicao, x3)
            else:
                deposicao[x3] = deposicao[x3] + 1

            aleatorio = lcg(m, a, b, aleatorio)

        arr_grafico.append(rugosidade(deposicao))
        contador = contador+1

    return arr_grafico




#Aleatória
grafico_al = do_deposicao(100, 2, 0)
#Relaxação Superficial
grafico_alrs = do_deposicao(200, 4, 1)
#Deposição Balística
grafico_bl = do_deposicao(300, 4, 2)

plt.figure(figsize=(14, 5))
plt.xscale("log")
plt.yscale("log")
plt.plot(grafico_al)
plt.plot(grafico_alrs)
plt.plot(grafico_bl)
plt.show()

















