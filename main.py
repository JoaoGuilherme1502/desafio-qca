import os
import argparse
from src.services.extractor import InvoiceExtractor
from src.services.storage import InvoiceStorage
from src.services.validator import InvoiceValidator
from src.services.analytics import InvoiceAnalytics

def run_ingest(pdf_dir: str, db_path: str):
    """Executa o pipeline de extração, validação e armazenamento."""
    print(f"Iniciando ingestão: Buscando PDFs na pasta {pdf_dir}\n")

    if not os.path.exists(pdf_dir):
        print(f"O diretório {pdf_dir} não foi encontrado")
        return

    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print("Nenhum arquivo PDF encontrado")
        return

    print(f"Encontrado(s) {len(pdf_files)} arquivo(s) PDF. Iniciando processamento...\n")

    added_invoices = 0
    ignored_duplicates = 0
    failures = 0

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)

        try:
            raw_data = InvoiceExtractor.extract_data(pdf_path)
            valid_invoice = InvoiceValidator.validate_invoice(raw_data)
            is_saved = InvoiceStorage.save_invoice(valid_invoice, db_path)
            
            if is_saved:
                added_invoices += 1
            else:
                ignored_duplicates += 1
            
        except Exception as e:
            print(f"Falha ao processar {pdf_file}: {e}")
            failures += 1

    total_processed = added_invoices + ignored_duplicates + failures

    print("=" * 40)
    print("     INGESTÃO CONCLUÍDA!")
    print("=" * 40)
    print(f"\nPDFs processados:           {total_processed}")
    print(f"Novas faturas adicionadas:    {added_invoices}")
    print(f"Duplicadas ignoradas:         {ignored_duplicates}")
    print(f"Falhas:                       {failures}")
    print(f"Banco de dados atualizado em: {db_path}\n")


def run_analytics(db_path: str):
    """Executa a análise de dados usando o Pandas."""
    print("=" * 40)
    print("     INICIANDO ANÁLISE DE DADOS")
    print("=" * 40)
    
    if not os.path.exists(db_path):
        print(f"Banco de dados não encontrado em {db_path}. Rode a ingestão primeiro!")
        return

    try:
        analytics = InvoiceAnalytics(db_path)
        
        print("\n Média do valor total das faturas:")
        print(f"   R$ {analytics.get_average_invoice_value():,.2f}")
        
        print("\n Produto com maior frequência de compra:")
        top_product, purchase_count = analytics.get_most_frequent_product()
        print(f"   {top_product}\n   Ocorrências: {purchase_count}")
        
        print("\n Valor total gasto por cada produto:")
        print(analytics.get_total_spent_per_product().head().to_string(index=False))
        
        print("\n Listagem de produtos (Nome e Preço Unitário):")
        print(analytics.get_unique_products_list().head().to_string(index=False))
        
    except Exception as e:
        print(f"Erro ao gerar relatórios analíticos: {e}")


def main():
    # Configuração do Argparse para a CLI
    parser = argparse.ArgumentParser(
        description="Pipeline de Processamento e Análise de Faturas da QCA",
        epilog="Exemplo de uso: python main.py all"
    )
    
    parser.add_argument(
        "command",
        choices=["ingest", "analytics", "all"],
        help="Comando a ser executado: 'ingest' (processar PDFs), 'analytics' (gerar relatórios) ou 'all' (ambos)."
    )

    # Faz o parser do que o usuário digitou no terminal
    args = parser.parse_args()

    # Caminhos padrão do desafio
    pdf_dir = os.path.join("data", "invoices")
    db_path = os.path.join("data", "database.json")

    # Roteamento dos comandos
    if args.command == "ingest":
        run_ingest(pdf_dir, db_path)
    elif args.command == "analytics":
        run_analytics(db_path)
    elif args.command == "all":
        run_ingest(pdf_dir, db_path)
        run_analytics(db_path)

if __name__ == "__main__":
    main()