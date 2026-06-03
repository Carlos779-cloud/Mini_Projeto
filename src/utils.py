# ==============
# BIBLIOTECAS
# ==============

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ignorar avisos
import warnings
warnings.filterwarnings("ignore")


# ===================
# FUNÇÕES AUXILIARES
# ===================

def gerar_dataset_vendas(n_registros=200, seed=42):
    
    """
    Gera um dataset sintético de vendas com dados intencionalmente sujos.
    """
    
    random.seed(seed)
    np.random.seed(seed)

    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse", "Headset"]
    categorias = {"Notebook": "Computadores", "Smartphone": "Celulares", "Tablet": "Celulares",
                  "Monitor": "Computadores", "Teclado": "Periféricos", "Mouse": "Periféricos",
                  "Headset": "Periféricos"}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    clientes = [f"Cliente_{i:03d}" for i in range(1, 51)]

    data_inicio = datetime(2024, 1, 1)
    dados = []

    for i in range(n_registros):
        produto = random.choice(produtos)
        quantidade = random.randint(1, 10)
        preco_base = {"Notebook": 3500, "Smartphone": 2200, "Tablet": 1800,
                      "Monitor": 1200, "Teclado": 250, "Mouse": 120, "Headset": 350}[produto]
        preco = round(preco_base * random.uniform(0.85, 1.15), 2)
        data = data_inicio + timedelta(days=random.randint(0, 364))

        # Inserindo dados intencionalmente sujos para limpeza
        if random.random() < 0.05:
            quantidade = None          # valor nulo
        if random.random() < 0.04:
            preco = None               # valor nulo
        if random.random() < 0.03:
            produto = "  " + produto   # espaço extra (string suja)

        dados.append({
            "id_venda": i + 1,
            "data_venda": data.strftime("%Y-%m-%d") if random.random() > 0.02 else "DATA INVÁLIDA",
            "cliente": random.choice(clientes),
            "produto": produto,
            "categoria": categorias.get(produto.strip(), "Outros"),
            "regiao": random.choice(regioes),
            "quantidade": quantidade,
            "preco_unitario": preco
        })

    return pd.DataFrame(dados)


def inspecionar_dados(df):
    
    """
    Exibe informações básicas do DataFrame.
    """
    
    print(f"{30*'='}\n INSPEÇÃO INICIAL DO DATASET \n{30*'='}\n")
    print("- ESTRUTURA:")
    print(f"   Quantidade de linhas: {df.shape[0]}")
    print(f"   Quantidade de colunas: {df.shape[1]}")
    print(f"\n- COLUNAS: {list(df.columns)}")
    print(f"\n- TIPOS DE DADOS:\n{df.dtypes}")
    print(f"\n- VALORES NULOS POR COLUNA:\n{df.isnull().sum().sort_values(ascending = False)}")
    print("\n- PRIMEIROS REGISTROS:")
    print(df.head())
    print("\n- ULTIMOS REGISTROS:")
    print(df.tail())
    print("\n- ESTATISTICAS DESCRITIVAS VARIAEIS NUMÉRICAS:")
    print(df.describe())
    print("\n- RESUMO ESTATISTICO VARIAVEIS CATEGORICAS:")
    print(df.describe(include = object))
    
def limpar_dados(df):
    
    """
    Limpa e trata o DataFrame de vendas.
    Retorna o DataFrame limpo e um relatório de limpeza.
    """
    n_inicial = len(df)
    relatorio = {}

    # 1. Remover espaços extras em colunas de texto
    colunas_texto = df.select_dtypes(include="object").columns
    for col in colunas_texto:
        df[col] = df[col].str.strip()

    # 2. Converter data e remover datas inválidas
    df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce")
    n_datas_invalidas = df["data_venda"].isnull().sum()
    df = df.dropna(subset=["data_venda"])
    relatorio["datas_invalidas_removidas"] = n_datas_invalidas

    # 3. Remover linhas com quantidade ou preço nulos
    n_antes = len(df)
    df = df.dropna(subset=["quantidade", "preco_unitario"])
    relatorio["linhas_nulas_removidas"] = n_antes - len(df)

    # 4. Garantir tipos numéricos corretos
    df["quantidade"] = df["quantidade"].astype(int)
    df["preco_unitario"] = df["preco_unitario"].astype(float)

    n_final = len(df)
    relatorio["registros_iniciais"] = n_inicial
    relatorio["registros_finais"] = n_final
    relatorio["registros_removidos_total"] = n_inicial - n_final

    print(f"{20*'='}\nRELATÓRIO DE LIMPEZA\n{20*'='}\n")
    for chave, valor in relatorio.items():
        print(f"  - {chave.upper()}: {valor}\n")

    return df, relatorio


def criar_colunas_derivadas(df):
    
    """
    Cria colunas calculadas e derivadas a partir do dataset limpo.
    """

    # Receita total por linha de venda
    df["receita_total"] = df["quantidade"] * df["preco_unitario"]

    # Extração de componentes de data
    df["mes"] = df["data_venda"].dt.month
    df["mes_nome"] = df["data_venda"].dt.strftime("%B")  # nome do mês
    df["trimestre"] = df["data_venda"].dt.quarter.apply(lambda q: f"Q{q}")
    df["ano"] = df["data_venda"].dt.year

    # Classificação da receita por item com numpy.select (transformação condicional vetorizada)
    condicoes = [
        df["receita_total"] < 500,
        (df["receita_total"] >= 500) & (df["receita_total"] < 5000),
        df["receita_total"] >= 5000
    ]
    classificacoes = ["Baixo Valor", "Médio Valor", "Alto Valor"]
    df["faixa_receita_item"] = np.select(condicoes, classificacoes, default="Não Classificado")
    print(f"{25*'='}\nCOLUNAS DERIVADAS CRIADAS\n{25*'='}")
    print(df[["data_venda", "receita_total", "ano","mes", "trimestre", "faixa_receita_item"]].head())

    return df


