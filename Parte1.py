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

@st.cache_data
def load_data():
    df_1 = pd.read_csv('https://api.onedrive.com/v1.0/shares/s!Asuw4D2AHTOZmZ1Y4DEo06n0wxvurw/root/content', sep=';')
    df_2 = pd.read_csv('https://api.onedrive.com/v1.0/shares/s!Asuw4D2AHTOZmZ1JcL7FojJ8B7yRKA/root/content', sep=';')
    df = pd.concat([df_1, df_2])

    df_coords = pd.read_csv('https://api.onedrive.com/v1.0/shares/s!Asuw4D2AHTOZnZ4Q5eHwZsinnTk5BQ/root/content', sep=',')

    df = df[df['regiao'] != 'Brasil']
    df = df[df['municipio'].notna()]

    df_coords.drop_duplicates(subset=['regiao', 'municipio'],inplace=True)
    df_coords['chave'] = df_coords['regiao'] + '_' + df_coords['municipio']

    df['chave'] = df['regiao'] + '_' + df['municipio']


    df['latitude'] = df['chave'].map(df_coords.set_index('chave')['latitude'])
    df['longitude'] = df['chave'].map(df_coords.set_index('chave')['longitude'])

    df.drop(columns=['chave'], inplace=True)

    return df

df = load_data()

st.dataframe(df.sample(5))

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
estado = st.selectbox('Selecione um estado', estados, key = 'estado_questao2')

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
    estado1 = st.selectbox('Selecione o primeiro estado', estados, key = 'estado1_questao4')
    df_estado1 = df[df['estado'] == estado1]
    df_agg1 = df_estado1.groupby('semanaEpi').agg({'casosAcumulado':'sum'}).reset_index()
    st.area_chart(df_agg1, x = 'semanaEpi', y = 'casosAcumulado')

with columns[1]:
    estado2 = st.selectbox('Selecione o segundo estado', estados, key = 'estado2_questao4')
    df_estado2 = df[df['estado'] == estado2]
    df_agg2 = df_estado2.groupby('semanaEpi').agg({'casosAcumulado':'sum'}).reset_index()
    st.area_chart(df_agg2, x = 'semanaEpi', y = 'casosAcumulado')

with columns[2]:
    estado3 = st.selectbox('Selecione o terceiro estado', estados, key = 'estado3_questao4')
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

estado_mapa = st.selectbox('Selecione um estado para ver os casos acumulados dos municípios', estados, key = 'estado_questao5')

df_estado_mapa = df[df['estado'] == estado_mapa]

df_mapa = df_estado_mapa.groupby(['municipio','latitude','longitude']).agg({'casosAcumulado':'sum'}).reset_index()

#df_mapa['casosAcumulado'] = np.log1p(df_mapa['casosAcumulado'])
df_mapa['casosAcumulado'] = df_mapa['casosAcumulado'] / 10000

st.map(df_mapa, latitude = 'latitude', longitude = 'longitude', size = 'casosAcumulado')


st.markdown('''**R.:** Esse tipo de visualização pode ajudar na análise geográfica da pandemia ao
permitir a identificação de áreas com maior incidência de casos.''')

#---------------------------------------------------------------------------------------------

st.subheader("6 - Visualização com Matplotlib:",divider=True)

#Utilize a biblioteca Matplotlib para criar um gráfico de barras que mostre a comparação 
# entre os casos novos e os óbitos novos de COVID-19 por estado na semana epidemiológica 
# mais recente disponível. Explique o que os dados sugerem sobre a relação entre casos e óbitos.

df_ultima_semana = df[df['semanaEpi'] == df['semanaEpi'].max()]

st.write(f"Semana epidemiológica mais recente: {df_ultima_semana['semanaEpi'].max()}")

df_ultima_semana = df_ultima_semana.groupby('estado').agg({'casosNovos':'sum','obitosNovos':'sum'}).reset_index()

fig, ax = plt.subplots()

df_ultima_semana.plot(kind = 'bar', x = 'estado', ax = ax)

st.pyplot(fig)

