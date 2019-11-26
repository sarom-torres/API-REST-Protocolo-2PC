import sys
from flask import Flask, jsonify, request, abort
import requests

from gerenciador import leitura_arq
import Tipo

#tipo = Tipo()
tipo = ""
log = Flask(__name__)
contas = leitura_arq()
replicas = []
transacoes = []
acoes = []

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

@log.route('/replicas',methods=['DELETE'])
def excluir_replicas():
    global tipo
    if len(replicas) == 0:
        abort(404)
    replicas.clear()
    tipo = 'replicas'
    return jsonify('replicas',replicas)

#
@log.route('/contas/transacao',methods=['PUT'])
def enviar_acao():
    global replicas
    if tipo == 'coordenador':
        transacoes.append(request.json)
#       r = requests.get('http://www.google.com')
        endereco = replicas[0]["endpoint"]+"/contas/transacao"
        print(endereco)
        r = requests.put(endereco)
        #,transacoes[0]
        #jsonify({"resposta": r}), 200
        return jsonify({"qq":"coisa"})
    else:
        return jsonify({"qq":"coisa"})





if __name__ == "__main__":


    print(tipo, "online...")
    log.run(host="0.0.0.0",port=sys.argv[1],debug=True)


