"""Gera matrizes e chaves e atualiza matrizes"""
import sys
sys.path.append('../')
import model.configurations as configurations
import utils

def create_m1_m2(n,master_key):
    """Devolve m1 que contém os primeiros n bytes e m2 que contém os ultimos n bytes"""
    m1 = master_key[:n]
    m2 = master_key[n:]
    return m1,m2

def create_matrix_Za(n,m1):
    """Devolve a matriz Za (de tamanho n) com recurso às sequências de bytes M1"""
    Za = []
    for i in range(n):
        if i == 0:
            Za.append(list(m1))
        else:
            rotated_M1 = utils.rotate(m1, i)
            Za.append(list(rotated_M1))
    return Za


def create_matrix_Zb(n, m2):
    """Devolve a matriz Zb (de tamanho n) com recurso às sequências de bytes M2"""
    Zb_transposed = utils.transpose(m2)
    Zb = []
    for i in range(n):
        #Do something: TODO
    return Zb




c = configurations.Configurations("../config.conf")
m1,m2 = create_m1_m2(c.n_matrix, c.master_key)

Za = create_matrix_Za(c.n_matrix, m1)
utils.print_matrix(Za, "Matriz Za", m1)

Zb = create_matrix_Zb(c.n_matrix, m2)
utils.print_matrix(Zb, "Matriz Zb", m2)