st.markdown('''**R.:** Os dados sugerem que a relação entre casos e óbitos varia entre os estados. 
Alguns estados podem ter uma proporção maior de óbitos em relação ao número de casos, o que pode
indicar uma sobrecarga do sistema de saúde ou uma maior letalidade do vírus. Outros estados podem
ter uma proporção menor de óbitos, o que pode indicar uma melhor capacidade de resposta do sistema
de saúde ou uma menor letalidade do vírus nessas regiões.''')


st.subheader("7 - Boxplot com Seaborn:",divider=True)

#Usando a biblioteca Seaborn, crie um boxplot que compare a distribuição dos casos novos de 
# COVID-19 por semana epidemiológica entre três regiões do Brasil (Norte, Nordeste, Sudeste). 
# Explique as principais diferenças observadas.

df_regioes = df[df['regiao'].isin(['Norte','Nordeste','Sudeste'])]

df_regioes = df_regioes.groupby(['regiao','semanaEpi']).agg({'casosNovos':'sum'}).reset_index()

fig, ax = plt.subplots()

sns.boxplot(data = df_regioes, x = 'regiao', y = 'casosNovos', ax = ax)

st.pyplot(fig)

st.markdown('''**R.:** A região sudeste possui a maior variação nos casos novos de COVID-19 por semana
epidemiológica, seguida pela região nordeste e norte, indicando maior descontrole na disseminação do
vírus, enquanto que a região norte possui a menor variabilidade nos casos, sugerindo maior controle da pandemia
nessa área, contudo, também é necessário levar em consideração o tamanho da população de cada região para se ter um melhor 
panorama a respeito do controle da disseminação da doença, pois regiões com maior população naturalmente terão mais casos. 
Os outliers podem indicar semanas com um número excepcionalmente alto ou baixo de casos
em uma determinada região.''')

st.subheader("8 - Gráfico de Área com Altair:",divider=True)

#Crie um gráfico de área em Altair para mostrar a evolução dos casos novos de COVID-19 por 
# semana epidemiológica de notificação em uma determinada região do Brasil. 
# Explique a escolha da região e as tendências observadas nos dados.

regioes = df['regiao'].unique()
regioes = regioes[~pd.isnull(regioes)]
regiao = st.selectbox('Selecione uma região', regioes, key = 'regiao_questao8')

df_regiao = df[df['regiao'] == regiao]

df_agg = df_regiao.groupby('semanaEpi').agg({'casosNovos':'sum'}).reset_index()

chart = alt.Chart(df_agg).mark_area().encode(

    x = 'semanaEpi',
    y = 'casosNovos'

).properties(height = 450)

st.altair_chart(chart, use_container_width = True)

st.markdown('''**R.:** A tendência geral dos casos novos de COVID-19 por semana epidemiológica
indicam uma redução no número de casos ao longo do tempo, sugerindo uma possível desaceleração
na disseminação do vírus.''')


st.subheader("9 - Heatmap com Altair:",divider=True)

#Desenvolva um heatmap em Altair que mostre a correlação entre casos novos, óbitos novos e 
# leitos hospitalares ocupados (caso os dados estejam disponíveis) em um determinado estado. 
# Explique as possíveis correlações observadas.

estados = df['estado'].unique()
estados = estados[~pd.isnull(estados)]
estado = st.selectbox('Selecione um estado', estados, key = 'estado_heatmap')

df_estado = df[df['estado'] == estado]

df_corr = df_estado[['casosNovos','obitosNovos', 'populacaoTCU2019']].copy()
df_corr = df_corr.corr()

chart = alt.Chart(df_corr.reset_index().melt('index')).mark_rect().encode(
    x = 'variable:N',
    y = 'index:N',
    color = 'value:Q'
)

st.altair_chart(chart)#, use_container_width = True)

st.markdown('''**R.:** Não há dados sobre leitos hospitalares ocupados disponíveis no dataset.''')


st.subheader("10 - Gráfico de Pizza com Plotly:",divider=True)

#Usando Plotly, crie um gráfico de pizza (pie chart) que mostre a distribuição percentual dos 
# casos acumulados de COVID-19 entre as cinco regiões do Brasil. 
# Explique o que os dados revelam sobre a distribuição geográfica dos casos.

df_regioes = df.groupby('regiao').agg({'casosAcumulado':'sum'}).reset_index()
df_regioes = df_regioes[df_regioes['regiao'] != 'Brasil']

