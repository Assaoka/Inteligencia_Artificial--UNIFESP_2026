# regras.py
import random
import streamlit as st

# Índices da tupla‑estado de cada quadrante
VISITADO, BURACO, VENTO, OURO, WUMPUS_VIVO, FEDOR, WUMPUS_MORTO = range(7)

# -------------- Geração do tabuleiro --------------
def _sorteio_quadrante(n):
    x, y =  random.randint(0, n - 1), random.randint(0, n - 1)
    if (x, y) == (0, 0):
        x, y = _sorteio_quadrante(n)  # não pode ser a casa inicial
    return x, y

def _marcar_adjacentes(x, y, n, elemento):
    if x > 0:
        st.session_state.tabuleiro[x - 1][y][elemento] = True
    if x < n - 1:
        st.session_state.tabuleiro[x + 1][y][elemento] = True
    if y > 0:
        st.session_state.tabuleiro[x][y - 1][elemento] = True
    if y < n - 1:
        st.session_state.tabuleiro[x][y + 1][elemento] = True

def alocar_quadrantes(n, flag, quantidade, marcar_clue=True):
    """Coloca 'quantidade' de elementos do tipo 'flag' em posições aleatórias."""
    for _ in range(quantidade):
        while True:
            x, y = _sorteio_quadrante(n)
            if not any(st.session_state.tabuleiro[x][y][k] for k in (BURACO, OURO, WUMPUS_VIVO)):
                st.session_state.tabuleiro[x][y][flag] = True
                if marcar_clue:
                    # vento ou fedor são sempre flag+1
                    _marcar_adjacentes(x, y, n, flag + 1)
                break

def criar_tabuleiro():
    n = st.session_state.num_quadrantes
    # matriz NxN com 7 flags cada
    st.session_state.tabuleiro = [
        [[False] * 7 for _ in range(n)] for _ in range(n)
    ]
    # ordem importa: primeiro buracos (com vento), depois ouro, depois Wumpus (com fedor)
    alocar_quadrantes(n, BURACO, st.session_state.num_buracos, marcar_clue=True)
    alocar_quadrantes(n, OURO,   st.session_state.num_ouro,   marcar_clue=False)
    alocar_quadrantes(n, WUMPUS_VIVO, 1, marcar_clue=True)

# -------------- Percepções --------------
def sentidos(x: int, y: int):
    cell = st.session_state.tabuleiro[x][y]
    cell[VISITADO] = True

    msg = ""
    vivo = True

    if cell[BURACO]:
        msg += "\n💀 Você caiu em um **buraco**!"
        vivo = False

    if cell[VENTO]:
        msg += "\n💨 Você sente um **vento**."

    if cell[OURO]:
        msg += "\n✨ Há **ouro** aqui!"

    if cell[WUMPUS_VIVO]:
        msg += "\n👹 O **Wumpus** está aqui… e te devorou!"
        vivo = False

    if cell[FEDOR] and not cell[WUMPUS_VIVO]:
        msg += "\n🤢 Você sente o **fedor** do Wumpus."

    if cell[WUMPUS_MORTO]:
        msg += "\n📣 Você vê o corpo do **Wumpus** abatido."

    st.session_state.sentidos += msg + "\n\n"
    return vivo

# -------------- Movimentação & ações --------------
def _respeita_limites(x, y):
    n = st.session_state.num_quadrantes
    return 0 <= x < n and 0 <= y < n

def _disparar_flecha(x, y):
    if st.session_state.flechas == 0:
        st.session_state.sentidos += "🚫 Você não tem flechas!\n\n"
        return

    st.session_state.flechas -= 1
    alvo = st.session_state.tabuleiro[x][y]
    if alvo[WUMPUS_VIVO]:
        alvo[WUMPUS_VIVO] = False
        alvo[WUMPUS_MORTO] = True
        st.session_state.wumpus_vivo = False
        st.session_state.pontuacao += 50
        st.session_state.sentidos += "🗡️ **ACERTO CRÍTICO!** Você matou o Wumpus. Ele deu um grito ensurdecedor!\n\n"
    else:
        st.session_state.sentidos += "↘️ Você disparou a flecha… mas nada aconteceu.\n\n"

