"""Classe que implementa a MIB"""
import system, config, keys

class MIB:
    def __init__(self, filename):
        self.dictionary = {}
        self.dictionary[1] = system.MIB_System(filename)
        self.dictionary[2] = config.MIB_Config(filename)
        self.dictionary[3] = keys.MIB_Keys(filename)

    def to_string(self):
        """Função que representa a MIB em string"""
        for _, o in self.dictionary.items():
            o.to_string()

    def get_group(self, oid):
        """Devolve o grupo dado o seu oid"""
        try:
            return self.dictionary.get(oid)
        except:
            print("Erro em obter grupo - OID não existente na MIB")

    def print_group(self, oid):
        """Imprime um grupo dado o seu OID"""
        try:
            group = self.get_group(oid)
            if group is not None:
                group.to_string()
            else:
                print("Erro em obter grupo - OID não existente na MIB")
        except:
            print("Erro em obter grupo - OID não existente na MIB")


mib = MIB("mib.mib")
mib.print_group(3)
