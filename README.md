### Repositório da UC de Gestão e Segurança de Redes - Ano letivo 2022/2023

Relatório: [Aqui](https://github.com/simaocunha71/gsr/blob/main/docs/GSR_22_23_93262.pdf)
### Bibliotecas a instalar
```
pip install cryptography
```

### Comandos de exemplo

**Gestor/Cliente**:
- para criar uma chave:
```
python .\manager.py username password set 1 3.2.6.0
```
- para alterar valor:
```
python .\manager.py username password set 4 2.1 42
python .\manager.py username password set 7 3.2.4.2 nova_palavra  
```
- para obter valor:
```
python .\manager.py username password get 12 2.1
```

**Agente/Servidor**:
- inicializar agente com ficheiro de registo de clientes encriptado:
```
python .\agent.py server_gsr -encrypt
```

- Agente apenas desencripta conteudo do ficheiro json com a password
```
python .\agent.py server_gsr -decrypt
```

#### Sintaxe do ficheiro de configuração
* K: Número de linhas ou colunas da matriz
* M: Chave mestra
* T: Intervalo (em ms) de atualizações de matrizes
* V: Tempo máximo do armazenamento da informação na matriz
* X: Número máximo de entradas na tabela
* Port: Porta de atendimento UDP
* Password: Password a ser utilizada pelo cliente

#### Estrutura do repositório
* *config.conf*: Ficheiro de configuração
* *agent.py*: Ficheiro que representa o agente SNMP
* *manager.py*: Ficheiro que representa o manager SNMP
* *clients.json*: Ficheiro (com conteúdo encriptado ou não) que contém todos os clientes alguma vez registados
* *model/*: Diretoria com a classe *configurations* e *pdu*
* *keys/*: Diretoria responsável pela criação e atualização de matrizes (*matrix.py* e *update_matrix.py*) e geração de chaves (*main.py*)
* *comunication/*: PDU usada no TP e Classe de registo de todos os clientes alguma vez ligados ao servidor
* *MIB/*: MIB SNMPkeyShare
* *security/*: Diretoria responsável por calcular o checksum e encriptar/desencriptar ficheiros
* *docs/*: Documentos necessários para o TP (enunciados, ...)

#### Códigos de erro
- Erro #1 ("*MIB FULL*"): Pedido de criação de chave mas MIB não suporta a adição de mais chaves
- Erro #2 ("*NON EXISTENT GROUP*"): Grupo acedido da MIB não existe
- Erro #3 ("*NON EXISTENT VALUE (Sys/Conf)*"): Objeto não existe no grupo System ou Config
- Erro #4 ("*NON EXISTENT ENTRY*"): Entrada da MIB a aceder não existe
- Erro #5 ("*NON EXISTENT OBJECT IN ENTRY*"): Campo da entrada acedida na tabela não existe
- Erro #6 ("*VALUE WITH DIFFERENT TYPE*"): Valor a adicionar não é do mesmo tipo que o estipulado para o objeto
- Erro #7 ("*PRIMITIVE NOT SUPPORTED*"): Primitiva efetuada não corresponde a get ou
- Erro #8 ("*OIDs len INCORRECT*"): Número de OIDS incorretos
- Erro #9 ("*SAME REQUEST_ID SENT IN V SECONDS| WRONG PASSWORD*"): Manager não pode enviar o mesmo request id dentro de V segundos ou a password inserida não é igual à primeira
- Erro #10 ("*WRONG CHECKSUM*"): Checksum mostra que cliente não é quem diz ser
