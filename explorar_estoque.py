import pandas as pd

# Lendo a base
df = pd.read_excel("base_estoque.xlsx")

# Quantas linhas e colunas?
print("Dimensões da base:")
print(f"{df.shape[0]} linhas x {df.shape[1]} colunas")

# Quais são as colunas?
print("\nColunas disponíveis:")
print(df.columns.tolist())

# Primeiras 5 linhas
print("\nPrimeiras 5 linhas:")
print(df.head())

# Resumo geral dos dados
print("\nResumo geral:")
print(df.info())


# ================================================
# PARTE 2 — Análises e perguntas sobre o estoque
# ================================================

# 1. Quais produtos estão com status "Em falta"?
print("Produtos em falta:")
em_falta = df[df["status"] == "Em falta"]
print(em_falta[["nome_produto", "categoria", "quantidade_estoque", "status"]])

# 2. Quais produtos estão abaixo do estoque mínimo?
print("\nProdutos abaixo do estoque mínimo:")
abaixo_minimo = df[df["quantidade_estoque"] < df["estoque_minimo"]]
print(abaixo_minimo[["nome_produto", "quantidade_estoque", "estoque_minimo"]])

# 3. Quantos produtos existem por categoria?
print("\nQuantidade de produtos por categoria:")
print(df.groupby("categoria")["nome_produto"].count())

# 4. Qual a média de preço de venda por categoria?
print("\nMédia de preço de venda por categoria:")
print(df.groupby("categoria")["preco_venda"].mean().round(2))

# 5. Qual categoria tem o maior valor total em estoque?
df["valor_total_estoque"] = df["quantidade_estoque"] * df["preco_custo"]
print("\nValor total em estoque por categoria:")
print(df.groupby("categoria")["valor_total_estoque"].sum().round(2).sort_values(ascending=False))