fig = px.pie(df_regioes, values = 'casosAcumulado', names = 'regiao')

st.plotly_chart(fig)

st.markdown('''**R.:** Os dados revelam a distribuição geográfica dos casos de COVID-19 entre as
cinco regiões do Brasil. A aparenta seguir a distribuição populacional do país, com a região sudeste
sendo a mais afetada, seguida pela região nordeste, sul, norte e centro-oeste.''')

st.subheader("11 - Subplots com Plotly:",divider=True)

#Crie subplots em Plotly que mostrem, lado a lado, gráficos de barras comparando os casos novos 
# e os óbitos novos de COVID-19 por semana epidemiológica em duas diferentes regiões do Brasil. 
# Explique as diferenças observadas entre as regiões.

regioes = df['regiao'].unique()
regioes = regioes[regioes != 'Brasil']

regioes = regioes[~pd.isnull(regioes)]
cols = st.columns(2)

with cols[0]:
    regiao1 = st.selectbox('Selecione a primeira região', regioes, index= 0, key = 'reg_1')
    df_regiao1 = df[df['regiao'] == regiao1]
    df_agg1 = df_regiao1.groupby('semanaEpi').agg({'casosNovos':'sum','obitosNovos':'sum'}).reset_index()
    fig = px.bar(df_agg1, x = 'semanaEpi', y = ['casosNovos','obitosNovos'], barmode = 'group')
    st.plotly_chart(fig)

with cols[1]:
    regiao2 = st.selectbox('Selecione a segunda região', regioes, index= 1, key = 'reg_2')
    df_regiao2 = df[df['regiao'] == regiao2]
    df_agg2 = df_regiao2.groupby('semanaEpi').agg({'casosNovos':'sum','obitosNovos':'sum'}).reset_index()
    fig2 = px.bar(df_agg2, x = 'semanaEpi', y = ['casosNovos','obitosNovos'], barmode = 'group')
    st.plotly_chart(fig2)

st.markdown('''**R.:** As diferenças observadas entre as regiões podem refletir as diferentes fases
da pandemia em cada área. No exemplo default de Norte e Nordeste, a região Nordeste parece estar com o pico
de casos novos deslocado para mais tarde em relação ao Norte, indicando uma possível diferença na propagação
do vírus entre as regiões.''')


st.subheader("12 - Mapa Interativo com PyDeck:",divider=True)

#Utilize PyDeck para criar um mapa interativo que mostre a densidade populacional ajustada para 
# os casos acumulados de COVID-19 por município em uma determinada região do Brasil. 
# Explique como a densidade populacional pode influenciar a disseminação da COVID-19.

regioes = df['regiao'].unique()
regioes = regioes[~pd.isnull(regioes)]
regiao = st.selectbox('Selecione uma região', regioes, key = 'regiao_questao12')

df_regiao = df[df['regiao'] == regiao]

df_mapa = df_regiao.groupby(['municipio','latitude','longitude']).agg({'casosAcumulado':'max','populacaoTCU2019':'max'}).reset_index()

df_mapa['densidade'] = df_mapa['casosAcumulado'] / df_mapa['populacaoTCU2019']

df_mapa['densidade'] = df_mapa['densidade'] * 10000

view = pdk.data_utils.compute_view(df_mapa[['longitude','latitude']])
layer = pdk.Layer('ScatterplotLayer', data = df_mapa, get_position = ['longitude','latitude'], get_radius = 'densidade', get_fill_color = [255,0,0], pickable = True)

tooltip = {'html': '<b>{municipio}</b><br>Densidade: {densidade}', 'style': {'backgroundColor': 'steelblue', 'color': 'white'}}
r = pdk.Deck(map_style = 'mapbox://styles/mapbox/light-v9', initial_view_state = view, layers = [layer], tooltip = tooltip)

st.pydeck_chart(r)

st.markdown('''**R.:** De forma contraintuitiva, a relação entre densidade populacional e disseminação da COVID-19
parece ser inversa, com áreas mais densamente povoadas apresentando uma menor incidência de casos em relação ao tamanho da população.
Isso pode ser explicado pela maior adesão a medidas de distanciamento social em áreas urbanas, onde a disseminação do vírus é mais rápida e
o risco de contágio é maior.''')
