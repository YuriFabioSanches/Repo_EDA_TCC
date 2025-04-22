import pandas as pd
import os

# Caminho onde estão os arquivos CSV
data_path = r'C:\Users\yuriu\Desktop\TCC\Data'
files = sorted([f for f in os.listdir(data_path) if f.lower().endswith('.csv')])

dfs = []
total_linhas_arquivos = 0
total_linhas_antes_limpeza = 0

print("🔍 Lendo arquivos...")

for file in files:
    file_path = os.path.join(data_path, file)
    df = None

    try:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig', low_memory=False)
    except Exception as e_utf8:
        try:
            df = pd.read_csv(file_path, sep=';', encoding='latin1', low_memory=False)
            print(f"⚠️ {file} lido com 'latin1' por falha com utf-8-sig.")
        except Exception as e_latin1:
            print(f"❌ Erro ao ler {file} com ambas codificações: {e_latin1}")
            continue

    num_linhas = len(df)
    total_linhas_arquivos += num_linhas
    print(f"✅ {file}: {num_linhas} linhas")
    df['ARQUIVO_ORIGEM'] = file
    dfs.append(df)

# Junta os DataFrames
df_geral = pd.concat(dfs, ignore_index=True)
total_linhas_antes_limpeza = len(df_geral)

# Padroniza nomes de colunas
df_geral.columns = [col.strip().upper() for col in df_geral.columns]

print("\n📋 Colunas disponíveis:")
print(df_geral.columns.tolist())

# Remove colunas completamente vazias
df_geral.dropna(axis=1, how='all', inplace=True)

# Mantém apenas linhas com VALOR DE VENDA
df_geral.dropna(subset=['VALOR DE VENDA'], inplace=True)

# Converte VALOR DE VENDA para float
def para_float(valor):
    try:
        return float(str(valor).replace(',', '.'))
    except:
        return None

df_geral['VALOR DE VENDA'] = df_geral['VALOR DE VENDA'].apply(para_float)

# Converte DATA DA COLETA para datetime
if 'DATA DA COLETA' in df_geral.columns:
    df_geral['DATA DA COLETA'] = pd.to_datetime(df_geral['DATA DA COLETA'], dayfirst=True, errors='coerce')

# Seleciona colunas finais para análise
colunas_desejadas = [
    'REGIAO - SIGLA',
    'ESTADO - SIGLA',
    'PRODUTO',
    'MUNICIPIO',
    'DATA DA COLETA',
    'VALOR DE VENDA',
    'UNIDADE DE MEDIDA'
]

df_final = df_geral[[col for col in colunas_desejadas if col in df_geral.columns]].copy()

# Relatório de valores nulos antes da limpeza final
nulos_por_coluna = df_final.isnull().sum()
total_linhas_antes_limpeza_final = len(df_final)

# Remove linhas com valores ausentes nas colunas finais
df_final.dropna(subset=colunas_desejadas, inplace=True)
linhas_removidas_final = total_linhas_antes_limpeza_final - len(df_final)

# Remove duplicatas completas
linhas_antes_deduplicacao = len(df_final)
df_final.drop_duplicates(inplace=True)
linhas_removidas_duplicadas = linhas_antes_deduplicacao - len(df_final)

# Cria colunas auxiliares para facilitar análises
df_final['ANO'] = df_final['DATA DA COLETA'].dt.year
df_final['MES'] = df_final['DATA DA COLETA'].dt.month

# Salva dataset final com datas no formato dd/mm/yyyy
output_path = os.path.join(data_path, 'dataset_combustiveis_automotivos_2004_2024.csv')
df_final.to_csv(output_path, index=False, encoding='utf-8-sig', date_format='%d/%m/%Y')

# Relatório final
print("\n📊 RESULTADO FINAL")
print(f"📁 Total de arquivos lidos: {len(files)}")
print(f"📄 Total de linhas originais (somadas dos arquivos): {total_linhas_arquivos}")
print(f"📦 Total de linhas no DataFrame unificado antes da limpeza: {total_linhas_antes_limpeza}")
print(f"🧹 Total de linhas após limpeza básica (VALOR DE VENDA): {len(df_geral)}")
print(f"🔽 Total de linhas antes da limpeza final com colunas selecionadas: {total_linhas_antes_limpeza_final}")
print(f"🚮 Linhas removidas por dados ausentes nas colunas finais: {linhas_removidas_final}")
print(f"♻️ Linhas removidas por duplicação total: {linhas_removidas_duplicadas}")
print(f"✅ Total final de linhas no dataset pronto: {len(df_final)}")
print(f"📁 Dataset final salvo em: {output_path}")
print("\n🔍 Quantidade de valores nulos por coluna antes da limpeza final:")
print(nulos_por_coluna)
