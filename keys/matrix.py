"""Gera matrizes e chaves e atualiza matrizes"""
import sys
sys.path.append('../')
import model.configurations as configurations
import utils
import numpy as np

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

def create_matrix_Zc(n, Za):
    """Devolve a matriz Zc (de tamanho n) com recurso à matriz Za"""
    Zc = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            Zc[i][j] = utils.create_random_number(0, 255, Za[i][j])
    return Zc


def create_matrix_Zd(n, Zb):
    """Devolve a matriz Zd (de tamanho n) com recurso à matriz Zb"""
    Zd = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            Zd[i][j] = utils.create_random_number(0,255,Zb[i][j])
    return Zd

def create_matrix_Z(n,Za,Zb,Zc,Zd):
    pass

c = configurations.Configurations("../config.conf")
m1,m2 = create_m1_m2(c.n_matrix, c.master_key)

Za = create_matrix_Za(c.n_matrix, m1)
utils.print_matrix(Za, "Matriz Za", m1)

Zb = create_matrix_Zb(c.n_matrix, m2)
utils.print_matrix(Zb, "Matriz Zb", m2)

Zc = create_matrix_Zc(c.n_matrix, Za)
utils.print_matrix(Zc, "Matriz Zc")

Zd = create_matrix_Zd(c.n_matrix, Zb)
utils.print_matrix(Zd, "Matriz Zd")

Z = create_matrix_Z(c.n_matrix, Za, Zb, Zc, Zd)
utils.print_matrix(Z, "Matriz Zd")