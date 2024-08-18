import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import pydeck as pdk
import altair as alt
from geopy.geocoders import Nominatim
import time



st.title("TP2 - Desenvolvimento Front-End com Python")

df_1 = pd.read_csv('https://api.onedrive.com/v1.0/shares/s!Asuw4D2AHTOZmZ1Y4DEo06n0wxvurw/root/content', sep=';')
df_2 = pd.read_csv('https://api.onedrive.com/v1.0/shares/s!Asuw4D2AHTOZmZ1JcL7FojJ8B7yRKA/root/content', sep=';')
df = pd.concat([df_1, df_2])

st.subheader("1 - Importância da Visualização de Dados:",divider=True)

#Explique a importância da visualização de dados no contexto de uma pandemia como a COVID-19. 
# Como essas visualizações podem ajudar gestores de saúde pública e a população em geral a 
# tomar decisões informadas?

st.subheader("2 - Gráfico de Barras com Streamlit:",divider=True)

#Usando os dados de casos novos de COVID-19 por semana epidemiológica de notificação, crie um gráfico
# de barras em Streamlit que mostre a evolução semanal dos casos em um determinado estado. 
# Indique o estado escolhido e explique sua escolha.


estados = df['estado'].unique()
estados = estados[~pd.isnull(estados)]
estado = st.selectbox('Selecione um estado', estados)

df_estado = df[df['estado'] == estado]

#Tem dados de casos novos negativos, seria uma correção de falsos positivos das semanas anteriores?
df_agg = df_estado.groupby('semanaEpi').agg({'casosNovos':'sum'}).reset_index()

st.bar_chart(df_agg, x = 'semanaEpi', y = 'casosNovos', stack = False)



st.subheader("3 - Gráfico de Linha com Streamlit:",divider=True)

#Crie um gráfico de linha utilizando Streamlit para representar o número de óbitos acumulados
# por COVID-19 ao longo das semanas epidemiológicas de notificação para todo o Brasil. 
# Explique como a curva de óbitos acumulados pode ser interpretada.

df_agg = df_estado.groupby('semanaEpi').agg({'obitosAcumulado':'sum'}).reset_index()

st.line_chart(df_agg, x = 'semanaEpi', y = 'obitosAcumulado')

st.markdown('''**R.:** A curva de óbitos acumulados pode ser interpretada como a quantidade total 
de mortes por COVID-19 ao longo do tempo. A inclinação da curva indica a velocidade de propagação 
do vírus e a eficácia das medidas de controle adotadas. Uma curva mais íngreme sugere um aumento 
rápido no número de óbitos, enquanto uma curva mais plana indica uma desaceleração na taxa de 
mortalidade.''')



st.subheader("4 - Gráfico de Área com Streamlit:",divider=True)

#Utilizando os dados de casos acumulados por COVID-19, crie um gráfico de área em Streamlit 
# para comparar a evolução dos casos em três estados diferentes. 
# Explique as diferenças observadas entre os estados escolhidos.

columns = st.columns([0.33,0.33,0.33])

with columns[0]:
    estado1 = st.selectbox('Selecione o primeiro estado', estados)
    df_estado1 = df[df['estado'] == estado1]
    df_agg1 = df_estado1.groupby('semanaEpi').agg({'casosAcumulado':'sum'}).reset_index()
    st.area_chart(df_agg1, x = 'semanaEpi', y = 'casosAcumulado')

with columns[1]:
    estado2 = st.selectbox('Selecione o segundo estado', estados)
    df_estado2 = df[df['estado'] == estado2]
    df_agg2 = df_estado2.groupby('semanaEpi').agg({'casosAcumulado':'sum'}).reset_index()
    st.area_chart(df_agg2, x = 'semanaEpi', y = 'casosAcumulado')

with columns[2]:
    estado3 = st.selectbox('Selecione o terceiro estado', estados)
    df_estado3 = df[df['estado'] == estado3]
    df_agg3 = df_estado3.groupby('semanaEpi').agg({'casosAcumulado':'sum'}).reset_index()
    st.area_chart(df_agg3, x = 'semanaEpi', y = 'casosAcumulado')

