import sys
from flask import Flask, jsonify, request, abort, Response
import requests
import random
import json

#from gerenciador import leitura_arq, escrever_arq
log = Flask(__name__)

#-Leitura e escrita em arquivo----------------------------------------------------------------------------------
def leitura_arq():
    arquivo = open('dados.txt', 'r')
    dados = arquivo.read()
    dados_dic = json.loads(dados)
    return dados_dic['contas']

def escrever_arq(contas):
    with open('dados.txt', 'w') as outfile:
        json.dump({'contas':contas},outfile)

#-Variáveis globais--------------------------------------------------------------------------------------------
tipo = ""
#lista de contas carregadas a partir do disco
contas = leitura_arq()
#lista de replicas enviada pelo cliente
replicas = []
#lista que armazena transacoes
transacoes = []
#lista que armazenas as acoes e seus status
acoes = []
seed = ''


#-[/contas]----------------------------------------------------------------------------------------------------
#retorna as contas em log
@log.route('/contas',methods=['GET'])
def obter_contas():
    global contas
    contas = leitura_arq()
    return jsonify({'contas': contas}),200


#-[/replicas]-----------------------------------------------------------------------------------------------------
#carrega as replicas em uma lista
@log.route('/replicas',methods=['POST'])
def carregar_replicas():
    global replicas
    global tipo

    replicas = request.json['replicas']

    enderecoR1 = replicas[0]["endpoint"] + "/replicas"
    enderecoR2 = replicas[1]["endpoint"] + "/replicas"
    r1 = requests.get(enderecoR1)
    r2 = requests.get(enderecoR2)

    if not request.json or r1.status_code==200 or r2.status_code==200:
        return Response(status=404, mimetype='application/json')

    tipo = 'coordenador'
    return Response(status=201, mimetype='application/json')

#exclui replicas
@log.route('/replicas',methods=['DELETE'])
def excluir_replicas():
    global tipo
    if len(replicas) == 0:
        return Response(status=404, mimetype='application/json')
    replicas.clear()
    tipo = 'replica'
    return Response(status=200, mimetype='application/json')

#obtem lista de replicas
@log.route('/replicas',methods=['GET'])
def obtem_replicas():
    global replicas
    if len(replicas)==0 or tipo != "coordenador":
       return Response(status=404, mimetype='application/json')
    return jsonify('replicas',replicas),200


#-[/seed]--------------------------------------------------------------------------------------------------------------
# carrega semente no coordenador e repassa para as réplicas
@log.route('/seed',methods=['POST'])
def carregar_semente():
    global seed
    seed = request.json['seed']
    random.seed(int(seed))
    return Response(status=201, mimetype='application/json')

#-[/transacao]---------------------------------------------------------------------------------------------------------
#Realiza transação
@log.route('/transacao',methods=['POST'])
def enviar_acao():
    global replicas
    global transacoes
    global seed
    global acoes
    dic_trans = request.json
    transacoes.append(dic_trans)
    print(tipo)
    #coordenador
    if tipo == 'coordenador':
        id = dic_trans['id']
        id_js = {"id": id}
        enderecoR1 = replicas[0]["endpoint"]+"/transacao"
        enderecoR2 = replicas[1]["endpoint"]+"/transacao"
        r1 = requests.post(enderecoR1,json=transacoes[0])
        r2 = requests.post(enderecoR2, json=transacoes[0])
        if (r1.status_code == 200 and r2.status_code == 200):
            put1 = requests.put(enderecoR1,json=id_js)
            put2 = requests.put(enderecoR2,json=id_js)
            if(put1.status_code==200 and put2.status_code==200):
                realiza_transacao(transacoes[0])
                escrever_arq(contas)
                acoes.append({'id':transacoes[0]['id'],'status':'success'})
                transacoes.clear()
            return Response(status=201, mimetype='application/json')
        else:
            requests.delete(enderecoR1)
            requests.delete(enderecoR2)
            acoes.append({'id': transacoes[0]['id'], 'status': 'fail'})
            transacoes.clear()
            return Response(status=403, mimetype='application/json')
    #replica
    else:
        rand = random.randint(1,11)
        if (rand <= 7):
            return Response(status=200, mimetype='application/json')
        else:
            return Response(status=403, mimetype='application/json')


@log.route('/transacao',methods=['PUT','DELETE'])
def enviar_confirmacao():
    global transacoes
    global contas
    global acoes
    decisao_id = request.json
    if (tipo == 'coordenador'):
        return Response(status=400, mimetype='application/json')

    if request.method == 'PUT':
        for transacao in transacoes:
            if(transacao ['id'] == decisao_id['id']):
                realiza_transacao(transacao)
                escrever_arq(contas)
                acoes.append({'id': transacao['id'], 'status': 'success'})
                return Response(status=200, mimetype='application/json')
        return Response(status=404, mimetype='application/json')

    elif request.method == 'DELETE':
        if (len(transacoes) != 0):
            trans = transacoes[0]
            del(transacoes[0])
            acoes.append({'id': trans['id'], 'status': 'fail'})
            return Response(status=200, mimetype='application/json')
        else:
            return Response(status=404, mimetype='application/json')

#-[/historico]-------------------------------------------------------------------------------------------------
@log.route('/historico',methods=['GET'])
def obter_historico():
    return jsonify({'acoes': acoes}),200

#-Funções auxiliares------------------------------------------------------------------------------------------
#Função para realização de transferência (usada nas funções enviar_confirmacao() e enviar_acao())
def realiza_transacao(transacao):
    global contas
    for conta in contas:
        if (conta['numero'] == transacao['conta']):
            if(transacao['operacao']=='debito'):
                conta['saldo'] = str(float(conta['saldo']) - float(transacao['valor']))
            else:
                conta['saldo'] = str(float(conta['saldo']) + float(transacao['valor']))
            break


if __name__ == "__main__":
    print("online...")
    log.run(host="0.0.0.0",port=sys.argv[1],debug=True)



