import json


# TODO é para ler de um arquivo já dentro do projeto ou deve ser passado
def leitura_arq():
    arquivo = open('dados.txt', 'r')
    dados = arquivo.read()
    return json.loads(dados)['contas']

