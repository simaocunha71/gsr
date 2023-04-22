import random

def rotate(line,n_times):
    """Função que devolve uma linha obtida por rodar os elementos de line para a direita n_times"""
    return line[-n_times:] + line[:-n_times]

def rotate_vertical(line_list,n_times):
    """Função que devolve uma coluna obtida por rodar os elementos de line_list para a direita n_times"""
    for _ in range(n_times):
        last_item = line_list.pop()
        line_list.insert(0, last_item)
    return line_list

def transpose(line):
    """Função que dá a transposta de uma linha (em formato string ou em lista de listas de caracteres)"""
    """Adaptado de https://stackoverflow.com/questions/65759358/convert-a-python-list-of-lists-to-a-single-string (consultado em 22 abril 2023)"""
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

def fm(Za, Zb, Zc, Zd):
    """Função que aplica a função fm a quatro valores inteiros"""
    """TODO: Mudar a implementação desta função"""
    return 0