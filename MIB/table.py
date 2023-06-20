from MIB.entry import DataTableGeneratedKeysEntry
import time
import datetime

class DataTableGeneratedKeys:
    id_key = 1
    
    def __init__(self):
        self.dataTableGeneratedKeys = {}
        self.dataNumberOfValidKeys = 0
    

    def create_entry(self, filename, keyValue, keyRequester, keyExpirationDate, keyExpirationTime, keyVisibility):
        # Verificar se há entradas expiradas
        self.remove_expired_entries()

        current_datetime = datetime.datetime.now()
        timestamp = int((current_datetime - current_datetime.replace(hour=0, minute=0, second=0)).total_seconds())

        entry = (DataTableGeneratedKeysEntry(filename, self.id_key, keyValue, keyRequester, keyExpirationDate, keyExpirationTime, keyVisibility), timestamp)

        self.dataTableGeneratedKeys[self.id_key] = entry
        self.dataNumberOfValidKeys += 1
        self.id_key += 1
        return self.id_key - 1

        
    def remove_expired_entries(self):
        expired_entries = []
        
        for key_id, (entry, timestamp) in self.dataTableGeneratedKeys.items():
            print(f"timestamp ({timestamp}) > entry.get_field(5).get_value() ({int(entry.get_field(5).get_value())})?????????????????")
            if timestamp > int(entry.get_field(5).get_value()):
                expired_entries.append(key_id)
        print("-----------------------------------------")
        
        for key_id in expired_entries:
            del self.dataTableGeneratedKeys[key_id]
            self.dataNumberOfValidKeys -= 1
    
    def to_string(self):
        """Função que imprime a tabela"""
        print("keyId        keyValue          KeyRequester    keyExpirationDate   keyExpirationTime   keyVisibility")
        for _, (entry, _) in self.dataTableGeneratedKeys.items():
            entry.prettier_to_string()
