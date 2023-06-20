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
import communication.client_registry as client_registry
import datetime

def get_date_and_time_expiration(ttl):
    """Função que calcula o expiration_date e o expiration_time de cada entrada da tabela"""
    current_datetime = datetime.datetime.now()
    expiration_date = current_datetime + datetime.timedelta(seconds=ttl)
    
    # Calcular o valor em segundos para expiration_date
    expiration_date_val = int(expiration_date.timestamp())
    
    # Calcular o valor em segundos para expiration_time
    expiration_time_val = int((expiration_date - expiration_date.replace(hour=0, minute=0, second=0)).total_seconds())
    
    return (expiration_date_val, expiration_time_val)


def send_error_PDU(pdu_received, title, socket, addr, primitive_type, security_level, n_security_parameters_number, n_security_parameters_list):
    """Função que envia a PDU com o devido código de erro"""
    errors_list = pdu_received.get_error_elements_list()
    errors_list.append(title)
    pdu_response = pdu.PDU(pdu_received.get_request_id(), primitive_type, 
                           pdu_received.get_instance_elements_size(), pdu_received.get_instance_elements_list(),
                           len(errors_list), errors_list,  
                           security_level, n_security_parameters_number, n_security_parameters_list) 
    socket.sendto(pdu_response.encode(), addr)

