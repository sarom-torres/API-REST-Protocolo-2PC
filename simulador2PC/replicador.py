import sys
import flask
import flask_httpauth
from gerenciador import leitura_arq


if __name__ == "__main__":

    #argv para definir se o simulador será coordenado 'c' ou réplica 'r'
    if sys.argv[1] == 'c':
        tipo = 'coordenador'
    else:
        tipo = 'replica'

    print(tipo, "online...")

    dados_json = leitura_arq()

    print(dados_json)