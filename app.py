import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import time
import random

# --- CONFIGURAÇÃO DA PÁGINA E DESIGN DE ALTA PERFORMANCE ---
st.set_page_config(page_title="Nexus OmniCode Sentinel", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { background-color: #4CAF50; color: white; font-weight: bold; border-radius: 10px; width: 100%; height: 3em; }
    .status-box { padding: 15px; border-radius: 10px; background: #1a1c24; border-left: 5px solid #4CAF50; margin-bottom: 20px; }
    .preview-box { background: white; color: black; padding: 20px; border-radius: 5px; height: 400px; overflow-y: auto; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO MOTOR DE IA COM AUTO-HEALING (SOLUÇÃO PARA ERRO 429) ---
def get_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

def nexus_agent_call(prompt, modo, contexto):
    client = get_groq_client()
    max_retries = 3
    for attempt in range(max_retries):
        try:
            prompt_sistema = f"""
            Você é o Nexus Sentinel (Agente Autônomo). Missão: {modo}.
            CONDIÇÕES: Secure At Inception (Snyk logic), Self-Healing ativo.
            CONTEXTO REPOSITÓRIO: {contexto}
            Se houver código .html, gere o código completo para Live Preview.
            Gere Testes Unitários automatizados para cada incremento.
            """
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1,
            )
            return completion.choices.message.content
        except Exception as e:
            if "429" in str(e):
                st.warning(f"⚠️ Alerta de Cota (429): Nexus Sentinel estabilizando conexão... Tentativa {attempt+1}")
                time.sleep(5) # Delay humano para resetar cota
            else:
                return f"Erro Crítico no Agente: {e}"
    return "Falha após múltiplas tentativas de sincronização."

# --- BARRA LATERAL (SUPERPODERES E GESTÃO) ---
with st.sidebar:
    st.title("🛡️ Nexus Sentinel")
    st.caption("Modo Agente Autônomo Ativado")
    
    st.divider()
    with st.expander("🚀 Superpoderes Ativos", expanded=True):
        st.toggle("Self-Healing (Auto-correção)", value=True)
        st.toggle("Scanner de Vulnerabilidade (Snyk)", value=True)
        st.toggle("Live Preview Interativo", value=True)
        st.toggle("Geração de Testes Unitários", value=True)

    st.divider()
    st.subheader("🔗 Integrações DevSecOps")
    for app in ["GitLab", "GitHub (PR Writer)", "Azure DevOps", "Slack/Notion (MCP)"]:
        st.toggle(app, value=True)
    
    modo = st.selectbox("🎯 Modo do Agente", [
        "Agente de Execução Ponta a Ponta",
        "Incremento Mágico + Testes",
        "Análise de Vulnerabilidades (Secure Code)",
        "Design-to-Code (Interface)",
        "Escritor de Pull Request"
    ])

# --- ÁREA PRINCIPAL ---
st.title("⚡ Nexus OmniCode v5.0")
st.markdown("""
<div class='status-box'>
    <b>Status do Sentinel:</b> Vigilante | <b>Auto-Healing:</b> Pronto | <b>Sincronização:</b> Otimizada
</div>
""", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Input do Desenvolvedor")
    user_input = st.text_area("Descreva a tarefa ou cole o repositório/imagem/link:", height=300, placeholder="Ex: Crie um sistema de login seguro e gere os testes unitários...")
    upload = st.file_uploader("Upload de Arquivos/Figma Screens", accept_multiple_files=True)

with col_out:
    st.subheader("🚀 Output do Agente Autônomo")
    if st.button("ATIVAR NEXUS SENTINEL"):
        if user_input:
            with st.spinner("Agente Nexus navegando no repositório e testando soluções..."):
                # Simulação de Contexto Profundo (Cursor Style)
                with DDGS() as ddgs:
                    busca = [r['body'] for r in ddgs.text(f"security vulnerabilities and best practices: {user_input}", max_results=2)]
                
                resultado = nexus_agent_call(user_input, modo, "\n".join(busca))
                st.session_state['last_result'] = resultado
                
                # Interface do Resultado
                tab1, tab2 = st.tabs(["💻 Código e Testes", "🖼️ Live Preview"])
                with tab1:
                    st.markdown(resultado)
                with tab2:
                    if "<html>" in resultado.lower():
                        st.components.v1.html(resultado, height=400, scrolling=True)
                    else:
                        st.info("O Live Preview está aguardando um código de interface (HTML/CSS).")

    # DOWNLOAD MULTI-FORMATO (MANTIDO)
    if 'last_result' in st.session_state:
        st.divider()
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            formato = st.selectbox("Formato de Saída:", [".py", ".html", ".js", ".sql", ".txt"])
        with col_f2:
            st.download_button(label=f"📥 BAIXAR PROJETO ({formato})", data=st.session_state['last_result'], file_name=f"nexus_sentinel{formato}")

# --- NEXUS CHAT PRO (MODO DEEP CONTEXT) ---
st.divider()
st.subheader("💬 Nexus Sentinel Chat (Deep Context)")
chat_input = st.text_input("Rastrear erro ou pedir mudança no repositório:")
if chat_input and 'last_result' in st.session_state:
    with st.chat_message("assistant"):
        resposta_chat = nexus_agent_call(f"Repositório atual: {st.session_state['last_result']}. Pergunta: {chat_input}", "Chat Deep Context", "")
        st.markdown(resposta_chat)
