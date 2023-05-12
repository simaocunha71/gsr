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

    def __init__(self, filename, id_key):
        with open(filename, 'r') as file:
            content = file.read().replace('\n', '')
        self.fields = {} 
        self.create_entry(content, id_key)

    def create_entry(self, content, id_key):
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
            #TODO:[adicionar mais condiçoes aqui???] arranjar forma de preencher os outros valores para object_type = keyValue, KeyRequester, keyExpirationDate, keyExpirationTime e keyVisibility
            if(object_type == "keyId"):
                entry = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, id_key)
            else:
                entry = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, None)
            self.fields[object_type] = entry

    def to_string(self):
        """Função que imprime uma entrada da tabela"""
        for _, f in self.fields.items():
            f.to_string()

    def prettier_to_string(self):
        """Função que imprime uma entrada da tabela de forma mais gráfica"""
        print(f'{str(self.fields["keyId"].get_value())}          {self.fields["keyValue"].get_value()}          {self.fields["keyRequester"].get_value()}              {self.fields["keyExpirationDate"].get_value()}               {self.fields["keyExpirationTime"].get_value()}               {str(self.fields["keyVisibility"].get_value())}')

    def get_field(self, index):
        """Função que devolve um campo de uma entrada, dado um ID (id_int)"""
        for f in self.fields:
            if (f.id_int == index):
                return f
        raise ValueError("Field with index {} doesn't exist".format(index))

#d = DataTableGeneratedKeysEntry("mib.mib", 0)
#d.to_string()
#d.prettier_to_string()
#field = d.get_field(1) #Value=0
#field = d.get_field(6) #Value=None
#field.to_string()

class DataTableGeneratedKeys:
    id_key = 1
    
    def __init__(self, filename):
        self.dataTableGeneratedKeys = {}
        self.dataNumberOfValidKeys = 0
        
        #TODO: Mudar este 10 - neste momento apenas adiciona entradas à tabela e muda o keyID
        self.create_entries(filename, 10) 
    
    def create_entries(self, filename, number_of_entries):

        for _ in range(number_of_entries):
            entry = DataTableGeneratedKeysEntry(filename, self.id_key)
            self.dataTableGeneratedKeys[self.id_key] = entry
            self.dataNumberOfValidKeys += 1
            self.id_key += 1

    def remove_entry(self, key_id):
        self.dataTableGeneratedKeys.pop(key_id)
        self.dataNumberOfValidKeys -= 1


    def to_string(self):
        """Função que imprime a tabela"""
        print(f"dataNumberOfValidKeys = {self.dataNumberOfValidKeys}")
        print("keyId    keyValue    KeyRequester    keyExpirationDate   keyExpirationTime   keyVisibility")
        for _, k in self.dataTableGeneratedKeys.items():
            k.prettier_to_string()

    """
    TODO:
    - Fazer funçoes de get, add e remove de entradas na tabela (ter atenção em mudar o valor de id_key (incrementar ou decrementar))
    - Ter atenção à concorrência (aplicar locks)
    """
    
#d = DataTableGeneratedKeys("mib.mib")    
#d.to_string()
#d.remove_entry(5)
#d.to_string()

class MIB_Keys:
    
    def __init__(self, filename):
        self.dataTableGeneratedKeys = DataTableGeneratedKeys(filename)

    def to_string(self):
        self.dataTableGeneratedKeys.to_string()

#k = MIB_Keys("mib.mib")
#k.print_table()