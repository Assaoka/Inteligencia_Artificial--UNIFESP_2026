# 🐍 Aula 03 - Introdução ao Python 🤖

## 🏗️ O Ambiente: Google Colab
Para IA e Ciência de Dados, é muito comum utilizar o **Jupyter Notebooks** (ou similares, como o Google Colab).

Este ambiente permite que executemos pequenos blocos de código de forma interativa, mantendo o estado das variáveis na memória. Além disso, permite intercalar textos explicativos (Markdown) e blocos de código (no nosso caso, em Python).

No Colab, os códigos são executados nos servidores do Google (com acesso a GPUs gratuitas), o que facilita muito o processamento de modelos de IA.

**Dicas de Atalho no Colab:**
- `Shift + Enter`: Executa a célula atual e pula para a próxima.
- `Ctrl + M + B`: Cria uma nova célula de código abaixo.

## 🐍 Filosofia: Por que Python para IA?
Python é uma linguagem com uma sintaxe muito simplificada, que se assemelha a uma redação em inglês.

Diferente do C, não há necessidade obrigatória de uma função `main` ou do uso de ponto e vírgula `;`. O código é interpretado e executado do topo para baixo. Compare o clássico "Hello World" e uma operação matemática simples:

**Em C:**
```c
#include <stdio.h>

int main() {
    int a = 5;
    float b = 2.5;
    printf("Resultado: %f\n", a + b);
    return 0;
}
```

**Em Python:**
```python
a: int = 5
b: float = 2.5
print(f"Resultado: {a + b}")
```

Além da simplicidade, o Python possui um suporte massivo da comunidade, permitindo implementar tarefas complexas com pouquíssimas linhas de código.

```python
# Treinando uma Rede Neural MLP em 3 linhas
from sklearn.neural_network import MLPClassifier
modelo = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=1000)
modelo.fit(X_treino, y_treino)
```

## 📦 Variáveis
Embora o Python seja dinamicamente tipado e não exija a declaração explícita do tipo (como `int` ou `float`), é uma boa prática utilizar **Type Hints**. Isso auxilia o autocomplete e a captura de erros na sua IDE.

**Declaração dinâmica (estilo "clássico"):**
```python
n = 100 
```

**Declaração com Type Hint (Recomendado!):**
```python
# Estrutura -> nome: tipo = valor
termo: int = 5
nome_aluno: str = 'João'
taxa_aprendizado: float = 0.001
treinamento_ativo: bool = True
```

### ⚙️ Operadores Aritméticos
Em geral, você utilizará os mesmos operadores do C (`+`, `-`, `*`, `/`, `%`).  As principais diferenças são a inclusão de um operador nativo para **potenciação** (`**`) e a **remoção** dos operadores de incremento/decremento (`++` e `--`).

```python
n: float = 100.0
raiz: float = n ** (1/2)
print(raiz)
```

```python
contador: int = 0
contador += 1
```

## ⌨️ Entrada e Saída
### 📢 Saída de Dados: `print()`
Para exibir dados, utilizamos a função `print()`. Basta chamar a função passando o texto entre aspas (simples ou duplas) como argumento:

```python
print('Teste') 
print("Teste 2")
```

Diferente da função `printf` em C, o `print` do Python adiciona uma quebra de linha (`\n`) ao final por padrão. Caso deseje evitar esse comportamento, utilize o parâmetro `end`.

```python
print('1', end=' ')
print('2')
```

Para colocar variáveis no meio do texto, podemos usar as **f-strings**:
```python
nome: str = 'João'
print(f'Olá, {nome}!')
```

### 📥 Entrada de Dados: `input()`
A função `input()` realiza a leitura de dados do teclado **sempre** retornando uma **string** (`str`). Ela aceita um argumento opcional: uma string que será exibida no console como o *prompt* para o usuário (em C, faríamos um `printf` separado antes do `scanf`).

```python
idade = input('Qual a sua idade? ')
idade = idade + 1 # ERRO: Estamos somando String com Int
```

**⚠️ Conversão Obrigatória (Casting):** Para realizar operações aritméticas com valores lidos, é necessário converter explicitamente o tipo do dado utilizando a função do tipo desejado (ex: `int()` ou `float()`).

