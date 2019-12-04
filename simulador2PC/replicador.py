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

# carrega semente
@log.route('/seed',methods=['POST'])
def carregar_semente():
    global seed
    seed = request.json['seed']
    print(seed)
    if(tipo == 'coordenador'):
        enderecoR1 = replicas[0]["endpoint"]+"/transacao"
        enderecoR2 = replicas[1]["endpoint"]+"/transacao"
        r1 = requests.put(enderecoR1,seed)
        r2 = requests.put(enderecoR2,seed)

    random.seed(int(seed))
    return Response(status=201, mimetype='application/json')

#Realiza transação
#TODO está correto ser PUT ou deveria ser POST
@log.route('/transacao',methods=['POST'])
def enviar_acao():
    global replicas
    global transacoes
    global seed
    dic_trans = request.json
    print("dic=>",dic_trans)
    id = dic_trans['id']
    print("id=> ",id)
    id_js = json.dumps({"id":id})
    print("id_js => ",id_js)
    transacoes.append(dic_trans)
    #coordenador
    if tipo == 'coordenador':
        enderecoR1 = replicas[0]["endpoint"]+"/transacao"
        enderecoR2 = replicas[1]["endpoint"]+"/transacao"
        r1 = requests.put(enderecoR1,transacoes[0])
        r2 = requests.put(enderecoR2, transacoes[0])
        if (r1.status_code == 200 and r2.status_code == 200):
            requests.put(enderecoR1,id_js)
            requests.put(enderecoR2,id_js)
            return Response(status=201, mimetype='application/json')
        else:
            requests.delete(enderecoR1)
            requests.delete(enderecoR2)
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
    #for para pegar a transacao relativa a confirmacao enviada

    if(tipo == 'coordenador'):
        return Response(status=400, mimetype='application/json')
    else:
        for transacao in transacoes:
            if(transacao ['id'] == decisao_id['id']):
                realiza_transacao(transacao)
                escrever_arq(contas)
                acoes.append({'id':transacao['id'],'status':'success'})
                return Response(status=200, mimetype='application/json')
        return Response(status=404, mimetype='application/json')

def realiza_transacao(transacao):
    global contas
    for conta in contas:
        if (conta['numero'] == transacao['conta']):
            if(transacao['operacao']=='debito'):
                conta['saldo'] = str(int(conta['saldo']) - int(transacao['valor']))
                print ("Saldo apos debito:",conta['saldo'])
            else:
                conta['saldo'] = str(int(conta['saldo']) + int(transacao['valor']))
                print("Saldo apos credito:", conta['saldo'])
            break


@log.route('/transacao',methods=['DELETE'])
def enviar_cancelamento():
    global transacoes
  #  decisao_id = request.json
  #  list_id = []

    if(tipo == 'coordenador'):
        return Response(status=400, mimetype='application/json')
    else:
       # for transacao in transacoes:
       #     list_id.append(transacao['id'])

     #   if (decisao_id['id'] in list_id):
        if(len(transacoes)!=0):
            trans = transacoes.get(0)
            acoes.append({'id': trans['id'], 'status': 'fail'})
            transacoes.remove(0)
            return Response(status=200, mimetype='application/json')
        else:
            return Response(status=404, mimetype='application/json')


@log.route('/historico',methods=['GET'])
def obter_historico():
    return jsonify({'acoes': acoes})

if __name__ == "__main__":


    print(tipo, "online...")
    log.run(host="0.0.0.0",port=sys.argv[1],debug=True)


