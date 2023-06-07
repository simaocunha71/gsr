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
import communication.pdu as pdu

import datetime

def get_date_and_time_expiration(ttl):
    current_datetime = datetime.datetime.now()
    
    expiration_date = current_datetime + datetime.timedelta(seconds=ttl)
    
    # Obter os componentes de data e hora
    YY = expiration_date.year 
    MM = expiration_date.month
    DD = expiration_date.day
    HH = expiration_date.hour
    MM = expiration_date.minute
    SS = expiration_date.second
    
    # Calcular os valores no formato desejado
    expiration_date_val = YY * 104 + MM * 102 + DD
    expiration_time_val = HH * 104 + MM * 102 + SS
    
    return (expiration_date_val, expiration_time_val)




def is_keygen_request(pdu_received):
    """Verifica se o último número é 0 e se a lista de ids é maior do que 0 (true se se verificar, false caso contrário)"""
    instance_elements_list = pdu_received.get_instance_elements_list()
    return instance_elements_list[-1] == 0 and len(instance_elements_list) > 0


def fill_initially_MIB(configurations):
    """Cria e preenche o MIB com chaves e valores aleatórios"""
    # System content
    K = configurations.get_n_matrix()
    updating_interval = configurations.get_update_interval()
    max_keys = configurations.get_n_max_entries()
    ttl = configurations.get_max_store_time()

    # Config content
    master_key = configurations.get_master_key()
    fst_ascii_code = configurations.get_min()
    _max = configurations.get_max()
    number_of_chars = _max - fst_ascii_code + 1

    return main.MIB("MIB/mib.mib", K, updating_interval, max_keys, ttl, master_key, fst_ascii_code, number_of_chars)



class Agent:
    def __init__(self):
        self.n_lock          = threading.Lock() # Lock para a variável "n_updated_times"
        self.id_lock         = threading.Lock() # Lock para a variável "idRequest"
        self.n_updated_times = 0                # Nº de vezes que agente atualizou a matriz Z
        self.bufferSize      = 4096             # Tamanho do buffer do socket entre agente e gestor
        self.HOST            = 'localhost'      # Endereço do socket
        self.current_time    = None             # Início em segundos do funcionamento do agente (sem valor aqui)
        
    def get_timestamp(current_time):
        """Devolve o timestamp S sempre que se chama esta função - nº de segundos passados em que o agente iniciou/reiniciou"""
        return int(time.time() - float(current_time))
    
    def get_n_inc_n_updated_times(self):
        """Função que faz controlo de concorrência na leitura e no incremento da variável "n_updated_times" """
        self.n_lock.acquire()
        n_updated_times = self.n_updated_times
        self.n_updated_times += 1
        self.n_lock.release()
        return n_updated_times

    def handle_request(self, sock, data, addr, F, mib):
        """Função que trata do pedido de um manager"""

        #TODO: 
        """
        - Na criação de uma chave, saber que valor colocar no key_visibility (neste momento está a 2)
        - Impedir o manager de usar o mesmo id_request de X em X segundos (ver enunciado)
        - Implementar comandos set (exceto o de criação de chave que ja está feito) e get
        - No comando response, adicionar corretamente a lista de instancias (adicionar os novos valores dependendo das primitivas)
        - No comando response, adicionar corretamente a lista de erros (adicionar os novos valores dependendo das primitivas)
        - Nao escrever novas chaves se o nº de chaves já existentes for o maximo permitido
        - Arranjar forma de como cliente vai estar ligado para consultar o valor da chave
            -> segundo o enunciado, cliente faz set() e depois faz get()
        """

        # Imprime a mensagem recebida
        pdu_received = pdu.PDU.decode(data)
        pdu_received.to_string()

        S = Agent.get_timestamp(self.current_time)

        client_ip = addr[0]

        if is_keygen_request(pdu_received) == True:
            # Criação das matrizes fm e Z (inicial)
            fm_matrix = utils.create_fm_matrix(F.min,F.max)
            Z = matrix.get_matrix(F.n_matrix, F.master_key, fm_matrix, S) 

            # Atualização de matrizes e geração da chave
            update_matrix.update_matrix_Z(F.n_matrix, Z, F.update_interval)

            n_updated_times = self.get_n_inc_n_updated_times()
            line_index, col_index = utils.get_random_indexes(n_updated_times, Z, F.n_matrix)

            key = keygen.generate_key(Z, line_index, col_index, fm_matrix)

            date = get_date_and_time_expiration(int(F.max_store_time))

            mib.get_group(3).get_table().create_entry("MIB/mib.mib", key, client_ip, date[0], date[1], 2)
            mib.to_string()
            
            #TODO: Adicionar uma nova linha à MIB e preencher os valores da PDU de resposta (apenas os necessários (ou todos???))


        elif pdu_received.get_primitive_type() == 1: #get
            #Verificar se pedido está na MIB e verificar se acontecem os erros que estão no enunciado
            pass
        elif pdu_received.get_primitive_type() == 2: #set
            #Verificar se pedido está na MIB e verificar se acontecem os erros que estão no enunciado
            pass
        else:
            #TODO: Criar erro de primitiva nao suportada e adicion+a-la à pdu de resposta
            pass


        #mib.to_string() #NOTE: DEBUG

        primitive_type = 0 #É valor tomado pelas responses

        #TODO: tratar dos instance_elements_list (e instance_elements_size)
        #TODO: tratar dos errors_elements_list (e errors_elements_size)
        
        #NOTE: No TP1, este valores vão ficar assim
        security_level=0
        n_security_parameters_number=0
        n_security_parameters_list=[]

        pdu_response = pdu.PDU(pdu_received.get_request_id(), primitive_type, 
                               pdu_received.get_instance_elements_size(), pdu_received.get_instance_elements_list(), # NOTE: Provisorio!
                               pdu_received.get_error_elements_size(), pdu_received.get_error_elements_list(),       # NOTE: Provisorio!
                               security_level, n_security_parameters_number, n_security_parameters_list) 

        sock.sendto(pdu_response.encode(), addr)


if __name__ == "__main__":
    print("----------Agent started----------")

    ag = Agent()

    # Leitura do ficheiro
    F = configurations.Configurations("config.conf") 

    mib = fill_initially_MIB(F)

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
        t = threading.Thread(target=ag.handle_request, args=(sock, data, addr, F, mib))
        t.start()

