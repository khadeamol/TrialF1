import streamlit as st
import pandas as pd 
import numpy as np 



st.title("Uber pickups in NYC")

date_column = "date/time"
data_url = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(data_url, nrows = nrows)
    lowercase = lambda x:str(x).lower()
    data.rename(lowercase, axis = 'columns', inplace = True)

    data[date_column] = pd.to_datetime(data[date_column])

    return data




data_load_state = st.text("Data loading..")

data = load_data(1000)
data_load_state.text("Data loaded using st.cache_data")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

    
hist_values = np.histogram(data[date_column].dt.hour, bins = 24, range=(0,24))[0]

st.bar_chart(hist_values)

st.subheader('Map of all pickups')
st.map(data)

hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[date_column].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickiups at {hour_to_filter}:00')
st.map(filtered_data)