```python
idade: int = int(input('Qual a sua idade? '))
idade = idade + 1 # Funciona corretamente
```

## 🔀 `if`, `elif` e `else`
A maior diferença visual do C para o Python é a ausência de chaves `{ }` e a indentação (o alinhamento do texto com espaços ou tabs). O que define o bloco de código (o escopo) é a indentação. 

Para iniciar um bloco, usamos os dois pontos `:`.
```python
nota: float = 8.5

# O parêntese é opcional e geralmente omitido
if nota >= 9.0:
    print('Aprovado com Louvor!')
elif nota >= 7.0: # Substitui o "else if" do C
    print('Aprovado!')
else:
    print('Reprovado.')
```

## 🔁 Laços de Repetição
### O laço `while`
Funciona com a exata mesma lógica da linguagem C, repetindo o bloco enquanto a condição for avaliada como verdadeira (`True`).

```python
contador: int = 0
while contador < 5:
    print(f'Processando lote {contador}...')
    contador += 1
```

**Simulando o `do-while` em Python:** Como não há `do-while`, aplicamos o clássico loop infinito controlado `while True`, quebrando o ciclo internamente com a palavra reservada `break` quando a condição for atingida:
```python
while True:
    tentativa = input('Digite a senha: ')
    if tentativa == 'admin':
        print('Acesso Liberado!')
        break # Foge imediatamente do loop
```

### O laço `for`
O `for` nativo da linguagem C é um manipulador explícito de contadores (`for(int i=0; i<10; i++)`). 
No Python, o `for` itera diretamente sobre coleções. 

Quando queremos simular o comportamento de contagem do C, usamos a função `range(start, stop, step)`:
- **start:** Onde começa (Padrão: 0).
- **stop:** Onde para (Atenção: esse número nunca é incluído!).
- **step:** De quanto em quanto pula (Padrão: 1).

```python
# Contando de 0 a 4 (stop=5 é exclusivo)
for i in range(5):
    print(f'Iteração {i}')

# Incremento customizado (Start=10, Stop=0, Step=-2)
for i in range(10, 0, -2):
    print(f'Regressiva {i}')
```

## 🛠️ Funções
Em Python, a sintaxe funciona exatamente como fizemos com o `if` e com o `for`: nós abrimos o bloco com a palavra-chave `def` e indentamos as ações internamente. 

```python
def calcular_erro(previsao: float, alvo: float) -> float:
    """
    Calcula o Erro Quadrático da Predição.

    Args:
        previsao (float): O valor predito pela equação matemática.
        alvo (float): O valor real subjacente em ground truth.

    Returns:
        float: O quadrado do módulo das diferenças baseadas.
    """
    erro = (previsao - alvo) ** 2
    return erro

res = calcular_erro(10.5, 9.5)
print(f'O erro estimado foi: {res}')
```

Observe que logo abaixo da assinatura `def` nós abrimos um bloco de aspas triplas `""" ... """`. Essa é a famosa **Docstring** (no caso acima, seguimos a padronização do *Google*). Isso permite que a IDE gere a documentação automática.

## 🏗️ Estruturas de Dados:
### 🔗 Listas
Em C, os vetores (arrays) exigem tamanho imutável estipulado em compilação ou alocação dinâmica (`malloc`, `free`).

No Python, podemos usar as Listas (`list`), que são arrays dinâmicos que crescem e encolhem em tempo real, permitindo até mesmo a mistura de tipos de dados.
```python
lista = [True, 1, 2.5, 'texto']
print(lista[0]) # True
print(lista[-1]) # texto
```

Os principais métodos são:

| Comando              | O que faz?                             | Exemplo                      |
| :------------------- | :------------------------------------- | :--------------------------- |
| `.append(item)`      | Adiciona ao **final** da lista.        | `nome_lista.append("item")`  |
| `.insert(pos, item)` | Coloca em uma posição **específica**.  | `nome_lista.insert(0, "item")` |
| `.pop(pos)`          | Remove e "entrega" o item da posição.  | `item = nome_lista.pop(2)`   |
| `.remove(item)`      | Procura e remove o item pelo **nome**. | `nome_lista.remove("item")`  |
| `len(lista)`         | Conta quantos itens existem.           | `total = len(nome_lista)`    |

