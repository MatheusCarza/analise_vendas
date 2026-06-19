import base64
import pandas as pd
from pathlib import Path
from datetime import datetime

# ── Configuração ──────────────────────────────────────────────────────────────
Path("reports").mkdir(exist_ok=True)

GRAFICOS = {
    "Evolução das Vendas ao Longo do Tempo": "outputs/evolucao_vendas.png",
    "Receita Total por Categoria de Produto": "outputs/vendas_por_categoria.png",
    "Distribuição do Valor das Vendas":       "outputs/distribuicao_valores.png",
    "Receita Total por Vendedor":             "outputs/vendas_por_vendedor.png",
}

# ── 1. Cálculo dos insights ───────────────────────────────────────────────────
df = pd.read_csv("dados/vendas_limpo.csv", parse_dates=["data_venda"])
df["valor_total"] = df["quantidade"] * df["preco_unitario"]

receita_total = df["valor_total"].sum()
ticket_medio  = df["valor_total"].mean()
total_vendas  = len(df)

vendas_por_mes = (
    df.set_index("data_venda")
    .resample("ME")["valor_total"]
    .sum()
    .reset_index()
)
MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março",    4: "Abril",
    5: "Maio",    6: "Junho",     7: "Julho",     8: "Agosto",
    9: "Setembro",10: "Outubro",  11: "Novembro", 12: "Dezembro",
}

idx_mes_top  = vendas_por_mes["valor_total"].idxmax()
mes_top_data = vendas_por_mes.loc[idx_mes_top, "data_venda"]
mes_top_nome = f"{MESES_PT[mes_top_data.month]}/{mes_top_data.year}"
mes_top_val  = vendas_por_mes.loc[idx_mes_top, "valor_total"]

categoria_top = (
    df.groupby("categoria")["valor_total"]
    .sum()
    .idxmax()
)

vendedor_top = (
    df.groupby("vendedor")["valor_total"]
    .sum()
    .idxmax()
)

# ── 2. Imagens em base64 ──────────────────────────────────────────────────────
def img_para_base64(caminho: str) -> str:
    with open(caminho, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

graficos_b64 = {
    titulo: img_para_base64(caminho)
    for titulo, caminho in GRAFICOS.items()
}

# ── 3. Montagem do HTML ───────────────────────────────────────────────────────
data_geracao = datetime.now().strftime("%d/%m/%Y às %H:%M")

cards = [
    ("💰", "Receita Total",       f"R$ {receita_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
    ("🎫", "Ticket Médio",        f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
    ("📅", "Mês em Destaque",     mes_top_nome),
    ("🏆", "Categoria Líder",     categoria_top),
    ("⭐", "Vendedor Destaque",   vendedor_top),
    ("📦", "Total de Vendas",     f"{total_vendas} vendas"),
]

def html_card(icone, titulo, valor):
    return f"""
        <div class="card">
            <div class="card-icon">{icone}</div>
            <div class="card-titulo">{titulo}</div>
            <div class="card-valor">{valor}</div>
        </div>"""

def html_grafico(titulo, b64):
    return f"""
        <div class="grafico-bloco">
            <h2 class="grafico-titulo">{titulo}</h2>
            <img src="data:image/png;base64,{b64}" alt="{titulo}" />
        </div>"""

cards_html    = "\n".join(html_card(i, t, v) for i, t, v in cards)
graficos_html = "\n".join(html_grafico(t, b) for t, b in graficos_b64.items())

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Relatório de Vendas</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: "Segoe UI", system-ui, sans-serif;
    background: #f0f2f5;
    color: #1e2a3a;
    min-height: 100vh;
  }}

  /* ── Cabeçalho ── */
  header {{
    background: linear-gradient(135deg, #1a3a5c 0%, #2d6a9f 100%);
    color: #fff;
    padding: 2.5rem 2rem 2rem;
    text-align: center;
  }}
  header h1 {{
    font-size: clamp(1.6rem, 4vw, 2.4rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 0.4rem;
  }}
  header .subtitulo {{
    font-size: 0.9rem;
    opacity: 0.75;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }}

  /* ── Container principal ── */
  main {{
    max-width: 1100px;
    margin: 2.5rem auto;
    padding: 0 1.25rem 3rem;
  }}

  /* ── Seção de cards ── */
  .secao-titulo {{
    font-size: 1.05rem;
    font-weight: 600;
    color: #2d6a9f;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 1rem;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid #d0e4f7;
  }}

  .cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin-bottom: 2.5rem;
  }}

  .card {{
    background: #fff;
    border-radius: 12px;
    padding: 1.25rem 1rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    transition: transform 0.15s, box-shadow 0.15s;
  }}
  .card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.11);
  }}
  .card-icon  {{ font-size: 1.8rem; margin-bottom: 0.5rem; }}
  .card-titulo {{
    font-size: 0.72rem;
    color: #6b7a8d;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.4rem;
  }}
  .card-valor {{
    font-size: 1.1rem;
    font-weight: 700;
    color: #1a3a5c;
    word-break: break-word;
  }}

  /* ── Gráficos ── */
  .graficos-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(460px, 1fr));
    gap: 1.5rem;
  }}

  .grafico-bloco {{
    background: #fff;
    border-radius: 12px;
    padding: 1.5rem 1.5rem 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  }}

  .grafico-titulo {{
    font-size: 0.95rem;
    font-weight: 600;
    color: #1a3a5c;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #e8edf3;
  }}

  .grafico-bloco img {{
    width: 100%;
    height: auto;
    border-radius: 6px;
    display: block;
  }}

  /* ── Rodapé ── */
  footer {{
    text-align: center;
    padding: 1.5rem;
    font-size: 0.78rem;
    color: #8a9ab0;
    border-top: 1px solid #dde4ed;
    margin-top: 3rem;
  }}

  @media (max-width: 520px) {{
    .graficos-grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<header>
  <h1>📊 Relatório de Vendas</h1>
  <p class="subtitulo">Gerado em {data_geracao}</p>
</header>

<main>
  <p class="secao-titulo">Principais Indicadores</p>
  <div class="cards-grid">
{cards_html}
  </div>

  <p class="secao-titulo">Visualizações</p>
  <div class="graficos-grid">
{graficos_html}
  </div>
</main>

<footer>
  Relatório gerado automaticamente em {data_geracao} &bull; Dados: dados/vendas_limpo.csv
</footer>

</body>
</html>
"""

# ── 4. Salvar arquivo ─────────────────────────────────────────────────────────
caminho_relatorio = Path("reports/relatorio_vendas.html")
caminho_relatorio.write_text(html, encoding="utf-8")

tamanho_kb = caminho_relatorio.stat().st_size / 1024
print(f"Relatório gerado com sucesso!")
print(f"  Caminho : {caminho_relatorio.resolve()}")
print(f"  Tamanho : {tamanho_kb:.1f} KB")
