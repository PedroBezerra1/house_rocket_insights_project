import pandas as pd
import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px


# ============================================================================================================================================
    # DATA EXTRACTION
# ============================================================================================================================================
# Extract data

@st.cache(allow_output_mutation=True) # Acelerar a leitura com cache
def get_data(path):
    data = pd.read_csv( path )
    return data

# ============================================================================================================================================
    # DATA TRANSFORMATION
# ============================================================================================================================================
st.set_page_config(	layout="wide")

# image

#headers



# ========================================================================
# FUNÇÕES
# ========================================================================

# ========================================================================
# INTRODUÇÃO
# ========================================================================

def cabeçalho ():

    st.sidebar.title('House Rocket Insights Project')
    st.sidebar.markdown('House Rocket é uma empresa que atua na compra e venda de imóveis nos EUA. Este projeto foi desenvolvido para auxiliar '
                        'a empresa na definição de quais imóveis comprar, definir o preço de compra e após comprados, definir o preço de venda e '
                        'qual melhor período para realizar a venda.')

    return None

# ========================================================================
# DATA TRANSFORMATION
# ========================================================================

def limpeza( data ):

    # Alterando os tipos das variaveis
    data['date'] = pd.to_datetime(data['date'])

    # Removendo dados duplicados
    data = data.drop_duplicates(subset=['id'], keep='last')

    # Corrigindo dados
    # Mudando outlier numero de quartos 33 para 3 , assumindo erro de digitação
    data.loc[data['bedrooms'] == 33, 'bedrooms'] = 3

    return data


def features (data):
    # Criação de novas features / variaveis
    #1. Filtro data de construção 1955.
    # 2. Filtro Porão.
    # 3. Filtro por Mês.
    # 4. Filtro por Ano.
    # 5. Filtro por Sazonalidade.
    # 6. Filtro Condição.
    # 7. Filtro Nível de Construção.

    # data = data.copy()
    # Filtro Ano de Construção <> 1955
    data['construcao'] = data['yr_built'].apply(lambda x: '> 1955' if x > 1955
    else '< 1955')

    # Filtro por Porão
    data['porao'] = data['sqft_basement'].apply(lambda x: 'nao' if x == 0
    else 'sim')
    # Filtro de Temporariedade
    # Filtro Ano
    data['ano'] = data['date'].dt.year

    # Filtro Mês
    data['mes'] = data['date'].dt.month

    # Filtro Sazonalidade
    # Primavera / Spring -> Março 03 a Maio 05
    # Verão / Summer -> Junho 06 a Agosto 08
    # Outono / fall -> Setembro 09 a Novembro 11
    # Inverno / Winter -> Dezembro 12 a Fevereiro 02
    data['estaçao'] = data['mes'].apply(lambda x: 'summer' if (x > 5) & (x < 8) else
    'spring' if (x > 2) & (x < 5) else
    'fall' if (x > 8) & (x < 12) else
    'winter')
    # Filtro de Condição do Imóvel
    # boa condição == 1
    # má condição == 0

    data['boa_condiçao'] = data['condition'].apply(lambda condicao: 1 if condicao >= 4 else 0)

    # Filtro Nível de Construção
    # bom nível de construcao == 1
    # má nível de construcao == 0
    data['bom_nivel_construcao'] = data['grade'].apply(lambda nivel: 1 if nivel >= 10 else 0)

    data['reformada'] = data['yr_renovated'].apply(lambda x: '1' if x > 0 else
    '0')

    data['banheiro'] = data['bathrooms'].apply(lambda x: '0-3' if (x > 0) & (x < 3) else
    '3-5' if (x > 3) & (x < 5) else
    '5-8')

    return data

def exploration_data (data):
    #ESTATISTICA DESCRITIVA
    # data = data.copy()
    # Incluindo somente variaveis numéricas
    num = data.select_dtypes(include=['int64', 'float64'])

    # deletando a coluna 'ID'
    num = num.iloc[:, 1:]

    # Analise Descritiva

    # Medidas de tentencia central - Média, Mediana,
    data_mean = pd.DataFrame(num.apply(np.mean)).T
    data_median = pd.DataFrame(num.apply(np.median)).T

    # Medidas de dispersão - std, min, max,

    data_std = pd.DataFrame(num.apply(np.std)).T
    data_min = pd.DataFrame(num.apply(np.min)).T
    data_max = pd.DataFrame(num.apply(np.max)).T

    # Concatenando
    estat = pd.concat([data_mean, data_median, data_std, data_min, data_max]).T.reset_index()
    estat.columns = ['atributos', 'média', 'mediana', 'std', 'min', 'max']

    # Table: Estatística Descritiva ----------------------------------------------------

    st.title('Estastística Descritiva')

    # Show all columns
    st.write(estat, height=400)

    return data

