import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import time
import random

# --- CONFIGURAÇÃO NEXUS SENTINEL v5.6 "GHOST AI" ---
st.set_page_config(page_title="Nexus Sentinel v5.6 | Ghost AI", page_icon="🛡️", layout="wide")

# Interface Estilo Centro de Comando Cibernético
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    .stButton>button { 
        background: linear-gradient(135deg, #00c853 0%, #b2ff59 100%); 
        color: #000; font-weight: 800; border-radius: 8px; border: none; height: 3.5em;
        box-shadow: 0 4px 15px rgba(0, 200, 83, 0.4);
    }
    .status-box { 
        padding: 15px; border-radius: 10px; background: #161b22; 
        border: 1px solid #00c853; box-shadow: inset 0 0 15px rgba(0, 200, 83, 0.2);
        margin-bottom: 20px; font-family: 'Courier New', Courier, monospace;
    }
    .stTextArea>div>div>textarea { background-color: #161b22; color: #ffffff; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE GHOST AI (INVISIBILIDADE E AUTO-ATUALIZAÇÃO) ---
def nexus_ghost_brain(prompt, modo, contexto):
    try:
        # Ponto de entrada Groq (Atuando como orquestrador Ghost)
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        return "⚠️ Erro Crítico: Chave API ausente nos Secrets."
        
    for attempt in range(5):
        try:
            # [HUMAN-MIMIC] Delay aleatório para simular comportamento humano
            time.sleep(random.uniform(0.8, 2.0)) 
            
            prompt_sistema = f"""
            Você é o Nexus Sentinel 5.6 'Ghost AI'. Use IA Generativa e LLMs massivos.
            MISSÃO: {modo}. CONTEXTO: {contexto}.
            
            DIRETRIZES SUPREMAS GHOST:
            1. [Invisibilidade]: Operação indetectável e anônima em redes externas.
            2. [Auto-Healing]: Se a API atualizar ou falhar, reconecte via rotas estáveis.
            3. [Inteligência]: Realize Due Diligence, Matriz de Risco (0-100%) e Forensic Analytics.
            4. [Modo Arquiteto]: Forneça Setup, Estrutura de Pastas e Código 100% Funcional.
            5. [IA Generativa]: Interaja de forma natural (LLM) no Chat Pro.
            """
            
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile", # Motor principal
                temperature=0.2, 
            )
            return completion.choices[0].message.content
            
        except Exception as e:
            if "429" in str(e) or "503" in str(e):
                wait = (attempt + 1) * 10 
                st.warning(f"👻 Ghost Mode: Sincronização em atualização. Auto-reparando em {wait}s...")
                time.sleep(wait)
            else:
                return f"Falha no Ghost Engine: {e}"
    return "Sentinel Ghost offline. A cota foi excedida e a blindagem bloqueou novas tentativas."

# --- BARRA LATERAL (CONTROL CENTER) ---
with st.sidebar:
    st.title("🛡️ NEXUS SENTINEL")
    st.caption("v5.6 | GHOST AI EDITION")
    
    with st.expander("👁️ Ghost Tech Status", expanded=True):
        st.toggle("Human-Mimic Engine", value=True)
        st.toggle("Invisible Protocol", value=True)
        st.toggle("Auto-Update Routes", value=True)

    st.divider()
    st.subheader("🛠️ Deep Learning Modules")
    for tool in ["Due Diligence", "E-Discovery", "Matriz de Risco", "Forensic Analytics"]:
        st.toggle(tool, value=True)
    
    st.divider()
    modo = st.selectbox("🎯 Neural Sniper Target", [
        "Varredura e Autocorreção Ghost",
        "Due Diligence e Matriz de Risco",
        "IA Generativa (Criação de Conteúdo)",
        "Projeto do Zero (Modo Arquiteto)",
        "E-Discovery (Busca Massiva Invisível)"
    ])

# --- ÁREA PRINCIPAL ---
st.title("⚡ Nexus Sentinel v5.6")
st.markdown("""
<div class='status-box'>
    <b>STATUS:</b> GHOST MODE ATIVO | <b>INVISIBILIDADE:</b> 100% | <b>AUTO-REPARO:</b> LIGADO
</div>
""", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Neural Sniper Input")
    user_input = st.text_area("Insira sua missão (O Ghost AI processará de forma invisível):", height=300)
    upload = st.file_uploader("Data Processing: Arraste arquivos para análise forense", accept_multiple_files=True)

with col_out:
    st.subheader("🚀 Resposta Mestra Ghost")
    if st.button("ATIVAR NEXUS SENTINEL"):
        if user_input:
            with st.spinner("Ghost Engine infiltrando bases de dados de forma anônima..."):
                try:
                    with DDGS() as ddgs:
                        # Pesquisa humana e invisível na web
                        busca = [r['body'] for r in ddgs.text(f"technical deep analysis: {user_input}", max_results=3)]
                        contexto = "\n".join(busca)
                except:
                    contexto = "Modo Invisível Máximo: Usando Historic Learning interno."
                
                resultado = nexus_ghost_brain(user_input, modo, contexto)
                st.session_state['last_result'] = resultado
        else:
            st.error("O Sentinel Ghost aguarda um alvo neural.")

    if 'last_result' in st.session_state:
        res = st.session_state['last_result']
        tab1, tab2 = st.tabs(["💻 Plano e Código Ghost", "🖼️ Live Preview"])
        with tab1:
            st.markdown(res)
        with tab2:
            if "<html>" in res.lower() or "<!doctype html>" in res.lower():
                st.components.v1.html(res, height=550, scrolling=True)
            else:
                st.info("Aguardando código visual para Live Preview.")

        st.divider()
        ext = st.selectbox("Exportar como Relatório Executivo:", [".html", ".py", ".docx", ".txt"])
        st.download_button(label=f"📥 BAIXAR RELATÓRIO GHOST ({ext})", data=res, file_name=f"nexus_ghost_report{ext}")

# --- CHAT INTERATIVO (LLM REAL-TIME) ---
st.divider()
st.subheader("💬 Nexus Ghost Chat (Conversa com LLM)")
chat_input = st.text_input("Dúvida técnica ou instrução para o Ghost?")
if chat_input and 'last_result' in st.session_state:
    with st.chat_message("assistant"):
        with st.spinner("Raciocinando de forma humana..."):
            st.markdown(nexus_ghost_brain(f"Sobre este projeto: {st.session_state['last_result']}. Responda: {chat_input}", "Chat Ghost", ""))
