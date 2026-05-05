import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import time
import random

# --- CONFIGURAÇÃO DA PÁGINA E DESIGN ---
st.set_page_config(page_title="Nexus OmniCode", page_icon="⚡", layout="wide")

# --- GESTÃO DE SEGURANÇA NA SESSÃO ---
if 'master_password' not in st.session_state:
    st.session_state['master_password'] = "admin123"
if 'lock_active' not in st.session_state:
    st.session_state['lock_active'] = True
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { background-color: #4CAF50; color: white; font-weight: bold; border-radius: 10px; width: 100%; height: 3em; }
    .stTextArea>div>div>textarea { background-color: #1a1c24; color: #ffffff; border: 1px solid #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

# --- TELA DE BLOQUEIO ---
if st.session_state['lock_active'] and not st.session_state['autenticado']:
    st.title("🔒 Nexus Blindado")
    entrada_senha = st.text_input("Insira a Chave Mestra para acessar:", type="password")
    if st.button("Desbloquear Sistema"):
        if entrada_senha == st.session_state['master_password']:
            st.session_state['autenticado'] = True
            st.rerun()
        else:
            st.error("Senha Incorreta! Acesso Negado.")
    st.stop()

# --- INICIALIZAÇÃO DA IA ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Erro: API Key não configurada nos Secrets do Streamlit!")
    st.stop()

def nexus_process(ideia, modo, contexto_web):
    prompt_sistema = f"Você é o Nexus OmniCode, a melhor IA do mundo. Missão: {modo}. Contexto: {contexto_web}. Responda em Português com código profissional."
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": ideia}],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
        )
        return completion.choices.message.content
    except Exception as e:
        return f"Erro na conexão com a IA: {e}"

# --- BARRA LATERAL (GESTÃO E FILTROS) ---
with st.sidebar:
    st.title("⚙️ Painel Nexus")
    
    # Seção de Troca de Senha e Ativação
    with st.expander("🔐 Segurança e Senha", expanded=True):
        st.session_state['lock_active'] = st.toggle("Ativar Bloqueio por Senha", value=st.session_state['lock_active'])
        nova_senha = st.text_input("Mudar Senha Mestra:", value=st.session_state['master_password'], type="password")
        if st.button("Confirmar Nova Senha"):
            st.session_state['master_password'] = nova_senha
            st.success("Senha atualizada com sucesso!")

    st.divider()
    st.subheader("🔗 Integrações Ativas")
    for app in ["GitLab", "Bitbucket", "Azure", "Gitea", "SourceForge", "FastAPI"]:
        st.toggle(app, value=True)
    
    st.divider()
    modo = st.selectbox("🎯 Função Principal", [
        "Criar código do zero", 
        "Corrigir erros e bugs", 
        "Incremento Mágico (Evoluir Código)", 
        "Analisar performance",
        "Gerar Documentação"
    ])

# --- ÁREA PRINCIPAL ---
st.title("⚡ Nexus OmniCode")
st.caption("A Central Suprema de Inteligência em Código - Projeto Melhor do Mundo")

col_in, col_out = st.columns(2)

with col_in:
    st.subheader("📥 Entrada de Inteligência")
    user_input = st.text_area("Descreva sua ideia ou cole o código:", height=300, placeholder="Ex: Crie um sistema de login ou corrija o código abaixo...")
    upload = st.file_uploader("Alimentar Nexus com arquivo", type=['py', 'js', 'html', 'txt', 'sql', 'css'])

with col_out:
    st.subheader("🚀 Resultado da IA")
    if st.button("EXECUTAR ANÁLISE SUPREMA"):
        if user_input:
            with st.spinner("Nexus emulando humano e processando bases globais..."):
                time.sleep(random.uniform(1.0, 2.5)) # Humanizer delay
                with DDGS() as ddgs:
                    search = [r['body'] for r in ddgs.text(f"melhores práticas para {user_input}", max_results=2)]
                    contexto = "\n".join(search)
                
                resultado = nexus_process(user_input, modo, contexto)
                st.session_state['last_result'] = resultado
                st.markdown(resultado)
        else:
            st.error("O campo de entrada está vazio!")

    # BOTÃO DE DOWNLOAD IMEDIATO (Melhoria implementada)
    if 'last_result' in st.session_state:
        st.download_button(
            label="📥 BAIXAR SOLUÇÃO AGORA",
            data=st.session_state['last_result'],
            file_name="nexus_output.py",
            mime="text/plain"
        )

# --- NEXUS CHAT (Nova Função) ---
st.divider()
st.subheader("💬 Nexus Chat Pro")
st.info("Converse com a IA sobre o código gerado acima para tirar dúvidas ou pedir ajustes rápidos.")
chat_input = st.text_input("Dúvida sobre o resultado?")
if chat_input and 'last_result' in st.session_state:
    with st.chat_message("assistant"):
        with st.spinner("Analisando..."):
            resposta_chat = nexus_process(f"Contexto do código: {st.session_state['last_result']}. Pergunta do usuário: {chat_input}", "Suporte via Chat", "")
            st.markdown(resposta_chat)

# --- BIBLIOTECA ---
st.divider()
with st.expander("📚 Biblioteca de Prompts de Elite"):
    st.code("Nexus, use o Incremento Mágico para adicionar um sistema de login.")
    st.code("Analise a performance deste script e otimize o código.")
