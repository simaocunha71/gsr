"""Classe que implementa a MIB"""
import system, config, keys

"""
TODO:
- Esta classe terá que ler o ficheiro principal e passar os dados às outras classes
- Parse dos OID's dos grupos ??? [Ver função init]
"""


class MIB:
    def __init__(self, filename):
        self.dictionary = {}
        self.dictionary[1] = system.MIB_System(filename)
        self.dictionary[2] = config.MIB_Config(filename)
        self.dictionary[3] = keys.MIB_Keys(filename)

    def to_string(self):
        """Função que representa a MIB em string"""
        print(len(self.system_list.objects))
        for mib_obj in self.system_list.objects:
            mib_obj.to_string()

        print(len(self.config_list.objects))
        for mib_obj in self.config_list.objects:
            mib_obj.to_string()

        print(len(self.data.objects))
        for mib_obj in self.data.objects:
            mib_obj.to_string()

mib = MIB("mib.mib")
mib.to_string()
