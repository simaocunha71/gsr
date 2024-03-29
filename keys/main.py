"""Módulo de geração de chaves"""

import keys.utils as utils
import sys
sys.path.append('../')


def generate_key(Z, line, col, fm_matrix):
    """Função que gera uma chave de comprimento K, usando a matriz Z, indices line e col escolhidos aleatoriamente e a matriz fm"""
    """Exempo de chave: "1 bdsahhaid#%i"""
    row1 = Z[line]
    row2 = [row[col] for row in Z]

    key = []
    for i in range(len(row1)):
        key.append(utils.get_element_from_fm(fm_matrix, int(row1[i]), int(row2[i])))

    result_ascii = [chr(i) for i in key]

    return ''.join(result_ascii)