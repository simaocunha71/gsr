"""Classe que representa um objeto da MIB"""
class MIB_Object:

    def __init__(self, id_type, id_int, object_type, syntax, max_access, status, description):
        self.id_type = id_type         # Nome do grupo ao qual aquele objeto pertence
        self.id_int = int(id_int)      # ID do objeto no grupo
        self.object_type = object_type # Tipo do objeto
        self.syntax = syntax           # Sintaxe do objeto
        self.max_access = max_access   # Tipo de acesso ao objeto
        self.status = status           # Estado do objeto
        self.description = description # Descrição do objeto
            

    def to_string(self):
        """Função que representa um objeto da MIB em string"""
        print(f"{self.object_type} OBJECT-TYPE")
        print(f"    SYNTAX {self.syntax}")
        print(f"    MAX-ACCESS {self.max_access}")
        print(f"    STATUS {self.status}")
        print(f"    DESCRIPTION \"{self.description}\"")
        print(f"    ::= {{ {self.id_type} {self.id_int} }} ")