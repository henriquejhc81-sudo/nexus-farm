import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import time
import random

# --- CONFIGURAÇÃO DA PÁGINA E DESIGN ---
st.set_page_config(page_title="Nexus OmniCode", page_icon="⚡", layout="wide")

# --- GERENCIAMENTO DE SENHA E SEGURANÇA ---
if 'master_password' not in st.session_state:
    st.session_state['master_password'] = "admin123"
if 'lock_active' not in st.session_state:
    st.session_state['lock_active'] = True
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

# --- ESTILO ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { background-color: #4CAF50; color: white; font-weight: bold; border-radius: 10px; width: 100%; height: 3em; }
    .stTextArea>div>div>textarea { background-color: #1a1c24; color: #ffffff; border: 1px solid #4CAF50; }
    .chat-box { padding: 10px; background: #1a1c24; border-radius: 10px; border-left: 5px solid #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

# --- TELA DE BLOQUEIO ---
if st.session_state['lock_active'] and not st.session_state['autenticado']:
    st.title("🔒 Nexus Blindado")
    entrada_senha = st.text_input("Insira a Chave Mestra:", type="password")
    if st.button("Desbloquear Sistema"):
        if entrada_senha == st.session_state['master_password']:
            st.session_state['autenticado'] = True
            st.rerun()
        else:
            st.error("Senha Incorreta!")
    st.stop()

# --- INICIALIZAÇÃO DA IA ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Erro: Configure a API Key nos Secrets!")
    st.stop()

def nexus_process(ideia, modo, contexto_web):
    prompt_sistema = f"Você é o Nexus OmniCode. Missão: {modo}. Contexto: {contexto_web}. Responda em Português com código limpo."
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": ideia}],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
        )
        return completion.choices.message.content
    except Exception as e:
        return f"Erro: {e}"

# --- BARRA LATERAL (GESTÃO E FILTROS) ---
with st.sidebar:
    st.title("⚙️ Nexus Manage")
    
    # Gestão de Senha
    with st.expander("🔐 Segurança e Chave"):
        st.session_state['lock_active'] = st.toggle("Ativar Senha", value=st.session_state['lock_active'])
        nova_senha = st.text_input("Nova Senha Mestra:", value=st.session_state['master_password'], type="password")
        if st.button("Salvar Nova Senha"):
            st.session_state['master_password'] = nova_senha
            st.success("Senha alterada!")

    st.divider()
    st.subheader("🔗 Integrações")
    for app in ["GitLab", "Bitbucket", "Azure", "Gitea", "SourceForge", "FastAPI"]:
        st.toggle(app, value=True)
    
    st.divider()
    modo = st.selectbox("🎯 Função Principal", ["Criar código do zero", "Corrigir erros e bugs", "Incremento Mágico (Evoluir Código)", "Analisar performance"])

# --- ÁREA PRINCIPAL ---
st.title("⚡ Nexus OmniCode")
st.caption("A Central Suprema de Inteligência em Código")

col_in, col_out = st.columns(2)

with col_in:
    st.subheader("📥 Entrada de Inteligência")
    user_input = st.text_area("Descreva sua ideia ou cole o código:", height=300)
    upload = st.file_uploader("Subir arquivo", type=['py', 'js', 'html', 'txt'])

with col_out:
    st.subheader("🚀 Resultado Nexus")
    if st.button("EXECUTAR ANÁLISE SUPREMA"):
        if user_input:
            with st.spinner("Simulando comportamento humano e processando..."):
                time.sleep(random.uniform(1.0, 2.5))
                with DDGS() as ddgs:
                    search = [r['body'] for r in ddgs.text(f"melhores práticas: {user_input}", max_results=2)]
                    contexto = "\n".join(search)
                
                resposta = nexus_process(user_input, modo, contexto)
                st.session_state['last_result'] = resposta
                st.markdown(resposta)
        else:
            st.error("Insira dados!")

    # BOTÃO DE DOWNLOAD IMEDIATO (Sugerido)
    if 'last_result' in st.session_state:
        st.download_button(
            label="📥 BAIXAR CÓDIGO AGORA",
            data=st.session_state['last_result'],
            file_name="nexus_solucao.py",
            mime="text/plain"
        )

# --- NEXUS CHAT (Sugerido) ---
st.divider()
st.subheader("💬 Nexus Chat (Conversar com a Solução)")
chat_input = st.text_input("Pergunte algo sobre o código gerado ou peça mudanças rápidas:")
if chat_input and 'last_result' in st.session_state:
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            conversa = nexus_process(f"Sobre este código: {st.session_state['last_result']}. Responda: {chat_input}", "Chat de Suporte", "")
            st.markdown(conversa)

st.divider()
with st.expander("📚 Biblioteca de Prompts"):
    st.code("Nexus, use o Incremento Mágico para adicionar um gráfico de pizza.")
