import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

from datetime import datetime

#tamanho dos plts na pág
st.set_page_config(layout='wide')

def set_feature( data ):
    # add new feature
    data['price_m2'] = data['price'] / data['sqft_lot']
    return data

def overview_data( data ):
    #sidebars or filters
    f_attributes = st.sidebar.multiselect('Enter Columns',
                                          data.columns)
    f_zipcode = st.sidebar.multiselect('Enter ZipCode',
                                       data['zipcode'].unique())
    #title
    st.title('Data Overview')

    if f_zipcode != []:
        data = data.loc[data['zipcode'].isin(f_zipcode), :]

    elif f_zipcode == []:
        data = data.copy()

    if (f_attributes != []) & (f_zipcode != []):
        dataframe = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]
        st.dataframe(dataframe)

    elif (f_attributes != []) & (f_zipcode == []):
        dataframe = data.loc[:, f_attributes]
        st.dataframe(dataframe)

    else:
        st.dataframe(data)


    # metrics size
    c1, c2 = st.columns((1, 1)) #layout

    # average metrics
    df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

    # merge metrical datasets
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    df = pd.merge(m2, df4, on='zipcode', how='inner')

    df.columns = ['ZIPCODE', 'TOTAL HOUSES', 'PRICE', 'SQFT LIVING',
                  'PRICE/m2']

    c1.header('Average Values')
    c1.dataframe(df, height=600)

    # descriptive metrics
    num_attribute = data.select_dtypes(include=['int64', 'float64'])
    media = pd.DataFrame(num_attribute.apply(np.mean))
    mediana = pd.DataFrame(num_attribute.apply(np.median))
    std = pd.DataFrame(num_attribute.apply(np.std))

    max_ = pd.DataFrame(num_attribute.apply(np.max))
    min_ = pd.DataFrame(num_attribute.apply(np.min))

    df1 = pd.concat([max_, min_, media, mediana, std], axis=1).reset_index()
    df1.columns = ['ATTRIBUTES', 'MAX', 'MIN', 'MEAN', 'MEDIAN', 'STD']

    c2.header('Descriptive Analysis')
    c2.dataframe(df1, height=600)

    # -------
    # maps
    # -------
    st.title('Region Overview')

    c1, c2 = st.columns((1, 1))

    c1.header('Portfolio Density')
    df = data.sample(10)

    # Base Map
    # add columns
    data['level'] = data['level'] = 'NA'
    data['level'] = data['price'].apply(lambda x: 0 if (x > 0) & (x <= 321950) else
    1 if (x > 321950) & (x <= 450000) else
    2 if (x > 450000) & (x <= 645000) else 3)
    if f_zipcode != []:
        houses = data.loc[data['zipcode'].isin(f_zipcode), :]

    elif f_zipcode == []:
        houses = data.copy()
    map = px.scatter_mapbox(data_frame=houses,
                            lat='lat',
                            lon='long',
                            color_continuous_scale='oryel',
                            size='price',
                            zoom=10,
                            mapbox_style='open-street-map',
                            color='level', )
    map.update_layout(height=600, margin={'r': 0, 'l': 0, 'b': 0, 't': 0}, width=980)
    st.plotly_chart(map)

    return None


def commercial_distribution( data ):
    # commercial attributes

    st.title('Commercial Attributes')

    st.sidebar.title('Commercial Options')

    # average price/ year
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    # filters
    min_year_built = int(data['yr_built'].min())
    max_year_built = int(data['yr_built'].max())

    st.sidebar.subheader('Select Max Year Built')
    f_year_built = st.sidebar.slider('Year Built',
                                     min_year_built,
                                     max_year_built,
                                     max_year_built)

    # graphic title
    st.header('Average Price per Year Built')

    # data select
    df = data.loc[data['yr_built'] < f_year_built]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    # plot
    fig = px.line(df, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # average price/ day

    st.header('Average Price per Day')
    st.sidebar.subheader('Select Max Date')

    # filters
    min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d')
    max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d')

    f_date = st.sidebar.slider('Date', min_date,
                               max_date,
                               max_date)

    # data filtering
    data['date'] = pd.to_datetime(data['date'])
    df = data.loc[data['date'] < f_date]
    df = df[['date', 'price']].groupby('date').mean().reset_index()

    # plot
    fig = px.line(df, x='date', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # histogram
    st.header('Price Distribution')
    st.sidebar.subheader('Select Max Price')

    # filter
    min_price = int(data['price'].min())
    max_price = int(data['price'].max())
    avg_price = int(data['price'].mean())

    f_price = st.sidebar.slider('Price',
                                min_price,
                                max_price,
                                avg_price)

    # data filtering
    df = data.loc[data['price'] < f_price]

    # data plot
    fig = px.histogram(df, x='price', nbins=50)
    st.plotly_chart(fig, use_container_width=True)
    return None

def attributes_distribution( data ):
    # Distribution by physical categorys
    st.sidebar.title('Attributes Options')
    st.title('House Attributes')

    # filters
    f_bedrooms = st.sidebar.selectbox('Max Numbers of Bedrooms',
                                      sorted(set(data['bedrooms'].unique())),
                                      index=10)
    f_bathrooms = st.sidebar.selectbox('Max Numbers of Bathrooms',
                                       sorted(set(data['bathrooms'].unique())),
                                       index=int(data['bathrooms'].mean()))

    c1, c2 = st.columns(2)
    # bedrooms

    c1.header('House per Bedrooms')
    df = data[data['bedrooms'] < f_bedrooms]
    fig = px.histogram(df, x='bedrooms', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # bathrooms
    c2.header('House per Bathrooms')
    df = data[data['bathrooms'] < f_bathrooms]
    fig = px.histogram(df, x='bathrooms', nbins=19)
    c2.plotly_chart(fig, use_container_width=True)

    # filters
    f_floors = st.sidebar.selectbox('Max Nuber of Floors',
                                    sorted(set(data['floors'].unique())))
    f_waterview = st.sidebar.checkbox('Only houses with Water View')

    c3, c4 = st.columns(2)

    # floors
    c3.header('Houses per Floor')
    df = data[data['floors'] < f_floors]
    fig = px.histogram(df, x='floors', nbins=19)
    c3.plotly_chart(fig, use_container_width=True)

    # waterview
    if f_waterview:
        df = data[data['waterfront'] == 1]
    else:
        df = data.copy()

    c4.header('Houses per Waterfront')
    fig = px.histogram(df, x='waterfront', nbins=10)
    c4.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    #ETL
    # EXTRACTION
    data = pd.read_csv('kc_house_data.csv')

    #TRANFORMATION
    data = set_feature(data)

    overview_data(data)

    commercial_distribution(data)

    attributes_distribution(data)