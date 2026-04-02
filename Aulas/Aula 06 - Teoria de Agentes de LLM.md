# Slide 1: Capa
Bom dia! Meu nome é João Assaoka, e eu estou aqui de novo pra dar outra aula pra voces. Dessa vez, de um tema que eu acredito que voces vão achar mais interessante, agentes de LLM.

# Slide 2: Perguntas de Engajamento
1. Quem aqui já estudou o funcionamento das LLMs mais a fundo?
2. Quem já estudou agentes de LLM?
3. Alguém fez o curso de LLMs do Hugging Face?

# Slide 3: Recomendação
Essa aula é fortemente baseada na unidade 1 do curso de agentes do Hugging Face. É um curso com 4 módulos completos + 3 bônus, e o conteudo é muito bom. Se alguém tiver interesse nessa área, eu recomendo fortemente fazer esse curso. (QR Code)

---

# O que é um Agente de LLM?
## Slide 4:
Conheçam Alfred. 
<!-- Alfred é um **Agente**. -->

<img src="https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/unit1/this-is-alfred.jpg" alt="Este é Alfred"/>

## Slide 5:
Imagine que Alfred **receba um comando**, como: "Alfred, eu gostaria de um café, por favor."

<img src="https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/unit1/coffee-please.jpg" alt="Eu gostaria de um café"/>

Como Alfred **entende linguagem natural**, ele compreende rapidamente o nosso pedido.

## Slide 6:
Antes de atender ao pedido, Alfred se engaja em **raciocínio e planejamento**, descobrindo os passos e ferramentas que ele precisa para:

1. Ir para a cozinha  
2. Usar a máquina de café  
3. Fazer o café  
4. Trazer o café de volta

<img src="https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/unit1/reason-and-plan.jpg" alt="Raciocinar e planejar"/>

## Slide 7:
Uma vez que ele tem um plano, ele **deve agir** (*act*). Para executar seu plano, **ele pode usar ferramentas (Tools) da lista de ferramentas que ele conhece**. 

Neste caso, para fazer um café, ele usa uma máquina de café. Ele ativa a máquina de café para passar o café.

<img src="https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/unit1/make-coffee.jpg" alt="Fazer café"/>

## Slide 8:
Finalmente, Alfred nos traz o café recém-passado.

<img src="https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/unit1/bring-coffee.jpg" alt="Trazer o café"/>

## Slide 9: Revisão da Aula 4
Na Aula 4 vocês estudaram a definição formal de Agentes.

> [!note] Definição Formal
> "Um **Agente** é tudo que pode **Perceber** seu ambiente por meio de **Sensores** e de Agir sobre esse ambiente por intermédio de **Atuadores**.

## Slide 10: Alfred é um Agente
Alfred é um Agente. Ele é capaz de ver o ambiente (usuário, ferramentas) e agir sobre ele (fazer café). 

Na programação que voces viram até agora, nós definimos um algoritmo para resolver um problema específico.

O que diferencia ele é capaz de interagir com o ambiente através de linguagem natural. Nós aproveitamos a capacidade das LLMs de entender e gerar linguagem natural para criar agentes que podem interagir com o ambiente de forma flexível.

<img src="https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/unit1/process.jpg" alt="Processo do Agente"/>

---

# Como Agentes de LLM funcionam?
## Slide 11: O que é uma LLM
Um LLM é um tipo de modelo de IA que se destaca por **entender e gerar linguagem humana**. Eles são treinados em vastas quantidades de dados de texto, o que lhes permite aprender padrões, estruturas e até nuances da linguagem. Esses modelos normalmente consistem em muitos bilhões de parâmetros.

![alt text](image.png)

## Slide 11.2: Tabela Atual:
Atualmente, a escala é ainda maior. O GPT-4 tem mais de 1.76 trilhões de parâmetros, o que é 100x maior que o Turing-NLG, um dos maiores modelos de 2020.