```python
# Declarando uma lista já com valores
pesos_da_rede: list[float] = [0.2, -0.5, 0.9]

# Adicionando um elemento dinamicamente ao *final* do vetor
pesos_da_rede.append(0.01)

# Listas aninhadas - O clássico Matriz n-dimensional
matriz_imagem: list[list[int]] = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
```

**⚠️ Atenção:** Em Python, estruturas de dados mutáveis (como Listas e Dicionários) não são copiadas ao usar o sinal de atribuição `=`. A variável final apenas guardará a **referência** para a estrutura original (como se fosse um ponteiro `*` natural do C).

```python
lista_a = [1, 2, 3]
lista_b = lista_a  # CUIDADO: lista_b aponta pro endereço de lista_a!

lista_b[0] = 99
print(lista_a[0])  # Saída: 99 (Alteração foi feita na mesma matriz subjacente!)

# Para forçar a cópia dos dados em outra região da memória (análogo ao memcpy):
lista_c = lista_a.copy()
```

Como as Listas são iteráveis pelo loop `for`, não é necessário usar contadores manuais para acessar os elementos.

**Técnica 1: O "For Each" embutido**
O Python lhe entrega o próprio valor guardado na posição a cada ciclo.
```python
for peso in pesos_da_rede:
    print(peso)
```

**Técnica 2: Enumeração Automática**
Precisa do índice atual da repetição para algum cálculo matricial? A função construtora `enumerate` devolve uma variável `indice` e uma variável `valor` pareadas em cada passo:
```python
for indice, valor in enumerate(pesos_da_rede):
    print(f'Na posição {indice} temos o peso: {valor}')
```

**Técnica 3: Combinando Listas com `zip`**
O `zip` "costura" e emparelha suas Listas lado a lado de uma só vez:
```python
y_reais: list[float] = [10.5, 20.0, 30.5]
y_previstos: list[float] = [10.0, 20.0, 30.0]

erro_total: float = 0
for real, previsto in zip(y_reais, y_previstos):
    erro_total += calcular_erro(previsto, real)
print(f'Erro médio: {erro_total / len(y_reais):.2f}')
```

### 📖 Dicionários
Em Python, temos uma estrutura chamada `dict` que é uma tabela hash que mapeia chaves para valores. Podemos construir um dicionário usando a sintaxe de chaves `{ }`.

Os principais métodos são:

| Comando | O que faz? | Exemplo Mínimo |
| :--- | :--- | :--- |
| `.keys()` | Retorna uma exibição com as chaves inseridas. | `dic.keys()` |
| `.values()` | Retorna uma exibição com os valores armazenados. | `dic.values()` |
| `.get(chave, padrao)` | Busca segura: tenta acessar a variável pela chave, e caso ela nunca tenha sido declarada, ele devolve o `padrao`! Resolve o seu *Segmentation Fault* lógico de forma espetacular. | `dic.get('idade', 18)` |
| `in` | Retorna um verificador muito rápido (`True` ou `False`) se a chave procurada já está registrada na HashTable. | `if 'email' in dic:` |

```python
config_modelo: dict = {
    'camadas_ocultas': 3,
    'funcao_ativacao': 'sigmoide',
    'learning_rate': 0.001
}
```

Podemos acessar os valores do dicionário usando a sintaxe de chaves `[chave]`.

```python
print(config_modelo['learning_rate'])
config_modelo['epocas'] = 1500
```

Além disso, o dicionário também pode ser iterado usando o método `items()`, que retorna uma lista de tuplas (chave, valor).

```python
# Retornando chaves e correspondências simultaneamente
for chave, valor in config_modelo.items():
    print(f'{chave}: {valor}')
```

### 🏨 Classes ("structs")
Em C, podemos criar um novo tipo de dados que agrupa múltiplas informações. Nós não temos `struct` no Python, mas podemos fazer isso com classes.

Classes não contém apenas variáveis (atributos), mas também funções (métodos). Podemos criar uma lista encadeada (parcialmente implementada) assim:

