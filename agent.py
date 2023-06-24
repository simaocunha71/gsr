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
import sys
import security.encrypted_data as enc
import security.checksum as ch

"""
Exemplos de comandos:
- inicializar agente com ficheiro de registo de clientes encriptado:
python .\agent.py server_gsr -encrypt

- Agente apenas desencripta conteudo do ficheiro json com a password
python .\agent.py server_gsr -decrypt
"""

def is_valid_checksum(client_username, client_password, client_checksum):
    """Verifica se o checksum recebido é o correto - calcular-se-á novo checksum e comparamos com o recebido"""
    client_checksum_dec = enc.decrypt_string(client_checksum, client_password)

    checksum = ch.get_checksum(client_username, client_password)

    return client_checksum_dec == checksum

def get_date_and_time_expiration(ttl):
    """Função que calcula o expiration_date e o expiration_time de cada entrada da tabela"""
    current_datetime = datetime.datetime.now()
    expiration_date = current_datetime + datetime.timedelta(seconds=ttl)
    
    # Calcular o valor em segundos para expiration_date
    expiration_date_val = int(expiration_date.timestamp())
    
    # Calcular o valor em segundos para expiration_time
    expiration_time_val = int((expiration_date - expiration_date.replace(hour=0, minute=0, second=0)).total_seconds())
    
    return (expiration_date_val, expiration_time_val)


def send_error_PDU(pdu_received, title, socket, addr, primitive_type, n_security_parameters_number, n_security_parameters_list):
    """Função que envia a PDU com o devido código de erro (codigo que está representado numa string ilustrativa)"""
    errors_list = pdu_received.get_error_elements_list()
    errors_list.append(title)
    pdu_response = pdu.PDU(pdu_received.get_request_id(), primitive_type, 
                           pdu_received.get_instance_elements_size(), pdu_received.get_instance_elements_list(),
                           len(errors_list), errors_list, n_security_parameters_number, n_security_parameters_list) 
    socket.sendto(pdu_response.encode(), addr)

def is_keygen_request(pdu_received):
    """Verifica se se trata de um pedido de geração de chaves:
     -> último número é 0 e se a lista de ids é maior do que 0 e menor que 4 (true se se verificar, false caso contrário)"""
    instance_elements_list = pdu_received.get_instance_elements_list()
    return instance_elements_list[-1] == 0 and len(instance_elements_list) > 0 and len(instance_elements_list) <= 4


