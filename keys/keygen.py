"""Módulo de geração de chaves"""

import utils, sys
import update_matrix, matrix
sys.path.append('../')
import model.configurations as configurations

n_updated_times = 0

def generate_key(Z, line, col, fm_matrix):
    """Função que gera uma chave de comprimento K, usando a matriz Z, indices line e col escolhidos aleatoriamente e a matriz fm"""
    row1 = Z[line]
    row2 = [row[col] for row in Z]

    #row1_int = [int(c) for c in row1]
    #row2_int = [int(c) for c in row2]

    key = []
    for i in range(len(row1)):
        key.append(utils.get_element_from_fm(fm_matrix, int(row1[i]), int(row2[i])))

    result_ascii = [chr(i) for i in key]

    return ''.join(result_ascii)



c = configurations.Configurations("../config.conf")
fm_matrix = utils.create_fm_matrix()
Z = matrix.get_matrix(c.n_matrix, c.master_key, fm_matrix)
fm_matrix = utils.create_fm_matrix()

while(True):
    update_matrix.update_matrix_Z(c.n_matrix, Z, c.update_interval)
    line_index, col_index = utils.get_random_indexes(n_updated_times, Z, c.n_matrix)
    key = generate_key(Z, line_index, col_index, fm_matrix)
    print(f"Got key \"{key}\"")
    n_updated_times += 1