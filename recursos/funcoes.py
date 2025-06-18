import os
import time
import json
from datetime import datetime


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def aguarde(segundos):
    time.sleep(segundos)


def inicializarBancoDeDados():
    if not os.path.exists("base.atitus"):
        print("Banco de Dados Inexistente. Criando...")
        with open("base.atitus", "w") as banco:
            banco.write("{}")


def escreverDados(nome, pontos):
    if os.path.exists("base.atitus"):
        with open("base.atitus", "r") as banco:
            dados = banco.read()
        if dados:
            dadosDict = json.loads(dados)
        else:
            dadosDict = {}
    else:
        dadosDict = {}

    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    dadosDict[nome] = (pontos, data_hora)

    with open("base.atitus", "w") as banco:
        banco.write(json.dumps(dadosDict))
