import streamlit as st
from groq import Groq
import google.generativeai as genai
import os

try:
    from ghost_engine import GhostEngine
except ImportError:
    st.error("Erro: ghost_engine.py ausente!")

# --- CONFIGURAÇÃO E CSS ORIGINAL v5.9/6.1 ---
st.set_page_config(page_title="Nexus Prime v6.1", page_icon="⚡", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    .stButton>button { 
        background: linear-gradient(135deg, #00c853 0%, #00e5ff 100%); 
        color: #000; font-weight: 800; border-radius: 8px; border: none; height: 3.5em;
    }
    .status-box { 
        padding: 15px; border-radius: 10px; background: #161b22; 
        border: 1px solid #00c853; box-shadow: inset 0 0 15px rgba(0, 200, 83, 0.2);
        margin-bottom: 20px; font-family: 'Courier New', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR NEURAL (HÍBRIDO) ---
def nexus_engine_prime(prompt, modo, contexto, engine):
    try:
        if engine == "Groq (Ultra-Fast)":
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            comp = client.chat.completions.create(
                messages=[{"role": "system", "content": f"Nexus Prime. Missão: {modo}. Contexto: {contexto}"}, 
                          {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile", temperature=0.2)
            return comp.choices[0].message.content
        else:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-pro')
            return model.generate_content(f"{modo}: {prompt} \nContexto: {contexto}").text
    except Exception as e:
        return f"Erro no Motor: {e}"

# --- SIDEBAR (RESTAURO DE TODAS AS FUNÇÕES) ---
with st.sidebar:
    st.title("🛡️ NEXUS PRIME")
    st.caption("v6.1 | RECON & STRIKE")
    
    with st.expander("🧬 DNA & Módulos", expanded=True):
        genesis_on = st.toggle("Gênesis Creator", value=False)
        legacy_on = st.toggle("Legacy Protector", value=True)
        ghost_mode = st.toggle("Ghost Stealth (AES-256)", value=False)
    
    st.divider()
    ia_provider = st.selectbox("Engine Neural", ["Groq (Ultra-Fast)", "Gemini Pro"])
    modo = st.selectbox("🎯 Neural Target", ["Recon & Strike", "Genesis: Arquitetura", "Due Diligence"])

# --- ÁREA PRINCIPAL ---
st.title("⚡ Nexus Prime Engine")
st.markdown(f"<div class='status-box'><b>STATUS:</b> VIGILANTE | <b>GHOST:</b> {'ATIVO' if ghost_mode else 'OFF'} | <b>LEGACY:</b> {'ON' if legacy_on else 'OFF'}</div>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Missão Sniper")
    user_input = st.text_area("Descreva a missão ou cole o log:", height=300)
    
    if st.button("EXECUTAR NEXUS PRIME"):
        recon_final = ""
        if ghost_mode:
            try:
                ghost = GhostEngine()
                recon_final = f"{ghost.scan_local_credentials()} | {ghost.shadow_cookie_scan()}"
                st.success("👻 Ghost Recon & Shadow-Cookie Ativos!")
            except:
                st.error("Erro na Chave .key!")
        
        with st.spinner("Sintetizando..."):
            res = nexus_engine_prime(user_input, modo, recon_final, ia_provider)
            st.session_state['last_res'] = res

with col_out:
    st.subheader("🚀 Resposta Mestra")
    if 'last_res' in st.session_state:
        st.markdown(st.session_state['last_res'])
        st.download_button("📥 Baixar Projeto", st.session_state['last_res'], file_name="nexus_output.md")
