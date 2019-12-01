import sys
from flask import Flask, jsonify, request, abort, Response
import requests
import random

from gerenciador import leitura_arq
import Tipo

#tipo = Tipo()
tipo = ""
log = Flask(__name__)
contas = leitura_arq()
replicas = []
transacoes = []
acoes = []
seed = ''

#retorna as contas em log
@log.route('/contas',methods=['GET'])
def obter_contas():
    return jsonify('contas', contas)

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
    random.seed(int(seed))
    return Response(status=201, mimetype='application/json')

#Realiza transação
#TODO está correto ser PUT ou deveria ser POST
#TODO seria mais correto /transacao
@log.route('/contas/transacao',methods=['PUT'])
def enviar_acao():
    global replicas
    global transacoes
    global seed
    transacoes.append(request.json)

    #coordenador
    if tipo == 'coordenador':
        enderecoR1 = replicas[0]["endpoint"]+"/contas/transacao"
        enderecoR2 = replicas[1]["endpoint"]+"/contas/transacao"
        r1 = requests.put(enderecoR1,transacoes[0])
        r2 = requests.put(enderecoR2, transacoes[0])
        if (r1.status_code == 200 and r2.status_code == 200):
            return Response(status=201, mimetype='application/json')
        else:
            return Response(status=403, mimetype='application/json')
    #replica
    else:
        rand = random.randint(1, 10)
        print("Random",rand) #TODO o valor não vai até 10
        if (rand <= 7):
            return Response(status=200, mimetype='application/json')
        else:
            return Response(status=403, mimetype='application/json')

#TODO seria mais correto /transacao
#@log.route('/contas/transacao/confirmacao',methods=['PUT'])
#def enviar_confirmacao

if __name__ == "__main__":


    print(tipo, "online...")
    log.run(host="0.0.0.0",port=sys.argv[1],debug=True)


