import ghost_vault
import motor_mestre # Importa a inteligência do Autobolt
import streamlit as st

# Parâmetros de Gestão de Risco do Simulador
TICKET_COMPRA_USDT = 500.0  # Vai simular compras de $500 por moeda
ALVO_LUCRO_PCT = 1.03       # Vende se bater +3% de lucro
STOP_LOSS_PCT = 0.98        # Vende se bater -2% de prejuízo

def executar_ciclo_simulacao():
    cofre = ghost_vault.carregar_cofre()
    
    # 1. Pede a análise atualizada para o Autobolt
    radar = motor_mestre.varredura_global()
    
    for moeda_dado in radar:
        ativo = moeda_dado['Ativo']
        
        # Limpa o "Erro API" ou símbolos e converte o preço para número
        try:
            preco_atual = float(moeda_dado['Preço'].replace('$', '').replace(',', ''))
        except:
            continue # Pula se houver erro de leitura na KuCoin

        veredicto = moeda_dado['Veredicto']
        
        # --- LÓGICA DE VENDA (Monitoramento de Posições Abertas) ---
        if ativo in cofre['operacoes_abertas']:
            operacao = cofre['operacoes_abertas'][ativo]
            preco_compra = operacao['preco_compra']
            
            lucro_atual_pct = preco_atual / preco_compra
            
            # Bateu o Alvo (Take Profit) ou Stop Loss?
            if lucro_atual_pct >= ALVO_LUCRO_PCT or lucro_atual_pct <= STOP_LOSS_PCT:
                # Calcula o PnL (Profit and Loss)
                valor_recebido = operacao['qtd'] * preco_atual
                lucro_usdt = valor_recebido - (operacao['qtd'] * preco_compra)
                
                # Atualiza o Cofre
                cofre['saldo_USDT'] += valor_recebido
                del cofre['operacoes_abertas'][ativo]
                ghost_vault.salvar_cofre(cofre)
                
                # Registra no log
                tipo_venda = "VENDA (LUCRO)" if lucro_usdt > 0 else "VENDA (STOP)"
                ghost_vault.registrar_historico(ativo, tipo_venda, preco_atual, operacao['qtd'], round(lucro_usdt, 2))


        # --- LÓGICA DE COMPRA (Buscando Oportunidades) ---
        # Só compra se estiver LIBERADO, se tiver saldo > 500 e se JÁ NÃO ESTIVER comprado na moeda
        elif "LIBERADO" in veredicto and cofre['saldo_USDT'] >= TICKET_COMPRA_USDT:
            qtd_comprada = TICKET_COMPRA_USDT / preco_atual
            
            # Debita o saldo e registra a operação
            cofre['saldo_USDT'] -= TICKET_COMPRA_USDT
            cofre['operacoes_abertas'][ativo] = {
                "preco_compra": preco_atual,
                "qtd": qtd_comprada
            }
            ghost_vault.salvar_cofre(cofre)
            ghost_vault.registrar_historico(ativo, "COMPRA", preco_atual, qtd_comprada, 0)

    return cofre # Retorna o cofre atualizado para o Dashboard