def segmentar_clientes(df):
    
    """
    Segmenta clientes pelo total gasto usando groupby e lambda.
    """

    clientes = df.groupby("cliente")["receita_total"].sum().reset_index()
    clientes.columns = ["cliente", "total_gasto"]

    # Classificação usando função lambda com condicionais
    clientes["segmento"] = clientes["total_gasto"].apply(
        lambda gasto: "Ouro" if gasto > 15000
                      else ("Prata" if gasto >= 5000 else "Bronze")
    )

    clientes = clientes.sort_values("total_gasto", ascending=False).reset_index(drop = True)

    print(f"{24*'='}\nSEGMENTAÇÃO DE CLIENTES\n{24*'='}\n")    
    print(clientes.head(10))
    print("\nDistribuição de segmentos:")
    print(clientes['segmento'].value_counts().reset_index())

    return clientes


def calcular_estatisticas_numpy(df):
    
    """
    Usa NumPy para calcular estatísticas sobre as receitas.
    
    """
    print(f"{23*'='}\nESTATÍSTICAS COM NUMPY\n{23*'='}")

    receitas = df["receita_total"].to_numpy()  # Converte para array NumPy

    media = np.mean(receitas)
    mediana = np.median(receitas)
    desvio_padrao = np.std(receitas)
    total = np.sum(receitas)
    p25 = np.percentile(receitas, 25)
    p75 = np.percentile(receitas, 75)

    print(f"  Receita média por venda:    R$ {media:.2f}")
    print(f"  Receita mediana por venda:  R$ {mediana:.2f}")
    print(f"  Desvio padrão:              R$ {desvio_padrao:.2f}")
    print(f"  Receita total:              R$ {total:.2f}")
    print(f"  Percentil 25 (Q1):          R$ {p25:.2f}")
    print(f"  Percentil 75 (Q3):          R$ {p75:.2f}")

    # Broadcasting: normalizar receitas entre 0 e 1
    receitas_normalizadas = (receitas - receitas.min()) / (receitas.max() - receitas.min())
    print(f"\n  Receitas normalizadas (primeiros 5): {receitas_normalizadas[:5].round(4)}")

    # Operação vetorizada: identificando quantidades sem loop
    acima_da_media = receitas[receitas > media]
    abaixo_da_media = receitas[receitas < media]
    q1 = receitas[receitas < p25]
    q2 = receitas[(receitas >= p25) & (receitas < mediana)]
    q3 = receitas[(receitas >= mediana) & (receitas < p75)]
    q4 = receitas[receitas > p75]
    print(f"\n  Vendas acima da média: {len(acima_da_media)}")
    print(f"  Vendas abaixo da média: {len(abaixo_da_media)}")
    print(f"  Vendas no primeiro quartil: {len(q1)}")
    print(f"  Vendas no segundo quartil: {len(q2)}")
    print(f"  Vendas no terceiro quartil: {len(q3)}")
    print(f"  Vendas no quarto quartil: {len(q3)}")

    return {
        "media": media, "mediana": mediana,
        "desvio_padrao": desvio_padrao, "total": total
    }
    

def gerar_visualizacoes(df, metricas, output_dir="outputs/graficos"):
    
    """
    Gera e exporta visualizações dos dados de vendas.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Configurações visuais globais
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams["figure.figsize"] = (12, 6)
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 12

    # --- Gráfico 1: Receita por Mês (linha) ---
    fig, ax = plt.subplots()
    por_mes = metricas["por_mes"]
    ax.plot(por_mes["mes"], por_mes["receita_total"], marker="o", linewidth=2, color="#2196F3")
    ax.fill_between(por_mes["mes"], por_mes["receita_total"], alpha=0.15, color="#2196F3")
    ax.set_title("Receita Total por Mês (2024)")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Receita Total (R$)")
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["Jan","Fev","Mar","Abr","Mai","Jun",
                         "Jul","Ago","Set","Out","Nov","Dez"], rotation=45)
    plt.tight_layout()
    caminho = os.path.join(output_dir, "vendas_por_mes.png")
    plt.savefig(caminho, dpi=150)
    plt.show()
    plt.close()
    print(f"  Gráfico exportado: {caminho}\n")

    # --- Gráfico 2: Top 5 Produtos (barras horizontais) ---
    fig, ax = plt.subplots()
    top = metricas["top_produtos"]
    sns.barplot(data=top, y="produto", x="receita_total", ax=ax, palette="Blues_d")
    ax.set_title("Top 5 Produtos por Receita Total")
    ax.set_xlabel("Receita Total (R$)")
    ax.set_ylabel("Produto")
    for container in ax.containers:
        ax.bar_label(container, fmt="R$ %.0f", padding=5)
    plt.tight_layout()
    caminho = os.path.join(output_dir, "top_produtos.png")
    plt.savefig(caminho, dpi=150)
    plt.show()
    plt.close()
    print(f"  Gráfico exportado: {caminho}\n")

    # --- Gráfico 3: Distribuição de Receita por Região (boxplot) ---
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x="regiao", y="receita_total", ax=ax, palette="Set2")
    ax.set_title("Distribuição de Receita por Transação – Por Região")
    ax.set_xlabel("Região")
    ax.set_ylabel("Receita por Venda (R$)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    caminho = os.path.join(output_dir, "distribuicao_regioes.png")
    plt.savefig(caminho, dpi=150)
    plt.show()
    plt.close()
    print(f"  Gráfico exportado: {caminho}")

    print(f"\n**VISUALIZAÇÕES GERADAS COM SUCESSO {60*'-'}")
