import streamlit as st
from collections import namedtuple
import math
import pandas as pd
import numpy as np
import seaborn as sns
sns.set()
import plost                # this package is used to create plots/charts within streamlit
from PIL import Image       # this package is used to put images within streamlit
# Standard plotly imports
import plotly
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
import plotly.figure_factory as ff

# Page setting
st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#%% Loading data
df_v52 = pd.read_csv('./data/V52_ExtensiveData.csv', sep='\t', skiprows=12)
# or replace the previous data with your own streamed data from API

# Data cleaning
df_v52['Date'] = pd.to_datetime(df_v52['Date'], format='%Y%m%d%H%M')
df_v52.set_index('Date', inplace=True)

#%% Web app design

# title
st.title('V52 Wind Turbine Data Analysis')

############################################################################################
# First Row
############################################################################################
a1, a2 = st.columns(2)

# put the image on a2
a2.image(Image.open('images/V52turbine.jpg'))

with a1:

    # inspect raw data
    st.subheader('Raw data')
    st.write(df_v52.head())

    # inspect data statistics
    st.subheader('Data statistics')
    st.write(df_v52.describe())

############################################################################################
# Second Row
############################################################################################

# correlation heatmap
st.subheader('Correlation heatmap')
corrs = df_v52.corr()
corr_heat = ff.create_annotated_heatmap(
    z=corrs.values,
    x=list(corrs.columns),
    y=list(corrs.index),
    annotation_text=corrs.round(2).values,
    showscale=True)
st.plotly_chart(corr_heat, use_container_width=True)

############################################################################################
# Third Row
############################################################################################

# Slider Widget
st.subheader('Time Series Data Visualization')

from plotting_funs import create_plot

# prepare dataframe
df_v52.reset_index(inplace=True)

# Sidebar with slider for selecting time frame for Active Power
st.sidebar.subheader('Active Power')
start_date_act_pow = st.sidebar.date_input('Select start date', pd.to_datetime(min(df_v52['Date'])), key="start_date_act_pow")
end_date_act_pow = st.sidebar.date_input('Select end date', pd.to_datetime(max(df_v52['Date'])), key="end_date_act_pow")
start_date_act_pow = pd.to_datetime(start_date_act_pow)
end_date_act_pow = pd.to_datetime(end_date_act_pow)
filtered_data_act_pow = df_v52[(df_v52['Date'] >= start_date_act_pow) & (df_v52['Date'] <= end_date_act_pow)]
fig_act_pow = create_plot(filtered_data_act_pow['Date'], filtered_data_act_pow['ActPow'],
                          'V52 Turbine Active Power Output', 'Power Output [kW]')

# Sidebar with slider for selecting time frame for Reactive Power
st.sidebar.subheader('Reactive Power')
start_date_react_pow = st.sidebar.date_input('Select start date', pd.to_datetime(min(df_v52['Date'])), key="start_date_react_pow")
end_date_react_pow = st.sidebar.date_input('Select end date', pd.to_datetime(max(df_v52['Date'])), key="end_date_react_pow")
start_date_react_pow = pd.to_datetime(start_date_react_pow)
end_date_react_pow = pd.to_datetime(end_date_react_pow)
filtered_data_react_pow = df_v52[(df_v52['Date'] >= start_date_react_pow) & (df_v52['Date'] <= end_date_react_pow)]
fig_react_pow = create_plot(filtered_data_react_pow['Date'], filtered_data_react_pow['RePow'],
                            'V52 Turbine Reactive Power Output', 'Reactive Power [kVAR]')


# Display the Plotly charts
st.plotly_chart(fig_act_pow)
st.plotly_chart(fig_react_pow)
