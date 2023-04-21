import sys
import re
import np

def load_configurations(filename):
    """TODO: Ler do ficheiro "config.conf" e carregar para uma estrutura de dados (ou fica em tuplo, depois vê-se)"""
    print(filename)
    return (8,"default key", 5, 10, 8, 112)

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

