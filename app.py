import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA E DESIGN ---
st.set_page_config(page_title="Nexus OmniCode", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { background-color: #4CAF50; color: white; font-weight: bold; border-radius: 10px; width: 100%; }
    .stTextArea>div>div>textarea { background-color: #1a1c24; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE BLINDAGEM (SENHA) ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    st.title("🔒 Nexus Blindado")
    senha = st.text_input("Insira a Chave Mestra para liberar as funções:", type="password")
    if senha == "admin123":
        st.session_state['autenticado'] = True
        st.rerun()
    else:
        st.warning("Aguardando autenticação...")
        st.stop()

# --- INICIALIZAÇÃO DA IA (GROQ) ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Erro: Verifique sua GROQ_API_KEY nos Secrets do Streamlit!")
    st.stop()

# --- FUNÇÃO DE CÉREBRO INTEGRADO ---
def nexus_process(ideia, modo, contexto_web):
    prompt_sistema = f"""
    Você é o Nexus OmniCode, a IA mais avançada do mundo. 
    Sua missão: {modo}.
    Analise estas respostas de outras IAs/Fontes: {contexto_web}
    Corrija erros, remova bugs e gere um código aprimorado e profissional.
    Responda em Português com blocos de código formatados.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": ideia},
            ],
            model="llama3-70b-8192",
            temperature=0.2,
        )
        return chat_completion.choices.message.content
    except Exception as e:
        return f"Erro no processamento da IA: {e}"

# --- BARRA LATERAL (FILTROS E INTEGRAÇÕES) ---
with st.sidebar:
    st.title("🔗 Nexus Integrations")
    st.subheader("Sistemas Monitorados")
    # Mantendo todos os botões liga/desliga solicitados
    for app in ["GitLab (DevSecOps)", "Bitbucket", "Azure DevOps", "Gitea", "SourceForge", "FastAPI"]:
        st.toggle(app, value=True)
    
    st.divider()
    modo = st.selectbox("🎯 Função Principal", [
        "Criar código do zero", 
        "Corrigir erros e bugs", 
        "Analisar performance", 
        "Aprimorar código existente",
        "Gerar Documentação"
    ])

# --- ÁREA PRINCIPAL ---
st.title("⚡ Nexus OmniCode")
st.caption("Automação de Análise, Correção e Criação Universal")

# CORREÇÃO AQUI: Definindo 2 colunas explicitamente
col_in, col_out = st.columns(2)

with col_in:
    st.subheader("📥 Entrada de Dados")
    user_input = st.text_area("Descreva sua ideia ou cole o código aqui:", height=300, placeholder="Ex: Analise este código e corrija erros de segurança...")
    upload = st.file_uploader("Upload de arquivo para análise", type=['py', 'js', 'html', 'txt', 'sql'])

with col_out:
    st.subheader("🚀 Resultado da IA Personalizada")
    if st.button("EXECUTAR ANÁLISE GLOBAL"):
        if user_input:
            with st.spinner("Nexus consultando bases mundiais e gerando código perfeito..."):
                # Busca "Invisível" para alimentar a inteligência
                contexto = ""
                try:
                    with DDGS() as ddgs:
                        search_results = [r['body'] for r in ddgs.text(f"melhores soluções e bugs para: {user_input}", max_results=3)]
                        contexto = "\n".join(search_results)
                except:
                    contexto = "Usando base interna de conhecimento."

                # Geração do código aprimorado
                resultado_final = nexus_process(user_input, modo, contexto)
                st.markdown(resultado_final)
                
                st.download_button(
                    label="📥 Baixar Código Nexus",
                    data=resultado_final,
                    file_name="nexus_optimized.txt",
                    mime="text/plain"
                )
        else:
            st.error("O campo de entrada não pode estar vazio!")

# --- BIBLIOTECA DE COMANDOS ---
st.divider()
with st.expander("📚 Biblioteca de Comandos Copie e Cole"):
    st.code("Nexus, aja como minha IA personalizada e crie um sistema para o GitLab.")
    st.code("Analise este código e gere uma versão aprimorada sem erros.")
    st.code("Crie uma automação que leia arquivos e faça upload para o Azure.")
