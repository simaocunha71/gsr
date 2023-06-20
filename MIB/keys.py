import MIB.table as table
import MIB.object as obj

class MIB_Keys:
    
    def __init__(self):
        self.objects = []
        self.dataTableGeneratedKeys = table.DataTableGeneratedKeys()
        self.get_objects()

    def get_objects(self):
        """Função que adiciona os objetos do grupo data manualmente (i.e. sem fazer o parsing)"""
        self.objects.extend([
            obj.MIB_Object("data", 1, "dataNumberOfValidKeys", "INTEGER", 
                           "read-only", "current", 
                           "The number of elements in the dataTableGeneratedKeys.", 
                           self.dataTableGeneratedKeys.dataNumberOfValidKeys),
            obj.MIB_Object("data", 2, "dataTableGeneratedKeys", "SEQUENCE OF DataTableGeneratedKeysEntryType", 
                           "not-accessible", "mandatory", 
                           "A table with information from all created keys that are still valid.", 
                           None),
            obj.MIB_Object("dataTableGeneratedKeys", 1, "dataTableGeneratedKeysEntry", "DataTableGeneratedKeysEntryType", 
                           "not-accessible", "current", 
                           "A row of the table with information for each key.", 
                           None)
        ])

    def get_table(self):
        self.update_n_valid_keys(self.objects)
        return self.dataTableGeneratedKeys
    
    def update_n_valid_keys(self, objects):
        new_val = self.dataTableGeneratedKeys.dataNumberOfValidKeys + 1
        return objects[0].set_value(new_val) 
    
    
    def to_string(self):
        #print(len(self.objects))
        for mib_obj in self.objects:
            mib_obj.to_string()
        self.dataTableGeneratedKeys.to_string()