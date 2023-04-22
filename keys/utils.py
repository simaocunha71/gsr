import numpy as np
import random

def rotate(line,n_times):
    """Função que devolve uma linha obtida por rodar os elementos de line para a direita n_times"""
    return line[-n_times:] + line[:-n_times]


def transpose(line):
    """Função que dá a transposta de uma linha (em formato string ou em lista de listas de caracteres)"""
    """Adaptado de https://stackoverflow.com/questions/65759358/convert-a-python-list-of-lists-to-a-single-string (consultado em 22 abril 2023)"""
    if isinstance(line, list): #Linha é lista de listas de caracteres
        return "".join(["".join([str(item) for item in sublist]) for sublist in line])
    else: #Assume-se que a linha é string
        return [[char] for char in line]

def concat_ll(mat1,mat2):
    """Função que concatena listas de listas numa só lista de listas"""
    if not mat1 and not mat2:
        return []
    elif not mat1:
        return mat2
    elif not mat2:
        return mat1
    else:
        result = []
        for i in range(len(mat1)):
            result.append(mat1[i] + mat2[i])
        return result
    

def print_matrix(mat, legenda, key=None):
    """Função que imprime uma matriz"""
    print(legenda)
    if key is not None:
        print(f"sequencia=\"{key}\"")
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            print(mat[i][j], end=" ")
        print()
    print()


def create_random_number(min,max,seed):
    """Função que cria um inteiro aleatorio com uma determinada seed no intervalo [min,max]"""
    random.seed(seed) 
    return random.randint(min, max) 

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