```python
class No:
    # Método Construtor: Inicializa o contexto da nossa struct e exige o argumento
    def __init__(self, valor: int, proximo: 'No' | None = None):
        self.valor = valor
        self.proximo = proximo
    
    def append(self, valor: int):
        if self.proximo is None:
            self.proximo = No(valor)
        else:
            self.proximo.append(valor)

    def __str__(self):
        return f'{self.valor} -> {self.proximo}'

lista = No(10, No(20))
lista.append(30)
print(lista) # Saída: 10 -> 20 -> 30 -> None
```

## 🗃️ Módulos Externos
Quando utilizamos o Colab, boa parte das dependências para IA já vem instaladas. O mesmo acontece caso baixe o Python através do Anaconda. Caso precise instalar módulos externos, use o comando `!pip install nome_do_modulo>=versão` no Colab.

```python
!pip install numpy>=2.0.0
```

Para importar módulos, usamos o comando `import`.

```python
import numpy
print(numpy.array([1, 2, 3]))
```

Para acessar qualquer função, você utiliza o nome do módulo seguido de um ponto e o nome da função. É comum atribuir um apelido ao módulo para facilitar a escrita:

```python
import numpy as np
print(np.array([1, 2, 3]))
```

Você pode importar apenas uma função específica do módulo, nesse caso, não é necessário o nome do módulo:

```python
from numpy import array
print(array([1, 2, 3]))
```

Você também pode importar todas as funções de um módulo para não precisar do nome do módulo:

```python
from numpy import * # Não recomendado
print(array([1, 2, 3]))
```

## 1. Normalização Min-Max 📊
Na preparação de dados para Redes Neurais, é muito comum precisarmos colocar todas as variáveis numéricas na mesma escala (geralmente entre 0 e 1). A fórmula da Normalização Min-Max é:
$$X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}}$$

**Tarefa:** Crie um programa que faça a leitura (via teclado) de cinco valores. Calcule e exiba o valor normalizado de cada um deles.

```python

```

## 2. A Matriz de Confusão 🎲
Vamos avaliar um classificador binário gerado aleatoriamente!
1. Importe o módulo `random`.
2. Construa duas listas de 20 posições cada: `y_real` e `y_predito`. Preencha-as com números binários aleatórios (0 ou 1) usando `random.randint(0, 1)`.

**Tarefa:** Crie um dicionário para rastrear a matriz de confusão desse classificador.

**Matriz de Confusão:**
| | Real 0 | Real 1 |
| :--- | :--- | :--- |
| **Predito 0** | VN | FP |
| **Predito 1** | FN | VP |

```python

```

## 3. Métricas Customizadas e Docstrings 📏
Usando o dicionário da Matriz de Confusão gerado no exercício anterior, vamos calcular o **F1-Score**.

O F1-Score é a média harmônica entre a *Precisão* e o *Recall*:
- **Precisão:** $\frac{VP}{VP + FP}$ (Dos que o modelo disse ser 1, quantos eram 1 de verdade?)
- **Recall:** $\frac{VP}{VP + FN}$ (Dos que eram realmente 1, quantos o modelo identificou?)
- **F1-Score:** $2 \times \frac{Precisão \times Recall}{Precisão + Recall}$

**Tarefa:**
1. Crie uma função chamada `calcular_f1_score(matriz_confusao: dict) -> float`.
2. Escreva uma **Docstring** completa para a função, descrevendo seu argumento e retorno.
3. Dentro da função, extraia os valores (VP, FP e FN) do dicionário recebido. Calcule a Precisão, o Recall e finalmente o F1-Score, retornando o valor final. *(Dica: Trate o caso de divisão por zero retornando 0.0 caso ocorra)*.
4. Ao final, chame a sua função passando o dicionário do Exercício 2 e exiba o resultado no console com 4 casas decimais.

```python

```

## 4. Árvore Binária de Busca 🌳
**Tarefa:** Crie uma classe `NoArvore`. Ela deve receber no método construtor `__init__` um valor inteiro e inicializar as referências `esquerda` e `direita`. Crie dois métodos para essa classe:
- `inserir(self, valor: int)`: Se o valor for menor que o do nó atual, desce para a esquerda (se estiver livre, aloca um nó novo, se não, chama a inserção recursiva à esquerda). Faz o espelho para a direita.
- `buscar(self, valor: int) -> bool`: Retorna `True` se o valor existir na árvore sob esse nó, e `False` caso contrário, usando a lógica clássica da BST.

```python

```