from pathlib import Path
from src.utils import gerar_dataset_vendas
from src.pipeline import *

def main():
    """
    Função principal: executa o pipeline completo do SalesInsight PY.
    """
    print("\n" + "="*60)
    print("   SALESINSIGHT PY – Pipeline de Análise de Dados de Vendas")
    print("="*60)
    
    # Definindo dinamicamente o caminho do dataset
    BASE_DIR = Path(__file__).resolve().parent
    DATA_RAW_DIR = BASE_DIR / "data" / "raw"
    ARQUIVO_VENDAS = DATA_RAW_DIR / "vendas.csv"
    
    # Etapa 0: Gerar dataset (se necessário)
    if not ARQUIVO_VENDAS.exists():
        print("\n[INFO] Gerando dataset sintético...")
        df_gerado = gerar_dataset_vendas(n_registros=200)
        DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
        df_gerado.to_csv(ARQUIVO_VENDAS, index=False)
        print(f"[INFO] Dataset gerado e salvo em: {ARQUIVO_VENDAS}")
    else:
        print(f"\n[INFO] Dataset já existe em: {ARQUIVO_VENDAS}")
        
    # Etapa 1 a 6: Pipeline via classe com herança
    analisador = AnalisadorComProjecao(ARQUIVO_VENDAS, meses_projecao=3)
    (analisador
        .carregar()
        .limpar()
        .transformar()
        .analisar()
        .projetar_tendencia()
        .visualizar()
        .exportar_relatorio()
    )
    
    # Etapa extra: limpeza com regex
    analisador.df_limpo = limpar_strings_com_regex(analisador.df_limpo)


    # Etapa extra: exportação JSON
    stats = calcular_estatisticas_numpy(analisador.df_limpo)
    exportar_resultados(analisador.metricas, analisador.clientes, stats)
    
        # Resumo final
    analisador.resumo()
    analisador.exibir_projecao_detalhada()





if __name__ == "__main__":
    main()
