"""Classe responsável pela PDU """


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

    def to_string(self):
        print(f"Nível de segurança = {self.security_level} ")
        print(f"Lista de parâmetros de segurança (tamanho = {self.n_security_parameters_number}):")
        for e in self.n_security_parameters_list:
            print(f" > {e}")
        print(f"\nID do pedido = {self.request_id}")
        print(f"Tipo da primitiva = {self.primitive_type}")
        print(f"Lista de elementos (tamanho = {self.instance_elements_size}):")
        for e in self.instance_elements_list:
            print(f" > {e}")
        print(f"Lista de erros (tamanho = {self.error_elements_size}):")
        for e in self.error_elements_list:
            print(f" > {e}")