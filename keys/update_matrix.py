import matrix, sys, utils, time
sys.path.append('../')
import model.configurations as configurations

def first_update_Z(n, Z):
    """Função que aplica a 1ª atualização da matriz Z de acordo com o enunciado"""
    for i in range(n):
        Z[i] = utils.rotate(Z[i], utils.create_random_number(0, n - 1, Z[i][0]))
        
def second_update_Z(n, Z):
    """Função que aplica a 2ª atualização da matriz Z de acordo com o enunciado"""
    for j in range(n):
        column = [row[j] for row in Z]  # obter a j-ésima coluna da matriz Z
        rotated_column = utils.rotate_vertical(column, utils.create_random_number(0, n - 1, column[0]))
        for i, row in enumerate(Z):
            row[j] = rotated_column[i]

def update_matrix_Z(n, Z, timestamp):
    """Função que aplica as duas atualizações à matriz Z de timestamp ms em timestamp ms"""
    #utils.print_matrix(Z, "Matriz Z Inicial")
    first_update_Z(n, Z)
    #utils.print_matrix(Z, "Matriz Z (1ª atualização)")
    second_update_Z(n, Z)
    #utils.print_matrix(Z, "Matriz Z (2ª atualização)")
    time.sleep(timestamp/1000)