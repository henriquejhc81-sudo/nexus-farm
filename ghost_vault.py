import json
import os
from datetime import datetime

ARQUIVO_COFRE = 'vault_data.json'

def carregar_cofre():
    # Se o cofre não existir, cria um novo com $10.000 fictícios
    if not os.path.exists(ARQUIVO_COFRE):
        cofre_inicial = {
            "saldo_USDT": 10000.0,
            "operacoes_abertas": {}, # Ex: {"BTC": {"preco_compra": 60000, "qtd": 0.01}}
            "historico": []
        }
        salvar_cofre(cofre_inicial)
        return cofre_inicial
    
    with open(ARQUIVO_COFRE, 'r') as f:
        return json.load(f)

def salvar_cofre(dados):
    with open(ARQUIVO_COFRE, 'w') as f:
        json.dump(dados, f, indent=4)

def registrar_historico(ativo, tipo, preco, qtd, lucro_prejuizo=0):
    cofre = carregar_cofre()
    registro = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ativo": ativo,
        "tipo": tipo, # 'COMPRA' ou 'VENDA'
        "preco": preco,
        "qtd": qtd,
        "pnl_usdt": lucro_prejuizo
    }
    cofre['historico'].insert(0, registro) # Insere no começo da lista
    salvar_cofre(cofre)
