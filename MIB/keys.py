import MIB.table as table
import MIB.object as obj

"""Módulo que representa o grupo data da MIB"""

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
        """Função que devolve a tabela da MIB e incrementa o número de chaves que lá se encontram
        - esta função só será chamada para adicionar entradas na tabela"""
        self.update_n_valid_keys(self.objects)
        return self.dataTableGeneratedKeys
    
    def update_n_valid_keys(self, objects):
        """Função que incrementa o número de chaves da tabela (i.e. incrementa a variável da classe dataTableGeneratedKeys responsável por contar chaves)
        e atualiza a variavel responsável por isso neste módulo """
        new_val = self.dataTableGeneratedKeys.dataNumberOfValidKeys + 1
        return objects[0].set_value(new_val) 
    
    
    def to_string(self):
        """Função que imprime o grupo data + tabela"""
        for mib_obj in self.objects:
            mib_obj.to_string()
        self.dataTableGeneratedKeys.to_string()