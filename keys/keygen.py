import utils, sys
import update_matrix, matrix
sys.path.append('../')
import model.configurations as configurations

n_updated_times = 0

def generate_key(Z, line, col):
    row1 = Z[line]
    row2 = [row[col] for row in Z]

    row1_int = [int(c) for c in row1]
    row2_int = [int(c) for c in row2]

    result_int = [row1_int[k] ^ row2_int[k] for k in range(len(row1_int))]

    result_ascii = [chr(i) for i in result_int]

    return ''.join(result_ascii)


c = configurations.Configurations("../config.conf")
Z = matrix.get_matrix(c.n_matrix, c.master_key)

while(True):
    update_matrix.update_matrix_Z(c.n_matrix, Z, c.update_interval)
    line_index, col_index = utils.get_random_indexes(n_updated_times, Z, c.n_matrix)
    key = generate_key(Z, line_index, col_index)
    print(f"Got key \"{key}\"")
    n_updated_times += 1