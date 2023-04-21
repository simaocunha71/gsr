"""
DEFINIÇÃO DA MIB:

- sysTime
- sysReset
- nRequests : todos os pedidos que já foram feitos
- updateInterval
- nValidKeys : nº de chaves que foram válidas que foram entregues e que estão numa tabela
- keyTTL : tempo máximo que as chaves são consideradas válidas (e que vão estar naquela tabela)
- keySize : tamanho da chave
- nMaxValidKeys : nº maximo de chaves validas
- keyTable
    -> com nlinhas = nValidKeys
    -> cada entrada ter:
        - ter um index (inteiro a começar em 0, autoincrementável)
        - ter um keyID 
        - ter um keyValue
        - ter um keyStatus (chave valida ou nao)
        - ter um keyExpirationTime (data onde a chave irá ter que ser removida - armazena-se o valor de sysTime + keyTTL)
        - (se quisermos, pôr outros valores)
"""
"""
Limpeza da tabela/entrada apenas quando se faz operaçoes na referida tabela/entrada
"""