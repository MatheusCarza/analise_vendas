import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

# ── Configuração geral ────────────────────────────────────────────────────────
Path("outputs").mkdir(exist_ok=True)
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 120

# ── 1. Carregamento e resumo ──────────────────────────────────────────────────
df = pd.read_csv("dados/vendas_limpo.csv", parse_dates=["data_venda"])

print("=" * 55)
print("RESUMO GERAL DOS DADOS")
print("=" * 55)
print(f"Shape : {df.shape[0]} linhas × {df.shape[1]} colunas")
print()
print("Tipos de cada coluna:")
print(df.dtypes.to_string())
print()
print("Estatísticas descritivas (colunas numéricas):")
print(df.describe().to_string())
print()

# Coluna auxiliar com o valor total de cada venda
df["valor_total"] = df["quantidade"] * df["preco_unitario"]

# ── 2. Visualizações ──────────────────────────────────────────────────────────

# --- 2.1 Evolução das vendas ao longo do tempo --------------------------------
vendas_por_mes = (
    df.set_index("data_venda")
    .resample("ME")["valor_total"]
    .sum()
    .reset_index()
)
vendas_por_mes["mes"] = vendas_por_mes["data_venda"].dt.strftime("%b/%Y")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(
    vendas_por_mes["mes"],
    vendas_por_mes["valor_total"],
    marker="o",
    linewidth=2,
    color="steelblue",
)
ax.fill_between(
    vendas_por_mes["mes"],
    vendas_por_mes["valor_total"],
    alpha=0.15,
    color="steelblue",
)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
ax.set_title("Evolução das Vendas ao Longo do Tempo", fontsize=13, pad=12)
ax.set_xlabel("Mês")
ax.set_ylabel("Receita Total (R$)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("outputs/evolucao_vendas.png")
plt.close()
print("✓ outputs/evolucao_vendas.png salvo")

# --- 2.2 Vendas totais por categoria de produto --------------------------------
vendas_categoria = (
    df.groupby("categoria")["valor_total"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=vendas_categoria, x="categoria", y="valor_total", ax=ax)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
ax.set_title("Receita Total por Categoria de Produto", fontsize=13, pad=12)
ax.set_xlabel("Categoria")
ax.set_ylabel("Receita Total (R$)")
plt.tight_layout()
plt.savefig("outputs/vendas_por_categoria.png")
plt.close()
print("✓ outputs/vendas_por_categoria.png salvo")

# --- 2.3 Distribuição do valor das vendas (histograma) ------------------------
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(df["valor_total"], bins=20, kde=True, ax=ax, color="mediumpurple")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
ax.set_title("Distribuição do Valor das Vendas", fontsize=13, pad=12)
ax.set_xlabel("Valor da Venda (R$)")
ax.set_ylabel("Frequência")
plt.tight_layout()
plt.savefig("outputs/distribuicao_valores.png")
plt.close()
print("✓ outputs/distribuicao_valores.png salvo")

# --- 2.4 Receita por vendedor (barras horizontais) ----------------------------
vendas_vendedor = (
    df.groupby("vendedor")["valor_total"]
    .sum()
    .sort_values()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    data=vendas_vendedor,
    y="vendedor",
    x="valor_total",
    hue="vendedor",
    orient="h",
    ax=ax,
    palette="Blues_d",
    legend=False,
)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
ax.set_title("Receita Total por Vendedor", fontsize=13, pad=12)
ax.set_xlabel("Receita Total (R$)")
ax.set_ylabel("Vendedor")
plt.tight_layout()
plt.savefig("outputs/vendas_por_vendedor.png")
plt.close()
print("✓ outputs/vendas_por_vendedor.png salvo")

# ── 3. Insights ───────────────────────────────────────────────────────────────
mes_top = vendas_por_mes.loc[vendas_por_mes["valor_total"].idxmax()]
categoria_top = vendas_categoria.iloc[0]
vendedor_top = vendas_vendedor.iloc[-1]  # já ordenado crescente, último = maior
ticket_medio = df["valor_total"].mean()
total_geral = df["valor_total"].sum()
status_counts = df["status"].value_counts()

print()
print("=" * 55)
print("PRINCIPAIS INSIGHTS")
print("=" * 55)
print(f"  Receita total gerada : R$ {total_geral:,.2f}")
print(f"  Ticket médio por venda: R$ {ticket_medio:,.2f}")
print(f"  Mês com mais vendas  : {mes_top['mes']} (R$ {mes_top['valor_total']:,.2f})")
print(f"  Categoria líder      : {categoria_top['categoria']} (R$ {categoria_top['valor_total']:,.2f})")
print(f"  Vendedor destaque    : {vendedor_top['vendedor']} (R$ {vendedor_top['valor_total']:,.2f})")
print()
print("  Status das vendas:")
for status, qtd in status_counts.items():
    pct = qtd / len(df) * 100
    print(f"    {status:<15} {qtd:>3} vendas ({pct:.1f}%)")
print("=" * 55)