def fill_initially_MIB(configurations):
    """Cria e preenche o MIB com os valores correspondentes para cada grupo da MIB"""
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
    
    def handle_request(self, sock, data, addr, F, mib, client_registry, server_password):
        """Função que trata do pedido de um manager"""

        pdu_received = pdu.PDU.decode(data)
        #pdu_received.to_string() #NOTE: Caso queiramos observar o que o agente recebeu do manager, retirar comentário à linha

        S = Agent.get_timestamp(self.current_time)

        client_ip = addr[0]

        primitive_type = 0 #É valor tomado pelas responses

        #Obtenção do client_id/client_username, password e checksum enviados pelo cliente através do campo da PDU 
        client_username = pdu_received.get_n_security_parameters_list()[0]
        client_username = enc.decrypt_string(client_username, server_password)
        client_password = pdu_received.get_n_security_parameters_list()[1]
        client_checksum = pdu_received.get_n_security_parameters_list()[2]

        #Valida o checksum recebido pelo cliente e compara com o checksum devidamente calculado
        if(is_valid_checksum(client_username, client_password, client_checksum) == True):
            
            #Verificação se o cliente que enviou um pedido enviou um request_id de um outro pedido seu há menos de max_store_time segundos
            #Além disso, o cliente terá de enviar a sua password igual à primeira que definiu
            if(client_registry.can_send_same_requestID(client_username, pdu_received.get_request_id(), F.max_store_time, client_password) == True):

                #Nesta fase, o cliente é válido e será registado ao ficheiro de clientes
                client_registry.add_client(client_username, client_ip, F.port, pdu_received.get_request_id(), client_password, "clients.json", server_password)

                #Não permitir que manager use lista de oids de tamanho maior que 4
                if(pdu_received.get_instance_elements_size() <= 4): 

                    #Verificação de pedido de geração de chave
                    if is_keygen_request(pdu_received) == True:

                        #Verificação se nº de entradas da tabela não excede o nº fixado no ficheiro de configuração
                        if int(mib.get_group(3).get_table().dataNumberOfValidKeys) < int(F.n_max_entries): 

                            #Criação das matrizes fm e Z (inicial)
                            fm_matrix = utils.create_fm_matrix(F.min,F.max)
                            Z = matrix.get_matrix(F.n_matrix, F.master_key, fm_matrix, S) 

                            #Atualização de matrizes e geração da chave
                            update_matrix.update_matrix_Z(F.n_matrix, Z, F.update_interval)
                            n_updated_times = self.get_n_inc_n_updated_times()
                            line_index, col_index = utils.get_random_indexes(n_updated_times, Z, F.n_matrix)
                            key = keygen.generate_key(Z, line_index, col_index, fm_matrix)
                            date = get_date_and_time_expiration(int(F.max_store_time))

                            #Criação de uma nova entrada na tabela com a chave gerada
                            key_id_generated = mib.get_group(3).get_table().create_entry("MIB/mib.mib", key, client_ip, date[0], date[1], 0)

                            #Envio da resposta ao cliente: adicionará o ID da chave à instance_elements_list da PDU de resposta
                            list_elements = pdu_received.get_instance_elements_list()
                            list_elements.append(key_id_generated)
                            pdu_response = pdu.PDU(pdu_received.get_request_id(), primitive_type, 
                                                   len(list_elements), list_elements,
                                                   pdu_received.get_error_elements_size(), pdu_received.get_error_elements_list(),
                                                    pdu_received.get_n_security_parameters_number(), 
                                                   pdu_received.get_n_security_parameters_list()) 
                            sock.sendto(pdu_response.encode(), addr)
                        else:
                            """Erro #1: Pedido de criação de chave mas MIB não suporta a adição de mais chaves"""
                            send_error_PDU(pdu_received, "MIB FULL", sock, addr, primitive_type,
                                            pdu_received.get_n_security_parameters_number(), 
                                           pdu_received.get_n_security_parameters_list()) 

                    #Verificação de pedido de get
                    elif pdu_received.get_primitive_type() == 1:
                        #Aqui far-se-á acessos sucessivos a estruturas de dados da MIB.
                        #Caso haja algum erro, é imediatamente enviado uma resposta com o referido erro (ignorando eventuais outros erros)
                        value_to_send = ""
                        index_list = pdu_received.get_instance_elements_list()
                        try:
                            group_got = mib.get_group(index_list[0])
                        except Exception as _:
                            """Erro #2: Grupo acedido da MIB não existe"""
                            send_error_PDU(pdu_received, "NON EXISTENT GROUP", sock, addr, primitive_type,
                                            pdu_received.get_n_security_parameters_number(), 
                                           pdu_received.get_n_security_parameters_list()) 

                        if (len(index_list) == 2):
                            #Get para objetos do grupo system ou config
                            try:
                                value_to_send = group_got.get_object(index_list[1]).get_value()
                            except Exception as _:
                                """Erro #3: Objeto não existe no grupo System ou Config"""
                                send_error_PDU(pdu_received, "NON EXISTENT VALUE (Sys/Conf)", sock, addr, primitive_type,
                                                pdu_received.get_n_security_parameters_number(), 
                                               pdu_received.get_n_security_parameters_list()) 

                        elif (len(index_list) == 4):
                            #Get para objetos do grupo data
                            try:
                                entry_got = group_got.get_table().get_object_entry(index_list[2])
                            except Exception as _:
                                """Erro #4: Entrada da MIB a aceder não existe"""
                                send_error_PDU(pdu_received, "NON EXISTENT ENTRY", sock, addr, primitive_type,
                                                pdu_received.get_n_security_parameters_number(), 
                                               pdu_received.get_n_security_parameters_list()) 
                            try:
                                value_to_send = entry_got.get_field(index_list[3]).get_value()
                            except Exception as _:
                                """Erro #5: Campo da entrada acedida na tabela não existe"""
                                send_error_PDU(pdu_received, "NON EXISTENT OBJECT IN ENTRY", sock, addr, primitive_type,
                                                pdu_received.get_n_security_parameters_number(), 
                                               pdu_received.get_n_security_parameters_list())  

                        #Não foi detetado erro nenhum: adicionará o valor que queremos saber à instance_elements_list da PDU de resposta e envia resposta ao manager
                        index_list.append(value_to_send)
                        pdu_response = pdu.PDU(pdu_received.get_request_id(), primitive_type, 
                                               len(index_list), index_list,
                                               pdu_received.get_error_elements_size(), pdu_received.get_error_elements_list(),
                                                pdu_received.get_n_security_parameters_number(), 
                                               pdu_received.get_n_security_parameters_list()) 
                        sock.sendto(pdu_response.encode(), addr)

                    #Verificação de pedido de set
                    elif pdu_received.get_primitive_type() == 2:
                        #Aqui far-se-á acessos sucessivos a estruturas de dados da MIB.
                        #Caso haja algum erro, é imediatamente enviado uma resposta com o referido erro (ignorando eventuais outros erros)
                        value_to_send = ""
                        index_list = pdu_received.get_instance_elements_list()
                        try:
                            group_got = mib.get_group(index_list[0])
                        except Exception as _:
                            """Erro #2: Grupo acedido da MIB não existe"""
                            send_error_PDU(pdu_received, "NON EXISTENT GROUP", sock, addr, primitive_type,
                                            pdu_received.get_n_security_parameters_number(), 
                                           pdu_received.get_n_security_parameters_list()) 
                        if (len(index_list) == 3):
                            #Set aos grupos system e config
                            try:
                                object_got = group_got.get_object(index_list[1])
                            except Exception as _:
                                """Erro #3: Objeto não existe no grupo System ou Config"""
                                send_error_PDU(pdu_received, "NON EXISTENT VALUE (Sys/Conf)", sock, addr, primitive_type,
                                                pdu_received.get_n_security_parameters_number(), 
                                               pdu_received.get_n_security_parameters_list()) 
                            try:
                                value_to_send = object_got.set_value(index_list[-1])
                            except Exception as _:
                                """Erro #6: Valor a adicionar não é do mesmo tipo que o estipulado para o objeto"""
                                send_error_PDU(pdu_received, "VALUE WITH DIFFERENT TYPE", sock, addr, primitive_type,
                                                pdu_received.get_n_security_parameters_number(), 
                                               pdu_received.get_n_security_parameters_list()) 
                        elif (len(index_list) == 5):
                            #Set ao grupo data
                            try:
                                entry_got = group_got.get_table().get_object_entry(index_list[2])
                            except Exception as _:
                                """Erro #4: Entrada da MIB a aceder não existe"""
                                send_error_PDU(pdu_received, "NON EXISTENT ENTRY", sock, addr, primitive_type,
                                                pdu_received.get_n_security_parameters_number(), 
                                               pdu_received.get_n_security_parameters_list()) 
                            try:
                                field_got = entry_got.get_field(index_list[3])
                            except Exception as _:
                                """Erro #5: Campo da entrada acedida na tabela não existe"""
                                send_error_PDU(pdu_received, "NON EXISTENT OBJECT IN ENTRY", sock, addr, primitive_type,
                                                pdu_received.get_n_security_parameters_number(), 
                                               pdu_received.get_n_security_parameters_list()) 
                            try:
                                value_to_send = field_got.set_value(index_list[-1])
                            except Exception as _:
                                """Erro #6: Valor a adicionar não é do mesmo tipo que o estipulado para o objeto"""
                                send_error_PDU(pdu_received, "VALUE WITH DIFFERENT TYPE", sock, addr, primitive_type,
                                                pdu_received.get_n_security_parameters_number(), 
                                               pdu_received.get_n_security_parameters_list()) 

                        #Não foi detetado erro nenhum: a lista instance_elements_list da PDU de resposta ficará igual e envia resposta ao manager
                        pdu_response = pdu.PDU(pdu_received.get_request_id(), primitive_type, 
                                               len(index_list), index_list,
                                               pdu_received.get_error_elements_size(), pdu_received.get_error_elements_list(),
                                                pdu_received.get_n_security_parameters_number(), 
                                               pdu_received.get_n_security_parameters_list()) 
                        mib.to_string()
                        sock.sendto(pdu_response.encode(), addr)
                    else:
                        """Erro #7: Primitiva efetuada não corresponde a get ou set"""
                        send_error_PDU(pdu_received, "PRIMITIVE NOT SUPPORTED", sock, addr, primitive_type,
                                        pdu_received.get_n_security_parameters_number(), 
                                       pdu_received.get_n_security_parameters_list()) 
                else:
                    """Erro #8: Numero de OIDS incorretos"""
                    send_error_PDU(pdu_received, "OIDs len INCORRECT", sock, addr, primitive_type,
                                    pdu_received.get_n_security_parameters_number(), 
                                   pdu_received.get_n_security_parameters_list()) 
            else:
                """Erro #9: Manager não pode enviar o mesmo request id dentro de V segundos ou a password inserida não é igual à primeira"""
                send_error_PDU(pdu_received, "SAME REQUEST_ID SENT IN V SECONDS | WRONG PASSWORD", sock, addr, primitive_type,
                                pdu_received.get_n_security_parameters_number(), 
                               pdu_received.get_n_security_parameters_list()) 
            mib.to_string()
        else:
            """Erro #10: Checksum mostra que cliente não é quem diz ser"""
            send_error_PDU(pdu_received, "WRONG CHECKSUM", sock, addr, primitive_type,
                           pdu_received.get_n_security_parameters_number(), 
                           pdu_received.get_n_security_parameters_list()) 


