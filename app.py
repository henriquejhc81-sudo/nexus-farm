import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import time
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Nexus OmniCode", page_icon="⚡", layout="wide")

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
        return completion.choices.message.content 
    except Exception as e:
        return f"Erro na conexão com a IA: {e}"

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("⚙️ Painel Nexus")
    st.caption("Projeto Melhor do Mundo")
    
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
st.caption("Central Suprema de Inteligência em Código - Versão Multi-Formato")

col_in, col_out = st.columns(2)

with col_in:
    st.subheader("📥 Entrada")
    user_input = st.text_area("Descreva sua ideia ou cole o código:", height=300, placeholder="Ex: Crie um sistema de gestão de vendas...")
    upload = st.file_uploader("Upload de arquivo para análise", type=['py', 'js', 'html', 'txt', 'sql', 'css'])

with col_out:
    st.subheader("🚀 Resultado da IA")
    if st.button("EXECUTAR ANÁLISE SUPREMA"):
        if user_input:
            with st.spinner("Nexus processando bases globais..."):
                time.sleep(random.uniform(0.5, 1.5))
                try:
                    with DDGS() as ddgs:
                        search = [r['body'] for r in ddgs.text(f"melhores práticas: {user_input}", max_results=2)]
                        contexto = "\n".join(search)
                except:
                    contexto = "Usando inteligência interna."
                
                resultado = nexus_process(user_input, modo, contexto)
                st.session_state['last_result'] = resultado
                st.markdown(resultado)
        else:
            st.error("Digite algo para começar!")

    # NOVA FUNÇÃO: SELETOR DE FORMATO E DOWNLOAD
    if 'last_result' in st.session_state:
        st.divider()
        st.subheader("💾 Opções de Download")
        formato = st.selectbox("Escolha o formato do arquivo:", [".py", ".js", ".html", ".txt", ".sql", ".css"])
        
        # Mapeamento de Mime Types para cada formato
        mimes = {".py": "text/x-python", ".js": "text/javascript", ".html": "text/html", ".txt": "text/plain", ".sql": "text/x-sql", ".css": "text/css"}
        
        st.download_button(
            label=f"📥 BAIXAR COMO {formato.upper()}",
            data=st.session_state['last_result'],
            file_name=f"nexus_output{formato}",
            mime=mimes[formato]
        )

# --- CHAT PRO ---
st.divider()
st.subheader("💬 Nexus Chat Pro")
chat_input = st.text_input("Dúvida sobre o código gerado acima?")
if chat_input and 'last_result' in st.session_state:
    with st.chat_message("assistant"):
        resposta_chat = nexus_process(f"Sobre este código: {st.session_state['last_result']}. Pergunta: {chat_input}", "Suporte Chat", "")
        st.markdown(resposta_chat)
