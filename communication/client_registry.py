import os
import json
import time
import security.encrypted_data as enc

"""Classe que representa um registo de um cliente já ligado ao agente. Contém um ID escrito por si, IP e porta utilizados, uma password sua e uma lista de pedidos cujos
elementos são do tipo (ID do pedido, timestamp em segundos desde que o agente foi iniciado)"""
class Client_Registration:
    def __init__(self, client_id, client_ip, client_port, password):
        self.client_id = client_id
        self.client_ip = client_ip
        self.client_port = client_port
        self.password = password
        self.requests = []

    def add_request(self, request_id, timestamp):
        """Função que adiciona um pedido com um determinado timestamp e um determinado request_id à lista de pedidos"""
        self.requests.append((request_id, timestamp))

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


"""Classe que contém um dicionário com todos os gestores alguma vez ligados ao agente. Também contém um ficheiro encriptado para facilitar a visualização do registo dos clientes"""
class Clients:
    def __init__(self, filename, server_password):
        self.clients = {}
        self.start_time = int(time.time())
        self.filename = filename
        self.initialize_json_file(server_password)

    def initialize_json_file(self, server_password):
        """Cria o ficheiro "clients.json" quando é criado uma instância de Clients"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                file.write(enc.encrypt_file("{}", server_password))

    def add_client(self, client_id, client_ip, client_port, request_id, password, server_password):
        """Função que adiciona um cliente ao dicionário e ao arquivo JSON"""
        client = self.clients.get(client_id)
        if client:
            # Caso o cliente já exista, verifica se o pedido já existe
            has_previous_request = any(request[0] == request_id for request in client.requests)
            if not has_previous_request:
                client.add_request(request_id, int(time.time()) - self.start_time)
        else:
            # Caso o cliente ainda não exista, adiciona um objeto Client_Registration com os devidos dados e de seguida adiciona ao dicionário de clientes
            client = Client_Registration(client_id, client_ip, client_port, password)
            client.add_request(request_id, int(time.time()) - self.start_time)
            self.clients[client_id] = client

        self.save_to_json(server_password)


    def save_to_json(self, server_password):
        """Guarda todas as entradas dos clientes no arquivo JSON"""
        data = {}
        for client_id, client in self.clients.items():
            data[client_id] = {
                'client_ip': client.client_ip,
                'client_port': client.client_port,
                'password': client.password,
                'requests': []
            }
            for request in client.requests:
                request_id, timestamp = request
                data[client_id]['requests'].append({
                    'request_id': request_id,
                    'timestamp': timestamp
                })

        encrypted_data = enc.encrypt_string(json.dumps(data), server_password)

        with open(self.filename, 'wb') as file:
            file.write(encrypted_data)

    def can_send_same_requestID(self, client_id, request_id, max_time, client_password):
        """Verifica se o pedido (identificado por request_id) do cliente (identificado por client_id) é enviado durante o intervalo
        de tempo max_time. Caso ainda esteja dentro do intervalo, retorna falso, caso contrário, retorna true 
        Além disso, o cliente terá de enviar a sua password igual à primeira que definiu"""
        if client_id not in self.clients:
            return True
        client = self.clients[client_id]
        if client.password == client_password:
            has_previous_request = any(request[0] == request_id for request in client.requests)
            current_time = int(time.time()) - self.start_time
            if not has_previous_request:
                client.add_request(request_id, current_time)
                return True
            latest_timestamp = client.get_latest_timestamp(request_id)
            time_difference = current_time - latest_timestamp
            return time_difference >= int(max_time)
        else:
            return False