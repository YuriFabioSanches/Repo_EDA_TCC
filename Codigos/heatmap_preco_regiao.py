import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Caminho do arquivo CSV consolidado
data_path = r'C:\Users\yuriu\Desktop\TCC\Data\dataset_combustiveis_automotivos_2004_2024.csv'

# Carrega os dados
df = pd.read_csv(data_path, parse_dates=['DATA DA COLETA'], dayfirst=True)

# Filtra apenas gasolina e colunas necessárias
df['PRODUTO'] = df['PRODUTO'].str.upper()
df_gas = df[df['PRODUTO'] == 'GASOLINA']

# Agrupa por ANO e REGIÃO, calculando a média
media_regiao_ano = df_gas.groupby(['ANO', 'REGIAO - SIGLA'])['VALOR DE VENDA'].mean().reset_index()

# Pivota a tabela: regiões como linhas, anos como colunas
heatmap_data = media_regiao_ano.pivot(index='REGIAO - SIGLA', columns='ANO', values='VALOR DE VENDA')

# Reorganiza as regiões na ordem tradicional
ordem_regioes = ['N', 'NE', 'CO', 'SE', 'S']
heatmap_data = heatmap_data.reindex(ordem_regioes)

# Gera o heatmap
plt.figure(figsize=(16, 5))
sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="YlOrRd", linewidths=0.5, cbar_kws={'label': 'Preço Médio (R$)'})
plt.title('Mapa de Calor: Preço Médio da Gasolina por Região e Ano (2004–2024)', fontsize=14)
plt.xlabel('Ano')
plt.ylabel('Região')
plt.yticks(rotation=0)
plt.tight_layout()

# Salva o gráfico
plt.savefig(r'C:\Users\yuriu\Desktop\TCC\src\Graficos\grafico_heatmap_gasolina_regiao_ano.png', dpi=300)
plt.show()