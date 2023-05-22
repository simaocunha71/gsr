"""Classe que cria contém todos os objetos do grupo System da MIB"""
import re, datetime
import object as obj
import utils

class MIB_System:
    regex = r"(?P<object_type>system\w+)\s+OBJECT-TYPE\s+SYNTAX\s+(?P<syntax>\w+)\s+MAX-ACCESS\s+(?P<max_access>\w+(?:-\w+)?)\s+STATUS\s+(?P<status>\w+)\s+DESCRIPTION\s+\"(?P<description>.*?)\"\s+::=\s+{\s+(?P<id_type>system)\s+(?P<id_int>\d+)\s+}\s*"

    def __init__(self, filename):
        with open(filename, 'r') as file:
            content = file.read().replace('\n', '')
        self.date = utils.get_timestamp()
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
                mib_obj = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, self.get_date())
            elif object_type == "systemRestartTime":
                mib_obj = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, self.get_time())
            elif object_type == "systemKeySize":
                mib_obj = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, self.get_key_size())
            elif object_type == "systemIntervalUpdate":
                mib_obj = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, self.get_interval_update())
            elif object_type == "systemMaxNumberOfKeys":
                mib_obj = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, self.get_max_n_keys())
            elif object_type == "systemKeysTimeToLive":
                mib_obj = obj.MIB_Object(id_type, id_int, object_type, syntax, max_access, status, description, self.get_keys_ttl())

            if mib_obj is not None: 
                self.objects.append(mib_obj)


    
    def get_date(self):
        return self.date[1]
    
    def get_time(self):
        return self.date[1]

    def get_key_size(self):
        #TODO: a mudar - agente vai comunicar este valor
        return 4
    
    def get_interval_update(self):
        #TODO: a mudar - agente vai comunicar este valor
        return 40

    def get_max_n_keys(self):
        #TODO: a mudar - agente vai comunicar este valor
        return 44
    
    def get_keys_ttl(self):
        #TODO: a mudar - agente vai comunicar este valor
        return 42
    
    def receive_values_from_agent():
        #TODO: Fazer o parse dos valores enviados pelo agente para povoar os objetos do system
        pass
    
    def to_string(self):
        """Função que representa o grupo System da MIB em string"""
        print(len(self.objects))
        for mib_obj in self.objects:
            mib_obj.to_string()

#o = MIB_System("mib.mib")
#o.to_string()
