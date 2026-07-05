import json
import os
from datetime import datetime

# Correção 1: Caminho Absoluto Blindado para o Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_COFRE = os.path.join(BASE_DIR, 'vault_data.json')

def criar_cofre_novo():
    cofre_inicial = {
        "saldo_USDT": 10000.0,
        "operacoes_abertas": {}, 
        "historico": []
    }
    salvar_cofre(cofre_inicial)
    return cofre_inicial

def carregar_cofre():
    # Correção 2: Tratamento de exceção robusto
    try:
        if not os.path.exists(ARQUIVO_COFRE):
            return criar_cofre_novo()
        
        with open(ARQUIVO_COFRE, 'r') as f:
            return json.load(f)
    except Exception as e:
        # Se houver qualquer erro de leitura (arquivo ausente ou corrompido), recria o cofre
        return criar_cofre_novo()

def salvar_cofre(dados):
    with open(ARQUIVO_COFRE, 'w') as f:
        json.dump(dados, f, indent=4)

def registrar_historico(ativo, tipo, preco, qtd, lucro_prejuizo=0):
    cofre = carregar_cofre()
    registro = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ativo": ativo,
        "tipo": tipo, 
        "preco": preco,
        "qtd": qtd,
        "pnl_usdt": lucro_prejuizo
    }
    cofre['historico'].insert(0, registro) 
    salvar_cofre(cofre)
