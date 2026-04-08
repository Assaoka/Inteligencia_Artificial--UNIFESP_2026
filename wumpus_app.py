import streamlit as st
import os
from Wumpus import regras
from Wumpus import agente_llm

st.set_page_config(page_title="Mundo de Wumpus", layout="wide", page_icon="👹")

# Variáveis globais de caminhos de imagens
IMG_DIR = "Wumpus"
IMG_ATUAL = os.path.join(IMG_DIR, "atual.png")
IMG_VISITADO = os.path.join(IMG_DIR, "visitado.png")
IMG_SEGREDO = os.path.join(IMG_DIR, "segredo.png")

# ---------- Sidebar – parâmetros de jogo ----------
with st.sidebar.expander("⚙️ Configuração do Jogo", expanded=True):
    st.number_input("Número de Quadrantes (N x N)",
                    min_value=3, max_value=10, value=3, step=1,
                    key="num_quadrantes")
    st.number_input("Número de Flechas",
                    min_value=1, max_value=10, value=1, step=1,
                    key="num_flechas")
    st.number_input("Quantidade de Ouro",
                    min_value=1, max_value=10, value=1, step=1,
                    key="num_ouro")
    st.number_input("Quantidade de Buracos",
                    min_value=1, max_value=10, value=1, step=1,
                    key="num_buracos")

    # validação básica
    total_itens = st.session_state.num_ouro + st.session_state.num_buracos + 1
    max_casas = st.session_state.num_quadrantes ** 2
    if total_itens > max_casas:
        st.error("A soma de Ouro, Buracos e o Wumpus não pode exceder o número de quadrantes.")
        st.stop()

# ---------- Sidebar – Agente LLM ----------
with st.sidebar.expander("🤖 Agente de IA (LLM)", expanded=True):
    api_key = st.text_input("Groq API Key", type="password")
    modelo = st.selectbox("Modelo", [
        "qwen/qwen3-32b", "llama-3.1-8b-instant"
        #, "llama-3.3-70b-versatile", "openai/gpt-oss-120b", "openai/gpt-oss-20b"
    ], accept_new_options=True)
    comando = st.text_area("Missão para o Agente", value="Encontre o ouro e saia da caverna em segurança.", key="missao_llm")
    
    if st.button("🚀 Iniciar Agente LLM", use_container_width=True):
        agente_llm.executar_agente_llm(comando, api_key, modelo)

# ---------- Reinício ou primeira execução ----------
if (
    "tabuleiro" not in st.session_state or
    st.session_state.num_quadrantes != len(st.session_state.tabuleiro) or
    st.sidebar.button("🔄 Reiniciar Jogo", use_container_width=True)    
):
    regras.criar_tabuleiro()
    st.session_state.atual = (0, 0)
    st.session_state.sentidos = ""
    st.session_state.flechas = st.session_state.num_flechas
    st.session_state.ouro_coletado = False
    st.session_state.wumpus_vivo = True
    st.session_state.pontuacao = 0
    # revela casa inicial
    regras.sentidos(0, 0)

# ---------- Renderização do tabuleiro ----------
st.title("🏹 Mundo de Wumpus")

N = st.session_state.num_quadrantes
cols = st.columns(N + 1)  # última coluna = painel de ações

for i in range(N):
    for j in range(N):
        cell = st.session_state.tabuleiro[i][j]
        # imagem
        if (i, j) == st.session_state.atual:
            cols[j].image(IMG_ATUAL, use_container_width=True)
        elif cell[regras.VISITADO]:
            cols[j].image(IMG_VISITADO, use_container_width=True)
        else:
            cols[j].image(IMG_SEGREDO, use_container_width=True)

# ---------- Painel de ações (última coluna) ----------
with cols[-1]:
    st.subheader("Controles")
    st.checkbox("Atirar", value=False, key="atirar")

    st.button("Mover ↑", on_click=regras.mover_cima, use_container_width=True)
    st.button("Mover ↓", on_click=regras.mover_baixo, use_container_width=True)
    st.button("Mover ←", on_click=regras.mover_esquerda, use_container_width=True)
    st.button("Mover →", on_click=regras.mover_direita, use_container_width=True)

    st.divider()
    st.button("🏆 Pegar Ouro", on_click=regras.pegar_ouro, use_container_width=True)
    st.button("🧗 Escalar (sair)", on_click=regras.escalar_caverna, use_container_width=True)

    st.divider()
    st.markdown(f"**Flechas restantes:** {st.session_state.flechas}")
    st.markdown(f"**Pontuação:** {st.session_state.pontuacao}")

# ---------- Painel de feedback / sentidos ----------
with st.sidebar.expander("🗣️ Sentidos do Agente", expanded=True):
    st.markdown(st.session_state.sentidos) 
