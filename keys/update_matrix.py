import matrix, sys, utils
sys.path.append('../')
import model.configurations as configurations

#TODO: FIX MODULE!
def first_update_Z(n, Z):
    """Função que aplica a 1ª atualização da matriz Z de acordo com o enunciado"""
    Z_updated = []
    for i in range(n):
        Z_updated.append(list(utils.rotate(Z,utils.create_random_number(0,n-1,int(Z[i][0])))))
    return Z_updated

"""
PS C:\Users\utilizador\Desktop\gsr\keys> python .\update_matrix.py
Traceback (most recent call last):
  File "C:\Users\utilizador\Desktop\gsr\keys\update_matrix.py", line 22, in <module>
    Z = first_update_Z(c.n_matrix, Z)
  File "C:\Users\utilizador\Desktop\gsr\keys\update_matrix.py", line 10, in first_update_Z
    Z_updated.append(list(utils.rotate(Z,utils.create_random_number(0,n-1,int(Z[i][0])))))
ValueError: invalid literal for int() with base 10: 'd'
"""

def second_update_Z(n, Z):
    """Função que aplica a 2ª atualização da matriz Z de acordo com o enunciado"""
    for j in range(n):
        Z = utils.rotate_vertical(Z*j,utils.create_random_number(0,n-1,int(Z[0][j])))
    return Z

c = configurations.Configurations("../config.conf")
Z = matrix.get_matrix(c.n_matrix, c.master_key)
Z = first_update_Z(c.n_matrix, Z)
utils.print_matrix(Z, "Matriz Z (1ª atualização)")
Z = second_update_Z(c.n_matrix, Z)
utils.print_matrix(Z, "Matriz Z (2ª atualização)")