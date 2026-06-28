import json
import os

from src.models.invoice import Invoice


class InvoiceStorage:
    """
    Classe responsável pela persistência das faturas em um arquivo JSON.
    Garante que não haja registros duplicados.
    """

    @staticmethod
    def _load_database(db_path: str) -> list[dict]:
        """
        Método auxiliar para carregar os dados atuais do arquivo JSON.
        Se o arquivo não existir ou estiver vazio, retorna uma lista vazia.
        """

        if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
            return []
        
        try: 
            with open(db_path, "r", encoding="utf-8") as file:
                return json.load(file)
        
        except json.JSONDecodeError:
            raise ValueError(f"O arquivo {db_path} continha dados inválidos")
        
    @classmethod
    def save_invoice(cls, invoice: Invoice, db_path: str = None) -> bool:
        """
        Salva uma fatura validada no arquivo JSON dentro da pasta data.
        Retorna True se salvou, ou False se o registro for duplicado.
        """
        if db_path is None:
            db_path = os.path.join("data", "database.json")

        try:
            current_data = cls._load_database(db_path)

            # Verifica se o order_id já existe para evitar duplicidade
            for entry in current_data:
                if entry.get("order_id") == invoice.order_id:
                    print(f"Fatura {invoice.order_id} já cadastrado\n")
                    return False
            
            invoice_dict = invoice.model_dump(mode="json")
            current_data.append(invoice_dict)

            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            with open(db_path, "w", encoding="utf-8") as file:
                json.dump(current_data, file, indent=4, ensure_ascii=False)

            print(f"Fatura {invoice.order_id} salva com sucesso em {db_path}")
            return True
        
        except Exception as e:
            raise RuntimeError(f"Falha ao tentar salvar no banco de dados: {e}")