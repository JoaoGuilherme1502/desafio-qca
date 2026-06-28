import json
import os

import pandas as pd


class InvoiceAnalytics:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.df = self._load_and_flatten_data()

    def _load_and_flatten_data(self) -> pd.DataFrame:
        """Lê o JSON e transforma os dados aninhados em um DataFrame Tabular."""

        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Banco de dados não encontrado em {self.db_path}")
        
        try:
            with open(self.db_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"O arquivo {self.db_path} está corrompido ou não é um JSON válido")
        
        if not data:
            raise ValueError("O banco de dados está vazio")
        
        try:
            df = pd.json_normalize(
                data,
                record_path=["products"],
                meta=["order_id", "date", "customer_id"]
            )
        except KeyError as e:
            raise KeyError(f"Estrutura de dados inválida. Chave não encontrada: {e}")
        
        try:
            df["total_value"] = df["quantity"] * df["unit_price"]
        except KeyError:
            raise KeyError("As colunas 'quantity' ou 'unit_price' estão ausentes nos dados.")
        except TypeError:
            raise TypeError("Os valores de quantidade ou preço não são numéricos.")

        return df
    
    # Regras Analíticas para o desafio
    
    def get_average_invoice_value(self) -> float:
        """Calcula a média do valor total das faturas."""

        if self.df.empty:
            return 0.0
        invoice_totals = self.df.groupby("order_id")["total_value"].sum()
        return float(invoice_totals.mean())
    
    def get_most_frequent_product(self) -> tuple[str, int]:
        """Produto com maior frequência de compra e sua quantidade de ocorrências."""

        if self.df.empty:
            return "nenhum produto", 0
        
        frequency = self.df["product"].value_counts()

        top_product = str(frequency.index[0])
        purchase_count = int(frequency.iloc[0])

        return top_product, purchase_count
    
    def get_total_spent_per_product(self) -> pd.DataFrame:
        """Valor total gasto por cada produto."""

        if self.df.empty:
            return pd.DataFrame()
        return (
            self.df.groupby("product")["total_value"]
            .sum()
            .reset_index()
            .sort_values(by="total_value", ascending=False)
        )
    
    def get_unique_products_list(self) -> pd.DataFrame:
        """Listagem de produtos contendo Nome e Preço Unitário."""

        if self.df.empty:
            return pd.DataFrame()
        return (
            self.df[["product", "unit_price"]]
            .drop_duplicates()
            .sort_values(by="product")
            .reset_index(drop=True)
        )