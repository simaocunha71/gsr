"""Classe que representa a tabela da MIB"""

from MIB.entry import DataTableGeneratedKeysEntry

class DataTableGeneratedKeys:
    id_key = 1
    
    def __init__(self):
        self.dataTableGeneratedKeys = {}
        self.dataNumberOfValidKeys = 0
    
    def create_entry(self, filename, keyValue, keyRequester, keyExpirationDate, keyExpirationTime, keyVisibility):
        et = DataTableGeneratedKeysEntry(filename, self.id_key, keyValue, keyRequester, keyExpirationDate, keyExpirationTime, keyVisibility)
        self.dataTableGeneratedKeys[self.id_key] = et
        self.dataNumberOfValidKeys += 1
        self.id_key += 1
        return self.id_key - 1

    def remove_entry(self, key_id):
        self.dataTableGeneratedKeys.pop(key_id)
        self.dataNumberOfValidKeys -= 1

    def get_object_entry(self,key_id):
        if key_id in self.dataTableGeneratedKeys:
            return self.dataTableGeneratedKeys[key_id]
        else:
            return None
        
    def to_string(self):
        """Função que imprime a tabela"""
        #print(f"dataNumberOfValidKeys = {self.dataNumberOfValidKeys}")
        print("keyId        keyValue          KeyRequester    keyExpirationDate   keyExpirationTime   keyVisibility")
        for _, k in self.dataTableGeneratedKeys.items():
            k.prettier_to_string()
    
#d = DataTableGeneratedKeys("mib.mib")    
#d.to_string()
#d.remove_entry(5)
#d.to_string()
