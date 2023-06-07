"""Classe que representa uma entrada da tabela da MIB"""
import re
from MIB.object import MIB_Object

class DataTableGeneratedKeysEntry:

    # Expressão regular para dar match com um objeto do grupo Key
    regex = r"(?P<object_type>\w+)\s+OBJECT-TYPE\s+SYNTAX\s+(?P<syntax>\w+(?:\s+\w+)*)\s+MAX-ACCESS\s+(?P<max_access>\w+(?:-\w+)?)\s+STATUS\s+(?P<status>\w+)\s+DESCRIPTION\s+\"(?P<description>[^\"]+)\"\s+::=\s+{\s+(?P<id_type>dataTableGeneratedKeysEntry)\s+(?P<id_int>\d+)\s+}\s*"

    def __init__(self, filename, id_key, keyValue, keyRequester, keyExpirationDate, keyExpirationTime, keyVisibility):
        with open(filename, 'r') as file:
            content = file.read().replace('\n', '')
        self.fields = {} 
        self.create_entry(content, id_key, keyValue, keyRequester, keyExpirationDate, keyExpirationTime, keyVisibility)

    def create_entry(self, content, id_key, keyValue, keyRequester, keyExpirationDate, keyExpirationTime, keyVisibility):
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
            
            entry = None

            if object_type == "keyId":
                entry = MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, id_key)
            elif object_type == "keyValue":
                entry = MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, keyValue)
            elif object_type == "keyRequester":
                entry = MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, keyRequester)
            elif object_type == "keyExpirationDate":
                entry = MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, keyExpirationDate)
            elif object_type == "keyExpirationTime":
                entry = MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, keyExpirationTime)
            elif object_type == "keyVisibility":
                entry = MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, keyVisibility)

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
                return f.get_value()
        raise ValueError("Não existe campo com índice {}".format(index))
    
    def set_field(self, index, value):
        """Função que define o valor de um campo de uma entrada, dado um ID (id_int)"""
        for f in self.fields:
            if f.id_int == index:
                f.set_value(value)
                return
        raise ValueError("Não existe campo com índice {}".format(index))



#d = DataTableGeneratedKeysEntry("mib.mib", 0)
#d.to_string()
#d.prettier_to_string()
#field = d.get_field(1) #Value=0
#field = d.get_field(6) #Value=None
#field.to_string()