import agent as agent
import os
import json
import time

"""Classe responsável por criar uma entrada para um determinado cliente"""
class Client_Registration:
    def __init__(self, client_ip, client_port, client_id, password):
        self.client_ip = client_ip
        self.client_port = client_port
        self.client_id = client_id
        self.password = password
        self.requests = []

    def add_request(self, request_id, timestamp):
        """Função que adiciona um pedido com um determinado timestamp e um determinado request_id à lista de pedidos"""
        self.requests.append([request_id, timestamp])

    def get_latest_timestamp(self, request_id):
        """Devolve o timestamp do pedido (identificado por request_id) mais recente. Se não existir nenhum pedido, devolve o valor default 0"""
        timestamps = [timestamp for request, timestamp in self.requests if request == request_id]
        if timestamps:
            return max(timestamps)
        return 0

    def to_string(self):
        """Imprime uma entrada de um cliente"""
        result = ""
        result += f"Client ID: {self.client_id} | "
        result += f"Client Port: {self.client_port} | "
        result += f"Client IP: {self.client_ip} | "
        result += "Requests:\n"
        for request in self.requests:
            request_id, timestamp = request
            result += f"  Request ID: {request_id} | Timestamp: {timestamp}\n"
        result += f"Password: {self.password}\n"
        print(result)

"""Classe responsável por registar todas as entradas dos clientes conectados e regista-as num ficheiro json"""
class Clients:
    def __init__(self):
        self.clients = {}
        self.start_time = int(time.time())
        self.initialize_json_file()

    def initialize_json_file(self):
        """Cria o ficheiro "clients.json" quando é criado uma instância de Clients"""
        if not os.path.exists("clients.json"):
            with open("clients.json", 'w') as file:
                file.write("{}")

    def add_client(self, client_ip, client_port, client_id, password):
        """Função que adiciona um cliente ao ficheiro json e ao dicionário"""
        client = self.clients.get(password)
        if client:
            client.add_request(client_id, int(time.time()) - self.start_time)
        else:
            client = Client_Registration(client_ip, client_port, client_id, password)
            client.add_request(client_id, int(time.time()) - self.start_time)
            self.clients[password] = client
        self.save_to_json()

    def save_to_json(self):
        """Guarda uma entrada de Clients no ficheiro json"""
        data = {}
        for client_password, client in self.clients.items():
            client_data = {
                'client_id': client.client_id,
                'client_ip': client.client_ip,
                'client_port': client.client_port,
                'password': client.password,
                'requests': []
            }
            for request in client.requests:
                request_id, timestamp = request
                client_data['requests'].append({
                    'request_id': request_id,
                    'timestamp': timestamp
                })
            data[client_password] = client_data
        with open("clients.json", 'w') as file:
            json.dump(data, file, indent=4)


    def can_send_same_requestID(self, client_password, request_id, max_time):
        """Verifica se o pedido (identificado por request_id) do cliente (identificado por client_password) é enviado durante o intervalo
        de tempo max_time. Caso ainda esteja dentro do intervalo, retorna falso, caso contrário, retorna true """

        # Cliente ainda não está registado
        # Um cliente é identificado pela sua senha única (nenhum outro cliente pode usar a mesma senha - não há controlo nesse aspeto) - limitação do projeto
        if client_password not in self.clients:
            return True 

        client = self.clients[client_password]

        # Verifica se existe algum pedido com o mesmo request_id na lista de pedidos do cliente
        has_previous_request = any(request[0] == request_id for request in client.requests)

        current_time = int(time.time()) - self.start_time

        if not has_previous_request:
            # Se não existir nenhum pedido anterior com o mesmo request_id, simplesmente adiciona o pedido à lista
            client.requests = []
            client.add_request(request_id, current_time)
            return True

        latest_timestamp = client.get_latest_timestamp(request_id)
        time_difference = current_time - latest_timestamp

        return time_difference >= int(max_time)






