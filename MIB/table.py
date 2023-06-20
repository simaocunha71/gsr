from MIB.entry import DataTableGeneratedKeysEntry
import datetime

class DataTableGeneratedKeys:
    id_key = 1
    
    def __init__(self):
        self.dataTableGeneratedKeys = {}
        self.dataNumberOfValidKeys = 0
    

    def create_entry(self, filename, keyValue, keyRequester, keyExpirationDate, keyExpirationTime, keyVisibility):
        """Função que cria uma entrada na tabela.
        Além disso, remove todas as entradas que expiraram"""
        self.remove_expired_entries()

        current_datetime = datetime.datetime.now()
        timestamp = int((current_datetime - current_datetime.replace(hour=0, minute=0, second=0)).total_seconds())

        entry = (DataTableGeneratedKeysEntry(filename, self.id_key, keyValue, keyRequester, keyExpirationDate, keyExpirationTime, keyVisibility), timestamp)

        self.dataTableGeneratedKeys[self.id_key] = entry
        self.dataNumberOfValidKeys += 1
        self.id_key += 1
        return self.id_key - 1

        
    def remove_expired_entries(self):
        """Função que remove todas as entradas expiradas (i.e. cujo timestamp atingiu keyExpirationTime)"""
        expired_entries = [] #Aqui serão guardadas todas as entradas expiradas

        for key_id, (entry, _) in self.dataTableGeneratedKeys.items():
            current_datetime = datetime.datetime.now()
            timestamp = int((current_datetime - current_datetime.replace(hour=0, minute=0, second=0)).total_seconds())

            if timestamp > int(entry.get_field(5).get_value()):
                expired_entries.append(key_id)

        #Remoção de todas as entradas expiradas
        for key_id in expired_entries:
            del self.dataTableGeneratedKeys[key_id]
            self.dataNumberOfValidKeys -= 1

    
    def to_string(self):
        """Função que imprime a tabela"""
        print("keyId        keyValue          KeyRequester    keyExpirationDate   keyExpirationTime   keyVisibility")
        for _, (entry, _) in self.dataTableGeneratedKeys.items():
            entry.prettier_to_string()
