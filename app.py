import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import time
import random

# --- CONFIGURAÇÃO NEXUS SENTINEL v5.7 "INCEPTION" ---
st.set_page_config(page_title="Nexus Sentinel v5.7 | Inception", page_icon="🛡️", layout="wide")

# CSS - Centro de Comando Cibernético
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
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR GHOST AI COM INJEÇÃO DE DNA E CORREÇÃO DE ATRIBUTO ---
def nexus_inception_brain(prompt, modo, contexto, dna_ativo):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        return "⚠️ Erro Crítico: Chave API ausente!"
        
    for attempt in range(5):
        try:
            time.sleep(random.uniform(0.5, 1.5)) 
            
            dna_prompt = ""
            if dna_ativo:
                dna_prompt = """
                INJEÇÃO DE DNA NEXUS ATIVA:
                Implemente obrigatoriamente no código gerado:
                1. Motor Neural (Orquestração Multi-IA).
                2. Tecnologia Ghost AI (Invisible & Auto-Healing).
                3. Segurança Blindada (Logs, Sanitização SQL/XSS, Snyk).
                4. Interface Cyber-Sentinel (HTML/CSS Neon).
                """

            prompt_sistema = f"Você é o Nexus Sentinel 5.7. MISSÃO: {modo}. {dna_prompt} CONTEXTO: {contexto}."
            
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.2,
            )
            # CORREÇÃO DEFINITIVA DO ERRO 'list' object has no attribute 'message'
            return completion.choices[0].message.content
            
        except Exception as e:
            if "429" in str(e):
                wait = (attempt + 1) * 8
                st.warning(f"🛡️ Auto-Healing em curso... Reconectando em {wait}s")
                time.sleep(wait)
            else:
                return f"Falha no Motor: {e}"
    return "Sentinel Offline após falhas de cota."

# --- BARRA LATERAL (DNA CONTROL) ---
with st.sidebar:
    st.title("🛡️ NEXUS SENTINEL")
    st.caption("v5.7 | INCEPTION DNA")
    
    with st.expander("🧬 DNA Tecnológico", expanded=True):
        dna_ativo = st.toggle("Injetar DNA Nexus", value=True)
        st.toggle("Human-Mimic Engine", value=True)
        st.toggle("Invisible Protocol", value=True)

    st.divider()
    st.subheader("🛠️ Deep Learning Engine")
    for tool in ["Due Diligence", "E-Discovery", "Matriz de Risco", "Forensic Analytics"]:
        st.toggle(tool, value=True)
    
    modo = st.selectbox("🎯 Neural Target", [
        "Projeto do Zero (Modo Arquiteto)",
        "Varredura e Autocorreção Ghost",
        "Due Diligence e Matriz de Risco",
        "Incremento Mágico + DNA",
        "E-Discovery (Busca Invisível)"
    ])

# --- ÁREA PRINCIPAL ---
st.title("⚡ Nexus Sentinel v5.7")
st.markdown(f"<div class='status-box'><b>DNA:</b> {'ATIVO' if dna_ativo else 'OFF'} | <b>GHOST:</b> LIGADO | <b>SISTEMA:</b> INCEPTION</div>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Missão Sniper")
    user_input = st.text_area("Descreva o projeto (DNA injetado automaticamente):", height=300)
    upload = st.file_uploader("Upload de Contexto", accept_multiple_files=True)

with col_out:
    st.subheader("🚀 Resposta Inception")
    if st.button("ATIVAR NEXUS SENTINEL"):
        if user_input:
            with st.spinner("Injetando DNA Nexus de forma invisível..."):
                try:
                    with DDGS() as ddgs:
                        busca = [r['body'] for r in ddgs.text(f"high level architecture: {user_input}", max_results=2)]
                        contexto = "\n".join(busca)
                except:
                    contexto = "Base interna ativa."
                
                resultado = nexus_inception_brain(user_input, modo, contexto, dna_ativo)
                st.session_state['last_result'] = resultado
        else:
            st.error("Insira o alvo da missão.")

    if 'last_result' in st.session_state:
        res = st.session_state['last_result']
        tab1, tab2 = st.tabs(["💻 Código DNA Nexus", "🖼️ Live Preview"])
        with tab1:
            st.markdown(res)
        with tab2:
            if "<html>" in res.lower() or "<!doctype html>" in res.lower():
                st.components.v1.html(res, height=550, scrolling=True)
            else:
                st.info("Aguardando interface visual.")

        st.divider()
        ext = st.selectbox("Exportar como:", [".html", ".py", ".docx", ".txt"])
        st.download_button(label=f"📥 BAIXAR PROJETO ({ext})", data=res, file_name=f"nexus_inception_project{ext}")

# --- CHAT ---
st.divider()
st.subheader("💬 Nexus Ghost Chat")
chat_input = st.text_input("Dúvida técnica?")
if chat_input and 'last_result' in st.session_state:
    with st.chat_message("assistant"):
        st.markdown(nexus_inception_brain(f"Sobre este projeto: {st.session_state['last_result']}. Pergunta: {chat_input}", "Chat Support", "", dna_ativo))
