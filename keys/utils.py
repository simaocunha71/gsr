import sys
import re
import numpy as np

def rotate(line,n_times):
    """Função que devolve uma linha obtida por rodar os elementos de line para a direita n_times"""
    return line[-n_times:] + line[:-n_times]

#Teste da função rotate
#line, n_times = "012345",1
#line = rotate(line, n_times)
#print(line)

def transpose(line):
    """Função que dá a transposta de uma linha (em formato string ou em lista de listas de caracteres)"""
    """Adaptado de https://stackoverflow.com/questions/65759358/convert-a-python-list-of-lists-to-a-single-string (consultado em 22 abril 2023)"""
    if isinstance(line, list): #Linha é lista de listas de caracteres
        return "".join(["".join([str(item) for item in sublist]) for sublist in line])
    else: #Assume-se que a linha é string
        return [[char] for char in line]

#Testes da função transpose
#line1 = "012345"
#line1 = transpose(line1)
#print(line1)
#
#line2 = [['0'], ['1'], ['2'], ['3'], ['4'], ['5']]
#line2 = transpose(line2)
#print(line2)

def print_matrix(mat, legenda, key):
    """Função que imprime uma matrix"""
    print(legenda)
    print(f"chave=\"{key}\"")
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            print(mat[i][j], end=" ")
        print()
    print()


"""NOTE: Rascunho de funções - provavelmente nenhuma vai estar aqui"""

def get_timestamp():
    """ Manter um objeto de gestão que indique (em segundos) há quanto tempo o agente
iniciou/reiniciou a sua execução (timespamp S); """
    return "10 s"


def generate_matrix():
    """Usar a biblioteca numpy que cria matrizes a partir de strings e tem métodos para calcular transposta, etc"""
    """Método a ser inserido em /generation_management"""
    """incluir todos os caracteres ascii estendidos nas matrizes"""
    """(colocar seed para geração de matriz aleatoria ou colocar matriz fm)"""
    return np.matrix('1 2 3; 3 4 6; 7 8 9')


def update_matrix(intervalo, matrix):
    """Atualiza a matriz de "intervalo" em "intervalo" ms" """
    """Método a ser inserido em /generation_management"""
    print(intervalo)
    print(matrix)
    return np.matrix('1 2 3; 3 10 6; 7 8 9')


def generate_key():
    """Atender um pedido de geração duma chave enviado por uma aplicação e devolver o seu valor C e o seu identificador D; """
    """Método a ser inserido em /generation_management"""
    return "new key", "id"
