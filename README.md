# Desafio Técnico QCA
Este projeto consiste em um pipeline de processamento de faturas (**Invoices**) desenvolvido em **Python**, cujo objetivo é extrair informações de arquivos PDF, validar os dados, armazená-los em um arquivo JSON e disponibilizar consultas analíticas utilizando **Pandas**.

A solução foi organizada seguindo o princípio de separação de responsabilidades, dividindo cada etapa do processamento em componentes independentes.

# 🛠️ Arquitetura e Tecnologias

O Projeto foi dividido em quatro responsabilidades principais:

1. **InvoiceExtractor**
   - Responsável pela leitura dos arquivos PDF utilizando **pdfplumber** e Expressões Regulares (Regex), extraindo os dados do cabeçalho e da tabela de produtos.

2. **InvoiceValidator**
   - Utiliza **Pydantic** para validar os dados extraídos, realizar conversões de tipos e garantir que a estrutura da fatura esteja correta antes do armazenamento.

3. **InvoiceStorage**
   - Responsável pela persistência dos dados em um arquivo `database.json`, evitando o armazenamento de faturas duplicadas por meio da verificação do `order_id`.

4. **InvoiceAnalytics**
   - Utiliza **Pandas** para carregar a base de dados e gerar as análises solicitadas pelo desafio.
  
--- 

## 📐 Fluxo da Aplicação

```text
PDFs
   │
   ▼
InvoiceExtractor
   │
   ▼
InvoiceValidator (Pydantic)
   │
   ▼
InvoiceStorage (database.json)
   │
   ▼
InvoiceAnalytics (Pandas)
```

---

# 📂 Estrutura do Projeto

```text
desafio-qca/
├── data/
│   ├── invoices/
│   └── database.json
├── src/
│   ├── models/
│   │   ├── invoice.py
│   │   └── item.py
│   └── services/
│       ├── extractor.py
│       ├── validator.py
│       ├── storage.py
│       └── analytics.py
├── main.py
├── requirements.txt
└── README.md
```

---

---

# 🚀 Como Executar

## 1. Criar um ambiente virtual

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## 3. Executar o projeto

### Ingestão dos PDFs

```bash
python main.py ingest
```

Lê todos os arquivos PDF presentes na pasta `data/invoices`, valida os dados extraídos e atualiza o arquivo `database.json`, ignorando faturas já cadastradas.

---

### Executar apenas as análises

```bash
python main.py analytics
```

Realiza as consultas analíticas utilizando os dados armazenados no banco JSON.

---

### Executar todo o pipeline

```bash
python main.py all
```

Executa a ingestão dos PDFs e, em seguida, apresenta as análises atualizadas.

---

# 📊 Funcionalidades Implementadas

O módulo de análises retorna:

- Média do valor total das faturas;
- Produto com maior frequência de compra;
- Valor total gasto por cada produto;
- Listagem de produtos contendo nome e preço unitário.

---

# 📚 Bibliotecas Utilizadas

- Python 3.13
- Pydantic
- Pandas
- pdfplumber
- argparse *(biblioteca nativa do Python utilizada para construção da interface de linha de comando).*
