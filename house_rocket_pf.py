# -------------------------
# Imports
# -------------------------
import pandas as pd
import numpy as np
import streamlit as st
import geopandas
import plotly.express as px
import folium
from streamlit_folium import folium_static

# -------------------------
# Config
# -------------------------
st.set_page_config( layout='centered' )
# Set the principal title
st.markdown("<h1 style='text-align: center;'>House Rocket Company</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Bem vindo à House Rocket Data Analysis!</h4>", unsafe_allow_html=True)

# -------------------------
# Functions
# -------------------------
# Read data
@st.cache( allow_output_mutation=True )
def get_data( path ):
    data = pd.read_csv( path )

    return data

# Read geofile
@st.cache( allow_output_mutation=True )
def get_geofile( url ):
    geofile = geopandas.read_file( url )

    return geofile

def set_attributes( data ):
    # Date
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    # Bedrooms
    data.loc[data['bedrooms'] == 33, 'bedrooms'] = 3

    # Median price per filters (waterfront, zipcode and grade)
    data['price_median'] = 0.0
    for h in data['waterfront'].unique():
        for i in data['zipcode'].unique():
            df = data.loc[(data['waterfront'] == h) & (data['zipcode'] == i), ['price', 'grade']].groupby(
                'grade').median().reset_index()
            for j in df['grade']:
                data.loc[(data['waterfront'] == h) & (data['zipcode'] == i) & (data['grade'] == j), 'price_median'] = float(
                    df.loc[df['grade'] == j, 'price'])

    # Upside
    data['upside'] = (data['price_median'] - data['price']) / data['price_median'] * 100

    # Status
    data['status'] = 'NA'
    for i in range(len(data)):
        if (data.loc[i, 'condition'] == 5) & (data.loc[i, 'price'] < data.loc[i, 'price_median']):
            data.loc[i, 'status'] = '1 compra A'
        elif (data.loc[i, 'condition'] == 4) & (data.loc[i, 'price'] < data.loc[i, 'price_median']):
            data.loc[i, 'status'] = '2 compra B'
        elif (data.loc[i, 'condition'] == 3) & (data.loc[i, 'price'] < data.loc[i, 'price_median']):
            data.loc[i, 'status'] = '3 neutro'
        else:
            data.loc[i, 'status'] = '4 nao compra'

    # Create the filters
    st.sidebar.title('Escolha os filtros desejados')
    # zipcode
    f_zipcode = st.sidebar.multiselect('Códigos postais', data['zipcode'].sort_values().unique())
    if f_zipcode != []:
        data = data.loc[data['zipcode'].isin(f_zipcode), :]
    else:
        data = data.copy()
    # price
    min_price = int(data['price'].min())
    max_price = int(data['price'].max())
    f_price = st.sidebar.slider('Preço máximo ($)', min_price, max_price, max_price)
    data = data.loc[data['price'] <= f_price, :]
    # upside
    min_upside = int(data['upside'].min())
    max_upside = int(data['upside'].max())
    f_upside = st.sidebar.slider('Upside mínimo (%)', min_upside, max_upside, min_upside)
    data = data.loc[data['upside'] >= f_upside, :]
    # grade
    f_grade = st.sidebar.multiselect('Avaliação do imóvel', data['grade'].sort_values().unique())
    if f_grade != []:
        data = data.loc[data['grade'].isin(f_grade), :]
    else:
        data = data.copy()
    # condition
    f_condition = st.sidebar.multiselect('Condição do imóvel', data['condition'].sort_values().unique())
    if f_condition != []:
        data = data.loc[data['condition'].isin(f_condition), :]
    else:
        data = data.copy()
    # waterfront
    f_waterfront = st.sidebar.radio("Vista para água", ('Ambos', 'Com', 'Sem'))
    if f_waterfront == 'Ambos':
        data = data.copy()
    elif f_waterfront == 'Com':
        data = data.loc[data['waterfront'] == 1, :]
    else:
        data = data.loc[data['waterfront'] == 0, :]
    # bedrooms
    f_bedrooms = st.sidebar.selectbox('Quantidade máxima de quartos', data['bedrooms'].sort_values(ascending=False).unique())
    data = data.loc[data['bedrooms'] <= f_bedrooms, :]
    # bathrooms
    f_bathrooms = st.sidebar.selectbox('Quantidade máxima de banheiros', data['bathrooms'].sort_values(ascending=False).unique())
    data = data.loc[data['bathrooms'] <= f_bathrooms, :]
    # floors
    f_floors = st.sidebar.selectbox('Quantidade máxima de pisos', data['floors'].sort_values(ascending=False).unique())
    data = data.loc[data['floors'] <= f_floors, :]
    st.sidebar.markdown( '\n\n\n' )

    return data

