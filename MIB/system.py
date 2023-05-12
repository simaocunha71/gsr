"""Classe que cria contém todos os objetos do grupo System da MIB"""
import re
import object as obj

class MIB_System:
    regex = r"(?P<object_type>\w+)\s+OBJECT-TYPE\s+SYNTAX\s+(?P<syntax>\w+)\s+MAX-ACCESS\s+(?P<max_access>\w+(?:-\w+)?)\s+STATUS\s+(?P<status>\w+)\s+DESCRIPTION\s+\"(?P<description>.*?)\"\s+::=\s+{\s+(?P<id_type>system)\s+(?P<id_int>\d+)\s+}\s*"
    
    def __init__(self, filename):
        with open(filename, 'r') as file:
            content = file.read().replace('\n', '')
        self.objects = []
        self.parse_objects(content)

    def parse_objects(self, content):
        """Função para fazer o parsing dos objetos do grupo System"""
        matches = re.finditer(self.regex, content)
        for match in matches:
            object_type = match.group('object_type')
            syntax = match.group('syntax')
            max_access = match.group('max_access')
            status = match.group('status')
            description = match.group('description')
            id_type = match.group('id_type')
            id_int = match.group('id_int')
            mib_obj = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description)
            self.objects.append(mib_obj)

    def to_string(self):
        """Função que representa o grupo System da MIB em string"""
        print(len(self.objects))
        for mib_obj in self.objects:
            mib_obj.to_string()

#o = MIB_System("mib.mib")
#o.to_string()
