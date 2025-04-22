import pandas as pd
import matplotlib.pyplot as plt

# Carrega dataset
data_path = r'C:\Users\yuriu\Desktop\TCC\Data\dataset_combustiveis_automotivos_2004_2024.csv'
df = pd.read_csv(data_path, parse_dates=['DATA DA COLETA'], dayfirst=True)

# Filtra apenas os combustíveis desejados
combustiveis = ['GASOLINA', 'ETANOL', 'DIESEL', 'DIESEL S10']
df['PRODUTO'] = df['PRODUTO'].str.upper()
df = df[df['PRODUTO'].isin(combustiveis)]

# Agrupa por ano e produto
media_anual = df.groupby(['ANO', 'PRODUTO'])['VALOR DE VENDA'].mean().reset_index()

# Calcula variação percentual ano a ano por combustível
media_anual['VAR_PERC'] = media_anual.groupby('PRODUTO')['VALOR DE VENDA'].pct_change() * 100

# Pivota para facilitar o gráfico
tabela = media_anual.pivot(index='ANO', columns='PRODUTO', values='VAR_PERC')

# Garante que todos os anos apareçam (2005–2024)
anos = list(range(2005, 2025))
tabela = tabela.reindex(anos)

# Cores padronizadas
cores = {
    'GASOLINA': '#1f77b4',     # azul
    'ETANOL': '#ff7f0e',       # laranja
    'DIESEL': '#2ca02c',       # verde
    'DIESEL S10': '#d62728'    # vermelho
}

# Gera gráfico
plt.figure(figsize=(14, 6))

for combustivel in combustiveis:
    plt.plot(tabela.index, tabela[combustivel], marker='o', label=combustivel, color=cores[combustivel])

# Estilo do gráfico
plt.title('Variação Percentual Anual dos Preços Médios dos Combustíveis no Brasil (2005–2024)', fontsize=14)
plt.xlabel('Ano')
plt.ylabel('Variação (%) em relação ao ano anterior')
plt.xticks(ticks=anos, rotation=45)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Combustível')
plt.tight_layout()

# Salva imagem
plt.savefig(r'C:\Users\yuriu\Desktop\TCC\src\Graficos\grafico_variacao_percentual.png', dpi=300)
plt.show()