| Modelo | Parâmetros |
| --- | --- |
| GPT-3 | 175 Bilhões |
| GPT-4 | 1.76 Trilhão |
| DeepSeek V3 | 671 Bilhões |
| PaLM 2 | 340 Bilhões |

## Slide 12: Arquitetura das LLMs
A maioria dos LLMs hoje em dia é **construída na arquitetura Transformer** — uma arquitetura de aprendizado profundo baseada no algoritmo de "Atenção" (*Attention*), que ganhou grande interesse desde o lançamento do BERT pelo Google em 2018.

![alt text](image-2.png)

## Slide 12.1: Autoregessivo
Mais especificamente, a maioria deles utiliza uma arquitetura **Decoder-Only**, um **gerando novos tokens para completar uma sequência, um token por vez** com base no que já foi "Lido".

Diz-se que os LLMs são **autorregressivos**, o que significa que **a saída de uma etapa se torna a entrada para a próxima**. Esse ciclo contínuo segue até que o modelo preveja que o próximo token será o token EOS (End of Sequence), momento em que o modelo pode parar.

![alt text](image-1.png)

## Slide 13: O Problema
Isso até foi mencionado algumas aulas atrás. Que a LLM não sabe o que está fazendo, ela está apenas prevendo o próximo token mais provável.

Isso é verdade de certa forma. Esses modelos foram treinados para isso, e além disso os modelos de chat são treinados para ser "úteis", ao usuário.

Isso causa um problema bem comum, as alucinações. Se nós perguntarmos para um modelo de linguagem algo que ele não sabe, ele vai continuar gerando uma resposta.

## Slide 14: Geração Aumentada por Recuperação (RAG)
O lado bom, é que o problema das alucinações estão na própria definição. Se nós conseguirmos fornecer o contexto necessário para o modelo, a chance dele alucinar diminui drasticamente.

Nós aproveitamos o fato de que a LLM é boa em interpretar e gerar texto para receber esses dados e dar uma resposta baseada neles. Isso é o que chamamos de RAG (Retrieval-Augmented Generation).

Ao invés de fazermos a LLM "adivinhar" a resposta, nós fornecemos dados como o FAQ do produto, planilhas, sites da internet ou documentos.

## Slide 15: Como recuperar informações?
Existem diversas formas de recuperar informações, mas a mais comum é o uso de embeddings, que são representações vetoriais de um conteúdo. Podemos fazer uma busca por similaridade para encontrar os documentos mais relevantes para a pergunta do usuário.

## Slide 16: Ferramentas
Pela nossa definição de agentes, eles precisam de conseguir ver o ambiente por meio de **Sensores** e agir sobre ele por meio de **Atuadores**.

Aqui nos agentes de LLM, ambos os conceitos estão representados sobre o conceito de **Ferramentas**. Se o Cérebro do Agente é a LLM, as ferramentas são o corpo. Elas definem tudo que o agente pode fazer.

## Slide 16.1: O que pode ser uma ferramenta?
Geração de Imagens
![alt text](image-3.png)

## Slide 16.2: Continuação
Acesso a uma API

## Slide 16.3: Continuação
Execução de Código
... Basicamente qualquer função que você consiga implementar.

## Slide 17:Alfred, o Agente do Clima
Para vocês entenderem melhor como funciona, vamos ver um exemplo prático.

Alfred é um cara muito trabalhador, ele tem 2 empregos. Eu apresento para vocês o Alfred, o Agente do Clima.

Um usuário pergunta ao Alfred: “Qual é o clima atual em Nova York?”

<img src="https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/unit1/alfred-agent.jpg" alt="Agente Alfred"/>

## Slide 18: 
O trabalho de Alfred é responder a esta solicitação usando uma ferramenta de API de clima.

Veja como o ciclo se desenrola:

**Raciocínio Interno:** Ao receber a consulta, o diálogo interno de Alfred pode ser:

