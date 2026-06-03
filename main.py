from pathlib import Path
from src.utils import gerar_dataset_vendas

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




if __name__ == "__main__":
    main()
