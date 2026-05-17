import pandas as pd

# Lendo a base
df = pd.read_excel("base_estoque.xlsx")

# ================================================
# LIMPEZA 1 — Padronizar a coluna status
# ================================================
# Removing espaços acidentais e padronizando maiúsculas
df["status"] = df["status"].str.strip().str.title()

print("Valores únicos de status:")
print(df["status"].unique())

# ================================================
# LIMPEZA 2 — Tratar a coluna data_validade
# ================================================
# Substituindo "N/A" por um valor nulo real do Pandas
df["data_validade"] = df["data_validade"].replace("N/A", None)

print("\nExemplo de data_validade após limpeza:")
print(df["data_validade"].head(10))

# ================================================
# LIMPEZA 3 — Verificar se há valores nulos
# ================================================
print("\nValores nulos por coluna:")
print(df.isnull().sum())

# ================================================
# RELATÓRIO 1 — Produtos em falta ou abaixo do mínimo
# ================================================
alerta = df[
    (df["status"] == "Em Falta") |
    (df["quantidade_estoque"] < df["estoque_minimo"])
].copy()

alerta["situacao"] = alerta.apply(
    lambda row: "Em Falta" if row["status"] == "Em Falta" else "Abaixo do Mínimo",
    axis=1
)

relatorio_alerta = alerta[[
    "id_produto", "nome_produto", "categoria",
    "quantidade_estoque", "estoque_minimo", "situacao"
]].sort_values("categoria")

print(f"\nProdutos em alerta: {len(relatorio_alerta)}")
print(relatorio_alerta)

# ================================================
# RELATÓRIO 2 — Resumo financeiro por categoria
# ================================================
df["valor_total_estoque"] = df["quantidade_estoque"] * df["preco_custo"]

resumo_financeiro = df.groupby("categoria").agg(
    total_produtos    = ("nome_produto", "count"),
    valor_em_estoque  = ("valor_total_estoque", "sum"),
    ticket_medio      = ("preco_venda", "mean")
).round(2).sort_values("valor_em_estoque", ascending=False)

print("\nResumo financeiro por categoria:")
print(resumo_financeiro)

# ================================================
# EXPORTANDO OS RELATÓRIOS PARA EXCEL
# ================================================
with pd.ExcelWriter("relatorios_estoque.xlsx", engine="openpyxl") as writer:
    relatorio_alerta.to_excel(writer, sheet_name="Alertas de Estoque", index=False)
    resumo_financeiro.to_excel(writer, sheet_name="Resumo Financeiro")
    df.to_excel(writer, sheet_name="Base Completa", index=False)

print("\nArquivo relatorios_estoque.xlsx exportado com sucesso!")
print("Abas criadas: Alertas de Estoque | Resumo Financeiro | Base Completa")