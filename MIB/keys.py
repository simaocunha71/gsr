import mib_table.table as table
import object as obj

class MIB_Keys:
    
    def __init__(self, filename):
        self.objects = []
        self.dataTableGeneratedKeys = table.DataTableGeneratedKeys(filename)
        self.get_objects()

    def get_objects(self):
        """Função que adiciona os objetos do grupo data manualmente (i.e. sem fazer o parsing)
           -> Não faço parse do valor do index (possível limitação do programa), mas que deve chegar para o propósito"""
        self.objects.extend([
            obj.MIB_Object("data", 1, "dataNumberOfValidKeys", "INTEGER", 
                           "read-only", "current", 
                           "The number of elements in the dataTableGeneratedKeys.", 
                           self.get_n_valid_keys()),
            obj.MIB_Object("data", 2, "dataTableGeneratedKeys", "SEQUENCE OF DataTableGeneratedKeysEntryType", 
                           "not-accessible", "mandatory", 
                           "A table with information from all created keys that are still valid.", 
                           None),
            obj.MIB_Object("dataTableGeneratedKeys", 1, "dataTableGeneratedKeysEntry", "DataTableGeneratedKeysEntryType", 
                           "not-accessible", "current", 
                           "A row of the table with information for each key.", 
                           None)
        ])

    def get_n_valid_keys(self):
        return self.dataTableGeneratedKeys.get_dataNumberOfValidKeys()
    
    def to_string(self):
        print(len(self.objects))
        for mib_obj in self.objects:
            mib_obj.to_string()
        self.dataTableGeneratedKeys.to_string()

    def receive_values_from_agent():
        #TODO: Fazer o parse dos valores enviados pelo agente para povoar os objetos do data (necessario???)
        pass