st.markdown('''**R.:** As diferenças observadas entre os estados escolhidos podem refletir
as diferentes fases da pandemia em cada região. Um estado com uma curva mais acentuada pode
estar enfrentando um surto de casos, enquanto um estado com uma curva mais plana pode ter
controlado a disseminação do vírus.''')



st.subheader("5 - Mapa com Streamlit:",divider=True)

#Crie um mapa interativo utilizando a função st.map do Streamlit que mostre a distribuição
#  dos casos acumulados de COVID-19 por município em um estado específico. 
# Explique como esse tipo de visualização pode ajudar na análise geográfica da pandemia.

estado_mapa = st.selectbox('Selecione um estado para ver os casos acumulados dos municípios', estados)

df_estado_mapa = df[df['estado'] == estado_mapa]

df_mapa = df_estado_mapa.groupby(['municipio']).agg({'casosAcumulado':'sum'}).reset_index()

#df_mapa['casosAcumulado'] = np.log1p(df_mapa['casosAcumulado'])
df_mapa['casosAcumulado'] = df_mapa['casosAcumulado'] / 10000

geolocator = Nominatim(user_agent="municipality_locator")

progress_bar = st.progress(0)
status_text = st.empty()

for i in df_mapa.index:
    location = geolocator.geocode(df_mapa.loc[i,'municipio'] + ', ' + estado_mapa)
    df_mapa.loc[i,'latitude'] = location.latitude
    df_mapa.loc[i,'longitude'] = location.longitude

    progress_bar.progress((i + 1) / len(df_mapa))
    status_text.text(f"Consultando coordenadas: {df_mapa.loc[i,'municipio']}")
    time.sleep(0.15)

st.map(df_mapa, latitude = 'latitude', longitude = 'longitude', size = 'casosAcumulado')

progress_bar.empty()
status_text.text("Consultas concluídas!")

st.markdown('''**R.:** Esse tipo de visualização pode ajudar na análise geográfica da pandemia ao
permitir a identificação de áreas com maior incidência de casos.''')

#---------------------------------------------------------------------------------------------

st.subheader("6 - Visualização com Matplotlib:",divider=True)

#Utilize a biblioteca Matplotlib para criar um gráfico de barras que mostre a comparação 
# entre os casos novos e os óbitos novos de COVID-19 por estado na semana epidemiológica 
# mais recente disponível. Explique o que os dados sugerem sobre a relação entre casos e óbitos.



st.subheader("7 - Boxplot com Seaborn:",divider=True)

#Usando a biblioteca Seaborn, crie um boxplot que compare a distribuição dos casos novos de 
# COVID-19 por semana epidemiológica entre três regiões do Brasil (Norte, Nordeste, Sudeste). 
# Explique as principais diferenças observadas.



st.subheader("8 - Gráfico de Área com Altair:",divider=True)

#Crie um gráfico de área em Altair para mostrar a evolução dos casos novos de COVID-19 por 
# semana epidemiológica de notificação em uma determinada região do Brasil. 
# Explique a escolha da região e as tendências observadas nos dados.



st.subheader("9 - Heatmap com Altair:",divider=True)

#Desenvolva um heatmap em Altair que mostre a correlação entre casos novos, óbitos novos e 
# leitos hospitalares ocupados (caso os dados estejam disponíveis) em um determinado estado. 
# Explique as possíveis correlações observadas.



st.subheader("10 - Gráfico de Pizza com Plotly:",divider=True)

#Usando Plotly, crie um gráfico de pizza (pie chart) que mostre a distribuição percentual dos 
# casos acumulados de COVID-19 entre as cinco regiões do Brasil. 
# Explique o que os dados revelam sobre a distribuição geográfica dos casos.



st.subheader("11 - Subplots com Plotly:",divider=True)

#Crie subplots em Plotly que mostrem, lado a lado, gráficos de barras comparando os casos novos 
# e os óbitos novos de COVID-19 por semana epidemiológica em duas diferentes regiões do Brasil. 
# Explique as diferenças observadas entre as regiões.



st.subheader("12 - Mapa Interativo com PyDeck:",divider=True)

#Utilize PyDeck para criar um mapa interativo que mostre a densidade populacional ajustada para 
# os casos acumulados de COVID-19 por município em uma determinada região do Brasil. 
# Explique como a densidade populacional pode influenciar a disseminação da COVID-19.

