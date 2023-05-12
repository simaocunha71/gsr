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
    f"""
    FORMATO: (Cada elemento vai ser um objeto MIB_Object)
    [
        \"keyId OBJECT-TYPE
        SYNTAX INTEGER
        MAX-ACCESS read-only
        STATUS current
        DESCRIPTION "The identification of a generated key."
        ::= {{ dataTableGeneratedKeysEntry 1 }}\"
        
        ,

        \"keyValue OBJECT-TYPE
        SYNTAX OCTET STRING
        MAX-ACCESS read-only
        STATUS current
        DESCRIPTION "The value of a generated key (K bytes/characters long)."
        ::= {{ dataTableGeneratedKeysEntry 2 }}\"

        ,

        ...
    ]
    """

    #TODO: Implementar a expressão regular que me faça o parse do objeto
    regex = r""

    def __init__(self, filename, id_key):
        with open(filename, 'r') as file:
            content = file.read().replace('\n', '')
        self.fields = self.get_entry(content, id_key)

    def get_entry(self, content, id_key):
        self.fields = [] #(dicionário ou array???)

        matches = re.finditer(self.regex, content)
        for match in matches:

            #TODO: Parse dos objetos (content) do tipo (basta escrever a expressão regular):
            #"
            #keyId OBJECT-TYPE
            #   SYNTAX INTEGER
            #   MAX-ACCESS read-only
            #   STATUS current
            #   DESCRIPTION "The identification of a generated key."
            #   ::= { dataTableGeneratedKeysEntry 1 }
            #"

            object_type = match.group('object_type')
            syntax = match.group('syntax')
            max_access = match.group('max_access')
            status = match.group('status')
            description = match.group('description')
            id_type = match.group('id_type')
            #id_int = match.group('id_int')
            entry = obj.MIB_Object(id_type, id_key, object_type, syntax, max_access, status, description)
            self.fields.append(entry)



class DataTableGeneratedKeys:

    id_key = 1
    
    def __init__(self, filename):
        self.dataNumberOfValidKeys = len(self.dataTableGeneratedKeys)
        self.dataTableGeneratedKeys = self.create_entries(self.dataTableGeneratedKeys, filename)
    
    def create_entries(self, filename):
        self.dataTableGeneratedKeys = [] #(dicionário ou array???)

        entry = DataTableGeneratedKeysEntry(filename, self.id_key)
        self.dataTableGeneratedKeys.append(entry)
        self.id_key += 1

    """
    TODO:
    - Fazer funçoes de get, add e remove de entradas na tabela (ter atenção em mudar o valor de id_key (incrementar ou decrementar))
    """


class MIB_Keys:
    
    def __init__(self):
        self.dataTableGeneratedKeys = DataTableGeneratedKeys("mib.mib")


