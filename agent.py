import model.configurations as configurations
import MIB.mib as mib
import keys.main as keygen
import keys.matrix as matrix
#TODO: Escrever os outros imports
import time

def get_timestamp(current_time):
    """Devolve o timestamp S sempre que se chama esta função - nº de segundos passados em que o agente iniciou/reiniciou"""
    return int(time.time() - float(current_time))
    

n_updated_times = 0

if __name__ == "__main__":
    F = configurations.Configurations("config.conf")
    current_time = time.time()
    #S = get_timestamp(current_time)
    fm_matrix = utils.create_fm_matrix()
    Z = matrix.get_matrix(c.n_matrix, c.master_key, fm_matrix, S) #NOTE: Este S para já vai forma a matriz Zs com elementos todos iguais, mas no programa final vai gerar matrizes Zs todas diferentes por causa do timestamp S ser sempre diferente
    while (True):
        update_matrix.update_matrix_Z(c.n_matrix, Z, c.update_interval)
        line_index, col_index = utils.get_random_indexes(
            n_updated_times, Z, c.n_matrix)
        key = generate_key(Z, line_index, col_index, fm_matrix, get_timestamp(current_time))
        print(f"Got key \"{key}\"")
        n_updated_times += 1