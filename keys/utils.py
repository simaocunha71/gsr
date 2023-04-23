import random

def rotate(line,n_times):
    """Função que devolve uma linha obtida por rodar os elementos de line para a direita n_times"""
    return line[-n_times:] + line[:-n_times]

def rotate_vertical(column,n_times):
    """Função que devolve uma coluna obtida por rodar os elementos de line_list para a direita n_times"""
    return column[-n_times:] + column[:-n_times]

def transpose(line):
    """Função que dá a transposta de uma linha (em formato string ou em lista de listas de caracteres)"""
    if isinstance(line, list): #Linha é lista de listas de caracteres
        return "".join(["".join([str(item) for item in sublist]) for sublist in line])
    else: #Assume-se que a linha é string
        return [[char] for char in line]

def concat_ll(mat1,mat2):
    """Função que concatena listas de listas numa só lista de listas"""
    if not mat1 and not mat2:
        return []
    elif not mat1:
        return mat2
    elif not mat2:
        return mat1
    else:
        result = []
        for i in range(len(mat1)):
            result.append(mat1[i] + mat2[i])
        return result
    
def print_matrix(mat, legenda, key=None):
    """Função que imprime uma matriz"""
    print(legenda)
    if key is not None:
        print(f"sequencia=\"{key}\"")
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            print(mat[i][j], end=" ")
        print()
    print()

def create_random_number(min,max,seed):
    """Função que cria um inteiro aleatorio com uma determinada seed no intervalo [min,max]"""
    random.seed(seed) 
    return random.randint(min, max)

def get_random_indexes(n_updated_times, Z, n):
    """Função que devolve os indices aleatorios para o cálculo da chave"""
    i = create_random_number(0, n - 1, n_updated_times + int(Z[0][0])) #Correto
    j = create_random_number(0, n - 1, int(Z[i][0])) #TODO: FIX!
    print("i " + str(i))
    print("j " + str(j))
    return i,j
