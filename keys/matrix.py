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
    Zb = []
    for i in range(n):
        if i == 0:
            Zb = utils.concat_ll(Zb, utils.transpose(list(m2)))
        else:
            rotated_M2 = utils.rotate(m2, i)
            Zb = utils.concat_ll(Zb, rotated_M2)
    return Zb

def create_matrix_Zs(n):
    """Devolve a matriz Zs (de tamanho n) com recurso ao valor K do ficheiro de configuração (que é o n, neste caso)"""
    Zs = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            Zs[i][j] = utils.create_random_number(0, 255, n)
    return Zs


#def create_matrix_Zc(n, Za):
#    """INUTILIZADO: Devolve a matriz Zc (de tamanho n) com recurso à matriz Za"""
#    Zc = [[0]*n for _ in range(n)]
#    for i in range(n):
#        for j in range(n):
#            Zc[i][j] = utils.create_random_number(0, 255, Za[i][j])
#    return Zc
#
#def create_matrix_Zd(n, Zb):
#    """INUTILIZADO: Devolve a matriz Zd (de tamanho n) com recurso à matriz Zb"""
#    Zd = [[0]*n for _ in range(n)]
#    for i in range(n):
#        for j in range(n):
#            Zd[i][j] = utils.create_random_number(0,255,Zb[i][j])
#    return Zd

def create_matrix_Z(n,Za,Zb,Zs,fm):
    """Devolve a matriz Z (de tamanho n) com recurso às matrizes Za, Zb, Zs e fm"""
    Z = []
    for i in range(n):
        row = []
        for j in range(n):
            line_index = int(utils.get_element_from_fm(fm, Za[i][j],Zb[i][j]))
            col_index = int(Zs[i][j])
            row.append(utils.get_element_from_fm(fm, line_index, col_index))
        Z.append(row)
    return Z




def get_matrix(n,master_key, fm_matrix):
    """Função principal deste módulo que devolve a matriz Z a partir do valor n e da master_key do ficheiro de configuração"""
    m1,m2 = create_m1_m2(n, master_key)
    Za = create_matrix_Za(n, m1)
    Zb = create_matrix_Zb(n, m2)
    Zs = create_matrix_Zs(n)
    #Zc = create_matrix_Zc(n, Za)
    #Zd = create_matrix_Zd(n, Zb)
    Z = create_matrix_Z(n, Za, Zb, Zs, fm_matrix)

    #utils.print_matrix(Za, "Matriz Za", m1)
    #utils.print_matrix(Zb, "Matriz Zb", m2)
    #utils.print_matrix(Zs, "Matriz Zs")
    #utils.print_matrix(fm_matrix, "Matriz fm")
    #utils.print_matrix(Z, "Matriz Z")
    return Z

#Eliminar este codigo quando a matriz Z tiver a implementação correta
#c = configurations.Configurations("../config.conf")
#fm_matrix = utils.create_fm_matrix()
#get_matrix(c.n_matrix, c.master_key, fm_matrix)