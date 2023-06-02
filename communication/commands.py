"""Criação dos comandos get(), set() e response()"""





"""TODO: IREI PRECISAR DESTE MODULO?????"""






import utils, sys



def snmp_keyshare_get(P,NL,L):
    """Função a ser implementada pelo manager"""
    """
    -> P (idRequest) é independente do agente - este apenas vai saber qual o ID do pedido recebido (nao vai gerar ids novos) - nao enviar novos pedidos com idRequest=P de V em V segundos
    """
    if len(sys.argv) < 2:
        print("Uso: python agent.py <assinatura>")
    else:
        commands = sys.argv[1]
        request_id, version_numbers = utils.parse_commands_id(commands)
        print("Request ID:", request_id)
        print("Version Numbers:", version_numbers)

    P = utils.get_request_id()
    pass


def snmp_keyshare_set(P, NW, W):
    """Função a ser implementada pelo manager"""
    P = utils.get_request_id()
    pass


def snmp_keyshare_response(P, NW, W, NR, R):
    """Função a ser implementada pelo agente"""
    P = utils.get_request_id()
    pass
