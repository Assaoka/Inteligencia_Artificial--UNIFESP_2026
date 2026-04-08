import streamlit as st
import json
import time
from langchain_groq import ChatGroq
from . import regras

SYSTEM_PROMPT = f"""Você é um agente inteligente explorando o Mundo de Wumpus.

REGRAS DO MUNDO DE WUMPUS:
1. Você começa na posição {st.session_state.atual} em um tabuleiro de tamanho {st.session_state.num_quadrantes}x{st.session_state.num_quadrantes}.
2. Seu objetivo é concluir uma missão que será passada para você.
3. Você só pode se mover para casas adjacentes (cima, baixo, esquerda ou direita).
4. Se você sentir 'brisa', há um buraco em uma das casas adjacentes. Existem {st.session_state.num_buracos} buracos no total. Se você pisar em uma casa com um buraco, você morre.
5. Se você sentir 'fedor', o Wumpus está em uma das casas adjacentes. Se você pisar na mesma casa que o Wumpus vivo, você morre. O 'fedor' permanece na casa mesmo após o Wumpus morrer.
6. Você tem {st.session_state.flechas} flechas no total. Se você atirar uma flecha e acertar o Wumpus, ele morre. Se você atirar uma flecha e errar o Wumpus, a flecha é perdida.
7. Existem {st.session_state.num_ouro} ouros no total. Você só descobre que tem ouro quando entra em uma casa que tem ouro.""" + """

Você tem acesso às seguintes ferramentas:
- mover: Move o agente para uma casa adjacente.
  Args:
   - direcao (string): 'cima', 'baixo', 'esquerda' ou 'direita'.
  Exemplo: {"action": "mover", "action_input": {"direcao": "cima"}}

- carregar_flecha: Carrega uma flecha para ser disparada. Ela será disparada na direção que você andar após carregar.
  Args: (nenhum)
  Exemplo: {"action": "carregar_flecha", "action_input": {}}

- coletar_ouro: Pega o ouro se ele estiver na casa atual.
  Args: (nenhum)
  Exemplo: {"action": "coletar_ouro", "action_input": {}}

- sair: Sai da caverna se você estiver na posição inicial (0,0) e com o ouro.
  Args: (nenhum)
  Exemplo: {"action": "sair", "action_input": {}}

Para usar uma ferramenta, você deve responder com um JSON no seguinte formato:
Action:
{
  "action": "NOME_DA_FERRAMENTA",
  "action_input": {"PARAMETRO": "VALOR"}
}

Utilize seus sentidos para deduzir a localização do Wumpus e dos buracos. Pense logicamente, planeje seus movimentos e utilize suas ferramentas para concluir sua missão.

O ciclo de interação deve ser SEMPRE:
Thought: Com base nas informações disponíveis, o que você acha que deveria fazer?
Action: (o bloco JSON acima)
Observation: (o resultado da ferramenta que eu te passarei)
... (repetir se necessário)

Final Answer: Quando você concluir sua missão (ou se for impossível vencer), crie uma resposta final em linguagem natural. Apenas escreva Final Answer quando tiver terminado tudo.
"""

def call_tool(action_name, action_input):
    if action_name == "mover":
        return regras.mover(**action_input)
    elif action_name == "carregar_flecha":
        return regras.carregar_flecha()
    elif action_name == "coletar_ouro":
        return regras.coletar_ouro()
    elif action_name == "sair":
        return regras.sair()
    else:
        return f"Erro: Ferramenta {action_name} não existe."

def executar_agente_llm(
    prompt_usuario: str, 
    api_key: str, 
    model_name: str,
    renderizar_jogo: callable
) -> None:
    if not api_key:
        st.error("Por favor, insira a GROQ API KEY na barra lateral.")
        return

    llm = ChatGroq(
        model=model_name,
        api_key=api_key,
        temperature=0.1,
        reasoning_format="parsed" if "qwen" in model_name else None
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Sua missão: {prompt_usuario}\nEstado inicial:\n{regras.get_estado_atual()}"},
    ]

    MAX_ITERACOES = 2 * (st.session_state.num_quadrantes ** 2)
    
    container = st.expander("🤖 Log do Agente LLM", expanded=True)

    for i in range(MAX_ITERACOES):
        # Chama a LLM parando antes da observação para não alucinar
        response = llm.invoke(messages, stop=["Observation:"])
        texto_gerado = response.content
        
        container.info(f"**Iteração {i+1}**")
        container.write(texto_gerado)
        
        if "Final Answer:" in texto_gerado:
            break

        if "Action:" in texto_gerado:
            try:
                # Extrai o JSON da resposta
                json_str = texto_gerado.split("Action:")[1].strip()
                tool_call = json.loads(json_str)
                
                # Executa a ferramenta real
                resultado = call_tool(tool_call["action"], tool_call["action_input"])
                
                observation_text = f"Observation:\n{resultado}\n"
                container.success(observation_text)
                
                # Atualiza o histórico
                messages.append({"role": "assistant", "content": texto_gerado + "\n" + observation_text})
                
                # --- ATUALIZAÇÃO VISUAL ---
                renderizar_jogo()
                
                # Se o estado indicar morte ou fim de jogo, para
                if "MORREU" in resultado or "Parabéns" in resultado:
                    # Envia uma última mensagem para a LLM saber que acabou e dar o Final Answer
                    messages.append({"role": "user", "content": "O jogo terminou baseado na sua última ação. Logo, você não pode realizar mais nenhuma ação. Dê sua resposta final ao usuário."})
                    
            except Exception as e:
                error_msg = f"Erro ao processar ação: {str(e)}"
                if not "There are multiple elements with" in error_msg:
                    container.error(error_msg)
                messages.append({"role": "assistant", "content": f"Observation:\n{error_msg}"})
        else:
            container.warning("O modelo não seguiu o formato Action. Encerrando.")
            break
    else:
        container.error("Limite de iterações atingido.")
