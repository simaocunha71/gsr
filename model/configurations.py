"""Classe responsável por carregar todos os dados do ficheiro de configuração "config.conf" """

import re

class Configurations:

    #Expressões regulares para o parsing do ficheiro de configuração
    regex_n_matrix        = r'K:\s*(\d+)'
    regex_master_key      = r'M:\s*(.+)'
    regex_update_interval = r'T:\s*(\d+)'
    regex_max_store_time  = r'V:\s*(\d+)'
    regex_n_max_entries   = r'X:\s*(\d+)'
    regex_port            = r'Port:\s*(\d+)'

    def __init__(self, filename):
        with open(filename, 'r') as f:
            f_lines = f.readlines()
        
        self.n_matrix = int(self.get_value(''.join(f_lines), self.regex_n_matrix))               # Número de linhas ou colunas da matriz
        self.master_key = self.get_value(''.join(f_lines), self.regex_master_key)                # Chave mestra
        self.update_interval = int(self.get_value(''.join(f_lines), self.regex_update_interval)) # Intervalo(em ms) de atualizações de matrizes
        self.max_store_time = self.get_value(''.join(f_lines), self.regex_max_store_time)        # Tempo máximo do armazenamento da informação na matriz
        self.n_max_entries = int(self.get_value(''.join(f_lines), self.regex_n_max_entries))     # Número máximo de entradas na tabela
        self.port = int(self.get_value(''.join(f_lines), self.regex_port))                       # Porta de atendimento UDP
        
    def get_value(self, file_content, regex):
        """Parse de um valor do ficheiro de configuração através de uma expressão regular qualquer"""
        match = re.search(regex, file_content)
        return match.group(1) if match else ""

    def print_configurations(self):
        "Função de debug: objeto Configurations com o conteúdo do ficheiro de configuração"
        print(f"K: {str(self.n_matrix)}")
        print(f"M: {self.master_key}")
        print(f"T: {self.update_interval}")
        print(f"V: {self.max_store_time}")
        print(f"X: {str(self.n_max_entries)}")
        print(f"Port: {str(self.port)}")

#c = Configurations("../config.conf")
#c.print_configurations()