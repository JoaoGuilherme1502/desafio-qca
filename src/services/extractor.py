import pdfplumber
import re

class InvoiceExtractor:
    """
    Classe responsável por extrair dados brutos de faturas em PDF.
    """

    @staticmethod
    def extract_data(pdf_path: str) -> dict[str, any]:
        """
        Lê um arquivo PDF e extrai os dados do cabeçalho via texto
        e a tabela de produtos via tabelas estruturadas.
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

                text = page.extract_text() or ""

                match_order = re.search(r"Order\s+ID:\s*(\d+)", text, re.IGNORECASE)
                if match_order:
                    raw_data["order_id"] = match_order.group(1)

                match_date = re.search(r"Order\s+Date:\s*([\d-]+)", text, re.IGNORECASE)
                if match_date:
                    raw_data["date"] = match_date.group(1)

                match_customer = re.search(r"Customer\s+ID:\s*([A-Z0-9]+)", text, re.IGNORECASE)
                if match_customer:
                    raw_data["customer_id"] = match_customer.group(1)

                tables = page.extract_tables()

                for table in tables:
                    if not table or not table[0]:
                        continue

                    header = [str(col).lower() for col in table[0] if col]

                    if any("product" in col for col in header):
                        for row in table[1:]:
                            if not row or not row[0] or "totalprice" in str(row[0]).replace(" ", "").lower():
                                continue
                            
                            if len(row) >= 4:
                                raw_data["products"].append({
                                    "product_id": row[0],
                                    "product": str(row[1]).replace("\n", " ").strip(),
                                    "quantity": row[2],
                                    "unit_price": row[3]
                                })
                        break 

        except FileNotFoundError:
            print(f"Arquivo não encontrado: {pdf_path}")
            raise
        except Exception as e:
            print(f"Falha ao processar o PDF: {str(e)}")
            raise

        return raw_data