"""Classe que cria contém todos os objetos do grupo System da MIB"""
import re
import MIB.object as obj
import MIB.utils as utils

class MIB_System:
    regex = r"(?P<object_type>system\w+)\s+OBJECT-TYPE\s+SYNTAX\s+(?P<syntax>\w+)\s+MAX-ACCESS\s+(?P<max_access>\w+(?:-\w+)?)\s+STATUS\s+(?P<status>\w+)\s+DESCRIPTION\s+\"(?P<description>.*?)\"\s+::=\s+{\s+(?P<id_type>system)\s+(?P<id_int>\d+)\s+}\s*"

    def __init__(self, filename, K, updating_interval, max_keys, ttl):
        with open(filename, 'r') as file:
            content = file.read().replace('\n', '')
        self.date = utils.get_timestamp()
        self.K = K
        self.updating_interval = updating_interval
        self.max_keys = max_keys
        self.ttl = ttl
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

            mib_obj = None

            if object_type == "systemRestartDate":
                mib_obj = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, self.date[0])
            elif object_type == "systemRestartTime":
                mib_obj = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, self.date[1])
            elif object_type == "systemKeySize":
                mib_obj = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, self.K)
            elif object_type == "systemIntervalUpdate":
                mib_obj = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, self.updating_interval)
            elif object_type == "systemMaxNumberOfKeys":
                mib_obj = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, self.max_keys)
            elif object_type == "systemKeysTimeToLive":
                mib_obj = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, self.ttl)

            if mib_obj is not None: 
                self.objects.append(mib_obj)
    
    def to_string(self):
        """Função que representa o grupo System da MIB em string"""
        #print(len(self.objects))
        for mib_obj in self.objects:
            mib_obj.to_string()

#o = MIB_System("mib.mib")
#o.to_string()
