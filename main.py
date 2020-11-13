import numpy as np
from numpy import random
import time
import matplotlib.pyplot as plt
import math
import csv





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
    media = altura_media(deposicao)
    for i in range(1, tamanho_deposicao):
        erro = erro + np.power((deposicao[i] - media), 2)

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

def do_deposicao(l=200, tempo_fim = 0, tipo_deposicao=0, grafico_instantaneo=False, aleatorio=0):

    tempo_instantaneo = 25
    max_tempo_instantaneo = 150

    m = np.power(2, 31)
    a = 843314861
    b = 453816693
    #aleatorio = lcg(m, a, b, aleatorio)

    amostras_independentes = 1

    l_instantaneo = []

    deposicao = np.zeros(l + 1)
    #l_deposicao_amostra_individual = np.zeros((tempo_fim, l + 1), dtype='uint8')
    l_deposicao_amostra_individual = []
    contador = 0
    contador_amostra = 0

    for tf in range(tempo_fim):
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
            if contador_amostra == tempo_instantaneo and tf <= max_tempo_instantaneo:
                l_instantaneo.append(deposicao.copy())
                contador_amostra = 0

        l_deposicao_amostra_individual.append(deposicao.copy())

        #contador = contador + 1
        contador_amostra = contador_amostra + 1

    """
        #média entre as amostras
        for temp in range(len(l_deposicao_amostra_individual)):
            tamanho_deposicao = len(l_deposicao_amostra_individual[temp])
            for dep in range(1, tamanho_deposicao):
                arr_amostras_media[temp][dep - 1] = arr_amostras_media[temp][dep - 1] + (l_deposicao_amostra_individual[temp][dep]/amostras_independentes)

    for med in range(len(arr_amostras_media)):
        l_rugosidade.append(rugosidade(arr_amostras_media[med]))    
    """
    return l_instantaneo, l_deposicao_amostra_individual, aleatorio


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


def rugosidade_media_amostras(l_rugosidade):

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

    return l_rugosidade_media


def cria_csv(arr_amostras_media, tipo_deposicao):

    l_rugosidade = []
    for i in range(len(arr_amostras_media)):
        l_rugosidade.append(rugosidade(arr_amostras_media[i]))

    titulo_csv = 'rugosidade_'+tipo_deposicao

    with open(titulo_csv+'.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for j in range(len(l_rugosidade)):
            spamwriter.writerow([j + 1, l_rugosidade[j]])


def gera_grafico_rugosidade(pasta_tipo_rugosidade, str_deposicao):

    plt.figure(figsize=(14, 5))

    l_deposicao = []
    l_deposicao.append(200)
    #l_deposicao.append(400)
    #l_deposicao.append(800)
    #l_deposicao.append(1600)

    l_legenda = []
    l_legenda.append('L = 200')
    l_legenda.append('L = 400')
    l_legenda.append('L = 800')
    l_legenda.append('L = 1600')


    for i in range(len(l_deposicao)):

        deposicao = l_deposicao[i]
        l_deposicao_grafico = []

        with open('./'+str_deposicao+'_'+str(deposicao)+'.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                l_deposicao_grafico.append(float(row[1]))

        plt.plot(l_deposicao_grafico.copy())

    plt.xscale("log")
    plt.yscale("log")
    plt.legend(l_legenda, bbox_to_anchor=(1, 1.02), loc="upper left")

    plt.show()

def media_amostras(l_deposito, arr_amostras_media, amostras_independentes):
    for tempo in range((len(l_deposito))):
        for dep in range(1, len(l_deposito[tempo])):
            arr_amostras_media[tempo][dep - 1] = arr_amostras_media[tempo][dep - 1] + (
                    l_deposito[tempo][dep] / amostras_independentes)


    return arr_amostras_media




#amostas independentes. Para 1000 amostras, basta elevar 10^3
amostras_independentes = int(np.power(1, 3))

#Tempo de cada substrato
tempo_1600 = np.power(10, 6)
tempo_800 = np.power(10, 5)
tempo_400 = np.power(10, 5)
tempo_200 = 11500


l_1600 = 1600
l_800 = 800
l_400 = 400
l_200 = 200

arr_amostras_media_1600 = np.zeros((tempo_1600, l_1600), dtype='f2')
arr_amostras_media_800 = np.zeros((tempo_800, l_800), dtype='f2')
arr_amostras_media_400 = np.zeros((tempo_400, l_400), dtype='f2')
arr_amostras_media_200 = np.zeros((tempo_200, l_200), dtype='f2')

m = np.power(2, 31)
a = 843314861
b = 453816693
aleatorio = lcg(m, a, b, 0)

#NA FUNÇÃO DA_DEPOSICAO, O 3º PARÃMETRO É O TIPO DE DEPOSICAO. 0 = ALEATÓRIA, 1 = DARS, 2 = DB
for i in range(amostras_independentes):

    """
    print(str(i)+' amostra 1600')

    l_da_instantaneo, l_da_deposito, aleatorio = do_deposicao(l_1600, tempo_1600, 1, False, aleatorio)
    arr_amostras_media_1600 = media_amostras(l_da_deposito, arr_amostras_media_1600, amostras_independentes)

    print(str(i)+' amostra 800')

    l_da_instantaneo = None
    l_da_deposito = None
    l_da_instantaneo, l_da_deposito, aleatorio = do_deposicao(l_800, tempo_800, 1, False, aleatorio)
    arr_amostras_media_800 = media_amostras(l_da_deposito, arr_amostras_media_800, amostras_independentes)

    print(str(i)+' amostra 400')

    l_da_instantaneo = None
    l_da_deposito = None
    l_da_instantaneo, l_da_deposito, aleatorio = do_deposicao(l_400, tempo_400, 1, False, aleatorio)
    arr_amostras_media_400 = media_amostras(l_da_deposito, arr_amostras_media_400, amostras_independentes)
    """

    print(str(i)+' amostra 200')

    l_da_instantaneo = None
    l_da_deposito = None
    l_da_instantaneo, l_da_deposito, aleatorio = do_deposicao(l_200, tempo_200, 1, False, aleatorio)
    arr_amostras_media_200 = media_amostras(l_da_deposito, arr_amostras_media_200, amostras_independentes)


#GERA TODOS OS CSVS

#cria_csv(arr_amostras_media_1600, 'DEPOSICAO_ALEATORIA_RELAXACAO_SUPERFICIAL_1600')
#cria_csv(arr_amostras_media_800, 'DEPOSICAO_ALEATORIA_RELAXACAO_SUPERFICIAL_800')
#cria_csv(arr_amostras_media_400, 'DEPOSICAO_ALEATORIA_RELAXACAO_SUPERFICIAL_400')
cria_csv(arr_amostras_media_200, 'DEPOSICAO_ALEATORIA_RELAXACAO_SUPERFICIAL_200')



gera_grafico_rugosidade('', 'rugosidade_DEPOSICAO_ALEATORIA_RELAXACAO_SUPERFICIAL')


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