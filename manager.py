"""Módulo que implementa o manager"""
import socket

class Manager:
    def __init__(self):
        self.AGENT_HOST  = 'localhost' # Endereço do socket
        self.AGENT_PORT  = 2048        # Porta de comunicação (a mesma que a do agente)
        self.BUFFER_SIZE = 4096        # Buffer do socket para a comunicação


if __name__ == "__main__":

    mn = Manager()

    # Cria um socket do tipo UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Envia uma mensagem para o agente
    message = "I want a key"
    sock.sendto(message.encode(), (mn.AGENT_HOST, mn.AGENT_PORT))
    print(f"Message sent to {mn.AGENT_HOST}:{mn.AGENT_PORT}")

    # Espera pela resposta do agente
    data, addr = sock.recvfrom(mn.BUFFER_SIZE)
    print(f"Resposta de {addr}: \"{data.decode()}\"")  # Imprime a mensagem recebida do agente

