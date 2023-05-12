"""Módulo que implementa o agente"""

import model.configurations as configurations
import MIB.main as main
import keys.main as keygen
import keys.matrix as matrix
import keys.update_matrix as update_matrix
import keys.utils as utils
import time
import socket
import threading

class Agent:
    def __init__(self):
        self.n_lock = threading.Lock()     # Lock para a variável "n_updated_times"
        self.id_lock = threading.Lock()    # Lock para a variável "idRequest"
        self.n_updated_times = 0           # Nº de vezes que agente atualizou a matriz Z
        self.bufferSize      = 4096        # Tamanho do buffer do socket entre agente e gestor
        self.HOST            = 'localhost' # Endereço do socket
        self.IDRequests      = 0           # ID de pedidos respondidos (a começar em 0)
        self.current_time    = None        # Início em segundos do funcionamento do agente (sem valor aqui)

    def get_timestamp(current_time):
        """Devolve o timestamp S sempre que se chama esta função - nº de segundos passados em que o agente iniciou/reiniciou"""
        return int(time.time() - float(current_time))

    def get_n_inc_idRequest(self):
        """Função que faz controlo de concorrência na leitura e no incremento da variável "idRequest" """
        self.id_lock.acquire()
        idRequest = self.IDRequests
        self.IDRequests += 1
        self.id_lock.release()
        return idRequest 
    
    def get_n_inc_n_updated_times(self):
        """Função que faz controlo de concorrência na leitura e no incremento da variável "n_updated_times" """
        self.n_lock.acquire()
        n_updated_times = self.n_updated_times
        self.n_updated_times += 1
        self.n_lock.release()
        return n_updated_times

    def handle_request(self, sock, data, addr, F):
        """Função que trata do pedido de um manager"""

        # Imprime a mensagem recebida
        print(f"Recebido de {addr}: {data.decode()}")  

        S = Agent.get_timestamp(self.current_time)

        # Criação das matrizes fm e Z (inicial)
        fm_matrix = utils.create_fm_matrix()
        Z = matrix.get_matrix(F.n_matrix, F.master_key, fm_matrix, S) 
    
        # Atualização de matrizes e geração da chave
        update_matrix.update_matrix_Z(F.n_matrix, Z, F.update_interval)

        n_updated_times = self.get_n_inc_n_updated_times()
        line_index, col_index = utils.get_random_indexes(n_updated_times, Z, F.n_matrix)
            
        idRequest = self.get_n_inc_idRequest()
        key = keygen.generate_key(Z, line_index, col_index, fm_matrix, idRequest)
        print(f"Created key \"{key}\"")

        # Envia a resposta para o cliente
        sock.sendto(key.encode(), addr)  


if __name__ == "__main__":
    print("----------Agent started----------")

    ag = Agent()

    # Leitura do ficheiro
    F = configurations.Configurations("config.conf") 

    # Criação do Socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Associa o socket ao endereço e porta especificados
    sock.bind((ag.HOST, F.port))

    print(f"Servidor UDP ouvindo em {ag.HOST}:{F.port}...")

    # Início da contagem do tempo de execução do agente
    ag.current_time = time.time()
    
    while True:
        data, addr = sock.recvfrom(ag.bufferSize)

        # Cria uma nova thread para tratar a mensagem recebida
        t = threading.Thread(target=ag.handle_request, args=(sock, data, addr, F))
        t.start()

