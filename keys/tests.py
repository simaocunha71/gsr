"""Módulo de testes das funções aplicadas às matrizes"""

import utils

########################################################################
print("######### Teste da função rotate #########")
line, n_times = "012345",1

print("line, n_times = \"012345\",1")
line = utils.rotate(line, n_times)
print("Esperado: " + "501234")
print("Obtido:   " + line)

########################################################################
print("######### Teste da função rotate_vertical #########")
line, n_times = [['0'], ['1'], ['2'], ['3'], ['4'], ['5']],1
print("line, n_times = [['0'], ['1'], ['2'], ['3'], ['4'], ['5']],1")
line = utils.rotate_vertical(line, n_times)
print("Esperado: " + "[['5'], ['0'], ['1'], ['2'], ['3'], ['4']]")
print("Obtido:   " + str(line))

########################################################################
print("######### Testes da função transpose #########")
print("> test 1")
line1 = "012345"
print("line1 = \"012345\"")
line1 = utils.transpose(line1)
print("Esperado: " + "[['0'], ['1'], ['2'], ['3'], ['4'], ['5']]")
print("Obtido:   " + str(line1))

print("> test 2")
line2 = [['0'], ['1'], ['2'], ['3'], ['4'], ['5']]
print("line2 = [['0'], ['1'], ['2'], ['3'], ['4'], ['5']]")
line2 = utils.transpose(line2)
print("Esperado: " + "012345")
print("Obtido:   " + str(line2))

########################################################################
print("######### Teste da função concat_ll #########")
print("> test 1")
m1 = [[1], [2], [3]]
m2 = [[4], [5], [6]]
print("m1 = [[1], [2], [3]]")
print("m2 = [[4], [5], [6]]")
m3 = utils.concat_ll(m1, m2)
print("Esperado: " + "[[1, 4], [2, 5], [3, 6]]")
print("Obtido:   " + str(m3))

print("> test 2")
m1 = []
m2 = [[1], [2], [3]]
print("m1 = []")
print("m2 = [[1], [2], [3]]")
m3 = utils.concat_ll(m1, m2)
print("Esperado: " + "[[1], [2], [3]]")
print("Obtido:   " + str(m3))

print("> test 3")
m1 = [[1], [2], [3]]
m2 = []
print("m1 = [[1], [2], [3]]")
print("m2 = []")
m3 = utils.concat_ll(m1, m2)
print("Esperado: " + "[[1], [2], [3]]")
print("Obtido:   " + str(m3))

print("> test 4")
m1 = []
m2 = []
print("m1 = [])")
print("m2 = [])")
m3 = utils.concat_ll(m1, m2)
print("Esperado: " + "[]")
print("Obtido:   " + str(m3))
print(m3)

########################################################################