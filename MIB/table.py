"""Classe que representa a tabela da MIB"""

from MIB.entry import DataTableGeneratedKeysEntry

class DataTableGeneratedKeys:
    id_key = 1
    
    def __init__(self, filename):
        self.dataTableGeneratedKeys = {}
        self.dataNumberOfValidKeys = 0
        
        #TODO: Mudar este 10 - neste momento apenas adiciona entradas à tabela e muda o keyID
        self.create_entries(filename, 10) 
    
    def create_entries(self, filename, number_of_entries):

        for _ in range(number_of_entries):
            et = DataTableGeneratedKeysEntry(filename, self.id_key)
            self.dataTableGeneratedKeys[self.id_key] = et
            self.dataNumberOfValidKeys += 1
            self.id_key += 1

    def remove_entry(self, key_id):
        self.dataTableGeneratedKeys.pop(key_id)
        self.dataNumberOfValidKeys -= 1

    def get_dataNumberOfValidKeys(self):
        """Devolve o numero de chaves válidas na tabela"""
        return self.dataNumberOfValidKeys


    def to_string(self):
        """Função que imprime a tabela"""
        print(f"dataNumberOfValidKeys = {self.dataNumberOfValidKeys}")
        print("keyId        keyValue          KeyRequester    keyExpirationDate   keyExpirationTime   keyVisibility")
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
