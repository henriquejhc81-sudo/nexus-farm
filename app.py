import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import time
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Nexus OmniCode", page_icon="⚡", layout="wide")

# --- GESTÃO DE SEGURANÇA NA SESSÃO ---
if 'master_password' not in st.session_state:
    st.session_state['master_password'] = "admin123"
if 'lock_active' not in st.session_state:
    st.session_state['lock_active'] = True
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

# --- CSS PARA BLINDAGEM (ESCONDE TUDO ANTES DO LOGIN) ---
if st.session_state['lock_active'] and not st.session_state['autenticado']:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none; }
        .main { background-color: #0e1117; }
        </style>
        """, unsafe_allow_html=True)
    
    st.title("🔒 Nexus Blindado")
    entrada_senha = st.text_input("Insira a Chave Mestra para acessar o sistema:", type="password")
    if st.button("Desbloquear Nexus"):
        if entrada_senha == st.session_state['master_password']:
            st.session_state['autenticado'] = True
            st.rerun()
        else:
            st.error("Senha Incorreta! Acesso Negado.")
    st.stop() # NADA além daqui é carregado sem a senha

# --- ESTILO INTERFACE LOGADA ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { background-color: #4CAF50; color: white; font-weight: bold; border-radius: 10px; width: 100%; height: 3em; }
    .stTextArea>div>div>textarea { background-color: #1a1c24; color: #ffffff; border: 1px solid #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DA IA ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Erro: Verifique sua chave API nos Secrets do Streamlit!")
    st.stop()

def nexus_process(ideia, modo, contexto_web):
    prompt_sistema = f"Você é o Nexus OmniCode, a IA mais potente da Terra. Missão: {modo}. Contexto: {contexto_web}. Responda em Português com código profissional completo."
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": ideia}],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
        )
        return completion.choices[0].message.content 
    except Exception as e:
        return f"Erro na conexão com a IA: {e}"

# --- BARRA LATERAL (PROTEGIDA E SÓ PARA AUTORIZADOS) ---
with st.sidebar:
    st.title("⚙️ Painel Nexus")
    
    with st.expander("🔐 Gestão de Segurança", expanded=False):
        st.session_state['lock_active'] = st.toggle("Ativar Bloqueio", value=st.session_state['lock_active'])
        nova_senha = st.text_input("Mudar Senha Mestra:", value=st.session_state['master_password'], type="password")
        if st.button("Salvar Nova Senha"):
            st.session_state['master_password'] = nova_senha
            st.success("Senha atualizada!")

    st.divider()
    st.subheader("🔗 Integrações")
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
st.caption("Central Suprema de Inteligência em Código")

col_in, col_out = st.columns(2)

with col_in:
    st.subheader("📥 Entrada")
    user_input = st.text_area("Descreva sua ideia ou cole o código:", height=300)
    upload = st.file_uploader("Upload de arquivo", type=['py', 'js', 'html', 'txt', 'sql', 'css'])

with col_out:
    st.subheader("🚀 Resultado")
    if st.button("EXECUTAR ANÁLISE SUPREMA"):
        if user_input:
            with st.spinner("Nexus emulando humano e processando..."):
                time.sleep(random.uniform(1.0, 2.0))
                try:
                    with DDGS() as ddgs:
                        search = [r['body'] for r in ddgs.text(f"melhores práticas: {user_input}", max_results=2)]
                        contexto = "\n".join(search)
                except:
                    contexto = "Base interna ativa."
                
                resultado = nexus_process(user_input, modo, contexto)
                st.session_state['last_result'] = resultado
                st.markdown(resultado)
        else:
            st.error("Digite algo para o Nexus processar!")

    # BOTÃO DE DOWNLOAD (CORRIGIDO)
    if 'last_result' in st.session_state:
        st.download_button(
            label="📥 BAIXAR SOLUÇÃO AGORA",
            data=st.session_state['last_result'],
            file_name="nexus_output.py",
            mime="text/x-python"
        )

# --- CHAT PRO ---
st.divider()
st.subheader("💬 Nexus Chat Pro")
chat_input = st.text_input("Dúvida sobre o código gerado?")
if chat_input and 'last_result' in st.session_state:
    with st.chat_message("assistant"):
        resposta_chat = nexus_process(f"Sobre este código: {st.session_state['last_result']}. Pergunta: {chat_input}", "Suporte Chat", "")
        st.markdown(resposta_chat)
