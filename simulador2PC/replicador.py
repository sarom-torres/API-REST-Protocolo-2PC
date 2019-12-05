import sys
from flask import Flask, jsonify, request, abort, Response
import requests
import random
import json

from gerenciador import leitura_arq, escrever_arq
import Tipo

#tipo = Tipo()
tipo = ""
log = Flask(__name__)
#lista de contas carregadas a partir do disco
contas = leitura_arq()
#lista de replicas enviada pelo cliente
replicas = []
#lista que armazena transacoes
transacoes = []
#lista que armazenas as acoes e seus status
acoes = []
seed = ''


#retorna as contas em log
@log.route('/contas',methods=['GET'])
def obter_contas():
    global contas
    contas = leitura_arq()
    return jsonify({'contas': contas})

#carrega as replicas em uma lista
@log.route('/replicas',methods=['POST'])
def carregar_replicas():
    global replicas
    global tipo

    if not request.json:
        abort(400)

    replicas = request.json['replicas']
    tipo = 'coordenador'
    return jsonify({'replicas': replicas}),201

#exclui replicas
@log.route('/replicas',methods=['DELETE'])
def excluir_replicas():
    global tipo
    if len(replicas) == 0:
        abort(404)
    replicas.clear()
    tipo = 'replicas'
    return jsonify('replicas',replicas)

#obtem lista de replicas
@log.route('/replicas',methods=['GET'])
def obtem_replicas():
    global replicas
    if len(replicas)==0:
        abort(404)
    return jsonify('replicas',replicas)

# carrega semente no coordenador e repassa para as réplicas
@log.route('/seed',methods=['POST'])
def carregar_semente():
    global seed
    seed = request.json['seed']
    if(tipo == 'coordenador'):
        enderecoR1 = replicas[0]["endpoint"]+"/seed"
        enderecoR2 = replicas[1]["endpoint"]+"/seed"
        r1 = requests.post(enderecoR1,json=request.json)
        r2 = requests.post(enderecoR2,json=request.json)
    random.seed(int(seed))
    return Response(status=201, mimetype='application/json')

#Realiza transação
#TODO está correto ser PUT ou deveria ser POST
@log.route('/transacao',methods=['POST'])
def enviar_acao():
    global replicas
    global transacoes
    global seed
    global acoes

    dic_trans = request.json
    transacoes.append(dic_trans)
    print("dic=>", dic_trans)
    #coordenador
    if tipo == 'coordenador':
        id = dic_trans['id']
        id_js = {"id": id}
        enderecoR1 = replicas[0]["endpoint"]+"/transacao"
        enderecoR2 = replicas[1]["endpoint"]+"/transacao"
        print("trans0=>",transacoes[0])
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
        rand = random.randint(1, 10)
        print("Random",rand) #TODO o valor não vai até 10
        if (rand <= 7):
            return Response(status=200, mimetype='application/json')
        else:
            return Response(status=403, mimetype='application/json')


@log.route('/transacao',methods=['PUT'])
def enviar_confirmacao():
    global transacoes
    global contas
    decisao_id = request.json

    if(tipo == 'coordenador'):
        return Response(status=400, mimetype='application/json')
    else:
        for transacao in transacoes:
            if(transacao ['id'] == decisao_id['id']):
                realiza_transacao(transacao)
                escrever_arq(contas)
                return Response(status=200, mimetype='application/json')
        return Response(status=404, mimetype='application/json')

@log.route('/transacao',methods=['DELETE'])
def enviar_cancelamento():
    global transacoes
    if(tipo == 'coordenador'):
        return Response(status=400, mimetype='application/json')
    else:
        if(len(transacoes)!=0):
            trans = transacoes.get(0)
            transacoes.remove(0)
            return Response(status=200, mimetype='application/json')
        else:
            return Response(status=404, mimetype='application/json')


@log.route('/historico',methods=['GET'])
def obter_historico():
    return jsonify({'acoes': acoes})

def realiza_transacao(transacao):
    global contas
    for conta in contas:
        if (conta['numero'] == transacao['conta']):
            if(transacao['operacao']=='debito'):
                conta['saldo'] = str(float(conta['saldo']) - float(transacao['valor']))
                print ("Saldo apos debito:",conta['saldo'])
            else:
                conta['saldo'] = str(float(conta['saldo']) + float(transacao['valor']))
                print("Saldo apos credito:", conta['saldo'])
            break


if __name__ == "__main__":
    print(tipo, "online...")
    log.run(host="0.0.0.0",port=sys.argv[1],debug=True)