def buy_recommendation( data, tab, geofile ):
    with tab:
        df = data.copy()

        # Calculate metrics
        quant = df['id'].count()
        quant1 = df.loc[df['status'] == '1 compra A', 'id'].count()
        quant2 = df.loc[df['status'] == '2 compra B', 'id'].count()
        quant3 = df.loc[df['status'] == '3 neutro', 'id'].count()
        quant4 = df.loc[df['status'] == '4 nao compra', 'id'].count()
        upside = round(df['upside'].mean(), 2)
        upside1 = round(df.loc[df['status'] == '1 compra A', 'upside'].mean(), 2)
        upside2 = round(df.loc[df['status'] == '2 compra B', 'upside'].mean(), 2)
        upside3 = round(df.loc[df['status'] == '3 neutro', 'upside'].mean(), 2)
        upside4 = round(df.loc[df['status'] == '4 nao compra', 'upside'].mean(), 2)

        # Map 1
        df_map = df[['upside', 'zipcode']].groupby('zipcode').mean().reset_index()
        df_map.columns = ['ZIP', 'UPSIDE']

        geofile = geofile[geofile['ZIP'].isin(df_map['ZIP'].tolist())]

        map1 = folium.Map(
            location=[df['lat'].mean(), df['long'].mean()],
            default_zoom_start=15)

        map1.choropleth(data=df_map,
                        geo_data=geofile,
                        columns=['ZIP', 'UPSIDE'],
                        key_on='feature.properties.ZIP',
                        fill_color='PuRd',
                        fill_opacity=0.7,
                        line_opacity=0.2)

        # Map 2
        df_map = df.copy()
        map2 = px.scatter_mapbox(df_map,
                                 lat="lat",
                                 lon="long",
                                 color="upside",
                                 color_continuous_scale=px.colors.cyclical.IceFire,
                                 zoom=10)

        map2.update_layout(mapbox_style="open-street-map")
        map2.update_traces(marker={'size': 10})
        map2.update_layout(height=800, margin={"r": 0, "t": 0, "l": 0, "b": 0})

        # Show
        df_print = df[['id', 'price', 'zipcode', 'grade', 'waterfront', 'condition', 'price_median', 'status', 'upside']]
        st.markdown("<h1 style='text-align: center;'>Recomendação de Compra</h1>", unsafe_allow_html=True)
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric( label="Quant. imóveis: ", value=quant )
        c2.metric(label="Compra A: ", value=quant1)
        c3.metric(label="Compra B: ", value=quant2)
        c4.metric(label="Neutro: ", value=quant3)
        c5.metric(label="Não compra: ", value=quant4)
        c1.metric(label="Upside médio: ", value=str(upside)+"%")
        c2.metric(label="Compra A: ", value=str(upside1)+"%")
        c3.metric(label="Compra B: ", value=str(upside2) + "%")
        c4.metric(label="Neutro: ", value=str(upside3) + "%")
        c5.metric(label="Não compra: ", value=str(upside4) + "%")

        st.dataframe(df_print, use_container_width=True)
        st.markdown("<h3 style='text-align: center;'>Upside médio por região</h3>", unsafe_allow_html=True)
        folium_static(map1)
        st.markdown("<h3 style='text-align: center;'>Localização e upside</h3>", unsafe_allow_html=True)
        st.plotly_chart(map2)

    return df

def sell_recommendation( data, tab, geofile ):
    with tab:
        # Median per season
        df = data.copy()

        df['month'] = pd.to_datetime(df['date']).dt.strftime('%m')
        df['month'] = df['month'].astype('int64')
        df['season'] = df['month'].apply(lambda x:
                                           'primavera' if (x >= 3) & (x <= 5) else
                                           'verao' if (x >= 6) & (x <= 8) else
                                           'outono' if (x >= 9) & (x <= 11) else 'inverno')
        df['season_variation'] = df['season'].apply(lambda x: 6.429 if x == 'inverno' else 4.098
                                        if x == 'outono' else 0.000 if x == 'primavera' else 1.065)

        # New upside and profit
        df = df.loc[(df['status'] != '3 neutro') & (df['status'] != '4 nao compra'), :]
        df['price_median'] = df['price_median'] * (1 + (df['season_variation'] / 100))
        df['upside'] = (df['price_median'] - df['price']) / df['price_median'] * 100
        df['profit'] = df['price_median'] * df['upside'] / 100
        df = df.rename(columns={"price": "price_buy", "price_median": "price_sell"})

        # Map
        df_map = df.copy()
        fig = px.scatter_mapbox(df_map,
                                lat="lat",
                                lon="long",
                                color="upside",
                                color_continuous_scale=px.colors.cyclical.IceFire,
                                zoom=10)

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_traces(marker={'size': 10})
        fig.update_layout(height=800, margin={"r": 0, "t": 0, "l": 0, "b": 0})

        # Calculate metrics
        quant = df['id'].count()
        investido = round(df['price_buy'].sum(), 2)
        faturado = round(df['price_sell'].sum(), 2)
        lucrototal = round(df['profit'].sum(), 2)
        lucromedio = round(df['profit'].mean(), 2)
        upside = round(df['upside'].mean(), 2)

        # Show
        df_print = df[['id', 'season', 'status', 'price_buy', 'price_sell', 'upside', 'profit']]
        st.markdown("<h1 style='text-align: center;'>Recomendação de Venda</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric(label="Quant. imóveis: ", value=quant)
        c2.metric(label="Total investido: ", value= "R$ " + str(investido))
        c1.metric(label="Total faturado: ", value="R$ " + str(faturado))
        c2.metric(label="Lucro Total: ", value="R$ " + str(lucrototal))
        c1.metric(label="Lucro médio: ", value="R$ " + str(lucromedio))
        c2.metric(label="Upside médio: ", value=str(upside) + "%")
        st.dataframe(df_print, use_container_width=True)
        st.markdown("<h3 style='text-align: center;'>Localização e upside</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig)

    return None

# -------------------------
# Main
# -------------------------
if __name__ == '__main__':
    path = 'kc_house_data.csv'
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

    # Load data
    data = get_data( path )
    geofile = get_geofile( url )

    # Transform data
    tabs = st.tabs(["Compra", "Venda"])
    data = set_attributes( data )

    data = buy_recommendation( data, tabs[0], geofile )

    sell_recommendation( data, tabs[1], geofile )
