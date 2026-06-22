# analise_vendas

Projeto de análise de dados de vendas fictícias. Objetivo principal: aprender a trabalhar com dados reais e bagunçados (valores nulos, tipos errados, duplicatas, datas inconsistentes).

## Desenvolvedor

Estudante de Data Science no primeiro semestre, iniciante em Python. Mac com VS Code.

## Ambiente

- Python 3.9 via `.venv` local
- Ativar antes de rodar qualquer script: `source .venv/bin/activate`
- Instalar pacotes: `pip install <pacote>` (com venv ativado)

## Estrutura esperada do projeto

```
analise_vendas/
├── dados/          # CSVs brutos (nunca editar manualmente)
├── notebooks/      # Jupyter Notebooks de exploração
├── scripts/        # Scripts Python de limpeza e análise
├── outputs/        # Gráficos e tabelas geradas
└── CLAUDE.md
```

## Como trabalhar aqui

- Preferir Jupyter Notebooks para exploração e aprendizado — é mais fácil ver o resultado célula por célula.
- Scripts `.py` para etapas que já estão prontas e precisam ser repetidas.
- Nunca sobrescrever os dados brutos em `dados/` — sempre salvar versões limpas com nome diferente (ex: `vendas_limpo.csv`).

## Bibliotecas usadas

| Biblioteca | Para quê |
|---|---|
| pandas | Carregar, limpar e manipular os dados |
| matplotlib / seaborn | Gráficos |
| jupyter | Notebooks interativos |
| streamlit | Dashboard interativo web |

Instalar tudo de uma vez:
```bash
pip install pandas matplotlib seaborn jupyter streamlit
```

Para rodar o dashboard:
```bash
streamlit run scripts/dashboard.py
```

## Padrões de código

- Manter o código simples e legível — prioridade é aprender, não otimizar.
- Nomear variáveis em português para facilitar o entendimento (ex: `df_vendas`, `total_por_mes`).
- Adicionar comentários explicando o raciocínio quando a operação não for óbvia.
- Usar `df.head()` e `df.info()` logo após carregar qualquer CSV para verificar o que veio.

## Problemas comuns neste projeto

Os dados são intencionalmente bagunçados. Espere encontrar:
- Datas em formatos diferentes (DD/MM/YYYY, MM-DD-YY, texto)
- Valores numéricos com vírgula como separador decimal
- Colunas com nomes inconsistentes (espaços, maiúsculas/minúsculas)
- Linhas duplicadas
- Valores nulos em colunas críticas