*"O usuário precisa de informações climáticas atuais de Nova York. Eu tenho acesso a uma ferramenta que busca dados sobre o clima. Primeiro, preciso chamar a API de clima para obter os detalhes atualizados."*

Este passo mostra o agente dividindo o problema em etapas: primeiro, coletando os dados necessários.

<img src="https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/unit1/alfred-agent-1.jpg" alt="Agente Alfred"/>

## Slide 19: 
**Uso de Ferramenta:** Com base em seu raciocínio e no fato de que Alfred conhece uma ferramenta `get_weather`, Alfred prepara um comando formatado em JSON que chama a ferramenta da API de clima. Por exemplo, sua primeira ação poderia ser:

Thought: Eu preciso verificar o clima atual em Nova York.
```json
    {
      "action": "get_weather",
      "action_input": {
        "location": "New York"
      }
    }
```

## Slide 20: 
<img src="https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/unit1/alfred-agent-2.jpg" alt="Agente Alfred"/>

**Retorno do Ambiente:** Após chamar a ferramenta, Alfred recebe uma observação. Podem ser os dados brutos de clima diretamente da API, como:

*"Clima atual em Nova York: parcialmente nublado, 15°C, 60% de umidade."*

<img src="https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/unit1/alfred-agent-3.jpg" alt="Agente Alfred"/>

Esta observação é então adicionada ao prompt como contexto adicional. Funciona como um feedback do mundo real, confirmando se a ação foi bem-sucedida e fornecendo os detalhes necessários.


## Slide 21:
**Refletindo:** Com a observação em mãos, Alfred atualiza seu raciocínio interno:

*"Agora que tenho os dados do clima de Nova York, posso compilar uma resposta para o usuário."*

<img src="https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/unit1/alfred-agent-4.jpg" alt="Agente Alfred"/>

## Slide 22:
Alfred então gera uma resposta final formatada da maneira que instruímos:

**Thought:** Eu tenho os dados do clima agora. O clima atual em Nova York é parcialmente nublado com uma temperatura de 15°C e 60% de umidade.

**Final answer:** O clima atual em Nova York é parcialmente nublado com uma temperatura de 15°C e 60% de umidade.

Esta ação final envia a resposta de volta ao usuário, fechando o ciclo.


<img src="https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/unit1/alfred-agent-5.jpg" alt="Agente Alfred"/>

## Slide 23: ReAct
<img src="https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/unit1/AgentCycle.gif" alt="Ciclo Pensar, Agir, Observar"/>

O que observamos neste exemplo:

**Agentes iteram através de um loop até o objetivo ser cumprido:**
    
**O processo de Alfred é cíclico**. Começa com um pensamento, depois age chamando uma ferramenta e, por fim, observa o resultado. Se a observação indicasse um erro ou dados incompletos, Alfred poderia ter reentrado no ciclo para corrigir sua abordagem.
    
**Integração de Ferramentas:**
A habilidade de chamar uma ferramenta (como uma API de clima) permite que Alfred vá **além do conhecimento estático e recupere dados em tempo real**, um aspecto essencial para muitos Agentes de IA.

**Adaptação Dinâmica:**
Cada ciclo permite que o agente incorpore novas informações (observações) no seu raciocínio (pensamento), garantindo que a resposta final seja bem informada e precisa.
    
Este exemplo demonstra o conceito central por trás do *ciclo ReAct* (**R**easoning + **Act**ion): **a interação entre Pensamento, Ação e Observação capacita agentes de IA a resolverem tarefas complexas de forma interativa**. 

## Os Componentes Principais
O trabalho dos agentes é um ciclo contínuo de: **pensar (*Thought*) → agir (*Act*) e observar (*Observe*)**.

Os três componentes trabalham juntos em um loop contínuo. Para usar uma analogia de programação, o agente usa um **loop while**: o loop continua até que o objetivo do agente tenha sido cumprido.

## Slide 24: Prática
Bom, era isso da parte teórica. Vocês tem alguma pergunta?
