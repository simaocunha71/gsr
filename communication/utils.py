def parse_version_numbers(version_string):
    """Função que, dada uma string do tipo "3.2.1", devolve a lista [3,2,1]"""
    version_numbers = list(map(int, version_string.split(".")))
    return version_numbers