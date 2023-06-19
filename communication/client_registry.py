import communication.utils as utils
import agent as agent
import os
import csv
import threading
import json
import time

class Client_Registration:
    def __init__(self, client_ip, client_port, client_id, password):
        self.client_ip = client_ip
        self.client_port = client_port
        self.client_id = client_id
        self.password = password
        self.requests = []

    def add_request(self, request_id, timestamp):
        self.requests.append([request_id, timestamp])

    def get_latest_timestamp(self, request_id):
        timestamps = [timestamp for request, timestamp in self.requests if request == request_id]
        if timestamps:
            return max(timestamps)
        return 0

    def to_string(self):
        result = ""
        result += f"Client ID: {self.client_id} | "
        result += f"Client Port: {self.client_port} | "
        result += f"Client IP: {self.client_ip} | "
        result += "Requests:\n"
        for request in self.requests:
            request_id, timestamp = request
            result += f"  Request ID: {request_id} | Timestamp: {timestamp}\n"
        result += f"Password: {self.password}\n"
        return result


class Clients:
    def __init__(self):
        self.clients = {}
        self.start_time = int(time.time())  # Registro do tempo inicial
        self.initialize_json_file()

    def initialize_json_file(self):
        if not os.path.exists("clients.json"):
            with open("clients.json", 'w') as file:
                file.write("{}")

    def add_client(self, client_ip, client_port, client_id, password):
        client = self.clients.get(password)
        if client:
            client.add_request(client_id, int(time.time()) - self.start_time)
        else:
            client = Client_Registration(client_ip, client_port, client_id, password)
            client.add_request(client_id, int(time.time()) - self.start_time)
            self.clients[password] = client
        self.save_to_json()

    def save_to_json(self):
        data = {}
        for client_password, client in self.clients.items():
            data[client_password] = {
                'client_ip': client.client_ip,
                'client_port': client.client_port,
                'password': client.password,
                'requests': client.requests
            }
        with open("clients.json", 'w') as file:
            json.dump(data, file, indent=4)

    def can_send_same_requestID(self, client_password, request_id, max_time):
        if client_password not in self.clients:
            print("Client does not exist.")
            return True 

        client = self.clients[client_password]
        latest_timestamp = client.get_latest_timestamp(request_id)  

        if latest_timestamp == 0:
            # Buscar o último timestamp válido para qualquer request_id
            last_valid_timestamp = max(timestamp for _, timestamp in client.requests)
            time_difference = int(time.time()) - self.start_time - last_valid_timestamp
            current_time = int(time.time()) - self.start_time  # Adicionado aqui
        else:
            current_time = int(time.time()) - self.start_time
            time_difference = current_time - latest_timestamp   

        print("=== Client Information ===")
        print(f"Client Password: {client_password}")
        print(f"Client IP: {client.client_ip}")
        print(f"Client Port: {client.client_port}")
        print(f"Latest Timestamp: {latest_timestamp}")
        print(f"Current Time: {current_time}")
        print(f"Time Difference: {time_difference}")
        print(f"Max Time: {max_time}")  

        return int(time_difference) < int(max_time)




