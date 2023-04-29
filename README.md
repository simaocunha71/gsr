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
* *comunication/*: Comunicação SNMPkeyShare - comandos get(), set() e response()
* *MIB/*: MIB SNMPkeyShare
* *docs/*: Documentos necessários para o TP (enunciado, ...)