def histograma(data):
    histograma = data.select_dtypes(include=['int64', 'float64', 'int32', 'float32'])
    plt.subplots()
    histograma.hist(figsize=(16, 9), bins=40)
    plt.tight_layout()

    st.title('Histograma')
    st.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False) # colocado para não aparecer um erro no streamlit ( recomendado la)

    return None


def hipoteses(data):

    st.markdown("<h1 style='text-align: center; color: black;'>Testando Hipóteses para o Negócio</h1>", unsafe_allow_html=True)

    c1, c2 = st.columns((1,1))

    c1.subheader('H1: Imóveis com vista para a água são em média 30% mais caros.')

    h1 = data[['price', 'waterfront']].groupby('waterfront').mean().reset_index()

    h1['percent'] = h1['price'].pct_change()
    c1.write(f'H1 é verdadeira, pois os imóveis com vista para a água, em média, são {h1.iloc[1, 2]:.2%} mais caros.')

    fig = px.bar(h1, x='waterfront', y='price', color='price', labels={"waterfront": "Vista para água", "price": "Preço"})
    # fig.update_layout(showlegend=False)
    c1.plotly_chart(fig, use_container_width=True)

    # =========================================
    # ========== H2 ==========
    # ==========================================
    c2.subheader('H2:Imóveis com data de construção menor que 1955 são em média 50% mais baratos.')

    h2 = h2 = data[['construcao', 'price']].groupby('construcao').mean().reset_index()

    h2['percent'] = h2['price'].pct_change()
    c2.write(f'H2 é falsa, pois os imóveis anteriores a 1955, são em média {h2.iloc[1, 2]:.2%} mais caros.')

    fig = px.bar(h2, x = 'construcao', y = 'price', color = 'price', labels = {"construcao": "Contrução", "price": "Preço" })
    c2.plotly_chart(fig,use_container_width=True)

    # =========================================
    # ========== H3 ==========
    # ==========================================

    c3, c4 = st.columns((1, 1))

    c3.subheader('H3:Imóveis sem porão possuem área total (sqrt_lot) 50% maiores do que imóveis com porões, na média.')

    h3 = data[['sqft_lot', 'porao']].groupby('porao').mean().reset_index()

    h3['percent'] = h3['sqft_lot'].pct_change()
    c3.write(f'H3 é falsa, pois os imóveis sem porão são, em média, {h3.iloc[1, 2]:.2%} maiores do que imóveis com porão.')

    fig = px.bar(h3, x='porao', y='sqft_lot', color='sqft_lot', labels={"porao": "Porão", "sqft_lot": "Area_total"})
    c3.plotly_chart(fig, use_container_width=True)

    # =========================================
    # ========== H4 ==========
    # ==========================================

    c4.subheader('H4: O crescimento do preço dos imóveis ano após ano (YoY) é de 10%, em média.')

    h4 = data[['price', 'ano']].groupby('ano').mean().reset_index()

    h4['percent'] = h4['ano'].pct_change()
    c4.write(f'H4 é falsa, pois o crescimento dos preços dos imóveis YoY, em média, é de {h4.iloc[1, 2]:.2%}')

    fig = px.bar(h4, x='ano', y='price', color='price', labels={"ano": "Ano", "price": "Preço"})
    c4.plotly_chart(fig, use_container_width=True)


    # =========================================
    # ========== H5 ==========
    # ==========================================

    st.subheader('H5: Imóveis com 3 banheiros tem um crescimento médio no Preço MoM (Month of Month) de 15%.')

    h5 = data[['price', 'mes']].loc[data['bathrooms'] == 3].groupby('mes').mean().reset_index()
    h5['percent'] = h5['price'].pct_change()
    media_h5 = h5['percent'].mean()
    st.write(f'H5 é falsa, os imóveis não possuem um crescimento MoM de 15%, pois ele possui uma variação média no período de {media_h5:.2%}')

    fig1 = px.bar(h5, x='mes', y='price', color='price', title = 'Variação média do preço por mês', labels={"mes": "Mês", "price": "Preço"})
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(h5, x='mes', y='percent', color='percent',title = 'Porcentagem de crescimento médio em relação ao mês anterior',  labels={"mes": "Mês", "percent": "Porcentagem"})
    st.plotly_chart(fig2, use_container_width=True)

    # =========================================
    # ========== H6 ==========
    # ==========================================

    st.subheader('H6: Imóveis que nunca foram reformados (yr_renovated == 0) são em média 20% mais baratos.')

    data['reformada'] = data['reformada'].astype(int)

    h6 = data[['price', 'reformada']].groupby('reformada').mean().reset_index()

    h6['percent'] = h6['price'].pct_change()
    st.write(f'H6 é verdadeira, pois os imoveis que não foram reformados são mais baratos, em média, {h6.iloc[1, 2]:.2%}')

    fig = px.bar(h6, x='reformada', y='price', color='price', labels={"reformada": "Reformada", "price": "Preço"})
    st.plotly_chart(fig, use_container_width=True)

    # =========================================
    # ========== H7 ==========
    # ==========================================
    c7, c8 = st.columns((1, 1))

    c7.subheader('H7: Pelo menos 80% dos imóveis com condição 4 e 5 tem níveis de construção 7 ou mais.')

    h7 = data[['boa_condiçao', 'grade']].loc[data['boa_condiçao'] == 1].groupby('grade').sum().reset_index()
    sns.barplot(data=h7, x='grade', y='boa_condiçao')

    h7_boa_condicao = h7['boa_condiçao'].loc[h7['grade'] >= 7].sum()
    h7_todas_condicoes = h7['boa_condiçao'].sum()
    h7_paretto = h7_boa_condicao / h7_todas_condicoes


    c7.write(f'H7 é verdadeira, pois {h7_paretto:.2%} dos imóveis estão em boa condição.')
    c7.write(f'Total de imóveis em boa condição: {h7_todas_condicoes} e os imóveis com nível de construção 7 ou mais: {h7_boa_condicao}.')

    fig = px.bar(h7, x='grade', y='boa_condiçao', color='boa_condiçao', labels={"grade": "Nivel_construção", "boa_condiçao": "Boa_condição"})
    c7.plotly_chart(fig, use_container_width=True)


    # =========================================
    # ========== H8 ==========
    # ==========================================

    c8.subheader('H8: Pelo menos 80% dos imóveis com vista para água possuem nível de construção 10 ou mais.')

    h8 = data[['waterfront', 'grade']].loc[data['waterfront'] == 1].groupby('grade').sum().reset_index()


    h8_vista_agua = h8['waterfront'].loc[h8['grade'] >= 10].sum()
    h8_todas_condicoes = h8['waterfront'].sum()
    h8_paretto = h8_vista_agua / h8_todas_condicoes

    c8.write(f'H8 é falsa, pois os imóveis com boa condição representão {h8_paretto:.2%}.')
    c8.write(f'Sendo o total de imóveis em boa condção: {h8_todas_condicoes} e os imóveis com nível de construção 10 ou mais: {h8_vista_agua}.')

    fig = px.bar(h8, x='grade', y='waterfront', color='waterfront', labels={"grade": "Nivel_construção", "waterfront": "Vista_para_agua"})
    c8.plotly_chart(fig, use_container_width=True)


    return None

