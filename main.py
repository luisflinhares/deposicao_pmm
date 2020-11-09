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

        # menor local ou valor igual a possível posição
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

        # maior local ou valor igual a possível posição
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


# ainda em desenvolvimento
def simulacao_da(tamanho_amostra, beta):
    arr = []
    for i in range(tamanho_amostra):
        arr.append(np.power(i, beta))

    return arr


# Cálculo da rugosidade. É determinado pelas fórmulas descritas no mestrado
# A rugosidade é determinada pelo desvio médio das alturas (parece bastante com o RMSE)
def rugosidade(deposicao):
    tamanho_deposicao = len(deposicao)
    # print(tamanho_amostra)
    erro = 0
    contador = 0
    media = altura_media(deposicao)
    for i in range(1, tamanho_deposicao):
        erro = erro + np.power((deposicao[i] - media), 2)
        contador = contador + 1

    # print(math.sqrt(erro/(tamanho_deposicao - 1)))
    return math.sqrt(erro / (tamanho_deposicao - 1))


# Altura média da deposição
def altura_media(deposicao):
    tamanho_deposicao = len(deposicao)
    soma = 0
    for i in range(1, tamanho_deposicao):
        soma = soma + deposicao[i]

    return soma / (tamanho_deposicao - 1)


# Criação de valores aleatórios
def lcg(modulo, a, b, aleatorio):
    num_aleatorio = (aleatorio * a + b) % modulo
    return num_aleatorio


# Criador da deposição.
# tipo_deposicao = 0 -> Deposição Aleatória
# tipo_deposicao = 1 -> Deposição Aleatória com Relaxação Superficial
# tipo_deposicao = 2 -> Deposição Balística
# l = tamanho da amostra
# tempo = sempre em 10^tempo

def do_deposicao(l=200, tempo=5, tipo_deposicao=0, grafico_instantaneo=False):

    tempo_instantaneo = 25
    max_tempo_instantaneo = 150
    amostras_independentes = 1

    if not grafico_instantaneo:
        # Mudar aqui a quantidade de amostras independentes
        amostras_independentes = np.power(1, 1)


    m = np.power(2, 31)
    a = 843314861
    b = 453816693
    deposicao = np.zeros(l + 1)


    # para executar a média das amostras
    l_rugosidade_total = []

    tempo_fim = np.power(10, tempo)
    semente = 0
    aleatorio = lcg(m, a, b, semente)

    for amostra in range(amostras_independentes):

        contador = 0
        contador_amostra = 0
        l_instantaneo = []
        l_rugosidade = []
        while (contador < tempo_fim):
            for i in range(l):
                x3 = (l - 1) / m * aleatorio + 1
                x3 = round(x3)
                x3 = int(x3)
                if tipo_deposicao == 1:
                    deposicao = do_relaxacao_superficial(deposicao, x3)
                elif tipo_deposicao == 2:
                    deposicao = do_deposicao_balistica(deposicao, x3)
                else:
                    deposicao[x3] = deposicao[x3] + 1

                aleatorio = lcg(m, a, b, aleatorio)

            if grafico_instantaneo:
                if contador_amostra == tempo_instantaneo and contador <= max_tempo_instantaneo:
                    l_instantaneo.append(deposicao.copy())
                    contador_amostra = 0

            l_rugosidade.append(deposicao.copy())

            contador = contador + 1
            contador_amostra = contador_amostra + 1

        l_rugosidade_total.append(l_rugosidade.copy())

    return l_instantaneo, l_rugosidade_total


def gera_grafico_instantaneo(l_instantaneo):
    plt.figure(figsize=(14, 5))

    tempo_instantaneo = 25
    tempo_instantaneo_count = tempo_instantaneo

    l_legenda = []
    for i in range(len(l_instantaneo)):
        grafico_al = []
        for j in range(1, len(l_instantaneo[i])):
            grafico_al.append(l_instantaneo[i][j])

        l_legenda.append('T = '+str(tempo_instantaneo_count))
        tempo_instantaneo_count = tempo_instantaneo_count + tempo_instantaneo
        plt.plot(grafico_al)

    plt.legend(l_legenda, bbox_to_anchor=(1, 1.02), loc="upper left")
    plt.show()

def gera_grafico_rugosidade(l_rugosidade):

    plt.figure(figsize=(14, 5))

    tempo = len(l_rugosidade[0])
    tamanho_substrato = len(l_rugosidade[0][0])
    qtd_amostras_independentes = len(l_rugosidade)
    l_rugosidade_media = []

    arr_rugosidade_media = np.zeros((tempo, (tamanho_substrato - 1)))
    for i in range(qtd_amostras_independentes):
        tempo = len(l_rugosidade[i])
        for j in range(tempo):
            substrato = l_rugosidade[i][j]
            for k in range(1, len(substrato)):
                arr_rugosidade_media[j][k - 1] = arr_rugosidade_media[j][k - 1] + substrato[k]/qtd_amostras_independentes


    for i in range(len(arr_rugosidade_media)):
        l_rugosidade_media.append(rugosidade(arr_rugosidade_media[i]))

    plt.xscale("log")
    plt.yscale("log")
    plt.plot(l_rugosidade_media)
    plt.legend(['L - '+str(tamanho_substrato - 1)])
    plt.show()

    return False


    #plt.show()


# Aleatória
grafico_da_instantaneo, grafico_da_rugosidade = do_deposicao(500, 3, 0, True)
gera_grafico_instantaneo(grafico_da_instantaneo)

# Relaxação Superficial
grafico_dars_instantaneo, grafico_dars_rugosidade  = do_deposicao(500, 3, 1, True)
gera_grafico_instantaneo(grafico_dars_instantaneo)

# Deposição Balística
grafico_db_instantaneo, grafico_db_rugosidade  = do_deposicao(500, 3, 2, True)
gera_grafico_instantaneo(grafico_db_instantaneo)

#Rugosidade com L = 200 e tempo = 10^2, DARS
grafico_dars_instantaneo, grafico_dars_rugosidade  = do_deposicao(200, 2, 1, False)
gera_grafico_rugosidade(grafico_dars_rugosidade)


# plt.xscale("log")
# plt.yscale("log")
# print(grafico_al_instantaneo[5])


# grafico_al_rugosidade = do_deposicao(100, 3, 0, False, True)
# Relaxação Superficial
# grafico_alrs = do_deposicao(200, 2, 1)
# Deposição Balística
# grafico_bl = do_deposicao(200, 2, 2)

# plt.figure(figsize=(14, 5))
# plt.xscale("log")
# plt.yscale("log")
# plt.plot(grafico_al)
# plt.plot(grafico_alrs)
# plt.plot(grafico_bl)
# plt.show()