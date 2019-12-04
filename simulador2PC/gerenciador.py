import json


# TODO é para ler de um arquivo já dentro do projeto ou deve ser passado
def leitura_arq():
    arquivo = open('dados.txt', 'r')
    dados = arquivo.read()
    dados_dic = json.loads(dados)
    return dados_dic['contas']

def escrever_arq(contas):
    arquivo = open('dados.txt', 'w')
    arquivo.writelines(json.dump({'contas':contas}))
    arquivo.close()