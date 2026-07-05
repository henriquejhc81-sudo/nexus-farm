import streamlit as st
import pandas as pd
import ghost_vault
import ghost_engine

st.set_page_config(
    page_title="NEXUS COMMAND // GHOST C2",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização CSS Premium (Dark Mode Profundo com Roxo/Neon)
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #e2e8f0; }
    .header-box {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #8b5cf6; /* Roxo Nexus */
        margin-bottom: 20px;
    }
    .titulo { color: #ffffff; font-weight: 800; font-family: 'Inter', sans-serif; margin: 0; }
    .subtitulo { color: #94a3b8; font-family: 'Inter', monospace; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-box">
        <h1 class="titulo">👻 NEXUS COMMAND // PAPER TRADING</h1>
        <div class="subtitulo">SISTEMA DE SIMULAÇÃO CONECTADO AO RADAR AUTOBOLT</div>
    </div>
""", unsafe_allow_html=True)

# Botão de Execução Manual do Motor
col_btn, col_espaco = st.columns([1, 4])
with col_btn:
    if st.button("⚡ FORÇAR CICLO DE TRADE", use_container_width=True):
        with st.spinner("Motor Fantasma operando no mercado e lendo o Autobolt..."):
            ghost_engine.executar_ciclo_simulacao()
        st.rerun() # Recarrega a página automaticamente para atualizar os números

# Carrega os dados do cofre para renderizar a tela
cofre = ghost_vault.carregar_cofre()
saldo_atual = cofre['saldo_USDT']
lucro_total = saldo_atual - 10000.0 # Subtrai o capital inicial

st.write("---")
st.markdown("### 💰 COFRE FANTASMA (USDT)")

# Métricas Financeiras
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    st.metric(label="Saldo Disponível", value=f"${saldo_atual:.2f}")
with metric_col2:
    st.metric(label="Capital Inicial (Simulação)", value="$10000.00")
with metric_col3:
    st.metric(label="PnL Fictício (Lucro/Prejuízo)", value=f"${lucro_total:.2f}", delta=f"{lucro_total:.2f}")

st.write("---")
col_pos, col_hist = st.columns(2)

# Coluna da Esquerda: O que o robô está segurando agora
with col_pos:
    st.markdown("### 📡 POSIÇÕES ABERTAS")
    if cofre['operacoes_abertas']:
        df_abertas = pd.DataFrame.from_dict(cofre['operacoes_abertas'], orient='index').reset_index()
        df_abertas.columns = ['Ativo', 'Preço de Compra ($)', 'Qtd Comprada']
        
        # Formatação para ficar bonito
        df_abertas['Preço de Compra ($)'] = df_abertas['Preço de Compra ($)'].apply(lambda x: f"${x:.4f}")
        df_abertas['Qtd Comprada'] = df_abertas['Qtd Comprada'].apply(lambda x: f"{x:.4f}")
        
        st.dataframe(df_abertas, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma operação aberta no momento. O Motor Fantasma está aguardando o sinal 🟢 LIBERADO do Autobolt.")

# Coluna da Direita: Histórico de todas as compras e vendas
with col_hist:
    st.markdown("### 📜 EXTRATO DE OPERAÇÕES")
    if cofre['historico']:
        df_hist = pd.DataFrame(cofre['historico'])
        
        # Função para colorir o lucro (Verde) e prejuízo (Vermelho)
        def colorir_pnl(val):
            try:
                v = float(val)
                if v > 0: return 'color: #10b981; font-weight: bold;'
                elif v < 0: return 'color: #ef4444; font-weight: bold;'
                return 'color: #64748b;'
            except: 
                return 'color: #64748b;'
        
        # Renomeando as colunas para a tabela ficar intuitiva
        df_hist = df_hist.rename(columns={
            "data": "Data/Hora", 
            "ativo": "Moeda", 
            "tipo": "Ação", 
            "preco": "Preço Executado", 
            "qtd": "Quantidade", 
            "pnl_usdt": "Lucro (USDT)"
        })
        
        st.dataframe(
            df_hist.style.map(colorir_pnl, subset=['Lucro (USDT)']), 
            use_container_width=True, 
            hide_index=True
        )
    else:
        st.caption("O extrato está vazio. Nenhuma simulação executada ainda.")
