import sys
from flask import Flask, jsonify, request, abort
from gerenciador import leitura_arq
import Tipo

log = Flask(__name__)
contas = leitura_arq()
replicas = []
tipo = ""

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


if __name__ == "__main__":

    #argv para definir se o simulador será coordenado 'c' ou réplica 'r'
    if sys.argv[1] == 'c':
        tipo = 'coordenador'
    else:
        tipo = 'replica'

    print(tipo, "online...")


    log.run(host='0.0.0.0',debug=True)

