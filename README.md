### Repositório da UC de Gestão e Segurança de Redes - Ano letivo 2022/2023

Relatório Overleaf: https://www.overleaf.com/project/64392ff091ff419dc81f0ab8

#### Sintaxe do ficheiro de configuração
* K: Número de linhas ou colunas da matriz
* M: Chave mestra
* T: Intervalo (em ms) de atualizações de matrizes
* V: Tempo máximo do armazenamento da informação na matriz
* X: Número máximo de entradas na tabela
* Port: Porta de atendimento UDP

#### Estrutura do repositório
* *config.conf*: Ficheiro de configuração
* *agent.py*: Ficheiro que representa o agente SNMP
* *manager.py*: Ficheiro que representa o manager SNMP
* *model/*: Diretoria com a classe *configurations* e *pdu*
* *keys/*: Diretoria responsável pela criação e atualização de matrizes (*matrix.py* e *update_matrix.py*) e geração de chaves (*main.py*)
* *comunication/*: PDU usada no TP
* *MIB/*: MIB SNMPkeyShare
* *docs/*: Documentos necessários para o TP (enunciado, ...)

#### Códigos de erro
* Erro #1: Pedido de criação de chave mas MIB não suporta a adição de mais chaves
* Erro #2: Grupo acedido da MIB não existe
* Erro #3: Objeto não existe no grupo System ou Config
* Erro #4: Entrada da MIB a aceder não existe
* Erro #5: Campo da entrada acedida na tabela não existe
* Erro #6: Valor a adicionar não é do mesmo tipo que o estipulado para o objeto
* Erro #7: Primitiva efetuada não corresponde a get ou set
* Erro #8: Número de OIDS incorretos
* Erro #9: Manager não pode enviar o mesmo request id dentro de V segundos
* Erro #10: Checksum mostra que cliente não é quem diz ser

#### TODO para o TP2

- Encriptar ficheiro de configuração e servidor so abre através de uma password
    -> Link util para encriptação em Python: https://www.geeksforgeeks.org/how-to-encrypt-and-decrypt-strings-in-python/
- Impedir que o mesmo cliente se ligue ao servidor com duas passwords diferentes (verificar se realmente será preciso) - adicionar flag para alterar a sua password???
- Verificar se a escrita no ficheiro json está a ser bem feita
- ~~Calcular checksum na PDU do cliente:~~
    ~~-> Link util para calcular checksum em Python: https://www.geeksforgeeks.org/implementing-checksum-using-python/~~
- ~~Adicionar mais uma variavel na linha de comandos do cliente, onde essa variavel vai simbolizar o id do cliente (este id não precisa de ser um inteiro)~~
- ~~Sabendo a existência deste client ID, o ficheiro de registo de clientes já não vai ter um client ID autoincrementado e este valor vai ser o client_id inserido pelo cliente~~
- ~~Mudar a chave do dicionário de clientes registados para ser este client_id~~
- ~~Verificar se existe algum cliente com o client_id inserido, caso exista, mandar mensagem de erro para o cliente a informar que não pode usar aquele client_id~~
- ~~PDU de pedido + client_id vai ser encriptados com a password do servidor~~
- ~~Checksum desta PDU será encriptado com a password do cliente.~~
- ~~No lado do servidor, cliente desencapsula PDU + ClientID e verifica se esse cliente pode ser inserido no ficheiro de registo. Se não estiver, adicionas esse cliente ao ficheiro e ignoras o checksum que possa existir. Caso já exista no ficheiro, desencapsulas o checksum e verificas se aquele cliente é realmente quem diz ser.~~