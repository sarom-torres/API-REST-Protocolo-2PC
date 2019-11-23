import json

def leitura_arq():
    arquivo = open('dados.txt', 'r')
    dados = arquivo.read()

    return json.loads(dados)
