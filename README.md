# Replicação mestre escravo

> Engenharia de Telecomunicações - Sistemas Distribuídos (STD29006)
>
> Instituto Federal de Santa Catarina - campus São José

Neste projeto foi desenvolvida uma API REST para simulação do protocolo 2PC na implementação de log de contas bancárias.
O sistema é composto por três máquinas em que uma assume o papel de coordenador e outras duas assumem o papel de réplicas. 
A aplicação coordenador é responsável pela interação com o usuário e pelo envio de ações para réplicas. As máquinas réplicas
são responsáveis por realizar a votação e persistir os dados atualizados em disco. No final da simulação todas as deverão possuir
mesmos dados em log.

## Definição do projeto


O projeto foi desenvolvido em Python3 e para sua execução é recomendado a criação de um [ambiente virtual](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) e a instalação das
seguintes bibliotecas python:

* [flask] (https://flask-ptbr.readthedocs.io/en/latest/installation.html). Sua instalação poderá ser feita da seguinte maneira:
```
pip install flask
```

* [requests] (https://requests.readthedocs.io/pt_BR/latest/user/install.html). Sua instalação poderá ser feita a partir do seguinte comando:
```
pip install requests
```


