"""Classe responsável pela PDU """
import pickle, sys

class PDU:
    def __init__(self, request_id, primitive_type, instance_elements_size, instance_elements_list,
                 error_elements_size, error_elements_list, security_level=0, n_security_parameters_number=0,
                 n_security_parameters_list=[]):
        self.security_level = security_level                             # Inteiro que identifica quais os mecanismos de segurança a utilizar (neste TP = 0)
        self.n_security_parameters_number = n_security_parameters_number # Número de parâmetros necessários à implementação dos mecanismos de segurança (neste TP = 0)
        self.n_security_parameters_list = n_security_parameters_list     # Lista de parâmetros necessários à implementação dos mecanismos de segurança
        self.request_id = request_id                                     # ID do pedido
        self.primitive_type = primitive_type                             # Tipo de primitiva (0 = response, 1 = get, 2 = set)
        self.instance_elements_size = instance_elements_size             # Inteiro que indica a quantidade de pares duma lista L (primitiva get) ou duma lista W (primitiva set ou primitiva response)
        self.instance_elements_list = instance_elements_list             # Lista de pares duma lista L (primitiva get) ou duma lista W (primitiva set ou primitiva response)
        self.error_elements_size = error_elements_size                   # Quantidade de erros reportados na primitiva
        self.error_elements_list = error_elements_list                   # Lista de erros e valores associados

    def get_security_level(self):
        """Identifica quais os mecanismos de segurança a utilizar"""
        return self.security_level

    def get_n_security_parameters_number(self):
        """Devolve o número de parâmetros necessários à implementação dos mecanismos de segurança"""
        return self.n_security_parameters_number

    def get_n_security_parameters_list(self):
        """Devolve a lista de parâmetros necessários à implementação dos mecanismos de segurança"""
        return self.n_security_parameters_list

    def get_request_id(self):
        """Devolve o ID do pedido"""
        return self.request_id

    def get_primitive_type(self):
        """Devolve o tipo de primitiva (0 = response, 1 = get, 2 = set)"""
        return self.primitive_type

    def get_instance_elements_size(self):
        """Inteiro que indica a quantidade de pares duma lista L (primitiva get) ou duma lista W (primitiva set ou primitiva response)"""
        return self.instance_elements_size

    def get_instance_elements_list(self):
        """Devolve a lista de pares duma lista L (primitiva get) ou duma lista W (primitiva set ou primitiva response)"""
        return self.instance_elements_list

    def get_error_elements_size(self):
        """Devolve a quantidade de erros reportados na primitiva"""
        return self.error_elements_size

    def get_error_elements_list(self):
        """Devolve a lista de erros e valores associados"""
        return self.error_elements_list
    
    def encode(self):
        """Codifica a PDU"""
        return pickle.dumps(self)

    @staticmethod
    def decode(encoded_data):
        """Descodifica a PDU"""
        try:
            return pickle.loads(encoded_data)
        except UnicodeDecodeError as e:
            print("Error Unicode decode:", e)
            sys.exit(0)
    
    def to_string(self):
        if self.primitive_type == 1 or self.primitive_type == 2:
            print("####################################### PDU (from client) ##########################################")
        elif self.primitive_type == 0:
            print("####################################### PDU (from server) ##########################################")
        print(f"Nível de segurança = {self.security_level} ")
        print(f"Lista de parâmetros de segurança (tamanho = {self.n_security_parameters_number}):")
        if not self.n_security_parameters_list:
            print(" > (Empty)")
        else:
            for e in self.n_security_parameters_list:
                print(f" > {e}")
        print(f"ID do pedido = {self.request_id}")
        print(f"Tipo da primitiva = {self.primitive_type}")
        print(f"Lista de elementos (tamanho = {self.instance_elements_size}):")
        if not self.instance_elements_list:
            print(" > (Empty)")
        else:
            for e in self.instance_elements_list:
                print(f" > {e}")
        print(f"Lista de erros (tamanho = {self.error_elements_size}):")
        if not self.error_elements_list:
            print(" > (Empty)")
        else:
            for e in self.error_elements_list:
                print(f" > {e}")
        print("####################################################################################################")