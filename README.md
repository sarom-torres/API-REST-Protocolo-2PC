# Replicação coordenador/réplicas

Neste projeto foi desenvolvida uma API REST para simulação do protocolo 2PC na implementação de log de contas bancárias.
O sistema é composto por três máquinas em que uma assume o papel de coordenador e outras duas assumem o papel de réplicas. 
A aplicação coordenador é responsável pela interação com o usuário e pelo envio de ações para réplicas. As máquinas réplicas
são responsáveis por realizar a votação e persistir os dados atualizados em disco. No final da simulação todas as deverão possuir
mesmos dados em log.

## Ambiente de execução

O projeto foi desenvolvido em Python3 e para sua execução é recomendado a criação de um [ambiente virtual](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) e a instalação das
seguintes bibliotecas python:

* [flask](https://flask-ptbr.readthedocs.io/en/latest/installation.html). Sua instalação poderá ser feita da seguinte maneira:
```
pip install flask
```

* [requests](https://requests.readthedocs.io/pt_BR/latest/user/install.html). Sua instalação poderá ser feita a partir do seguinte comando:
```
pip install requests
```
* Outras bibliotecas necessárias estão no arquivo requirements.txt

## Executando a API

A API desenvolvida está no arquivo `replicador.py` e ao ser executada o seguinte parâmetro deve ser passados na linha de comando:
* porta : porta no qual o processo estará rodando

A execução deverá ser feita da seguinte maneira:
```
python3 replicador.py porta
```
Exemplo:
```
python3 replicador.py 5000
```
Para rodar o cenário de replicação através do 2PC será necessária a execução de três processos com três portas diferentes.

## Utilizando os recursos da API

Após a executar os três processos basta seguir a documentação da [API](https://github.com/sarom-torres/API-REST-Protocolo-2PC/blob/master/apiary.apib) para fazer o registro de log. 

