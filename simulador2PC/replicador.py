import sys
import flask
import flask_httpauth
from flask import Flask, jsonify, request, abort

from gerenciador import leitura_arq


log = Flask(__name__)

dados_json = leitura_arq()


@log.route('/contas',methods=['GET'])
def obter_contas():
    return dados_json

@log.route('/replicas',methods=['POST'])
def carregar_replicas():
    if not request.json:
        abort(400)
    replicas = request.json
    return jsonify('replicas',replicas),201

if __name__ == "__main__":

    #argv para definir se o simulador será coordenado 'c' ou réplica 'r'
    if sys.argv[1] == 'c':
        tipo = 'coordenador'
    else:
        tipo = 'replica'

    print(tipo, "online...")
    print(dados_json)

    log.run(host='0.0.0.0',debug=True)

