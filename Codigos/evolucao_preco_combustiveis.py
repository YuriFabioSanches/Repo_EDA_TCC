import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Caminho do dataset
data_path = r'C:\Users\yuriu\Desktop\TCC\Data\dataset_combustiveis_automotivos_2004_2024.csv'

# Carrega o dataset com datas
df = pd.read_csv(data_path, parse_dates=['DATA DA COLETA'], dayfirst=True)

# Normaliza combustíveis de interesse
combustiveis = ['GASOLINA', 'ETANOL', 'DIESEL', 'DIESEL S10']
df['PRODUTO'] = df['PRODUTO'].str.upper()
df = df[df['PRODUTO'].isin(combustiveis)]

# Cria coluna ANO_MES como primeiro dia de cada mês
df['ANO_MES'] = pd.to_datetime(dict(year=df['ANO'], month=df['MES'], day=1))

# Agrupa por mês e produto
media_mensal = df.groupby(['ANO_MES', 'PRODUTO'])['VALOR DE VENDA'].mean().reset_index()

# Descobre o período real dos dados
data_inicio = df['ANO_MES'].min().strftime('%b/%Y')
data_fim = df['ANO_MES'].max().strftime('%b/%Y')

# Gera o gráfico
plt.figure(figsize=(14, 6))
for produto in combustiveis:
    dados = media_mensal[media_mensal['PRODUTO'] == produto]
    plt.plot(dados['ANO_MES'], dados['VALOR DE VENDA'], label=produto)

# Títulos e eixos
plt.title(f'Evolução dos Preços Médios Mensais dos Combustíveis no Brasil ({data_inicio} – {data_fim})', fontsize=14)
plt.xlabel('Ano')
plt.ylabel('Preço Médio (R$)')
plt.grid(True)
plt.legend(title='Combustível')

# Define ticks de ano a ano
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator(1))  # Ticks anuais
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Mostra só o ano
plt.xticks(rotation=45)

# Layout e salvamento
plt.tight_layout()
plt.savefig(r'C:\Users\yuriu\Desktop\TCC\src\Graficos\grafico_evolucao_precos_combustiveis.png', dpi=300)
plt.show()