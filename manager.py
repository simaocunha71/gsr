"""Módulo que implementa o manager"""
import socket
import sys
import communication.utils as comm_utils
import communication.pdu as pdu

class Manager:
    def __init__(self):
        self.AGENT_HOST  = 'localhost' # Endereço do socket
        self.AGENT_PORT  = 2048        # Porta de comunicação (a mesma que a do agente)
        self.BUFFER_SIZE = 4096        # Buffer do socket para a comunicação


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Use format: python manager.py [get/set] [request-id] [version-numbers] [new-value]")
    else:
        action = sys.argv[1]
        request_id = sys.argv[2]
        version_numbers = sys.argv[3]
        version_numbers = comm_utils.parse_version_numbers(version_numbers)

        if action == "get":
            primitive_type = 1
        elif action == "set":
            if len(sys.argv) < 5:
                print("Missing new_value argument for SET command")
                sys.exit(0)
            new_value = sys.argv[4]
            primitive_type = 2
        else:
            print("Invalid action")
            sys.exit(0)

    mn = Manager()

    pdu_to_send = pdu.PDU(request_id, primitive_type, len(version_numbers), version_numbers, 0, [])

    # Cria um socket do tipo UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Envia uma mensagem para o agente
    sock.sendto(pdu_to_send.encode(), (mn.AGENT_HOST, mn.AGENT_PORT))
    print(f"Message sent to {mn.AGENT_HOST}:{mn.AGENT_PORT}")

    # Espera pela resposta do agente
    data, addr = sock.recvfrom(mn.BUFFER_SIZE)
    pdu_received = pdu.PDU.decode(data) #TODO: CORRIGIR AQUI!
    pdu_received.to_string()
    #print(f"Resposta de {addr}: \"{pdu_received.to_string()}\"")  # Imprime a mensagem recebida do agente

