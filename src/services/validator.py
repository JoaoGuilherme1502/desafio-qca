from src.models.invoice import Invoice
from pydantic import ValidationError


class InvoiceValidator:
    """
    Classe responsável por validar e converter dados brutos em modelos de domínio.
    """

    @staticmethod
    def validate(raw_data: dict) -> Invoice:
        """
        Recebe o dicionário bruto, injeta no modelo Invoice e retorna o objeto validado.
        """

        try:
            invoice = Invoice(**raw_data)
            return invoice
        
        except ValidationError as e:
            print(f"Os dados do PDF não correspondem à estrutura esperada\n{e}")