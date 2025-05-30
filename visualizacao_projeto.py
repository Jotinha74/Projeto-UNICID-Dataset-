# Importando as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify # Importa a biblioteca para Treemap

# Configurando o estilo dos gráficos (opcional, mas deixa mais bonito)
sns.set_theme(style="whitegrid")

# --- Carregar o dataset ---
# Certifique-se de que o arquivo 'USD_BRL_hist (1).csv' esteja na mesma pasta do seu script/notebook.
file_path = 'USD_BRL_hist (1).csv'

try:
    df = pd.read_csv(file_path)
    print(f"Dataset '{file_path}' carregado com sucesso!")
    print("\nPrimeiras 5 linhas do DataFrame:")
    print(df.head())
    print("\nInformações iniciais do DataFrame:")
    df.info()
except FileNotFoundError:
    print(f"ERRO: O arquivo '{file_path}' não foi encontrado. Verifique o caminho.")
    exit() # Para parar a execução se o arquivo não for encontrado

# --- Pré-processamento dos dados ---
# Converter a coluna 'Data' para o tipo datetime
# O formato original é 'DD.MM.YYYY', então especificamos isso.
df['Data'] = pd.to_datetime(df['Data'], format='%d.%m.%Y')

# Ordenar o DataFrame pela coluna 'Data' para garantir a ordem cronológica
df = df.sort_values(by='Data').reset_index(drop=True)

print("\nDataFrame após conversão de data e ordenação:")
print(df.head())
print("\nInformações do DataFrame após pré-processamento:")
df.info()

# --- Verificar os tipos de dados e valores nulos (boa prática) ---
print("\nVerificação de valores nulos:")
print(df.isnull().sum())

# --- Resumo estatístico da coluna USD_BRL ---
print("\nEstatísticas descritivas para USD_BRL:")
print(df['USD_BRL'].describe())

# Agora o DataFrame 'df' está pronto para a visualização!
# As colunas são 'Data' (como datetime) e 'USD_BRL' (como float).

# --- Gráfico 1: Visualização da Informação Temporal (Gráfico de Linhas) ---
# Unidade: Visualização da Informação Temporal

plt.figure(figsize=(15, 7)) # Define o tamanho da figura para melhor visualização
sns.lineplot(data=df, x='Data', y='USD_BRL') # Cria o gráfico de linhas
plt.title('Variação da Cotação USD/BRL ao Longo do Tempo (2010-2019)') # Título do gráfico
plt.xlabel('Data') # Rótulo do eixo X
plt.ylabel('Cotação USD/BRL') # Rótulo do eixo Y
plt.grid(True) # Adiciona uma grade ao gráfico
plt.tight_layout() # Ajusta o layout para evitar sobreposição
# plt.show() # COMENTE ESTA LINHA PARA MOSTRAR TODOS OS GRÁFICOS NO FINAL

print("\n--- Gráfico 1 gerado: Gráfico de Linhas da cotação USD/BRL ---")

# --- Gráfico 2: Visualização para Informação Estatística Descritiva (Histograma) ---
# Unidade: Visualização para Informação Estatística Descritiva

plt.figure(figsize=(10, 6)) # Define o tamanho da figura
sns.histplot(df['USD_BRL'], bins=30, kde=True) # Cria o histograma com 30 barras e estimativa de densidade
plt.title('Distribuição da Cotação USD/BRL') # Título do gráfico
plt.xlabel('Cotação USD/BRL') # Rótulo do eixo X
plt.ylabel('Frequência') # Rótulo do eixo Y
plt.tight_layout()
# plt.show() # COMENTE ESTA LINHA PARA MOSTRAR TODOS OS GRÁFICOS NO FINAL

print("\n--- Gráfico 2 gerado: Histograma da cotação USD/BRL ---")

# --- Gráfico 3: Visualização de Informação Hierárquica (Treemap) ---
# Unidade: Visualização de Informação Hierárquica

# Criar uma hierarquia temporal: Ano e Mês
df['Ano'] = df['Data'].dt.year
df['Mes'] = df['Data'].dt.month

# Calcular a média da cotação por Ano e Mês
df_grouped = df.groupby(['Ano', 'Mes'])['USD_BRL'].mean().reset_index()

# **CONSERTO DO ERRO APRIMORADO:**
# Vamos garantir que 'Mes' seja int antes de gerar os labels.
# Se ainda assim der erro, converter diretamente na f-string.
df_grouped['Mes'] = df_grouped['Mes'].astype(int)

# Para o Treemap, precisamos de um 'tamanho' para cada célula. Usaremos a média da cotação.
# A cor pode ser baseada no ano ou na própria cotação.
sizes = df_grouped['USD_BRL'].values
# O problema está no formatador ':02d' aplicado a um float.
# Embora tenhamos feito o astype(int), vamos garantir que o valor seja int na f-string.
labels = [f'{row.Ano}-{(int(row.Mes)):02d}\nMédia: {row.USD_BRL:.2f}' for index, row in df_grouped.iterrows()]

plt.figure(figsize=(18, 10))
# Cores: podemos usar um colormap ou definir uma lista.
# Para uma melhor visualização, é bom que as cores representem alguma escala.
# Aqui, vamos usar um colormap baseado na cotação para o Treemap
# A normalização é para mapear os valores da cotação para o intervalo de cores
norm = plt.Normalize(df_grouped['USD_BRL'].min(), df_grouped['USD_BRL'].max())
colors = [plt.cm.viridis(norm(value)) for value in df_grouped['USD_BRL']] # Exemplo usando colormap viridis

squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.8)
plt.title('Cotação Média USD/BRL por Ano e Mês (Treemap)')
plt.axis('off') # Remove os eixos
# plt.show() # COMENTE ESTA LINHA PARA MOSTRAR TODOS OS GRÁFICOS NO FINAL

print("\n--- Gráfico 3 gerado: Treemap da cotação média USD/BRL por Ano e Mês ---")

# Mostra todos os gráficos que foram gerados e não exibidos individualmente
plt.show()