if __name__ == "__main__":
    print("----------Agent started----------")
    # Verificar a senha fornecida na linha de comandos
    server_password = "server_gsr"  # Password esperada

    if len(sys.argv) == 3 and sys.argv[1] == server_password and sys.argv[2] == "-encrypt":
        ag = Agent()

        # Leitura do ficheiro
        F = configurations.Configurations("config.conf") 

        # Povoa os grupos da MIB
        mib = fill_initially_MIB(F)

        # Criação do Socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Associa o socket ao endereço e porta especificados
        sock.bind((ag.HOST, F.port))

        print(f"Servidor UDP ouvindo em {ag.HOST}:{F.port}...")

        enc.encrypt_file("clients.json", sys.argv[1])
        
        client_registry = client_registry.Clients("clients.json", server_password)

        # Início da contagem do tempo de execução do agente
        ag.current_time = time.time()

        thread_running = True
        while True:
            data, addr = sock.recvfrom(ag.bufferSize)
            # Cria uma nova thread para tratar a mensagem recebida
            t = threading.Thread(target=ag.handle_request, args=(sock, data, addr, F, mib, client_registry, server_password))
            t.start()
    elif len(sys.argv) == 3 and sys.argv[1] == server_password and sys.argv[2] == "-decrypt":
        #Caso o agente queira desencriptar o ficheiro clients.json, poderá colocar a flag "-decrypt"
        enc.decrypt_file("clients.json", server_password)
    else:
        print("Password inválida!")