def is_keygen_request(pdu_received):
    """Verifica se o último número é 0 e se a lista de ids é maior do que 0 e menor que 4 (true se se verificar, false caso contrário)"""
    instance_elements_list = pdu_received.get_instance_elements_list()
    return instance_elements_list[-1] == 0 and len(instance_elements_list) > 0 and len(instance_elements_list) <= 4


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
        self.n_lock           = threading.Lock() # Lock para a variável "n_updated_times"
        self.n_updated_times  = 0                # Nº de vezes que agente atualizou a matriz Z
        self.bufferSize       = 8192             # Tamanho do buffer do socket entre agente e gestor
        self.HOST             = 'localhost'      # Endereço do socket
        self.current_time     = None             # Início em segundos do funcionamento do agente (sem valor aqui)
        
        
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
    
    def handle_request(self, sock, data, addr, F, mib, client_registry):
        """Função que trata do pedido de um manager"""

        #TODO: 
        """
        - Remover entradas da tabela (que passam ao estado "expired"???) (DICA: ver o que fazer com os estados da chave)
        """

        # Imprime a mensagem recebida
        pdu_received = pdu.PDU.decode(data)
        #pdu_received.to_string()

        S = Agent.get_timestamp(self.current_time)

        client_ip = addr[0]

        primitive_type = 0 #É valor tomado pelas responses

        #NOTE: No TP1, este valores vão ficar assim
        security_level=0
        n_security_parameters_number=0
        n_security_parameters_list=[]

        client_password = pdu_received.get_n_security_parameters_list()[0]

        if(client_registry.can_send_same_requestID(client_password, pdu_received.get_request_id(), F.max_store_time) == True):
            client_registry.add_client(client_ip, F.port, pdu_received.get_request_id(), client_password)
            if(pdu_received.get_instance_elements_size() <= 4): #Não permitir que manager use lista de oids de tamanho maior que 4
                if is_keygen_request(pdu_received) == True:
                    if int(mib.get_group(3).get_table().dataNumberOfValidKeys) < int(F.n_max_entries): # Nº de entradas da tabela não excede o nº fixado no ficheiro de configuração
                        # Criação das matrizes fm e Z (inicial)
                        fm_matrix = utils.create_fm_matrix(F.min,F.max)
                        Z = matrix.get_matrix(F.n_matrix, F.master_key, fm_matrix, S) 
                        # Atualização de matrizes e geração da chave
                        update_matrix.update_matrix_Z(F.n_matrix, Z, F.update_interval)
                        n_updated_times = self.get_n_inc_n_updated_times()
                        line_index, col_index = utils.get_random_indexes(n_updated_times, Z, F.n_matrix)
                        key = keygen.generate_key(Z, line_index, col_index, fm_matrix)
                        date = get_date_and_time_expiration(int(F.max_store_time))
                        key_id_generated = mib.get_group(3).get_table().create_entry("MIB/mib.mib", key, client_ip, date[0], date[1], 0)
                        #mib.to_string()
                        list_elements = pdu_received.get_instance_elements_list()
                        list_elements.append(key_id_generated)
                        pdu_response = pdu.PDU(pdu_received.get_request_id(), primitive_type, 
                                               len(list_elements), list_elements,
                                               pdu_received.get_error_elements_size(), pdu_received.get_error_elements_list(),
                                               security_level, n_security_parameters_number, n_security_parameters_list) 
                        sock.sendto(pdu_response.encode(), addr)
                    else:
                        """Erro #1: Pedido de criação de chave mas MIB não suporta a adição de mais chaves"""
                        send_error_PDU(pdu_received, "MIB FULL", sock, addr, primitive_type,
                                       security_level, n_security_parameters_number, n_security_parameters_list)
                elif pdu_received.get_primitive_type() == 1: #get
                    value_to_send = ""
                    index_list = pdu_received.get_instance_elements_list()
                    try:
                        group_got = mib.get_group(index_list[0])
                    except Exception as _:
                        """Erro #2: Grupo acedido da MIB não existe"""
                        send_error_PDU(pdu_received, "NON EXISTENT GROUP", sock, addr, primitive_type,
                                       security_level, n_security_parameters_number, n_security_parameters_list)
                    if (len(index_list) == 2):
                        #Get para objetos do grupo system ou config
                        try:
                            value_to_send = group_got.get_object(index_list[1]).get_value()
                        except Exception as _:
                            """Erro #3: Objeto não existe no grupo System ou Config"""
                            send_error_PDU(pdu_received, "NON EXISTENT VALUE (Sys/Conf)", sock, addr, primitive_type,
                                           security_level, n_security_parameters_number, n_security_parameters_list)
                    elif (len(index_list) == 4):
                        #Get para objetos do grupo data
                        try:
                            entry_got = group_got.get_table().get_object_entry(index_list[2])
                        except Exception as _:
                            """Erro #4: Entrada da MIB a aceder não existe"""
                            send_error_PDU(pdu_received, "NON EXISTENT ENTRY", sock, addr, primitive_type,
                                           security_level, n_security_parameters_number, n_security_parameters_list)
                        try:
                            value_to_send = entry_got.get_field(index_list[3]).get_value()
                        except Exception as _:
                            """Erro #5: Campo da entrada acedida na tabela não existe"""
                            send_error_PDU(pdu_received, "NON EXISTENT OBJECT IN ENTRY", sock, addr, primitive_type,
                                           security_level, n_security_parameters_number, n_security_parameters_list)                    
                    #Não foi detetado erro nenhum
                    index_list.append(value_to_send)
                    pdu_response = pdu.PDU(pdu_received.get_request_id(), primitive_type, 
                                           len(index_list), index_list,
                                           pdu_received.get_error_elements_size(), pdu_received.get_error_elements_list(),
                                           security_level, n_security_parameters_number, n_security_parameters_list) 
                    #mib.to_string()
                    sock.sendto(pdu_response.encode(), addr)
                elif pdu_received.get_primitive_type() == 2: #set
                    value_to_send = ""
                    index_list = pdu_received.get_instance_elements_list()
                    try:
                        group_got = mib.get_group(index_list[0])
                    except Exception as _:
                        """Erro #2: Grupo acedido da MIB não existe"""
                        send_error_PDU(pdu_received, "NON EXISTENT GROUP", sock, addr, primitive_type,
                                       security_level, n_security_parameters_number, n_security_parameters_list)
                    if (len(index_list) == 3):
                        #Set aos grupos system e config
                        try:
                            object_got = group_got.get_object(index_list[1])
                        except Exception as _:
                            """Erro #3: Objeto não existe no grupo System ou Config"""
                            send_error_PDU(pdu_received, "NON EXISTENT VALUE (Sys/Conf)", sock, addr, primitive_type,
                                           security_level, n_security_parameters_number, n_security_parameters_list)
                        try:
                            value_to_send = object_got.set_value(index_list[-1])
                        except Exception as _:
                            """Erro #6: Valor a adicionar não é do mesmo tipo que o estipulado para o objeto"""
                            send_error_PDU(pdu_received, "VALUE WITH DIFFERENT TYPE", sock, addr, primitive_type,
                                           security_level, n_security_parameters_number, n_security_parameters_list)
                    elif (len(index_list) == 5):
                        #Set ao grupo data
                        try:
                            entry_got = group_got.get_table().get_object_entry(index_list[2])
                        except Exception as _:
                            """Erro #4: Entrada da MIB a aceder não existe"""
                            send_error_PDU(pdu_received, "NON EXISTENT ENTRY", sock, addr, primitive_type,
                                           security_level, n_security_parameters_number, n_security_parameters_list) 
                        try:
                            field_got = entry_got.get_field(index_list[3])
                        except Exception as _:
                            """Erro #5: Campo da entrada acedida na tabela não existe"""
                            send_error_PDU(pdu_received, "NON EXISTENT OBJECT IN ENTRY", sock, addr, primitive_type,
                                           security_level, n_security_parameters_number, n_security_parameters_list)
                        try:
                            value_to_send = field_got.set_value(index_list[-1])
                        except Exception as _:
                            """Erro #6: Valor a adicionar não é do mesmo tipo que o estipulado para o objeto"""
                            send_error_PDU(pdu_received, "VALUE WITH DIFFERENT TYPE", sock, addr, primitive_type,
                                           security_level, n_security_parameters_number, n_security_parameters_list)
                    #Não foi detetado erro nenhum
                    pdu_response = pdu.PDU(pdu_received.get_request_id(), primitive_type, 
                                           len(index_list), index_list,
                                           pdu_received.get_error_elements_size(), pdu_received.get_error_elements_list(),
                                           security_level, n_security_parameters_number, n_security_parameters_list) 
                    mib.to_string()
                    sock.sendto(pdu_response.encode(), addr)
                else:
                    """Erro #7: Primitiva efetuada não corresponde a get ou set"""
                    send_error_PDU(pdu_received, "PRIMITIVE NOT SUPPORTED", sock, addr, primitive_type,security_level, n_security_parameters_number, n_security_parameters_list)
            else:
                """Erro #8: Numero de OIDS incorretos"""
                send_error_PDU(pdu_received, "OIDs len INCORRECT", sock, addr, primitive_type,security_level, n_security_parameters_number, n_security_parameters_list)
        else:
            """Erro #9: Manager não pode enviar o mesmo request id dentro de V segundos"""
            send_error_PDU(pdu_received, "SAME REQUEST_ID SENT IN V SECONDS", sock, addr, primitive_type,security_level, n_security_parameters_number, n_security_parameters_list)
        mib.to_string()
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

    client_registry = client_registry.Clients()

    # Início da contagem do tempo de execução do agente
    ag.current_time = time.time()
    
    while True:
        data, addr = sock.recvfrom(ag.bufferSize)
        # Cria uma nova thread para tratar a mensagem recebida
        t = threading.Thread(target=ag.handle_request, args=(sock, data, addr, F, mib, client_registry))
        t.start()

