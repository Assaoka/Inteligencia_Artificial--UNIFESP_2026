import json
import re
import os
import glob

def converter_md_para_ipynb(conteudo_md):
    cells = []
    current_md = []
    current_code = []
    in_code_block = False
    in_yaml = False
    
    # Processa o arquivo linha por linha
    for i, line in enumerate(conteudo_md.split('\n')):
        # 1. Ignorar o cabeçalho YAML (tags e metadados iniciais)
        if i == 0 and line.strip() == '---':
            in_yaml = True
            continue
        if in_yaml:
            if line.strip() == '---':
                in_yaml = False
            continue
            
        # 2. Detectar início de blocos de código Python
        if line.strip().startswith('```python'):
            # Salva o markdown acumulado até aqui como uma célula
            if current_md and any(l.strip() for l in current_md):
                cells.append({
                    "cell_type": "markdown", 
                    "metadata": {}, 
                    "source": [l + '\n' for l in current_md]
                })
            current_md = []
            in_code_block = True
            continue
            
        # 3. Detectar fim do bloco de código
        if in_code_block and line.strip() == '```':
            # Salva o código acumulado como uma célula executável
            cells.append({
                "cell_type": "code", 
                "execution_count": None, 
                "metadata": {}, 
                "outputs": [], 
                "source": [l + '\n' for l in current_code]
            })
            current_code = []
            in_code_block = False
            continue
            
        # 4. Acumular o conteúdo na célula correta
        if in_code_block:
            current_code.append(line)
        else:
            # Separar temas: cria uma nova célula de markdown ao encontrar Títulos H1 (#) ou H2 (##)
            if re.match(r'^#{1,2}\s', line):
                if current_md and any(l.strip() for l in current_md):
                    cells.append({
                        "cell_type": "markdown", 
                        "metadata": {}, 
                        "source": [l + '\n' for l in current_md]
                    })
                current_md = [line]
            else:
                current_md.append(line)
                
    # Adicionar qualquer markdown residual no final do arquivo
    if current_md and any(l.strip() for l in current_md):
        cells.append({
            "cell_type": "markdown", 
            "metadata": {}, 
            "source": [l + '\n' for l in current_md]
        })
        
    # Limpar a quebra de linha da última string de cada célula (Padrão do formato IPYNB)
    for cell in cells:
        if cell['source']:
            cell['source'][-1] = cell['source'][-1].rstrip('\n')
            
    # Montar a estrutura final do JSON
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    return json.dumps(notebook, indent=2)

def processar_arquivos():
    # Busca todos os arquivos .md na pasta atual
    arquivos_md = glob.glob('*.md')
    
    if not arquivos_md:
        print("Nenhum arquivo .md encontrado na pasta atual.")
        return

    for arquivo in arquivos_md:
        nome_base = os.path.splitext(arquivo)[0]
        if nome_base == "README":
            continue
        caminho_saida = f"{nome_base}.ipynb"
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            
        ipynb_json = converter_md_para_ipynb(conteudo)
        
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(ipynb_json)
            
        print(f"✅ Convertido: '{arquivo}' -> '{caminho_saida}'")

# Executa a conversão
if __name__ == "__main__":
    processar_arquivos()