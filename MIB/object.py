"""Classe que representa um objeto da MIB"""
class MIB_Object:

    def __init__(self, id_type, id_int, object_type, syntax, max_access, status, description, value):
        self.id_type = id_type         # Nome do grupo ao qual aquele objeto pertence
        self.id_int = int(id_int)      # ID do objeto no grupo
        self.object_type = object_type # Tipo do objeto
        self.syntax = syntax           # Sintaxe do objeto
        self.max_access = max_access   # Tipo de acesso ao objeto
        self.status = status           # Estado do objeto
        self.description = description # Descrição do objeto
        self.value = value             # Valor contido no objeto
            

    def to_string(self):
        """Função que representa um objeto da MIB em string"""
        print(f"{self.object_type} OBJECT-TYPE")
        print(f"    SYNTAX {self.syntax}")
        print(f"    MAX-ACCESS {self.max_access}")
        print(f"    STATUS {self.status}")
        print(f"    DESCRIPTION \"{self.description}\"")
        if self.value is not None:
            print(f"    VALUE = {self.value}")
        print(f"    ::= {{ {self.id_type} {self.id_int} }} ")

    """Getters da classe Object"""
    def get_id_type(self):
        return self.id_type
    
    def get_id_int(self):
        return self.id_int
    
    def get_object_type(self):
        return self.object_type
    
    def get_syntax(self):
        return self.syntax
    
    def get_max_access(self):
        return self.max_access
    
    def get_status(self):
        return self.status
    
    def get_description(self):
        return self.description
    
    def get_value(self):
        return self.value
    
    """Setters a classe Object"""
    def set_id_type(self, id_type):
        self.id_type = id_type

    def set_id_int(self, id_int):
        self.id_int = id_int

    def set_object_type(self, object_type):
        self.object_type = object_type

    def set_syntax(self, syntax):
        self.syntax = syntax

    def set_max_access(self, max_access):
        self.max_access = max_access

    def set_status(self, status):
        self.status = status

    def set_description(self, description):
        self.description = description

    def set_value(self, value):
        self.value = value