def questao_negocio (data):


    st.markdown("<h1 style='text-align: center; color: black;'>Questões de Negócio</h1>", unsafe_allow_html=True)
    st.subheader(' 1 - Quais são os melhores imóveis para se comprar e qual valor devo pagar?')

    c9, c10 = st.columns((2, 1))

    resp1 = data[['id', 'price', 'boa_condiçao', 'zipcode', 'estaçao']].copy()

    # Calculando a mediana do preço de compra
    resp1_median = resp1[['price', 'zipcode']].groupby('zipcode').median().reset_index()
    resp1_median.rename(columns={'price': 'mediana_preco'}, inplace=True)

    resp1 = pd.merge(resp1, resp1_median, on='zipcode', how='inner')

    # Pode comprar = 1
    # Não pode comprar = 0
    resp1['comprar'] = 0
    resp1.loc[(resp1['boa_condiçao'] == 1) & (resp1['price'] < resp1['mediana_preco']), 'comprar'] = 1

    c9.write('Relatório de compra de imóveis')
    c9.write(resp1, height=1000, width = 1000)

    # ------------------CALCULANDO NÚMERO TOTAL DE RECOMENDAÇÃO DE COMPRA -----------------------------

    apto_compra = resp1.loc[resp1['comprar'] == 1].copy()

    valor_imovel = apto_compra.describe().T
    valor_imovel.drop(['std', '25%', '75%'], axis=1, inplace=True)
    valor_imovel.drop(['zipcode', 'comprar', 'boa_condiçao'], axis=0, inplace=True)

    valor_compra = apto_compra['price'].sum()

    apto_compra['economia'] = 0
    apto_compra['economia'] = apto_compra.apply(lambda x: x['mediana_preco'] - x['price'], axis=1)

    valor_economizado = apto_compra['economia'].sum()

    c10.write(f'O número total de imóveis aptos a serem comprados são: {apto_compra.shape[0]:,.2f}')
    c10.write(f'O valor do aporte para adiquirir os imóveis é: {valor_compra:,.2f}')
    c10.write(f'O valor a ser economizado ao adiquirir todos os imóveis é: {valor_economizado:,.2f}')

    # ========================================================================
    #                            "MAPA"
    # ========================================================================

    st.subheader('Dashboard - Mapa dos Imóveis aptos a compra')
    data_map = pd.merge(data,apto_compra, how ='inner', on ='id')
    if st.checkbox('Mostre o dataset'):
        st.write(data_map)
    fig = px.scatter_mapbox(
        data_map,
        lat='lat',
        lon='long',
        color='price_x',
        size='price_x',
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=15,
        zoom=10)

    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(height=600, width = 1000, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

    st.plotly_chart(fig)
    # ========================================================================
    #                            "Segunda Questão"
    # ========================================================================
    st.subheader(' 2 - Qual o melhor período de venda dos imóveis e por quanto vender?')

    resp2 = data[['id', 'price', 'zipcode', 'estaçao']].copy()

    resp2_median = resp2[['price', 'zipcode', 'estaçao']].groupby(['zipcode', 'estaçao']).median().reset_index()
    resp2_median.rename(columns={'price': 'mediana_preco'}, inplace=True)

    resp2 = pd.merge(resp2, resp2_median, on=['zipcode', 'estaçao'], how='inner')

    resp2['preco_venda'] = resp2[['mediana_preco', 'price']].apply(
        lambda x: (x['price'] * 1.1) if x['price'] >= x['mediana_preco']
        else (x['price'] * 1.3), axis=1)

    resp2['lucro_venda'] = resp2['preco_venda'] - resp2['price']

    st.write(resp2,width = 1000)

    apto_venda = resp2.copy()
    apto_venda = pd.merge(apto_venda, apto_compra[['id', 'mediana_preco', 'economia', 'price']], on='id', how='right')
    apto_venda.rename(columns={'mediana_preco_x': 'mediana_preco_venda', 'mediana_preco_y': 'mediana_preco_compra',
                               'preco': 'preco_compra'}, inplace=True)

    lucro_venda = apto_venda['lucro_venda'].sum()
    lucro_sazonalidade = apto_venda[['lucro_venda', 'estaçao']].groupby('estaçao').sum().reset_index()

    st.write(f'A lucratividade total estimada é de: {lucro_venda:,.2f}')

    return fig

# ========================================================================
# "Data Overview"
# ========================================================================

def overview_data( data ):
    # 1. Filtros dos imóveis por um ou várias regiões.
    # Objetivo: Visualizar imóveis por código postal (zipcode)
    # Obs: várias lat/lot neste dataset tem mesmo zipcode, logo podemos utilizar como agrupador de região.
    # Ação do Usuário: Digitar um ou mais códigos desejados.
    # A visualização: Uma tabela com todos os atributos e filtrada por código postal.

    # 2. Escolher uma ou mais variáveis para visualizar.
    # Objetivo: Visualizar características do imóvel.
    # Ação do Usuário: Digitar características desejadas.
    # A visualização: Uma tabela com todos os atributos selecionados.

# Filters: Overview -------------------------------------------------------

    st.title('Data Overview')
    f_attributes = st.multiselect('Enter Columns', data.columns)

    f_zipcode = st.multiselect('Enter zipcode',
                                       data['zipcode'].unique())

    # Attributes + zipcode -> need rows and cols
    if (f_zipcode != []) & (f_attributes != []):
        # data_overview is used just for the first table
        data_overview = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]
        # data is used for the other components that not first table
        data = data.loc[data['zipcode'].isin(f_zipcode), :]

        # just zipcode -> just filter rows, all colums
    elif (f_zipcode != []) & (f_attributes == []):
        data_overview = data.loc[data['zipcode'].isin(f_zipcode), :]
        data = data.loc[data['zipcode'].isin(f_zipcode), :]

        # just attributes -> just filter cols, all rows
    elif (f_zipcode == []) & (f_attributes != []):
        data_overview = data.loc[:, f_attributes]

        # no attributes -> returns original ds
    else:
        data_overview = data.copy()

    # Table: Data Overview ---------------------------------------------------
    # Show all columns
    st.write(data_overview, height=400)

    return data


if __name__ == '__main__':  # ETL:
    # ============================================================================================================================================
    # DATA EXTRACTION
    # ============================================================================================================================================
    # Extract data
    path = 'kc_house_data.csv'
    data = get_data(path)

    # ============================================================================================================================================
    # DATA TRANSFORMATION
    # ============================================================================================================================================
    cabeçalho()
    limpeza(data)
    features(data)
    questao_negocio(data)
    overview_data( data )
    exploration_data(data)
    histograma(data)
    hipoteses(data)


























