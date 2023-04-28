"""Módulo que implementa o agente"""

import model.configurations as configurations
import MIB.mib as mib
import keys.main as keygen
import keys.matrix as matrix
import keys.update_matrix as update_matrix
import keys.utils as utils
import time

def get_timestamp(current_time):
    """Devolve o timestamp S sempre que se chama esta função - nº de segundos passados em que o agente iniciou/reiniciou"""
    return int(time.time() - float(current_time))
    

n_updated_times = 0

if __name__ == "__main__":
    F = configurations.Configurations("config.conf")
    current_time = time.time()
    S = get_timestamp(current_time) #NOTE: Está sempre com o mesmo valor, mas no futuro vai variando (ver NOTE abaixo)
    fm_matrix = utils.create_fm_matrix()
    Z = matrix.get_matrix(F.n_matrix, F.master_key, fm_matrix, S) #NOTE: Este S para já vai forma a matriz Zs com elementos todos iguais, mas no programa final vai gerar matrizes Zs todas diferentes por causa do timestamp S ser sempre diferente
    while (True):
        update_matrix.update_matrix_Z(F.n_matrix, Z, F.update_interval)
        line_index, col_index = utils.get_random_indexes(
            n_updated_times, Z, F.n_matrix)
        key = keygen.generate_key(Z, line_index, col_index, fm_matrix)
        print(f"Got key \"{key}\"")
        n_updated_times += 1