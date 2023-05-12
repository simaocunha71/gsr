"""Classe que cria contém todos os objetos do grupo Keys da MIB"""
import object as obj
import re

"""
TODO:
- criar objetos dataNumberOfValidKeys, dataTableGeneratedKeys, dataTableGeneratedKeysEntry
- dataTableGeneratedKeys vai conter, alem dos parametros da classe Object, uma lista de objetos da classe dataTableGeneratedKeysEntry
- dataNumberOfValidKeys vai ser o nº de dataTableGeneratedKeysEntry presentes em dataTableGeneratedKeys
"""
class DataTableGeneratedKeysEntry:

    # Expressão regular para dar match com um objeto do grupo Key
    regex = r"(?P<object_type>\w+)\s+OBJECT-TYPE\s+SYNTAX\s+(?P<syntax>\w+(?:\s+\w+)*)\s+MAX-ACCESS\s+(?P<max_access>\w+(?:-\w+)?)\s+STATUS\s+(?P<status>\w+)\s+DESCRIPTION\s+\"(?P<description>[^\"]+)\"\s+::=\s+{\s+(?P<id_type>dataTableGeneratedKeysEntry)\s+(?P<id_int>\d+)\s+}\s*"

    def __init__(self, filename):
        with open(filename, 'r') as file:
            content = file.read().replace('\n', '')
        self.fields = [] 
        self.create_entry(content)

    def create_entry(self, content):
        """Função que adiciona todos os parâmetros de uma entrada da tabela"""
        matches = re.finditer(self.regex, content)
        for match in matches:
            object_type = match.group('object_type')
            syntax = match.group('syntax')
            max_access = match.group('max_access')
            status = match.group('status')
            description = match.group('description')
            id_type = match.group('id_type')
            id_int = match.group('id_int')
            entry = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description)
            self.fields.append(entry)

    def to_string(self):
        """Função que imprime uma entrada da tabela"""
        for f in self.fields:
            f.to_string()

    def get_field(self, index):
        """Função que devolve um campo de uma entrada, dado um ID (id_int)"""
        for f in self.fields:
            if (f.id_int == index):
                return f
        raise ValueError("Field with index {} doesn't exist".format(index))

#d = DataTableGeneratedKeysEntry("mib.mib")
#d.to_string()
#field = d.get_field(6)
#field.to_string()

class DataTableGeneratedKeys:
    
    def __init__(self, filename):
        self.dataNumberOfValidKeys = len(self.dataTableGeneratedKeys)
        self.dataTableGeneratedKeys = []
        self.create_entries(self.dataTableGeneratedKeys, filename)
    
    def create_entries(self, filename):
        self.dataTableGeneratedKeys = [] 

        entry = DataTableGeneratedKeysEntry(filename)
        self.dataTableGeneratedKeys.append(entry)

    """
    TODO:
    - Fazer funçoes de get, add e remove de entradas na tabela (ter atenção em mudar o valor de id_key (incrementar ou decrementar))
    """


#class MIB_Keys:
#    
#    def __init__(self):
#        self.dataTableGeneratedKeys = DataTableGeneratedKeys("mib.mib")
