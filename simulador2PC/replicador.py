import sys
from flask import Flask, jsonify, request, abort
from gerenciador import leitura_arq
import Tipo

tipo = ""
log = Flask(__name__)
contas = leitura_arq()
replicas = []
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
    if tipo == 'coordenador':
        replicas.append(request.json)
    else:
        abort(404)

#request p/



if __name__ == "__main__":

    #argv[1] host
    #argv[2] tipo
    #argv para definir se o simulador será coordenado 'c' ou réplica 'r'
    if sys.argv[2] == 'c':
        tipo = 'coordenador'
    else:
        tipo = 'replica'

    print(tipo, "online...")
    log.run(host="0.0.0.0",port=sys.argv[1],debug=True)