def _pos_mover(x, y, dir_txt):
    st.session_state.sentidos += f"➡️ Você tentou mover para **{dir_txt}**.\n"

    if not _respeita_limites(x, y):
        st.session_state.sentidos += "🧱 Você bateu na **parede**!\n\n"
        st.session_state.pontuacao -= 10
        return

    # se checkbox 'atirar' estava marcada, primeiro dispara no alvo
    if st.session_state.atirar:
        _disparar_flecha(x, y)
        st.session_state.atirar = False  # desmarca a checkbox

    # move efetivamente
    st.session_state.atual = (x, y)
    vivo = sentidos(x, y)
    st.session_state.pontuacao -= 1  # cada ação custa 1 ponto

    if not vivo:
        st.session_state.pontuacao -= 100
        st.session_state.sentidos += "💀 **Você morreu!**\n\n"

def mover_cima():
    x, y = st.session_state.atual
    _pos_mover(x - 1, y, "cima")

def mover_baixo():
    x, y = st.session_state.atual
    _pos_mover(x + 1, y, "baixo")

def mover_esquerda():
    x, y = st.session_state.atual
    _pos_mover(x, y - 1, "esquerda")

def mover_direita():
    x, y = st.session_state.atual
    _pos_mover(x, y + 1, "direita")

# -------------- Outras ações --------------
def pegar_ouro():
    x, y = st.session_state.atual
    cell = st.session_state.tabuleiro[x][y]
    if cell[OURO]:
        cell[OURO] = False
        st.session_state.ouro_coletado = True
        st.session_state.pontuacao += 50
        st.session_state.sentidos += "💰 Você **pegou o ouro**!\n\n"
    else:
        st.session_state.sentidos += "🤔 Não há ouro aqui.\n\n"
    st.session_state.pontuacao -= 1

def escalar_caverna():
    if st.session_state.atual != (0, 0):
        st.session_state.sentidos += "📍 Você precisa estar na posição inicial (0,0) para escalar.\n\n"
        return
    if not st.session_state.ouro_coletado:
        st.session_state.sentidos += "💎 Você ainda não está carregando o ouro!\n\n"
        return

    st.session_state.pontuacao += 50
    st.session_state.sentidos += f"🎉 **Parabéns!** Você escapou com o ouro. Pontuação final: {st.session_state.pontuacao}\n\n"

# -------------- Funções Auxiliares para Agentes --------------

def get_estado_atual():
    """Retorna uma descrição em texto das percepções atuais e status do jogo."""
    x, y = st.session_state.atual
    cell = st.session_state.tabuleiro[x][y]
    
    percepcoes = []
    if cell[VENTO]: percepcoes.append("Sinto uma brisa (buraco próximo).")
    if cell[FEDOR]: percepcoes.append("Sinto um fedor (Wumpus próximo).")
    if cell[OURO]: percepcoes.append("Vejo um brilho (ouro aqui!).")
    if cell[WUMPUS_MORTO]: percepcoes.append("Ouço o silêncio de um Wumpus morto.")
    
    estado = f"Posição Atual: ({x}, {y})\n"
    estado += f"Percepções: {', '.join(percepcoes) if percepcoes else 'Nenhuma'}\n"
    estado += f"Flechas: {st.session_state.flechas}\n"
    estado += f"Ouro coletado: {'Sim' if st.session_state.ouro_coletado else 'Não'}\n"
    estado += f"Pontuação: {st.session_state.pontuacao}\n"
    
    if cell[BURACO]:
        estado += "STATUS: VOCÊ CAIU EM UM BURACO E MORREU.\n"
    elif cell[WUMPUS_VIVO]:
        estado += "STATUS: O WUMPUS TE DEVOROU.\n"
    
    return estado

def mover(direcao):
    """
    Move o agente. 
    Direções: 'cima', 'baixo', 'esquerda', 'direita'.
    Retorna o novo estado ou mensagem de erro.
    """
    if direcao == "cima": mover_cima()
    elif direcao == "baixo": mover_baixo()
    elif direcao == "esquerda": mover_esquerda()
    elif direcao == "direita": mover_direita()
    else: return "Direção inválida."
    return get_estado_atual()

def carregar_flecha():
    st.session_state.atirar = True
    return "Flecha carregada! Agora mova-se para uma direção para atirar."

def coletar_ouro():
    pegar_ouro()
    return get_estado_atual()

def sair():
    escalar_caverna()
    return get_estado_atual()
