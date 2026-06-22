import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── 1. CARREGAMENTO DOS DADOS ──────────────────────────────────────────────────
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados/vendas_limpo.csv")
    df["data_venda"] = pd.to_datetime(df["data_venda"])
    df["receita"] = df["quantidade"] * df["preco_unitario"]
    return df

try:
    df = carregar_dados()
except FileNotFoundError:
    st.error("Arquivo dados/vendas_limpo.csv não encontrado.")
    st.stop()

# ── 2. SIDEBAR COM FILTROS ─────────────────────────────────────────────────────
st.sidebar.title("Filtros")

categorias_disponiveis = sorted(df["categoria"].unique())
categorias_sel = st.sidebar.multiselect(
    "Categoria",
    options=categorias_disponiveis,
    default=categorias_disponiveis,
)

vendedores_disponiveis = sorted(
    df[df["vendedor"] != "Não informado"]["vendedor"].unique()
)
vendedores_sel = st.sidebar.multiselect(
    "Vendedor",
    options=vendedores_disponiveis,
    default=vendedores_disponiveis,
)
incluir_sem_vendedor = st.sidebar.checkbox(
    "Incluir vendas sem vendedor identificado", value=True
)

mask_vendedor = df["vendedor"].isin(vendedores_sel)
if incluir_sem_vendedor:
    mask_vendedor = mask_vendedor | (df["vendedor"] == "Não informado")

df_filtrado = df[df["categoria"].isin(categorias_sel) & mask_vendedor]

# ── 3. TÍTULO PRINCIPAL ────────────────────────────────────────────────────────
st.title("Dashboard de Vendas")
st.caption(f"{len(df_filtrado)} registro(s) exibidos após os filtros")

# ── 4. KPIs ───────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

receita_total = df_filtrado["receita"].sum()
num_vendas = len(df_filtrado)
ticket_medio = receita_total / num_vendas if num_vendas > 0 else 0

col1.metric("Receita Total", f"R$ {receita_total:,.2f}")
col2.metric("Número de Vendas", num_vendas)
col3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

# ── 5. GRÁFICOS LADO A LADO ────────────────────────────────────────────────────
col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("Receita por Categoria")
    receita_cat = df_filtrado.groupby("categoria")["receita"].sum().sort_values()
    fig, ax = plt.subplots()
    ax.barh(receita_cat.index, receita_cat.values, color=sns.color_palette("pastel"))
    ax.set_xlabel("Receita (R$)")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col_dir:
    st.subheader("Receita por Mês")
    receita_mes = (
        df_filtrado.groupby(df_filtrado["data_venda"].dt.to_period("M"))["receita"]
        .sum()
    )
    receita_mes.index = receita_mes.index.astype(str)
    fig, ax = plt.subplots()
    ax.plot(receita_mes.index, receita_mes.values, marker="o", color="steelblue")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Receita (R$)")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ── 6. GRÁFICO DE VENDEDORES ───────────────────────────────────────────────────
st.subheader("Receita por Vendedor")
df_vendedores = df_filtrado[df_filtrado["vendedor"] != "Não informado"]
receita_vendedor = (
    df_vendedores.groupby("vendedor")["receita"].sum().sort_values(ascending=False)
)
fig, ax = plt.subplots(figsize=(10, 4))
sns.barplot(x=receita_vendedor.index, y=receita_vendedor.values, palette="pastel", ax=ax)
ax.set_xlabel("Vendedor")
ax.set_ylabel("Receita (R$)")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"R$ {y:,.0f}"))
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ── 7. TABELA DE DADOS ─────────────────────────────────────────────────────────
with st.expander("Ver dados brutos"):
    st.dataframe(df_filtrado)