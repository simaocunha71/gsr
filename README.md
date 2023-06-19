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

Link util para encriptação em Python: https://www.geeksforgeeks.org/how-to-encrypt-and-decrypt-strings-in-python/