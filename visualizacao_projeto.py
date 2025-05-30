# Importando bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify

# Configuração visual dos gráficos
sns.set_theme(style="whitegrid")

# --- Carregamento e Preparação do Dataset ---
file_path = 'USD_BRL_hist (1).csv' # Caminho do arquivo de dados

try:
    df = pd.read_csv(file_path)
    print(f"Dataset '{file_path}' carregado.")
    print("Primeiras linhas:")
    print(df.head())
    print("Informações iniciais:")
    df.info()
except FileNotFoundError:
    print(f"ERRO: Arquivo '{file_path}' não encontrado.")
    exit()

# Conversão da coluna de data e ordenação
df['Data'] = pd.to_datetime(df['Data'], format='%d.%m.%Y')
df = df.sort_values(by='Data').reset_index(drop=True)

print("DataFrame após pré-processamento:")
print(df.head())
print("Novas informações do DataFrame:")
df.info()

# Verificação de valores ausentes
print("Valores nulos por coluna:")
print(df.isnull().sum())

# Resumo estatístico
print("Estatísticas para USD_BRL:")
print(df['USD_BRL'].describe())

# --- Geração dos Gráficos ---

# Gráfico 1: Variação Temporal (Gráfico de Linhas)
plt.figure(figsize=(15, 7))
sns.lineplot(data=df, x='Data', y='USD_BRL')
plt.title('Variação da Cotação USD/BRL (2010-2019)')
plt.xlabel('Data')
plt.ylabel('Cotação USD/BRL')
plt.grid(True)
plt.tight_layout()
# plt.show() # Descomente para mostrar individualmente

print("\n--- Gráfico 1: Linhas de Cotação USD/BRL gerado ---")

# Gráfico 2: Distribuição Estatística (Histograma)
plt.figure(figsize=(10, 6))
sns.histplot(df['USD_BRL'], bins=30, kde=True)
plt.title('Distribuição da Cotação USD/BRL')
plt.xlabel('Cotação USD/BRL')
plt.ylabel('Frequência')
plt.tight_layout()
# plt.show() # Descomente para mostrar individualmente

print("\n--- Gráfico 2: Histograma da Cotação USD/BRL gerado ---")

# Gráfico 3: Análise Hierárquica (Treemap)
df['Ano'] = df['Data'].dt.year
df['Mes'] = df['Data'].dt.month

df_grouped = df.groupby(['Ano', 'Mes'])['USD_BRL'].mean().reset_index()
df_grouped['Mes'] = df_grouped['Mes'].astype(int) # Garante tipo inteiro para o mês

sizes = df_grouped['USD_BRL'].values
labels = [f'{row.Ano}-{(int(row.Mes)):02d}\nMédia: {row.USD_BRL:.2f}' for index, row in df_grouped.iterrows()]

plt.figure(figsize=(18, 10))
norm = plt.Normalize(df_grouped['USD_BRL'].min(), df_grouped['USD_BRL'].max())
colors = [plt.cm.viridis(norm(value)) for value in df_grouped['USD_BRL']]

squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.8)
plt.title('Cotação Média USD/BRL por Ano e Mês (Treemap)')
plt.axis('off')
# plt.show() # Descomente para mostrar individualmente

print("\n--- Gráfico 3: Treemap da Cotação Média USD/BRL gerado ---")

# Exibe todos os gráficos gerados
plt.show()