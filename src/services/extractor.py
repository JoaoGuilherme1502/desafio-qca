import pdfplumber

class InvoiceExtractor:
    """
    Classe responsável por extrair dados brutos de faturas em PDF.
    """

    @staticmethod
    def extract_data(pdf_path: str) -> dict[str, any]:
        """
        Lê um arquivo PDF e extrai os dados do cabeçalho e a tabela de produtos.
        Retorna um dicionário com os dados brutos.
        """

        raw_data = {
            "order_id": None,
            "date": None,
            "customer_id": None,
            "products": []
        }

        try:
            with pdfplumber.open(pdf_path) as pdf:
                if not pdf.pages:
                    raise ValueError("O arquivo PDF está vazio")
                
                page = pdf.pages[0]
                tables = page.extract_tables()

                if len(tables) < 2:
                    raise ValueError(f"Esperando pelo menos 2 tabelas, encontrado {len(tables)}")

                header_table = tables[0]
                if len(header_table) >= 2:
                    header_values = header_table[1]  
                    if len(header_values) >= 3:
                        raw_data["order_id"] = header_values[0]
                        raw_data["date"] = header_values[1]
                        raw_data["customer_id"] = header_values[2]

                products_table = tables[1]
                for row in products_table[1:]:
                    if row and len(row) >= 4:
                        raw_data["products"].append({
                            "product_id": row[0],
                            "product": row[1],
                            "quantity": row[2],
                            "unit_price": row[3]
                        })

        except FileNotFoundError:
            print(f"Arquivo não encontrado: {pdf_path}")
            raise
        except Exception as e:
            print(f"Falha ao processar o PDF: {str(e)}")
            raise

        return raw_data