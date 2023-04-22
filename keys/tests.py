import utils

########################################################################
print("######### Teste da função rotate #########")
line, n_times = "012345",1
line = utils.rotate(line, n_times)
print("Esperado: " + "501234")
print("Obtido: " + line)

########################################################################
print("######### Testes da função transpose #########")
print("> test 1")
line1 = "012345"
line1 = utils.transpose(line1)
print("Esperado: " + "[['0'], ['1'], ['2'], ['3'], ['4'], ['5']]")
print("Obtido:   " + str(line1))

print("> test 2")
line2 = [['0'], ['1'], ['2'], ['3'], ['4'], ['5']]
line2 = utils.transpose(line2)
print("Esperado: " + "012345")
print("Obtido:   " + str(line2))

########################################################################
print("######### Teste da função concat_ll #########")
print("> test 1")
m1 = [[1], [2], [3]]
m2 = [[4], [5], [6]]
m3 = utils.concat_ll(m1, m2)
print("Esperado: " + "[[1, 4], [2, 5], [3, 6]]")
print("Obtido:   " + str(m3))

print("> test 2")
m1 = []
m2 = [[1], [2], [3]]
m3 = utils.concat_ll(m1, m2)
print("Esperado: " + "[[1], [2], [3]]")
print("Obtido:   " + str(m3))

print("> test 3")
m1 = [[1], [2], [3]]
m2 = []
m3 = utils.concat_ll(m1, m2)
print("Esperado: " + "[[1], [2], [3]]")
print("Obtido:   " + str(m3))

print("> test 4")
m1 = []
m2 = []
m3 = utils.concat_ll(m1, m2)
print("Esperado: " + "[]")
print("Obtido:   " + str(m3))
print(m3)

########################################################################