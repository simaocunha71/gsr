"""Módulo que implementa o manager"""
import socket
import sys
import communication.utils as comm_utils
import communication.pdu as pdu
import security.checksum as checksum
import security.encrypted_data as enc

"""
Comandos de exemplo:

- para criar uma chave:
python .\manager.py username password set 1 3.2.6.0

- para alterar valor:
python .\manager.py username password set 4 2.1 42
python .\manager.py username password set 7 3.2.4.2 nova_password       -> 7 é o ID do pedido e 4 é o ID da chave (cujo valor foi recebido aquando a criação de chave)

- para obter valor:
python .\manager.py username password get 12 2.1

"""


class Manager:
    def __init__(self):
        self.AGENT_HOST  = 'localhost' # Endereço do socket
        self.AGENT_PORT  = 2048        # Porta de comunicação (a mesma que a do agente)
        self.BUFFER_SIZE = 8192        # Buffer do socket para a comunicação


if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Use format: python manager.py [client_id] [password] [get/set] [request-id] [version-numbers] [new-value]")
        sys.exit(0)
    else:

        # Atribuição dos argumentos às respetivas variáveis
        client_id = sys.argv[1]
        password = sys.argv[2]
        action = sys.argv[3]
        request_id = sys.argv[4]
        version_numbers = sys.argv[5]
        version_numbers = comm_utils.parse_version_numbers(version_numbers) #Strings do tipo "1.2.3" passarão a ser [1,2,3]

        if action == "get":
            primitive_type = 1
        elif action == "set":
            #Quando é para criar uma entrada na MIB, 
            #a primitiva set permite que não haja novo elemento a adicionar deste que ultimo OID seja 0
            if len(version_numbers) > 0 and version_numbers[-1] == 0 and len(sys.argv) < 7: 
                #Pedido de geração de chave
                new_value = None
                primitive_type = 2
            else:
                #Pedido de set com um determinado valor
                if len(sys.argv) < 7:
                    print("Missing new_value argument for SET command")
                    sys.exit(0)
                new_value = sys.argv[6]
                primitive_type = 2
                version_numbers.append(new_value)
        else:
            print("Invalid action")
            sys.exit(0)

    mn = Manager()

    #Calculo do checksum do cliente;
    password_from_server = "server_gsr"
    checksum = checksum.get_checksum((client_id).encode(), password_from_server)

    n_security_parameters_list = []

    #Client_id encriptado com a password do servidor
    client_id = enc.encrypt_string(client_id, password_from_server)
    n_security_parameters_list.append(client_id)

    #Password vai em plain text (talvez não seja o mais adequado)
    n_security_parameters_list.append(password)
    
    #Checksum encriptado com a password do cliente
    checksum = enc.encrypt_string(checksum, password)
    n_security_parameters_list.append(checksum)
    n_security_parameters_number = len (n_security_parameters_list)

    pdu_to_send = pdu.PDU(request_id, primitive_type, len(version_numbers), version_numbers, 0, [], n_security_parameters_number, n_security_parameters_list)

    # Cria um socket do tipo UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Envia uma mensagem para o agente
    sock.sendto(pdu_to_send.encode(), (mn.AGENT_HOST, mn.AGENT_PORT))
    print(f"Message sent to {mn.AGENT_HOST}:{mn.AGENT_PORT}")

    # Espera pela resposta do agente
    data, addr = sock.recvfrom(mn.BUFFER_SIZE)
    pdu_received = pdu.PDU.decode(data)
    pdu_received.to_string()