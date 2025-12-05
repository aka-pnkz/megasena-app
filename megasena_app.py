import streamlit as st
import pandas as pd
import numpy as np
import itertools
from collections import Counter, defaultdict
import plotly.express as px
from datetime import datetime, timedelta
import io

st.set_page_config(
    page_title="Mega Sena App",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# [FUNÇÕES iguais às anteriores - carregar_dados_realistas, analise_completa, validar_jogo, gerar_jogos, monte_carlo]
# ... (manter todas as funções anteriores)

# ===============================================
# INTERFACE PRINCIPAL CORRIGIDA
# ===============================================
st.title("🎯 Mega Sena App v3.4")

col1, col2 = st.columns([2,1])
with col1:
    st.markdown("""
    ## 🚀 **Como usar em 3 passos:**
    1. **Escolha** quantidade de jogos (1-100)
    2. **Selecione** estratégia (👈 explicações)
    3. **Clique** "🔄 Analisar" → **📥 Baixe CSV**
    """)
with col2:
    st.success("✅ Grátis | Mobile | Auto-update")

st.markdown("---")

# Sidebar
st.sidebar.markdown("### ⚙️ **Configurações**")
numeros_por_jogo = st.sidebar.radio("🎮 Números por Jogo", [6, 7], index=0)
qtd_jogos = st.sidebar.number_input("Quantidade de jogos:", min_value=1, max_value=100, value=7, step=1)
estrategia = st.sidebar.selectbox("🎯 Estratégia:", [
    "🥇 Descarte Wheeling - Garante Quadra",
    "⚖️ Mix Balance - Quentes + Atrasados", 
    "📊 Setorial - Distribuição perfeita"
])

if st.sidebar.button("🔄 **Analisar 2800 Concursos**", type="primary", use_container_width=True):
    with st.spinner("🔥 Analisando histórico completo..."):
        df = carregar_dados_realistas()
        analise = analise_completa(df)
        st.session_state.df = df
        st.session_state.analise = analise
        st.session_state.numeros_por_jogo = numeros_por_jogo
        st.session_state.qtd_jogos = qtd_jogos
        st.session_state.estrategia = estrategia.split(" - ")[0]
        st.rerun()

# ===============================================
# RESULTADOS - DOWNLOAD VISÍVEL + TABELA
# ===============================================
if 'analise' in st.session_state:
    analise = st.session_state.analise
    numeros_selecionados = st.session_state.numeros_por_jogo
    qtd_selecionada = st.session_state.qtd_jogos
    estrategia_limpa = st.session_state.estrategia
    
    # DASHBOARD
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("📊 Concursos", f"{len(analise['df']):,}")
    with col2: st.metric("🔥 Top Frequente", max(analise['freq'], key=analise['freq'].get))
    with col3: st.metric("❄️ Top Atrasado", max(analise['atrasos'], key=analise['atrasos'].get))
    
    st.info(f"🎯 **{qtd_selecionada} jogos** | **{numeros_selecionados} números** | **{estrategia_limpa}**")
    
    # GERAR JOGOS
    jogos = gerar_jogos(analise, qtd_selecionada, estrategia_limpa, numeros_selecionados)
    
    # ===============================================
    # TABELA DE JOGOS (SEMPRE VISÍVEL)
    # ===============================================
    st.header(f"🎮 **{qtd_selecionada} Jogos Gerados**")
    
    jogos_df = pd.DataFrame([
        {'Jogo': f"Jogo {i+1}", **{f'N{j+1}': f"{n:2d}" for j,n in enumerate(jogo)}}
        for i, jogo in enumerate(jogos)
    ])
    
    # MOSTRAR TABELA
    st.dataframe(jogos_df, use_container_width=True, height=400)
    
    # ===============================================
    # DOWNLOAD CSV - BEM VISÍVEL
    # ===============================================
    st.markdown("---")
    
    col_dl1, col_dl2 = st.columns([1,3])
    with col_dl1:
        csv = jogos_df.to_csv(index=False)
        st.download_button(
            label="📥 **DOWNLOAD CSV**",
            data=csv,
            file_name=f"megasena_{numeros_selecionados}n_{estrategia_limpa.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    
    with col_dl2:
        st.markdown("**✅ CSV pronto para lotérica**")
        st.caption(f"*megasena_{numeros_selecionados}n_{estrategia_limpa.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.csv*")
    
    # ===============================================
    # MONTE CARLO
    # ===============================================
    with st.expander("🎲 **Monte Carlo - 10K simulações**", expanded=False):
        mc = monte_carlo(jogos)
        st.json(mc)
    
    st.balloons()
    
else:
    st.info("""
    🚀 **Clique "Analisar 2800 Concursos"** para gerar seus jogos!
    
    📖 **Estratégias explicadas** na lateral 👈
    📱 **Funciona no celular**
    """)

st.markdown("---")
st.caption("🎯 Mega Sena App v3.4 | 2800+ sorteios | Download sempre visível")
