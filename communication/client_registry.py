import agent as agent
import os
import json
import time
import security.checksum as ch
import security.encrypted_data as enc

class Client_Registration:
    def __init__(self, client_id, client_ip, client_port, password):
        self.client_id = client_id
        self.client_ip = client_ip
        self.client_port = client_port
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

class Clients:
    def __init__(self, filename, server_password):
        self.clients = {}
        self.start_time = int(time.time())
        self.initialize_json_file(filename, server_password)

    def initialize_json_file(self, filename, server_password):
        """Cria o ficheiro "clients.json" quando é criado uma instância de Clients"""
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write("{}")

    def add_client(self, client_id, client_ip, client_port, request_id, password, filename, server_password):
        """Função que adiciona um cliente ao ficheiro json e ao dicionário"""
        client = self.clients.get(client_id)
        if client:
            client.add_request(client_id, int(time.time()) - self.start_time)
        else:
            client = Client_Registration(client_id, client_ip, client_port, password)
            client.add_request(request_id, int(time.time()) - self.start_time)
            self.clients[client_id] = client
        self.save_to_json(filename, server_password)

    def save_to_json(self, filename, server_password):
        """NOTE: server_password irá ser util para encriptar/desencriptar o ficheiro json"""
        """Guarda uma entrada de Clients no ficheiro json"""
        data = {}
        for client_id, client in self.clients.items():
            client_data = {
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
            data[client_id] = client_data
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def can_send_same_requestID(self, client_id, request_id, max_time):
        """Verifica se o pedido (identificado por request_id) do cliente (identificado por client_id) é enviado durante o intervalo
        de tempo max_time. Caso ainda esteja dentro do intervalo, retorna falso, caso contrário, retorna true """
        if client_id not in self.clients:
            return True
        client = self.clients[client_id]
        has_previous_request = any(request[0] == request_id for request in client.requests)
        current_time = int(time.time()) - self.start_time
        if not has_previous_request:
            client.requests = []
            client.add_request(request_id, current_time)
            return True
        latest_timestamp = client.get_latest_timestamp(request_id)
        time_difference = current_time - latest_timestamp
        return time_difference >= int(max_time)