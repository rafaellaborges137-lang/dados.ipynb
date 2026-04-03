# -*- coding: utf-8 -*-
"""netflix.ipynb


Original file is located at
    https://colab.research.google.com/drive/1nEgL2sf4jDCj2bcjx3LzMeIkCJrqpwkU
"""

import pandas as pd
import os

# O dataset foi baixado para o caminho contido na variável `path`
# Assumindo que o arquivo CSV principal é 'netflix_titles.csv' dentro desse diretório.

data_file_path = os.path.join(path, 'netflix_titles.csv')

df_netflix = pd.read_csv(data_file_path)


display(df_netflix.head())

# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter


file_path = "netflix_titles.csv"

# Load the latest version
df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "shivamb/netflix-shows",
  file_path,
  # Provide any additional arguments like
  # sql_query or pandas_kwargs. See the
  # documenation for more information:
  # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
)

print("First 5 records:", df.head())

import matplotlib.pyplot as plt
import seaborn as sns


content_type_counts = df_netflix['type'].value_counts().reset_index()
content_type_counts.columns = ['Content Type', 'Count']


plt.figure(figsize=(8, 6))
sns.barplot(x='Content Type', y='Count', data=content_type_counts, palette='viridis', hue='Content Type', legend=False)
plt.title('Distribuição de Filmes vs. Séries de TV na Netflix')
plt.xlabel('Tipo de Conteúdo')
plt.ylabel('Quantidade')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()



print('Informações do DataFrame df_netflix:')
df_netflix.info()

print('\nContagem de valores ausentes por coluna:')
display(df_netflix.isnull().sum())

productions_per_year = df_netflix.groupby('release_year').size().reset_index(name='count')
display(productions_per_year.sort_values(by='release_year', ascending=False).head())

"""### Gráfico Interativo: Produções por Ano e Distribuição de Tipo de Conteúdo



import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Gráfico de Linha Interativo para Produções por Ano
fig_year = px.line(productions_per_year, x='release_year', y='count', title='Número de Produções Lançadas por Ano na Netflix')
fig_year.update_traces(mode='lines+markers')
fig_year.show()

# 2. Gráfico de Barras Interativo para Distribuição de Tipo de Conteúdo
fig_type = px.bar(content_type_counts, x='Content Type', y='Count', title='Distribuição de Filmes vs. Séries de TV na Netflix', color='Content Type')
fig_type.show()



import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Criar subplots: 1 linha, 3 colunas
fig_combined = make_subplots(
    rows=1, cols=3,
    subplot_titles=(
        'Número de Produções Lançadas por Ano na Netflix',
        'Distribuição de Filmes vs. Séries de TV na Netflix',
        'Distribuição da Duração dos Filmes na Netflix'
    )
)


fig_combined.add_trace(
    go.Scatter(x=productions_per_year['release_year'], y=productions_per_year['count'], mode='lines+markers', name='Produções por Ano', marker_color='blue'),
    row=1, col=1
)


movie_count = content_type_counts[content_type_counts['Content Type'] == 'Movie']['Count'].iloc[0]
tv_show_count = content_type_counts[content_type_counts['Content Type'] == 'TV Show']['Count'].iloc[0]

fig_combined.add_trace(
    go.Bar(x=['Filme'], y=[movie_count], name='Filme', marker_color='purple'),
    row=1, col=2
)
fig_combined.add_trace(
    go.Bar(x=['Série de TV'], y=[tv_show_count], name='Série de TV', marker_color='green'),
    row=1, col=2
)


fig_combined.add_trace(
    go.Histogram(x=df_movies['duration_minutes'], nbinsx=30, name='Duração de Filmes', marker_color='orange'),
    row=1, col=3
)


fig_combined.update_layout(
    title_text='Dashboard Netflix: Tendências de Lançamento, Distribuição de Conteúdo e Duração de Filmes',
    height=450, # Ajuste a altura para melhor visualização dos 3 gráficos
    showlegend=True # Mostra a legenda combinada para todos os gráficos
)


fig_combined.update_xaxes(title_text='Ano de Lançamento', row=1, col=1)
fig_combined.update_yaxes(title_text='Número de Produções', row=1, col=1)

fig_combined.update_xaxes(title_text='Tipo de Conteúdo', row=1, col=2)
fig_combined.update_yaxes(title_text='Quantidade', row=1, col=2)

fig_combined.update_xaxes(title_text='Duração (minutos)', row=1, col=3)
fig_combined.update_yaxes(title_text='Número de Filmes', row=1, col=3)

fig_combined.show()


import plotly.express as px


fig_duration_hist = px.histogram(df_movies, x='duration_minutes',
                                 nbins=30, # Número de "barras" no histograma
                                 title='Distribuição da Duração dos Filmes na Netflix',
                                 labels={'duration_minutes': 'Duração (minutos)', 'count': 'Número de Filmes'})

fig_duration_hist.update_layout(xaxis_title='Duração (minutos)', yaxis_title='Número de Filmes')
fig_duration_hist.show()



# Filtrar o DataFrame para apenas filmes
df_movies = df_netflix[df_netflix['type'] == 'Movie'].copy()

# Remover linhas com valores ausentes na coluna 'duration' antes de processar
df_movies = df_movies.dropna(subset=['duration'])

# Remover ' min' da coluna 'duration' e converter para numérico
df_movies['duration_minutes'] = df_movies['duration'].str.replace(' min', '').astype(int)

# Calcular a duração média dos filmes
average_movie_duration = df_movies['duration_minutes'].mean()

print(f"A duração média dos filmes na Netflix é de: {average_movie_duration:.2f} minutos.")


import kagglehub
path = kagglehub.dataset_download("shivamb/netflix-shows")
