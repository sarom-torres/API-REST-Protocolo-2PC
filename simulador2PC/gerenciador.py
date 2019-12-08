import json


def leitura_arq():
    arquivo = open('dados.txt', 'r')
    dados = arquivo.read()
    dados_dic = json.loads(dados)
    return dados_dic['contas']

def escrever_arq(contas):
    with open('dados.txt', 'w') as outfile:
        json.dump({'contas':contas},outfile)