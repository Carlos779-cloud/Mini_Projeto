# SalesInsight PY

## Sobre o projeto

O SalesInsight PY é um pipeline completo de análise de dados de vendas desenvolvido em Python.
O sistema lê, limpa, transforma e visualiza um dataset de vendas, gerando métricas,
segmentações e projeções simples de tendência.

## Vídeo de demonstração

[(https://drive.google.com/file/d/1Qr4tY0xXJDXS7UqQx9lhcko6wNV99m-5/view?usp=sharing)]

## O que o sistema analisa

- Receita total e volume de vendas por mês e trimestre
- Top produtos e categorias por receita
- Desempenho por região
- Segmentação de clientes por nível de gasto (Bronze, Prata, Ouro)
- Projeção simples de tendência para os próximos meses
- Exportação de relatórios em CSV e JSON

## Objetivo

Praticar os principais conceitos do Módulo 01 de IA para Análise Preditiva:

- Lógica de programação com Python
- Variáveis, tipos de dados e operadores
- Condicionais (if, elif, else) e repetição (for, while)
- Funções, parâmetros, retorno e funções lambda
- Funções de ordem superior (função que recebe função)
- Leitura e escrita de arquivos CSV e JSON
- Módulo datetime para manipulação de datas
- Expressões regulares com o módulo re
- Pandas: DataFrames, limpeza, groupby, filtros e transformações
- NumPy: arrays, operações vetorizadas, broadcasting, np.select
- Matplotlib e Seaborn: gráficos, customização e exportação em PNG
- Classes, construtores, atributos, métodos, herança e super()
- GitHub, branches, commits e GitFlow simplificado
- Kanban para organização do projeto

## Estrutura do projeto:

```text
SalesInsight_PY/
│
├── data/                           
│   ├── raw/                        # Dados sintéticos brutos gerados
│
├── notebooks/                      # Espaço de experimentação
|
├──outputs                          # Saidas geradas pelo código
|
├── src/                            # Codigo Produtivo
│   ├── __init__.py                 # Transforma a pasta src num pacote Python
│   ├── pipeline.py                 # Classes do Pipeline de Dados
│   ├── utils.py                    # Funções
│
├── main.py                         # Importa do src e executa tudo
├── .gitignore                      # Proteção de arquivos 
├── requirements.txt                # Bibliotecas necessárias 
└── README.md                       # Documentação do projeto

```


## Como Executar o Projeto (Via VS Code)

Este guia foi estruturado para que o projeto possa ser executado de forma idêntica tanto em ambiente **Linux (Ubuntu)** quanto **Windows**, utilizando o **VS Code** como interface padrão.

### 1. Clonar o Repositório e Abrir no VS Code
Abra o seu terminal de preferência e execute os comandos para baixar o projeto e abri-lo diretamente no VS Code:

```bash
git clone https://github.com/Carlos779-cloud/Mini_Projeto.git
```

### 2. Instalar um ambiente virtual e as Bibliotecas Necessárias

Com o projeto aberto no VS Code, abra o terminal integrado da IDE (atalho: Ctrl + ' ou indo no menu superior em Terminal > New Terminal) e execute os comandos abaixo para instalar as dependências do projeto:

```bash
python -m venv venv
```
e em seguida

```bash
pip install -r requirements.txt
```

### 3. Executar o Pipeline Principal

Para rodar todo o ecossistema (geração de dados sintéticos, limpeza e análises), você tem duas opções simples no VS Code:

  - Opção A (Via Terminal do VS Code)    
    Digite o comando abaixo e pressione Enter:
    
    ```bash
    python main.py
    ```

  - Opção B (Via Interface Visual):
    
    1 Abra o arquivo main.py na barra lateral do VS Code.
    
    2 Clique no botão de Play (Run Python File) localizado no canto superior direito da tela.

## Tecnologias Utilizadas
[![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)
<br>
[![Jupyter Notebook](https://img.shields.io/badge/Jupyter-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white)](https://jupyter.org/)
<br>
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
<br>
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
<br>
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
